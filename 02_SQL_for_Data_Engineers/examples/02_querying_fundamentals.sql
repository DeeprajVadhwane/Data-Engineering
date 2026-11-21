-- Module 02, 02 · Querying Fundamentals
-- Every query from the topic, in order.
-- Run:  python run_sql.py 02_querying_fundamentals.sql

-- Look at a few rows first
SELECT * FROM customers LIMIT 5;

-- Choose columns and filter rows: completed app orders in December, newest first
SELECT order_id, customer_id, order_date, channel
FROM orders
WHERE status = 'completed'
  AND channel = 'app'
  AND order_date >= '2025-12-01'
ORDER BY order_date DESC, order_id DESC
LIMIT 5;

-- IN, BETWEEN and LIKE together
SELECT product_id, name, category, list_price
FROM products
WHERE category IN ('Electronics', 'Home')
  AND list_price BETWEEN 1000 AND 4500
  AND name LIKE '%er%'
ORDER BY list_price;

-- Same words, different meaning
SELECT COUNT(*) AS without_brackets
FROM orders
WHERE channel = 'web' OR channel = 'app' AND status = 'cancelled';

SELECT COUNT(*) AS with_brackets
FROM orders
WHERE (channel = 'web' OR channel = 'app') AND status = 'cancelled';

-- Which values does a column hold? A first step in exploring any table
SELECT DISTINCT status
FROM orders
ORDER BY status;

-- Attempt 2 from the business problem
SELECT COUNT(*) AS exact_match FROM orders WHERE status = 'completed';
SELECT COUNT(*) AS wrong_case   FROM orders WHERE status = 'Completed';

-- = NULL never matches. IS NULL does.
SELECT COUNT(*) AS wrong_way FROM customers WHERE city = NULL;
SELECT COUNT(*) AS right_way FROM customers WHERE city IS NULL;

-- Do the groups add up? (the CASE counts each group; Topic 03 explains the pattern)
SELECT SUM(CASE WHEN city = 'Pune'  THEN 1 ELSE 0 END) AS in_pune,
       SUM(CASE WHEN city <> 'Pune' THEN 1 ELSE 0 END) AS not_pune,
       SUM(CASE WHEN city IS NULL   THEN 1 ELSE 0 END) AS city_unknown,
       COUNT(*)                                        AS all_customers
FROM customers;

-- Test for NULL explicitly to include the unknowns
SELECT COUNT(*) AS everyone_outside_pune
FROM customers
WHERE city <> 'Pune' OR city IS NULL;

SELECT customer_id, name, COALESCE(city, 'Unknown') AS city
FROM customers
WHERE customer_id BETWEEN 14 AND 16;

SELECT customer_id, segment
FROM customers
ORDER BY segment, customer_id
LIMIT 4;

-- As text, '10' sorts before '9'. As numbers, it does not.
SELECT '10' < '9'                           AS text_compare,
       CAST('10' AS INTEGER) < CAST('9' AS INTEGER) AS number_compare;

SELECT typeof(order_id)     AS id_type,
       typeof(order_date)   AS date_type,
       typeof(shipping_fee) AS fee_type
FROM orders
LIMIT 1;
