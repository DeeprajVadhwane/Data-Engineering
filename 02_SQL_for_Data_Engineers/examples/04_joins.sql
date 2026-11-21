-- Module 02, 04 · Joins
-- Every query from the topic, in order.
-- Run:  python run_sql.py 04_joins.sql

-- Each order with its customer's name and region
SELECT o.order_id, o.order_date, c.name, c.region
FROM orders AS o
INNER JOIN customers AS c ON c.customer_id = o.customer_id
ORDER BY o.order_id
LIMIT 5;

-- Every customer with an order count, including customers who never ordered
SELECT c.customer_id, c.name, COUNT(o.order_id) AS orders
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name
ORDER BY orders, c.customer_id
LIMIT 8;

-- Customer 9 has never ordered
SELECT COUNT(*)          AS count_star,
       COUNT(o.order_id) AS count_orders
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
WHERE c.customer_id = 9;

-- 60 customers x 916 orders: a missing ON condition
SELECT COUNT(*) AS accidental_rows FROM customers, orders;

-- 60 customers x 16 products: on purpose, every customer-product combination
SELECT COUNT(*) AS combinations FROM customers CROSS JOIN products;

-- a.customer_id < b.customer_id removes self-pairs and mirrored duplicates
SELECT a.name AS customer_a, b.name AS customer_b, a.city
FROM customers AS a
JOIN customers AS b ON a.city = b.city AND a.customer_id < b.customer_id
ORDER BY a.city, a.customer_id, b.customer_id
LIMIT 5;

-- Anti-join: customers who have never placed an order
SELECT c.customer_id, c.name, c.region
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL
ORDER BY c.customer_id;

-- Semi-join: customers with at least one returned item. Each customer counts once
SELECT COUNT(*) AS customers_with_a_return
FROM customers AS c
WHERE EXISTS (SELECT 1
              FROM orders AS o
              JOIN returns AS r ON r.order_id = o.order_id
              WHERE o.customer_id = c.customer_id);

-- Condition in ON: still lists every customer (60), matching only cancelled orders
SELECT COUNT(DISTINCT c.customer_id) AS customers_in_on
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id AND o.status = 'cancelled';

-- Condition in WHERE: customers without a cancelled order are filtered out again
SELECT COUNT(DISTINCT c.customer_id) AS customers_in_where
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
WHERE o.status = 'cancelled';

-- Right answer: the shipping fee is charged once per order
SELECT ROUND(SUM(shipping_fee), 2) AS shipping_total, COUNT(*) AS orders
FROM orders
WHERE status = 'completed';

-- Wrong answer: after joining to the lines, each order's fee repeats once per line
SELECT ROUND(SUM(o.shipping_fee), 2) AS shipping_after_join, COUNT(*) AS rows_joined
FROM orders AS o
JOIN order_items AS oi ON oi.order_id = o.order_id
WHERE o.status = 'completed';

-- order_items becomes one row per order first, so the join no longer repeats orders
SELECT ROUND(SUM(o.shipping_fee), 2) AS shipping_total, COUNT(*) AS orders
FROM orders AS o
JOIN (SELECT order_id, SUM(quantity * unit_price) AS items_total
      FROM order_items
      GROUP BY order_id) AS t ON t.order_id = o.order_id
WHERE o.status = 'completed';

SELECT COUNT(*) AS both_key_columns
FROM order_items AS oi
JOIN returns AS r ON r.order_id = oi.order_id AND r.line_no = oi.line_no;

SELECT COUNT(*) AS order_id_only
FROM order_items AS oi
JOIN returns AS r ON r.order_id = oi.order_id;

SELECT customer_id, COUNT(*) AS n
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;

-- SCAN the orders, then SEARCH customers by primary key for each one
EXPLAIN QUERY PLAN
SELECT o.order_id, c.name
FROM orders AS o
JOIN customers AS c ON c.customer_id = o.customer_id
WHERE o.order_date >= '2025-12-01';
