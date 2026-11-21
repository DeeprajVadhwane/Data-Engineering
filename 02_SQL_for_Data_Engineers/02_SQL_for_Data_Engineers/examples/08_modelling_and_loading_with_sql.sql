-- Module 02, 08 · Modelling and Loading with SQL
-- Every query from the topic, in order.
-- Run:  python run_sql.py 08_modelling_and_loading_with_sql.sql

CREATE TABLE dim_date (
    date_key   INTEGER PRIMARY KEY,   -- 20251001
    full_date  TEXT NOT NULL,         -- 2025-10-01
    year       INTEGER,
    quarter    INTEGER,
    month      INTEGER,
    year_month TEXT,
    day_name   TEXT,
    is_weekend INTEGER
);

INSERT INTO dim_date
WITH RECURSIVE d(day) AS (
    SELECT '2025-07-01'
    UNION ALL
    SELECT date(day, '+1 day') FROM d WHERE day < '2025-12-31'
)
SELECT CAST(REPLACE(day, '-', '') AS INTEGER),
       day,
       CAST(strftime('%Y', day) AS INTEGER),
       (CAST(strftime('%m', day) AS INTEGER) + 2) / 3,
       CAST(strftime('%m', day) AS INTEGER),
       strftime('%Y-%m', day),
       CASE strftime('%w', day) WHEN '0' THEN 'Sun' WHEN '1' THEN 'Mon' WHEN '2' THEN 'Tue'
                                WHEN '3' THEN 'Wed' WHEN '4' THEN 'Thu' WHEN '5' THEN 'Fri' ELSE 'Sat' END,
       CASE WHEN strftime('%w', day) IN ('0', '6') THEN 1 ELSE 0 END
FROM d;

SELECT * FROM dim_date WHERE full_date IN ('2025-10-01', '2025-12-27') ORDER BY date_key;

CREATE TABLE dim_product (
    product_key INTEGER PRIMARY KEY,   -- surrogate key
    product_id  INTEGER NOT NULL,      -- natural key from the source
    name        TEXT NOT NULL,
    category    TEXT NOT NULL
);
INSERT INTO dim_product (product_id, name, category)
SELECT product_id, name, category FROM products ORDER BY product_id;

CREATE TABLE dim_customer (
    customer_key INTEGER PRIMARY KEY,  -- surrogate key: one per VERSION of a customer
    customer_id  INTEGER NOT NULL,     -- natural key from the source
    name         TEXT NOT NULL,
    city         TEXT,
    region       TEXT NOT NULL,
    segment      TEXT,
    valid_from   TEXT NOT NULL,
    valid_to     TEXT NOT NULL,        -- '9999-12-31' means "still current"
    is_current   INTEGER NOT NULL
);
INSERT INTO dim_customer (customer_id, name, city, region, segment, valid_from, valid_to, is_current)
SELECT customer_id, name, city, region, segment, '2025-07-01', '9999-12-31', 1
FROM customers
ORDER BY customer_id;

SELECT customer_key, customer_id, name, city, region, valid_from, valid_to, is_current
FROM dim_customer
WHERE customer_id IN (3, 4);

CREATE TABLE customer_changes (
    customer_id    INTEGER,
    new_city       TEXT,
    new_region     TEXT,
    effective_date TEXT
);
INSERT INTO customer_changes VALUES (3, 'Delhi', 'North', '2025-11-15');

-- Step 1: insert a new version, copying the unchanged attributes from the current row
INSERT INTO dim_customer (customer_id, name, city, region, segment, valid_from, valid_to, is_current)
SELECT d.customer_id, d.name, ch.new_city, ch.new_region, d.segment, ch.effective_date, '9999-12-31', 1
FROM dim_customer AS d
JOIN customer_changes AS ch ON ch.customer_id = d.customer_id
WHERE d.is_current = 1
  AND (d.city IS NOT ch.new_city OR d.region <> ch.new_region);

-- Step 2: close the old version on the day the change takes effect
UPDATE dim_customer
SET valid_to   = (SELECT ch.effective_date FROM customer_changes AS ch
                  WHERE ch.customer_id = dim_customer.customer_id),
    is_current = 0
WHERE customer_id IN (SELECT customer_id FROM customer_changes)
  AND is_current = 1
  AND valid_from < (SELECT ch.effective_date FROM customer_changes AS ch
                    WHERE ch.customer_id = dim_customer.customer_id);

SELECT customer_key, customer_id, name, city, region, valid_from, valid_to, is_current
FROM dim_customer
WHERE customer_id = 3
ORDER BY customer_key;

CREATE TABLE fact_sales (
    order_id       INTEGER NOT NULL,
    line_no        INTEGER NOT NULL,
    order_date_key INTEGER NOT NULL,
    customer_key   INTEGER NOT NULL,
    product_key    INTEGER NOT NULL,
    order_status   TEXT NOT NULL,
    quantity       INTEGER NOT NULL,
    unit_price     REAL NOT NULL,
    line_amount    REAL NOT NULL,
    PRIMARY KEY (order_id, line_no)          -- the declared grain: one row per order line
);

INSERT INTO fact_sales
SELECT oi.order_id,
       oi.line_no,
       CAST(REPLACE(o.order_date, '-', '') AS INTEGER),
       c.customer_key,
       p.product_key,
       o.status,
       oi.quantity,
       oi.unit_price,
       oi.quantity * oi.unit_price
FROM order_items AS oi
JOIN orders AS o       ON o.order_id = oi.order_id
JOIN dim_customer AS c ON c.customer_id = o.customer_id
                      AND o.order_date >= c.valid_from
                      AND o.order_date <  c.valid_to       -- the version valid on the order date
JOIN dim_product AS p  ON p.product_id = oi.product_id;

SELECT (SELECT COUNT(*) FROM fact_sales)                       AS fact_rows,
       (SELECT COUNT(*) FROM order_items)                      AS source_rows,
       (SELECT ROUND(SUM(line_amount), 2) FROM fact_sales)     AS fact_total,
       (SELECT ROUND(SUM(quantity * unit_price), 2) FROM order_items) AS source_total;

SELECT c.customer_key, c.city, c.region, c.valid_from,
       COUNT(*)                     AS lines,
       ROUND(SUM(f.line_amount), 2) AS revenue
FROM fact_sales AS f
JOIN dim_customer AS c ON c.customer_key = f.customer_key
WHERE c.customer_id = 3
GROUP BY c.customer_key, c.city, c.region, c.valid_from
ORDER BY c.customer_key;

-- Completed revenue by month and region, as the customer's region was at the time
SELECT d.year_month,
       c.region,
       ROUND(SUM(f.line_amount), 2) AS revenue
FROM fact_sales AS f
JOIN dim_date AS d     ON d.date_key     = f.order_date_key
JOIN dim_customer AS c ON c.customer_key = f.customer_key
WHERE f.order_status = 'completed'
  AND d.year_month >= '2025-11'
GROUP BY d.year_month, c.region
ORDER BY d.year_month, c.region;

WITH as_was AS (
    SELECT c.region, SUM(f.line_amount) AS revenue
    FROM fact_sales AS f
    JOIN dim_customer AS c ON c.customer_key = f.customer_key
    WHERE f.order_status = 'completed' AND f.order_date_key >= 20251001
    GROUP BY c.region
),
as_is AS (
    SELECT cur.region, SUM(f.line_amount) AS revenue
    FROM fact_sales AS f
    JOIN dim_customer AS c   ON c.customer_key = f.customer_key
    JOIN dim_customer AS cur ON cur.customer_id = c.customer_id AND cur.is_current = 1
    WHERE f.order_status = 'completed' AND f.order_date_key >= 20251001
    GROUP BY cur.region
)
SELECT w.region,
       ROUND(w.revenue, 2) AS q4_as_was,
       ROUND(i.revenue, 2) AS q4_as_is
FROM as_was AS w
JOIN as_is AS i ON i.region = w.region
ORDER BY w.region;

-- Daily summary built with a plain INSERT. The job runs, fails later, and is run again
CREATE TABLE daily_sales_naive (order_date TEXT, orders INTEGER, revenue REAL);

INSERT INTO daily_sales_naive
SELECT d.full_date, COUNT(DISTINCT f.order_id), ROUND(SUM(f.line_amount), 2)
FROM fact_sales AS f
JOIN dim_date AS d ON d.date_key = f.order_date_key
WHERE f.order_status = 'completed' AND d.full_date >= '2025-12-26'
GROUP BY d.full_date;

INSERT INTO daily_sales_naive          -- the retry
SELECT d.full_date, COUNT(DISTINCT f.order_id), ROUND(SUM(f.line_amount), 2)
FROM fact_sales AS f
JOIN dim_date AS d ON d.date_key = f.order_date_key
WHERE f.order_status = 'completed' AND d.full_date >= '2025-12-26'
GROUP BY d.full_date;

SELECT COUNT(*) AS rows_loaded, COUNT(DISTINCT order_date) AS distinct_days,
       ROUND(SUM(revenue), 2) AS total_revenue
FROM daily_sales_naive;

CREATE TABLE daily_sales (
    order_date TEXT PRIMARY KEY,
    orders     INTEGER NOT NULL,
    revenue    REAL NOT NULL
);

INSERT INTO daily_sales (order_date, orders, revenue)
SELECT d.full_date, COUNT(DISTINCT f.order_id), ROUND(SUM(f.line_amount), 2)
FROM fact_sales AS f
JOIN dim_date AS d ON d.date_key = f.order_date_key
WHERE f.order_status = 'completed' AND d.full_date >= '2025-12-26'
GROUP BY d.full_date
ON CONFLICT (order_date) DO UPDATE SET orders = excluded.orders, revenue = excluded.revenue;

INSERT INTO daily_sales (order_date, orders, revenue)          -- the retry: identical statement
SELECT d.full_date, COUNT(DISTINCT f.order_id), ROUND(SUM(f.line_amount), 2)
FROM fact_sales AS f
JOIN dim_date AS d ON d.date_key = f.order_date_key
WHERE f.order_status = 'completed' AND d.full_date >= '2025-12-26'
GROUP BY d.full_date
ON CONFLICT (order_date) DO UPDATE SET orders = excluded.orders, revenue = excluded.revenue;

SELECT COUNT(*) AS rows_loaded, ROUND(SUM(revenue), 2) AS total_revenue FROM daily_sales;
