"""
Retail sales ETL with the Medallion architecture, runnable on your laptop.

    data/sales_raw_dirty.csv  ->  Bronze  ->  Silver  ->  Gold

Bronze: raw data, stored exactly as it arrived
Silver: cleaned (trim/standardise city, drop duplicates, remove bad rows)
Gold:   business-ready aggregates

Run:  python examples/local/retail_medallion_pipeline.py
Output tables are written as Parquet under ./output/ (git-ignored).
On Databricks you would write Delta tables instead (see notebooks/04_*).
"""
from pyspark.sql import SparkSession, functions as F

spark = (
    SparkSession.builder.master("local[*]")
    .appName("retail-medallion")
    .config("spark.ui.showConsoleProgress", "false")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

# ------------------------------------------------------------------ BRONZE
bronze = (
    spark.read.csv("data/sales_raw_dirty.csv", header=True, inferSchema=True)
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_source_file", F.lit("sales_raw_dirty.csv"))
)
bronze.write.mode("overwrite").parquet("output/bronze/sales")
print(f"BRONZE rows: {bronze.count()}")

# ------------------------------------------------------------------ SILVER
silver = (
    spark.read.parquet("output/bronze/sales")
    .dropDuplicates()                                              # exact duplicates
    .withColumn("city", F.initcap(F.trim(F.col("city"))))          # ' mumbai ' -> 'Mumbai'
    .filter(F.col("city").isNotNull() & (F.col("city") != ""))     # missing city
    .filter(F.col("quantity").isNotNull())                         # missing quantity
    .filter(F.col("revenue") > 0)                                  # invalid revenue
    .withColumn("order_date", F.to_date("order_date"))
    .withColumn("promised_date", F.to_date("promised_date"))
    .withColumn("delivered_date", F.to_date("delivered_date"))
    .withColumn(
        "is_late", F.col("delivered_date") > F.col("promised_date")
    )
    .drop("_ingested_at", "_source_file")
)
silver.write.mode("overwrite").parquet("output/silver/sales")
print(f"SILVER rows: {silver.count()}  (rejected {bronze.count() - silver.count()})")

# -------------------------------------------------------------------- GOLD
gold_city = (
    silver.groupBy("city")
    .agg(
        F.count("*").alias("orders"),
        F.sum("revenue").alias("total_revenue"),
        F.round(F.avg("revenue"), 1).alias("avg_order_value"),
    )
    .orderBy(F.desc("total_revenue"))
)
gold_city.write.mode("overwrite").parquet("output/gold/revenue_by_city")

gold_late = (
    silver.groupBy("city")
    .agg(
        F.sum(F.col("is_late").cast("int")).alias("late_orders"),
        F.count("*").alias("orders"),
    )
    .withColumn("late_pct", F.round(100 * F.col("late_orders") / F.col("orders"), 1))
    .orderBy(F.desc("late_pct"))
)
gold_late.write.mode("overwrite").parquet("output/gold/late_deliveries")

print("\nGOLD: revenue by city")
gold_city.show()
print("GOLD: late deliveries by city")
gold_late.show()

spark.stop()
