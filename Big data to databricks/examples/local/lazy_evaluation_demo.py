"""
Prove to yourself that Spark transformations are lazy.

Run:  python examples/local/lazy_evaluation_demo.py
"""
import time
from pyspark.sql import SparkSession, functions as F

spark = (
    SparkSession.builder.master("local[*]")
    .appName("lazy-demo")
    .config("spark.ui.showConsoleProgress", "false")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

df = spark.read.csv("data/sales_sample.csv", header=True, inferSchema=True)

t0 = time.perf_counter()
filtered = df.filter(F.col("revenue") > 5000)          # transformation
selected = filtered.select("order_id", "city", "revenue")  # transformation
t1 = time.perf_counter()
print(f"Defining filter + select took {t1 - t0:.3f}s  (only builds a plan)")

print("\nPhysical plan (no data processed yet):")
selected.explain(mode="formatted")

t2 = time.perf_counter()
n = selected.count()                                   # ACTION
t3 = time.perf_counter()
print(f"\ncount() = {n}   (took {t3 - t2:.3f}s  -> real work happens here)")

spark.stop()
