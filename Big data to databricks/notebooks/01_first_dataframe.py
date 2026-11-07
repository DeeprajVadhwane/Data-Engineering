# Databricks notebook source
# MAGIC %md
# MAGIC # 01 · Your first Spark DataFrame
# MAGIC **Goal:** create a DataFrame, inspect partitions, filter, and aggregate revenue by city.
# MAGIC
# MAGIC 📖 Companion guide: `docs/08-hands-on-guide.md`

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 1 · Create a DataFrame

# COMMAND ----------
data = [
    (101, "Hyderabad", 500),
    (102, "Mumbai", 700),
    (103, "Hyderabad", 300),
    (104, "Bangalore", 800),
    (105, "Mumbai", 200),
    (106, "Hyderabad", 400),
]
columns = ["order_id", "city", "revenue"]

df = spark.createDataFrame(data, columns)
display(df)

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 2 · Partitions
# MAGIC Partitions are *logical slices* of the data. Three partitions does **not** mean three machines.
# MAGIC
# MAGIC > On serverless compute, RDD APIs such as `df.rdd` are not available.
# MAGIC > The `spark_partition_id()` approach below works everywhere.

# COMMAND ----------
from pyspark.sql import functions as F

df3 = df.repartition(3)
display(
    df3.withColumn("partition_id", F.spark_partition_id())
       .groupBy("partition_id").count().orderBy("partition_id")
)

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 3 · Transform

# COMMAND ----------
display(df.filter(F.col("revenue") > 300))

# COMMAND ----------
city_revenue = (
    df.groupBy("city")
      .agg(F.sum("revenue").alias("total_revenue"))
      .orderBy(F.desc("total_revenue"))
)
display(city_revenue)

# COMMAND ----------
# MAGIC %md
# MAGIC ✅ **Expected:** Hyderabad 1200 · Mumbai 900 · Bangalore 800
