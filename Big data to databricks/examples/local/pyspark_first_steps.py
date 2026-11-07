"""
Your first PySpark DataFrame: create, partition, filter, aggregate.
Mirrors docs/08-hands-on-guide.md.

Run:  python examples/local/pyspark_first_steps.py
"""
from pyspark.sql import SparkSession, functions as F

spark = (
    SparkSession.builder.master("local[*]")
    .appName("first-steps")
    .config("spark.ui.showConsoleProgress", "false")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

# Step 1 - create a DataFrame
data = [
    (101, "Hyderabad", 500),
    (102, "Mumbai", 700),
    (103, "Hyderabad", 300),
    (104, "Bangalore", 800),
    (105, "Mumbai", 200),
    (106, "Hyderabad", 400),
]
df = spark.createDataFrame(data, ["order_id", "city", "revenue"])
df.show()

# Step 2 - partitions are logical slices of the data
df = df.repartition(3)
print("Partitions:", df.rdd.getNumPartitions())

# Step 3 - transform: filter, then aggregate
print("Orders with revenue > 300")
df.filter(F.col("revenue") > 300).orderBy("order_id").show()

print("Total revenue by city")
(
    df.groupBy("city")
    .agg(F.sum("revenue").alias("total_revenue"))
    .orderBy(F.desc("total_revenue"))
    .show()
)

spark.stop()
