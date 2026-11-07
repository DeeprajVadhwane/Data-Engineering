# Databricks notebook source
# MAGIC %md
# MAGIC # 03 · Answering the five management questions
# MAGIC Uses `data/sales_sample.csv` to answer the questions from Part 1 of the guide.

# COMMAND ----------
from pyspark.sql import functions as F, Window

CSV_PATH = "/Volumes/<catalog>/<schema>/<volume>/sales_sample.csv"   # <- change me
sales = (
    spark.read.csv(CSV_PATH, header=True, inferSchema=True)
    .withColumn("order_date", F.to_date("order_date"))
    .withColumn("promised_date", F.to_date("promised_date"))
    .withColumn("delivered_date", F.to_date("delivered_date"))
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## Q1 · Top 10 selling products (by revenue)

# COMMAND ----------
display(
    sales.groupBy("product")
         .agg(F.sum("revenue").alias("total_revenue"), F.sum("quantity").alias("units"))
         .orderBy(F.desc("total_revenue")).limit(10)
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## Q2 · Which city generates the highest revenue?

# COMMAND ----------
display(sales.groupBy("city").agg(F.sum("revenue").alias("total_revenue")).orderBy(F.desc("total_revenue")))

# COMMAND ----------
# MAGIC %md
# MAGIC ## Q3 · Purchase trend (monthly revenue)

# COMMAND ----------
display(
    sales.withColumn("month", F.date_format("order_date", "yyyy-MM"))
         .groupBy("month").agg(F.sum("revenue").alias("revenue")).orderBy("month")
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## Q4 · Products with declining sales (month-over-month)

# COMMAND ----------
monthly = (
    sales.withColumn("month", F.date_format("order_date", "yyyy-MM"))
         .groupBy("product", "month").agg(F.sum("revenue").alias("revenue"))
)
w = Window.partitionBy("product").orderBy("month")
trend = (
    monthly.withColumn("prev_revenue", F.lag("revenue").over(w))
           .withColumn("change", F.col("revenue") - F.col("prev_revenue"))
           .filter(F.col("change") < 0)
)
display(trend.orderBy("change"))

# COMMAND ----------
# MAGIC %md
# MAGIC ## Q5 · How many orders were delivered late?

# COMMAND ----------
late = sales.filter(F.col("delivered_date") > F.col("promised_date"))
print(f"Late orders: {late.count()} of {sales.count()}")
display(late.groupBy("city").count().orderBy(F.desc("count")))
