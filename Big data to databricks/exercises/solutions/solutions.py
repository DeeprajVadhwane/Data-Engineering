"""
Reference solutions for exercises/README.md.

Run all:  python exercises/solutions/solutions.py
"""
from pyspark.sql import SparkSession, Window, functions as F

spark = (
    SparkSession.builder.master("local[*]")
    .appName("exercise-solutions")
    .config("spark.ui.showConsoleProgress", "false")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

sales = (
    spark.read.csv("data/sales_sample.csv", header=True, inferSchema=True)
    .withColumn("order_date", F.to_date("order_date"))
    .withColumn("promised_date", F.to_date("promised_date"))
    .withColumn("delivered_date", F.to_date("delivered_date"))
)

# ---------------------------------------------------------------- Exercise 1
print("Exercise 1 - orders and average order value per city")
(
    sales.groupBy("city")
    .agg(F.count("*").alias("orders"), F.round(F.avg("revenue"), 1).alias("avg_order_value"))
    .orderBy(F.desc("orders"), "city")
    .show()
)

# ---------------------------------------------------------------- Exercise 2
print("Exercise 2 - top 3 products by revenue")
(
    sales.groupBy("product")
    .agg(F.sum("revenue").alias("total_revenue"))
    .orderBy(F.desc("total_revenue"))
    .limit(3)
    .show()
)

# ---------------------------------------------------------------- Exercise 3
print("Exercise 3 - revenue share by category")
total = sales.agg(F.sum("revenue")).first()[0]
(
    sales.groupBy("category")
    .agg(F.sum("revenue").alias("revenue"))
    .withColumn("pct_of_total", F.round(100 * F.col("revenue") / F.lit(total), 1))
    .orderBy(F.desc("revenue"))
    .show()
)

# ---------------------------------------------------------------- Exercise 4
print("Exercise 4 - late delivery rate by category")
(
    sales.withColumn("is_late", F.col("delivered_date") > F.col("promised_date"))
    .groupBy("category")
    .agg(
        F.sum(F.col("is_late").cast("int")).alias("late_orders"),
        F.count("*").alias("orders"),
    )
    .withColumn("late_pct", F.round(100 * F.col("late_orders") / F.col("orders"), 1))
    .orderBy(F.desc("late_pct"))
    .show()
)

# ---------------------------------------------------------------- Exercise 5
print("Exercise 5 - monthly revenue with month-over-month change")
monthly = (
    sales.withColumn("month", F.date_format("order_date", "yyyy-MM"))
    .groupBy("month")
    .agg(F.sum("revenue").alias("revenue"))
)
w = Window.orderBy("month")
(
    monthly.withColumn("prev_month", F.lag("revenue").over(w))
    .withColumn("change", F.col("revenue") - F.col("prev_month"))
    .orderBy("month")
    .show()
)

# ---------------------------------------------------------------- Exercise 6
print("Exercise 6 - which rows does the Silver step reject?")
raw = spark.read.csv("data/sales_raw_dirty.csv", header=True, inferSchema=True)
dupes = raw.groupBy(raw.columns).count().filter("count > 1")
print("duplicate rows:")
dupes.select("order_id", "count").show()
print("missing city / missing quantity / non-positive revenue:")
raw.filter(
    F.col("city").isNull() | F.col("quantity").isNull() | (F.col("revenue") <= 0)
).select("order_id", "city", "quantity", "revenue").show()

spark.stop()
