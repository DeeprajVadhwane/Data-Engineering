# Exercises

[🏠 Home](../README.md) · [Knowledge check](../docs/11-knowledge-check.md) · [Reference solutions](solutions/solutions.py)

Practice with the 60-row dataset [`data/sales_sample.csv`](../data/sales_sample.csv). Try each exercise before opening the answer.

## Setup

```python
from pyspark.sql import functions as F, Window

sales = (
    spark.read.csv("data/sales_sample.csv", header=True, inferSchema=True)
    .withColumn("order_date", F.to_date("order_date"))
    .withColumn("promised_date", F.to_date("promised_date"))
    .withColumn("delivered_date", F.to_date("delivered_date"))
)
```

**Columns:** `order_id, order_date, city, category, product, quantity, unit_price, revenue, promised_date, delivered_date`

| # | Exercise | Skills | Level |
| --- | --- | --- | --- |
| [1](#exercise-1-orders-per-city) | Orders and average order value per city | `groupBy`, `agg` | ⭐ |
| [2](#exercise-2-top-3-products) | Top 3 products by revenue | `orderBy`, `limit` | ⭐ |
| [3](#exercise-3-revenue-share-by-category) | Revenue share by category | aggregation, percentages | ⭐⭐ |
| [4](#exercise-4-late-delivery-rate) | Late delivery rate by category | boolean columns, conditional counting | ⭐⭐ |
| [5](#exercise-5-month-over-month-change) | Monthly revenue with month-over-month change | window functions (`lag`) | ⭐⭐⭐ |
| [6](#exercise-6-find-the-bad-rows) | Find the rows Silver would reject | data quality | ⭐⭐⭐ |

Run every reference solution: `python exercises/solutions/solutions.py`

---

## Exercise 1: orders per city

Count orders and compute the average `revenue` per order for each city. Sort by order count.

<details><summary>Hint</summary>`F.count("*")` and `F.avg("revenue")` inside `agg()`.</details>

<details><summary>Expected result</summary>

```text
+---------+------+---------------+
|     city|orders|avg_order_value|
+---------+------+---------------+
|  Chennai|    16|         5631.3|
|   Mumbai|    15|         5526.7|
|    Delhi|    12|         3300.0|
|Hyderabad|     9|         4655.6|
|Bangalore|     8|         4875.0|
+---------+------+---------------+
```

</details>

## Exercise 2: top 3 products

Which three products earn the most revenue?

<details><summary>Expected result</summary>

```text
+------------+-------------+
|     product|total_revenue|
+------------+-------------+
| Smart Watch|        66000|
|Denim Jacket|        50400|
|   Air Fryer|        31200|
+------------+-------------+
```

</details>

## Exercise 3: revenue share by category

For each category, show revenue and its percentage of total revenue (1 decimal place).

<details><summary>Hint</summary>Get the grand total first with `sales.agg(F.sum("revenue")).first()[0]`, then use `F.lit(total)`.</details>

<details><summary>Expected result</summary>

```text
+-----------+-------+------------+
|   category|revenue|pct_of_total|
+-----------+-------+------------+
|Electronics| 115500|        39.4|
|    Fashion| 109800|        37.4|
|       Home|  68200|        23.2|
+-----------+-------+------------+
```

</details>

## Exercise 4: late delivery rate

A delivery is **late** when `delivered_date > promised_date`. Compute late orders, total orders and late percentage per category.

<details><summary>Hint</summary>Cast a boolean to int with `.cast("int")` so you can `sum()` it.</details>

<details><summary>Expected result</summary>

```text
+-----------+-----------+------+--------+
|   category|late_orders|orders|late_pct|
+-----------+-----------+------+--------+
|Electronics|         11|    20|    55.0|
|       Home|          7|    15|    46.7|
|    Fashion|          9|    25|    36.0|
+-----------+-----------+------+--------+
```

</details>

## Exercise 5: month-over-month change

Compute monthly revenue, then the change versus the previous month.

<details><summary>Hint</summary>`F.lag("revenue").over(Window.orderBy("month"))`</details>

<details><summary>Expected result</summary>

```text
+-------+-------+----------+-------+
|  month|revenue|prev_month| change|
+-------+-------+----------+-------+
|2025-01| 159600|      NULL|   NULL|
|2025-02|  37400|    159600|-122200|
|2025-03|  96500|     37400|  59100|
+-------+-------+----------+-------+
```

</details>

## Exercise 6: find the bad rows

Load [`data/sales_raw_dirty.csv`](../data/sales_raw_dirty.csv) and find (a) exact duplicate rows and (b) rows with a missing city, missing quantity or non-positive revenue.

<details><summary>Hint</summary>Group by all columns (`raw.columns`) and keep groups with `count > 1`.</details>

<details><summary>Expected result</summary>

Duplicates: orders **1003** and **1006**. Invalid rows: order **1009** (missing city), **1019** (revenue −500), **1022** (missing quantity). That is five rejected rows in total, matching the Silver step in [Chapter 07](../docs/07-lakehouse-delta-medallion.md#run-the-pipeline-locally).

</details>

## Bonus challenges

1. Add a `top_product_per_city` Gold table using `row_number()` over a window partitioned by city.
2. Write the Silver step so rejected rows go to a separate **quarantine** table instead of being dropped.
3. Use `explain()` on Exercise 1 and identify the shuffle (`Exchange`).
4. Re-implement Exercise 1 with Spark SQL (`spark.sql(...)`) and compare plans.

---

[🏠 Home](../README.md)
