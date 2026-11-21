-- Module 02, 05 · Subqueries, CTEs and Set Operations
-- Every query from the topic, in order.
-- Run:  python run_sql.py 05_subqueries_ctes_and_set_operations.sql

-- Scalar subquery: products priced above the average list price
SELECT name, list_price
FROM products
WHERE list_price > (SELECT AVG(list_price) FROM products)
ORDER BY list_price DESC;

-- Each customer's most recent order date
SELECT c.name,
       (SELECT MAX(o.order_date)
        FROM orders AS o
        WHERE o.customer_id = c.customer_id) AS last_order
FROM customers AS c
ORDER BY c.customer_id
LIMIT 5;

-- Customers whose city is not a city used by a North-region customer
-- One North customer has a NULL city, so NOT IN returns nothing at all
SELECT COUNT(*) AS not_in_result
FROM customers
WHERE city NOT IN (SELECT city FROM customers WHERE region = 'North');

SELECT COUNT(*) AS not_exists_result
FROM customers AS c
WHERE NOT EXISTS (SELECT 1
                  FROM customers AS n
                  WHERE n.region = 'North' AND n.city = c.city);

WITH completed_lines AS (
    -- Grain: one row per completed order line, with its region and quarter
    SELECT c.region,
           CASE WHEN o.order_date < '2025-10-01' THEN 'Q3' ELSE 'Q4' END AS quarter,
           oi.quantity * oi.unit_price AS line_revenue
    FROM orders AS o
    JOIN customers AS c    ON c.customer_id = o.customer_id
    JOIN order_items AS oi ON oi.order_id   = o.order_id
    WHERE o.status = 'completed'
),
by_region AS (
    -- Grain: one row per region
    SELECT region,
           SUM(CASE WHEN quarter = 'Q3' THEN line_revenue ELSE 0 END) AS q3_revenue,
           SUM(CASE WHEN quarter = 'Q4' THEN line_revenue ELSE 0 END) AS q4_revenue
    FROM completed_lines
    GROUP BY region
)
SELECT region,
       ROUND(q3_revenue, 2) AS q3_revenue,
       ROUND(q4_revenue, 2) AS q4_revenue,
       ROUND(100.0 * (q4_revenue - q3_revenue) / q3_revenue, 1) AS growth_pct
FROM by_region
ORDER BY growth_pct DESC, region;

WITH sold AS (
    -- Grain: one row per product, completed orders only
    SELECT oi.product_id,
           COUNT(*) AS lines_sold
    FROM order_items AS oi
    JOIN orders AS o ON o.order_id = oi.order_id
    WHERE o.status = 'completed'
    GROUP BY oi.product_id
),
returned AS (
    -- Grain: one row per product
    SELECT oi.product_id,
           COUNT(*) AS lines_returned
    FROM returns AS r
    JOIN order_items AS oi ON oi.order_id = r.order_id AND oi.line_no = r.line_no
    GROUP BY oi.product_id
)
SELECT p.name,
       p.category,
       s.lines_sold,
       COALESCE(r.lines_returned, 0) AS lines_returned,
       ROUND(100.0 * COALESCE(r.lines_returned, 0) / s.lines_sold, 1) AS return_rate_pct
FROM sold AS s
JOIN products AS p      ON p.product_id = s.product_id
LEFT JOIN returned AS r ON r.product_id = s.product_id
ORDER BY return_rate_pct DESC, p.name
LIMIT 6;

-- Orders per day, with a row for every day. Jan 1 and 2 have no orders and still appear
WITH RECURSIVE calendar(day) AS (
    SELECT '2025-12-29'                                  -- start
    UNION ALL
    SELECT date(day, '+1 day')                           -- repeat: add a day
    FROM calendar
    WHERE day < '2026-01-02'                             -- stop condition
)
SELECT cal.day, COUNT(o.order_id) AS orders
FROM calendar AS cal
LEFT JOIN orders AS o ON o.order_date = cal.day
GROUP BY cal.day
ORDER BY cal.day;

-- UNION ALL stacks two tables into one long list: orders and returns per month
SELECT strftime('%Y-%m', order_date) AS month, 'orders' AS metric, COUNT(*) AS value
FROM orders
GROUP BY strftime('%Y-%m', order_date)
UNION ALL
SELECT strftime('%Y-%m', return_date), 'returns', COUNT(*)
FROM returns
GROUP BY strftime('%Y-%m', return_date)
ORDER BY month, metric;

SELECT COUNT(*) AS with_union_all
FROM (SELECT region FROM customers UNION ALL SELECT region FROM customers);

SELECT COUNT(*) AS with_union
FROM (SELECT region FROM customers UNION SELECT region FROM customers);

EXPLAIN QUERY PLAN
SELECT customer_id FROM orders UNION SELECT customer_id FROM customers;

EXPLAIN QUERY PLAN
SELECT customer_id FROM orders UNION ALL SELECT customer_id FROM customers;

-- INTERSECT: customers who ordered on the app and on the web
SELECT COUNT(*) AS app_and_web
FROM (SELECT customer_id FROM orders WHERE channel = 'app'
      INTERSECT
      SELECT customer_id FROM orders WHERE channel = 'web');

-- EXCEPT: customers who ordered but have never had a return
SELECT COUNT(*) AS never_returned
FROM (SELECT customer_id FROM orders
      EXCEPT
      SELECT o.customer_id FROM orders AS o JOIN returns AS r ON r.order_id = o.order_id);
