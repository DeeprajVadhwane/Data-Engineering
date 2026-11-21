-- Module 02, 09 · Query Performance and Execution
-- Every query from the topic, in order.
-- Run:  python run_sql.py 09_query_performance_and_execution.sql

EXPLAIN QUERY PLAN
SELECT order_id, order_date, status
FROM orders
WHERE customer_id = 17;

CREATE INDEX idx_orders_customer ON orders (customer_id);

EXPLAIN QUERY PLAN
SELECT order_id, order_date, status
FROM orders
WHERE customer_id = 17;

CREATE INDEX idx_orders_cust_date_status ON orders (customer_id, order_date, status);

EXPLAIN QUERY PLAN
SELECT order_date, status
FROM orders
WHERE customer_id = 17;

EXPLAIN QUERY PLAN
SELECT order_id FROM orders WHERE order_date = '2025-12-01';

EXPLAIN QUERY PLAN
SELECT COUNT(*) FROM orders WHERE strftime('%Y-%m', order_date) = '2025-12';

CREATE INDEX idx_orders_date ON orders (order_date);

EXPLAIN QUERY PLAN
SELECT COUNT(*) FROM orders WHERE order_date >= '2025-12-01' AND order_date < '2026-01-01';

EXPLAIN QUERY PLAN
SELECT o.order_id, oi.product_id, oi.quantity
FROM orders AS o
JOIN order_items AS oi ON oi.order_id = o.order_id
WHERE o.customer_id = 17;

-- Which customers own the most order lines? A heavy hitter here would be a skew risk
SELECT o.customer_id, COUNT(*) AS lines
FROM order_items AS oi
JOIN orders AS o ON o.order_id = oi.order_id
GROUP BY o.customer_id
ORDER BY lines DESC, o.customer_id
LIMIT 5;
