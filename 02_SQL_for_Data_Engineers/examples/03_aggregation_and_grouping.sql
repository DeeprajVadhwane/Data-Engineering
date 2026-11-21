-- Module 02, 03 · Aggregation and Grouping
-- Every query from the topic, in order.
-- Run:  python run_sql.py 03_aggregation_and_grouping.sql

-- COUNT(*) versus COUNT(column) versus COUNT(DISTINCT column)
SELECT COUNT(*)                AS total_customers,
       COUNT(segment)          AS with_segment,
       COUNT(DISTINCT region)  AS regions,
       COUNT(DISTINCT segment) AS segments
FROM customers;

-- Summary statistics for the order lines
SELECT COUNT(*)                     AS line_count,
       SUM(quantity)                AS units,
       ROUND(AVG(unit_price), 2)    AS avg_price,
       MIN(unit_price)              AS min_price,
       MAX(unit_price)              AS max_price
FROM order_items;

-- Nothing matches: COUNT gives 0, SUM gives NULL
SELECT COUNT(*)                     AS line_count,
       SUM(quantity)                AS total_units,
       COALESCE(SUM(quantity), 0)   AS total_units_or_zero
FROM order_items
WHERE quantity > 100;

-- One row per status
SELECT status,
       COUNT(*)                   AS orders,
       ROUND(AVG(shipping_fee), 2) AS avg_shipping_fee
FROM orders
GROUP BY status
ORDER BY orders DESC;

-- Orders per month. strftime('%Y-%m', ...) is SQLite's way to cut a date down to year-month
SELECT strftime('%Y-%m', order_date) AS month,
       COUNT(*)                      AS orders
FROM orders
GROUP BY strftime('%Y-%m', order_date)
ORDER BY month;

-- Completed orders per month and channel, November and December only
SELECT strftime('%Y-%m', order_date) AS month,
       channel,
       COUNT(*)                      AS orders
FROM orders
WHERE status = 'completed'
  AND order_date >= '2025-11-01'
GROUP BY strftime('%Y-%m', order_date), channel
ORDER BY month, channel;

SELECT segment, COUNT(*) AS customers
FROM customers
GROUP BY segment
ORDER BY segment;

-- Products with more than 500,000 of gross sales (a condition on a total, so HAVING)
SELECT product_id,
       SUM(quantity)                      AS units,
       ROUND(SUM(quantity * unit_price), 2) AS gross_sales
FROM order_items
GROUP BY product_id
HAVING SUM(quantity * unit_price) > 500000
ORDER BY gross_sales DESC;

-- Monthly orders with one column per channel
SELECT strftime('%Y-%m', order_date) AS month,
       SUM(CASE WHEN channel = 'web'         THEN 1 ELSE 0 END) AS web,
       SUM(CASE WHEN channel = 'app'         THEN 1 ELSE 0 END) AS app,
       SUM(CASE WHEN channel = 'marketplace' THEN 1 ELSE 0 END) AS marketplace,
       COUNT(*)                                                 AS total
FROM orders
GROUP BY strftime('%Y-%m', order_date)
ORDER BY month;

-- Cancellation rate by channel
SELECT channel,
       COUNT(*) AS orders,
       ROUND(100.0 * SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*), 1) AS cancel_pct
FROM orders
GROUP BY channel
ORDER BY cancel_pct DESC;

-- SQLite's plan for a simple GROUP BY
EXPLAIN QUERY PLAN
SELECT channel, COUNT(*) AS orders
FROM orders
GROUP BY channel;

-- A profile of the customers table
SELECT COUNT(*)                     AS total_rows,
       COUNT(city)                  AS non_null_city,
       COUNT(*) - COUNT(city)       AS null_city,
       COUNT(DISTINCT customer_id)  AS distinct_ids,
       MIN(signup_date)             AS first_signup,
       MAX(signup_date)             AS last_signup
FROM customers;
