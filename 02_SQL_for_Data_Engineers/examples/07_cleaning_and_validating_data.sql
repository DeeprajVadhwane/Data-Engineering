-- Module 02, 07 · Cleaning and Validating Data
-- Every query from the topic, in order.
-- Run:  python run_sql.py 07_cleaning_and_validating_data.sql

-- The raw feed, exactly as it arrived
SELECT order_ref, customer, region, order_ts, amount, status, loaded_at
FROM raw_orders_stage
ORDER BY order_ref, loaded_at;

-- The naive conversion: no error, wrong numbers
SELECT order_ref, amount, CAST(amount AS REAL) AS naive_cast
FROM raw_orders_stage
ORDER BY order_ref, loaded_at;

-- Step 1: standardise text, status, dates and amounts into a view
CREATE VIEW stage_standardised AS
SELECT order_ref,
       TRIM(customer) AS customer,
       -- blank region becomes NULL; otherwise capitalise the first letter only
       CASE WHEN TRIM(region) = '' THEN NULL
            ELSE UPPER(SUBSTR(TRIM(region), 1, 1)) || LOWER(SUBSTR(TRIM(region), 2)) END AS region,
       -- two date formats, both converted to ISO yyyy-mm-dd (assumes dd/mm/yyyy for the slashed form)
       CASE WHEN order_ts GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]*' THEN date(order_ts)
            WHEN order_ts GLOB '[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]'
                 THEN SUBSTR(order_ts, 7, 4) || '-' || SUBSTR(order_ts, 4, 2) || '-' || SUBSTR(order_ts, 1, 2)
       END AS order_date,
       -- remove thousands separators; empty text becomes NULL
       NULLIF(REPLACE(TRIM(amount), ',', ''), '') AS amount_text,
       CASE LOWER(TRIM(status)) WHEN 'complete' THEN 'completed' ELSE LOWER(TRIM(status)) END AS status,
       loaded_at
FROM raw_orders_stage;

SELECT * FROM stage_standardised ORDER BY order_ref, loaded_at;

-- Step 2 and 3: keep the latest delivery of each order, then validate it
CREATE VIEW stage_checked AS
WITH latest AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY order_ref ORDER BY loaded_at DESC) AS rn
    FROM stage_standardised
)
SELECT order_ref, customer, region, order_date, status,
       -- convert only text that is a plain number; everything else stays NULL
       CASE WHEN amount_text NOT GLOB '*[^0-9.-]*' THEN CAST(amount_text AS REAL) END AS amount,
       -- the first rule that fails names the reason; NULL means the row is good
       CASE WHEN amount_text IS NULL              THEN 'amount missing'
            WHEN amount_text GLOB '*[^0-9.-]*'    THEN 'amount not a number'
            WHEN CAST(amount_text AS REAL) < 0    THEN 'amount negative'
            WHEN region IS NULL                   THEN 'region missing'
            WHEN order_date IS NULL               THEN 'order date unreadable'
       END AS reject_reason
FROM latest
WHERE rn = 1;

SELECT * FROM stage_checked ORDER BY order_ref;

CREATE TABLE clean_orders AS
SELECT order_ref, customer, region, order_date, status, amount
FROM stage_checked
WHERE reject_reason IS NULL;

CREATE TABLE rejected_orders AS
SELECT order_ref, customer, reject_reason
FROM stage_checked
WHERE reject_reason IS NOT NULL;

SELECT * FROM clean_orders ORDER BY order_ref;

SELECT * FROM rejected_orders ORDER BY order_ref;

-- Every check must return 0 before clean_orders is published
SELECT 'duplicate order_ref' AS check_name, COUNT(*) AS failed_rows
FROM (SELECT order_ref FROM clean_orders GROUP BY order_ref HAVING COUNT(*) > 1)
UNION ALL
SELECT 'region missing', COUNT(*) FROM clean_orders WHERE region IS NULL OR TRIM(region) = ''
UNION ALL
SELECT 'amount not positive', COUNT(*) FROM clean_orders WHERE amount IS NULL OR amount <= 0
UNION ALL
SELECT 'status outside allowed set', COUNT(*) FROM clean_orders
WHERE status NOT IN ('completed', 'cancelled', 'shipped', 'pending')
UNION ALL
SELECT 'order_date outside feed window', COUNT(*) FROM clean_orders
WHERE order_date NOT BETWEEN '2025-12-01' AND '2025-12-31'
UNION ALL
SELECT 'rows lost (raw orders minus clean and rejected)',
       (SELECT COUNT(DISTINCT order_ref) FROM raw_orders_stage)
       - ((SELECT COUNT(*) FROM clean_orders) + (SELECT COUNT(*) FROM rejected_orders));

SELECT 'orders without a customer' AS check_name, COUNT(*) AS failed_rows
FROM orders AS o
LEFT JOIN customers AS c ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL
UNION ALL
SELECT 'order lines without a product', COUNT(*)
FROM order_items AS oi
LEFT JOIN products AS p ON p.product_id = oi.product_id
WHERE p.product_id IS NULL
UNION ALL
SELECT 'returns without an order line', COUNT(*)
FROM returns AS r
LEFT JOIN order_items AS oi ON oi.order_id = r.order_id AND oi.line_no = r.line_no
WHERE oi.order_id IS NULL
UNION ALL
SELECT 'order lines with quantity <= 0', COUNT(*) FROM order_items WHERE quantity <= 0
UNION ALL
SELECT 'orders with no lines', COUNT(*)
FROM orders AS o
WHERE NOT EXISTS (SELECT 1 FROM order_items AS oi WHERE oi.order_id = o.order_id);
