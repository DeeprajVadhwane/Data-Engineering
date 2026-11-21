-- Module 02, 01 · Why SQL Still Matters
-- Every query from the topic, in order.
-- Run:  python run_sql.py 01_why_sql_still_matters.sql

-- How big is the XYZ database?  (UNION ALL stacks results: see Topic 05)
SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers
UNION ALL SELECT 'products',    COUNT(*) FROM products
UNION ALL SELECT 'orders',      COUNT(*) FROM orders
UNION ALL SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL SELECT 'returns',     COUNT(*) FROM returns;

-- Revenue by region, completed orders only
SELECT c.region,
       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
FROM orders AS o
JOIN customers AS c    ON c.customer_id = o.customer_id
JOIN order_items AS oi ON oi.order_id   = o.order_id
WHERE o.status = 'completed'
GROUP BY c.region
ORDER BY revenue DESC;

-- The plan the engine chose for the revenue query
EXPLAIN QUERY PLAN
SELECT c.region,
       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
FROM orders AS o
JOIN customers AS c    ON c.customer_id = o.customer_id
JOIN order_items AS oi ON oi.order_id   = o.order_id
WHERE o.status = 'completed'
GROUP BY c.region
ORDER BY revenue DESC;
