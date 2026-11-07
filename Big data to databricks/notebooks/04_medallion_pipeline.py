# Databricks notebook source
# MAGIC %md
# MAGIC # 04 · Bronze → Silver → Gold with Delta tables
# MAGIC Databricks version of `examples/local/retail_medallion_pipeline.py`.
# MAGIC
# MAGIC **Before you run:** upload `data/sales_raw_dirty.csv` to a Volume and set the widgets below.

# COMMAND ----------
dbutils.widgets.text("catalog", "etl_pipeline")
dbutils.widgets.text("csv_path", "/Volumes/etl_pipeline/default/raw/sales_raw_dirty.csv")
catalog = dbutils.widgets.get("catalog")
csv_path = dbutils.widgets.get("csv_path")

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.bronze")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.silver")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.gold")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 🥉 Bronze: raw data, as ingested

# COMMAND ----------
from pyspark.sql import functions as F

bronze = (
    spark.read.csv(csv_path, header=True, inferSchema=True)
    .withColumn("_ingested_at", F.current_timestamp())
)
bronze.write.format("delta").mode("overwrite").saveAsTable(f"{catalog}.bronze.sales")
print("bronze rows:", spark.table(f"{catalog}.bronze.sales").count())

# COMMAND ----------
# MAGIC %md
# MAGIC ## 🥈 Silver: cleaned and validated

# COMMAND ----------
silver = (
    spark.table(f"{catalog}.bronze.sales")
    .dropDuplicates(["order_id"])
    .withColumn("city", F.initcap(F.trim("city")))
    .filter(F.col("city").isNotNull() & (F.col("city") != ""))
    .filter(F.col("quantity").isNotNull() & (F.col("revenue") > 0))
    .withColumn("order_date", F.to_date("order_date"))
    .withColumn("promised_date", F.to_date("promised_date"))
    .withColumn("delivered_date", F.to_date("delivered_date"))
    .withColumn("is_late", F.col("delivered_date") > F.col("promised_date"))
    .drop("_ingested_at")
)
silver.write.format("delta").mode("overwrite").saveAsTable(f"{catalog}.silver.sales")
print("silver rows:", spark.table(f"{catalog}.silver.sales").count())

# COMMAND ----------
# MAGIC %md
# MAGIC ## 🥇 Gold: business-ready tables

# COMMAND ----------
(
    spark.table(f"{catalog}.silver.sales")
    .groupBy("city")
    .agg(F.count("*").alias("orders"),
         F.sum("revenue").alias("total_revenue"),
         F.round(F.avg("revenue"), 1).alias("avg_order_value"))
    .write.format("delta").mode("overwrite").saveAsTable(f"{catalog}.gold.revenue_by_city")
)
display(spark.table(f"{catalog}.gold.revenue_by_city").orderBy(F.desc("total_revenue")))

# COMMAND ----------
# MAGIC %md
# MAGIC ## 🕰️ Bonus: Delta time travel

# COMMAND ----------
display(spark.sql(f"DESCRIBE HISTORY {catalog}.gold.revenue_by_city"))
