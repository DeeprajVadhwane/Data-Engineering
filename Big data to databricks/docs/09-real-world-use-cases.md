# 09 · Real-World Use Cases

**← Previous** [08 · Hands-On Guide](08-hands-on-guide.md) · [🏠 Home](../README.md) · **Next →** [10 · Common Misconceptions](10-common-misconceptions.md)

> **In this chapter:** apply what you've learned to the management questions from Chapter 01, then see the same patterns in other industries.
> ⏱️ 30 minutes · 🎯 Level: intermediate · 🧪 Code: [`03_retail_sales_analysis.py`](../notebooks/03_retail_sales_analysis.py), [`use_case_snippets.py`](../examples/local/use_case_snippets.py)

## Table of contents

- [Use case 1: e-commerce analytics](#use-case-1-e-commerce-analytics)
- [Use case 2: log analytics](#use-case-2-log-analytics)
- [Use case 3: fraud signals](#use-case-3-fraud-signals)
- [Use case 4: IoT monitoring](#use-case-4-iot-monitoring)
- [More patterns](#more-patterns)
- [How the layers apply](#how-the-layers-apply)

---

> 📊 Numbers below come from the 60-row teaching dataset [`data/sales_sample.csv`](../data/sales_sample.csv). The same code runs unchanged on billions of rows; only the cluster size changes.

## Use case 1: e-commerce analytics

Back to the five questions management asked in [Chapter 01](01-big-data-problem.md#a-business-scenario). Setup:

```python
from pyspark.sql import functions as F, Window

sales = (
    spark.read.csv("data/sales_sample.csv", header=True, inferSchema=True)
    .withColumn("order_date", F.to_date("order_date"))
    .withColumn("promised_date", F.to_date("promised_date"))
    .withColumn("delivered_date", F.to_date("delivered_date"))
)
```

### Q1 · Top selling products

```python
(sales.groupBy("product")
      .agg(F.sum("revenue").alias("total_revenue"), F.sum("quantity").alias("units"))
      .orderBy(F.desc("total_revenue")).limit(5).show())
```

```text
+-------------+-------------+-----+
|      product|total_revenue|units|
+-------------+-------------+-----+
|  Smart Watch|        66000|   11|
| Denim Jacket|        50400|   18|
|    Air Fryer|        31200|    6|
|     Backpack|        30600|   17|
|Running Shoes|        28800|    9|
+-------------+-------------+-----+
```

> 💡 Rank by revenue *and* units: Denim Jacket sells the most units among the top two, while Smart Watch earns more per sale.

### Q2 · Revenue by city

```python
sales.groupBy("city").agg(F.sum("revenue").alias("total_revenue")).orderBy(F.desc("total_revenue")).show()
```

```text
+---------+-------------+
|     city|total_revenue|
+---------+-------------+
|  Chennai|        90100|
|   Mumbai|        82900|
|Hyderabad|        41900|
|    Delhi|        39600|
|Bangalore|        39000|
+---------+-------------+
```

### Q3 · Purchase trend

```python
(sales.withColumn("month", F.date_format("order_date", "yyyy-MM"))
      .groupBy("month").agg(F.sum("revenue").alias("revenue")).orderBy("month").show())
```

```text
+-------+-------+
|  month|revenue|
+-------+-------+
|2025-01| 159600|
|2025-02|  37400|
|2025-03|  96500|
+-------+-------+
```

### Q4 · Products with declining sales

Compare each product's monthly revenue with the previous month using a **window function**:

```python
monthly = (sales.withColumn("month", F.date_format("order_date", "yyyy-MM"))
                .groupBy("product", "month").agg(F.sum("revenue").alias("revenue")))

w = Window.partitionBy("product").orderBy("month")
(monthly.withColumn("prev_revenue", F.lag("revenue").over(w))
        .withColumn("change", F.col("revenue") - F.col("prev_revenue"))
        .filter(F.col("change") < 0)
        .orderBy("change").show(5))
```

```text
+----------------+-------+-------+------------+------+
|         product|  month|revenue|prev_revenue|change|
+----------------+-------+-------+------------+------+
|     Smart Watch|2025-03|  18000|       48000|-30000|
|    Denim Jacket|2025-02|  11200|       36400|-25200|
|       Air Fryer|2025-02|   5200|       15600|-10400|
|    Denim Jacket|2025-03|   2800|       11200| -8400|
|Wireless Earbuds|2025-03|   7500|       15000| -7500|
+----------------+-------+-------+------------+------+
```

### Q5 · Late deliveries

```python
late = sales.filter(F.col("delivered_date") > F.col("promised_date"))
print(f"Late orders: {late.count()} of {sales.count()}")
late.groupBy("city").count().orderBy(F.desc("count")).show()
```

```text
Late orders: 27 of 60
+---------+-----+
|     city|count|
+---------+-----+
|  Chennai|    8|
|   Mumbai|    8|
|Bangalore|    5|
|    Delhi|    4|
|Hyderabad|    2|
+---------+-----+
```

## Use case 2: log analytics

**Scenario:** a platform emits billions of request logs per day. Operations wants hourly error rates per service.

```python
(logs.groupBy("service", F.date_trunc("hour", "ts").alias("hour"))
     .agg(F.count("*").alias("requests"),
          F.sum((F.col("status") >= 500).cast("int")).alias("errors"))
     .withColumn("error_pct", F.round(100 * F.col("errors") / F.col("requests"), 1))
     .orderBy("service", "hour").show(truncate=False))
```

```text
+--------+-------------------+--------+------+---------+
|service |hour               |requests|errors|error_pct|
+--------+-------------------+--------+------+---------+
|checkout|2025-03-01 10:00:00|3       |1     |33.3     |
|checkout|2025-03-01 11:00:00|2       |2     |100.0    |
|search  |2025-03-01 10:00:00|1       |0     |0.0      |
|search  |2025-03-01 11:00:00|1       |0     |0.0      |
+--------+-------------------+--------+------+---------+
```

**Why Spark:** log volumes outgrow a single machine, and the query is a simple distributed `groupBy`.

## Use case 3: fraud signals

**Scenario:** flag any card with three or more transactions inside ten minutes.

```python
(tx.groupBy("card_id", F.window("ts", "10 minutes").alias("w"))
   .agg(F.count("*").alias("txn_count"), F.sum("amount").alias("total_amount"))
   .filter(F.col("txn_count") >= 3)
   .select("card_id", F.col("w.start").alias("window_start"), "txn_count", "total_amount")
   .show(truncate=False))
```

```text
+-------+-------------------+---------+------------+
|card_id|window_start       |txn_count|total_amount|
+-------+-------------------+---------+------------+
|card_1 |2025-03-01 12:00:00|3        |2660.0      |
+-------+-------------------+---------+------------+
```

> ⚠️ **Limitation:** fixed (tumbling) windows can miss a burst that straddles a window boundary. Production systems use sliding windows or per-card stateful logic with **Structured Streaming**.

## Use case 4: IoT monitoring

**Scenario:** thousands of sensors report temperatures; alert on any sensor whose average is too high.

```python
(readings.groupBy("sensor_id")
         .agg(F.round(F.avg("temp_c"), 1).alias("avg_temp"), F.max("temp_c").alias("max_temp"))
         .filter(F.col("avg_temp") > 80).show())
```

```text
+---------+--------+--------+
|sensor_id|avg_temp|max_temp|
+---------+--------+--------+
|       s3|   100.0|   101.0|
|       s1|    80.9|    98.5|
+---------+--------+--------+
```

Run all three snippets: `python examples/local/use_case_snippets.py`

## More patterns

| Industry | Problem | Spark capability used |
| --- | --- | --- |
| Retail | Product recommendations from purchase history | DataFrames + MLlib |
| Banking | Regulatory reporting across millions of accounts | Batch SQL + Delta time travel for audit |
| Telecom | Network quality from call-detail records | Large joins and aggregations |
| Logistics | Delivery-time prediction | Feature engineering at scale + ML |
| Media | Real-time viewer engagement | Structured Streaming |
| Healthcare | Combining records from many systems | Schema management + governance (Unity Catalog) |

## How the layers apply

| Use case | Bronze | Silver | Gold |
| --- | --- | --- | --- |
| E-commerce | Raw order exports | Deduplicated, typed orders | Revenue by city / product / month |
| Logs | Raw log lines | Parsed fields, valid timestamps | Hourly error rates per service |
| Fraud | Raw transactions | Validated, enriched with customer info | Flagged cards, daily risk scores |
| IoT | Raw sensor events | Outliers removed, units normalised | Per-sensor health metrics |

---

**← Previous** [08 · Hands-On Guide](08-hands-on-guide.md) · [🏠 Home](../README.md) · **Next →** [10 · Common Misconceptions](10-common-misconceptions.md)
