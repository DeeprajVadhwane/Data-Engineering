-- Module 02, 06 · Window Functions
-- Every query from the topic, in order.
-- Run:  python run_sql.py 06_window_functions.sql

-- Customers ranked by completed orders, three ways
WITH n AS (
    SELECT customer_id, COUNT(*) AS orders
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
)
SELECT customer_id,
       orders,
       ROW_NUMBER() OVER (ORDER BY orders DESC, customer_id) AS row_num,
       RANK()       OVER (ORDER BY orders DESC)              AS rnk,
       DENSE_RANK() OVER (ORDER BY orders DESC)              AS dense_rnk
FROM n
ORDER BY orders DESC, customer_id
LIMIT 8;

-- The 2 best-selling products in each category
WITH product_revenue AS (
    SELECT p.category, p.name,
           ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
    FROM order_items AS oi
    JOIN products AS p ON p.product_id = oi.product_id
    JOIN orders AS o   ON o.order_id   = oi.order_id
    WHERE o.status = 'completed'
    GROUP BY p.product_id, p.category, p.name
)
SELECT category, name, revenue, rn
FROM (SELECT category, name, revenue,
             ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC) AS rn
      FROM product_revenue) AS ranked
WHERE rn <= 2
ORDER BY category, rn;

-- Each customer's latest order, with a tie-breaker so there is exactly one
WITH ranked AS (
    SELECT customer_id, order_id, order_date,
           ROW_NUMBER() OVER (PARTITION BY customer_id
                              ORDER BY order_date DESC, order_id DESC) AS rn
    FROM orders
)
SELECT customer_id, order_id, order_date
FROM ranked
WHERE rn = 1
ORDER BY customer_id
LIMIT 5;

-- Month-over-month revenue change
WITH monthly AS (
    SELECT strftime('%Y-%m', o.order_date) AS month,
           ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
    FROM orders AS o
    JOIN order_items AS oi ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY strftime('%Y-%m', o.order_date)
)
SELECT month,
       revenue,
       LAG(revenue) OVER (ORDER BY month) AS prev_month,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
                   / LAG(revenue) OVER (ORDER BY month), 1) AS mom_pct
FROM monthly
ORDER BY month;

-- Daily orders with a running total and a 3-day moving average
WITH daily AS (
    SELECT order_date, COUNT(*) AS orders
    FROM orders
    WHERE order_date >= '2025-12-24'
    GROUP BY order_date
)
SELECT order_date,
       orders,
       SUM(orders) OVER (ORDER BY order_date) AS running_orders,
       ROUND(AVG(orders) OVER (ORDER BY order_date
                               ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2) AS moving_avg_3d
FROM daily
ORDER BY order_date;

-- LAST_VALUE with the default frame returns the current row. It needs the full frame
WITH d AS (
    SELECT order_date, COUNT(*) AS orders
    FROM orders
    WHERE order_date BETWEEN '2025-12-27' AND '2025-12-31'
    GROUP BY order_date
)
SELECT order_date,
       orders,
       LAST_VALUE(orders) OVER (ORDER BY order_date) AS last_default_frame,
       LAST_VALUE(orders) OVER (ORDER BY order_date
                                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_full_frame
FROM d
ORDER BY order_date;

-- Each region's share of total revenue, and its rank
WITH region_revenue AS (
    SELECT c.region,
           ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
    FROM orders AS o
    JOIN customers AS c    ON c.customer_id = o.customer_id
    JOIN order_items AS oi ON oi.order_id   = o.order_id
    WHERE o.status = 'completed'
    GROUP BY c.region
)
SELECT region,
       revenue,
       ROUND(100.0 * revenue / SUM(revenue) OVER (), 1) AS share_pct,
       RANK() OVER (ORDER BY revenue DESC)              AS rnk
FROM region_revenue
ORDER BY rnk;

-- Customers split into four spend quartiles (the size is 54 / 4, so two have 14 and two have 13)
WITH spend AS (
    SELECT o.customer_id,
           ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_spend
    FROM orders AS o
    JOIN order_items AS oi ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY o.customer_id
)
SELECT quartile,
       COUNT(*)         AS customers,
       MIN(total_spend) AS min_spend,
       MAX(total_spend) AS max_spend
FROM (SELECT customer_id, total_spend,
             NTILE(4) OVER (ORDER BY total_spend) AS quartile
      FROM spend) AS bucketed
GROUP BY quartile
ORDER BY quartile;

-- SQLite sorts the rows (the window's PARTITION BY and ORDER BY), then streams through them
EXPLAIN QUERY PLAN
SELECT customer_id, order_id,
       ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn
FROM orders;
