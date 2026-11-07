"""PySpark quickstart: DataFrames, lazy evaluation, shuffles and SQL.

Setup:  pip install pyspark      (Java 17+ required)
Run:    python 04_pyspark_quickstart.py
Also runs unchanged in a Databricks notebook if you delete the SparkSession lines.
"""
from pyspark.sql import SparkSession, functions as F

spark = (SparkSession.builder.master("local[2]").appName("quickstart")
         .config("spark.ui.enabled", "false")
         .config("spark.sql.shuffle.partitions", "4")
         .config("spark.sql.adaptive.enabled", "false")   # keeps the plan simple to read
         .getOrCreate())
spark.sparkContext.setLogLevel("ERROR")

# 1. Create a small DataFrame (in real life: spark.read.parquet("..."))
rows = [(1, "South", 120.0), (2, "North", 80.0), (3, "South", 300.0),
        (4, "East", 150.0), (5, "North", 220.0), (6, "South", 90.0),
        (7, "East", 60.0), (8, "North", 400.0)]
df = spark.createDataFrame(rows, ["order_id", "region", "amount"])
print("Schema:"); df.printSchema()

# 2. Transformations only BUILD A PLAN. Nothing runs yet.
result = (df.filter(F.col("amount") > 100)
            .groupBy("region")
            .agg(F.count("*").alias("orders"), F.sum("amount").alias("revenue")))
print("Plan built. No work has been done yet.\n")

# 3. An ACTION triggers execution.
print("Result (action: show):")
result.orderBy("region").show()

# 4. Look at the plan Spark made. 'Exchange' marks a shuffle (caused by groupBy).
print("Physical plan:")
result.explain()

# 5. The same question in SQL: both compile to the same engine.
df.createOrReplaceTempView("sales")
print("\nSame question in SQL:")
spark.sql("""
    SELECT region, COUNT(*) AS orders, SUM(amount) AS revenue
    FROM sales WHERE amount > 100
    GROUP BY region ORDER BY region
""").show()

# 6. UDFs vs built-in functions: prefer built-ins (they run inside the JVM and can be optimised).
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

@udf(StringType())
def band_udf(amount):                      # Python UDF: rows are copied to Python and back
    return "large" if amount >= 200 else "small"

print("Python UDF vs built-in when/otherwise (same answer):")
(df.withColumn("band_udf", band_udf("amount"))
   .withColumn("band_builtin", F.when(F.col("amount") >= 200, "large").otherwise("small"))
   .orderBy("order_id").show(4))

spark.stop()
