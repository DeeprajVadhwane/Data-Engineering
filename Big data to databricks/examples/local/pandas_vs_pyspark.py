"""
The same business question answered with Pandas and with PySpark.

Question: what is the total revenue per city?

Run:  python examples/local/pandas_vs_pyspark.py
Requires:  pip install pandas pyspark   (and Java 17+ for PySpark)
"""
import pandas as pd
from pyspark.sql import SparkSession, functions as F

CSV = "data/sales_sample.csv"

# ---------------------------------------------------------------- Pandas
pdf = pd.read_csv(CSV)
pandas_result = (
    pdf.groupby("city")["revenue"].sum().sort_values(ascending=False)
)
print("PANDAS\n", pandas_result, "\n")

# --------------------------------------------------------------- PySpark
spark = (
    SparkSession.builder.master("local[*]")
    .appName("pandas-vs-pyspark")
    .config("spark.ui.showConsoleProgress", "false")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")

sdf = spark.read.csv(CSV, header=True, inferSchema=True)
spark_result = (
    sdf.groupBy("city")
    .agg(F.sum("revenue").alias("total_revenue"))
    .orderBy(F.desc("total_revenue"))
)
print("PYSPARK")
spark_result.show()

spark.stop()
