"""
Small, runnable versions of the real-world use cases in docs/12-real-world-use-cases.md
They use tiny in-memory data so you can see the pattern; the same code scales to billions of rows.

Run:  python examples/local/use_case_snippets.py
"""
from pyspark.sql import SparkSession, functions as F

spark = (
    SparkSession.builder.master("local[*]")
    .appName("use-cases")
    .config("spark.ui.showConsoleProgress", "false")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

# ------------------------------------------------------------------------------
# Use case A - Log analytics: error rate per service per hour
# ------------------------------------------------------------------------------
logs = spark.createDataFrame(
    [
        ("2025-03-01 10:05:00", "checkout", 200),
        ("2025-03-01 10:15:00", "checkout", 500),
        ("2025-03-01 10:40:00", "checkout", 200),
        ("2025-03-01 10:50:00", "search", 200),
        ("2025-03-01 11:10:00", "checkout", 500),
        ("2025-03-01 11:20:00", "checkout", 500),
        ("2025-03-01 11:30:00", "search", 200),
    ],
    ["ts", "service", "status"],
).withColumn("ts", F.to_timestamp("ts"))

print("Use case A: hourly error rate per service")
(
    logs.groupBy("service", F.date_trunc("hour", "ts").alias("hour"))
    .agg(
        F.count("*").alias("requests"),
        F.sum((F.col("status") >= 500).cast("int")).alias("errors"),
    )
    .withColumn("error_pct", F.round(100 * F.col("errors") / F.col("requests"), 1))
    .orderBy("service", "hour")
    .show(truncate=False)
)

# ------------------------------------------------------------------------------
# Use case B - Fraud signal: 3+ transactions by one card within 10 minutes
# ------------------------------------------------------------------------------
tx = spark.createDataFrame(
    [
        ("card_1", "2025-03-01 12:00:10", 900.0),
        ("card_1", "2025-03-01 12:03:45", 850.0),
        ("card_1", "2025-03-01 12:07:20", 910.0),
        ("card_2", "2025-03-01 12:01:00", 40.0),
        ("card_2", "2025-03-01 12:45:00", 55.0),
        ("card_3", "2025-03-01 12:02:00", 20.0),
    ],
    ["card_id", "ts", "amount"],
).withColumn("ts", F.to_timestamp("ts"))

print("Use case B: cards with 3+ transactions in a 10-minute window")
(
    tx.groupBy("card_id", F.window("ts", "10 minutes").alias("w"))
    .agg(F.count("*").alias("txn_count"), F.sum("amount").alias("total_amount"))
    .filter(F.col("txn_count") >= 3)
    .select("card_id", F.col("w.start").alias("window_start"), "txn_count", "total_amount")
    .show(truncate=False)
)

# ------------------------------------------------------------------------------
# Use case C - IoT: flag sensors whose average temperature is too high
# ------------------------------------------------------------------------------
readings = spark.createDataFrame(
    [("s1", 71.2), ("s1", 73.0), ("s1", 98.5), ("s2", 65.1), ("s2", 66.0), ("s3", 101.0), ("s3", 99.0)],
    ["sensor_id", "temp_c"],
)
print("Use case C: sensors with average temperature above 80")
(
    readings.groupBy("sensor_id")
    .agg(F.round(F.avg("temp_c"), 1).alias("avg_temp"), F.max("temp_c").alias("max_temp"))
    .filter(F.col("avg_temp") > 80)
    .show()
)

spark.stop()
