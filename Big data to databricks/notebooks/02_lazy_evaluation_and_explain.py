# Databricks notebook source
# MAGIC %md
# MAGIC # 02 · Lazy evaluation and execution plans
# MAGIC Transformations only *describe* work. An **action** runs it.
# MAGIC
# MAGIC 📖 Companion guide: `docs/08-hands-on-guide.md`

# COMMAND ----------
# MAGIC %md
# MAGIC ## Load the sample data
# MAGIC Upload `data/sales_sample.csv` to a Unity Catalog **Volume** and update the path.

# COMMAND ----------
from pyspark.sql import functions as F

CSV_PATH = "/Volumes/<catalog>/<schema>/<volume>/sales_sample.csv"   # <- change me

df = spark.read.csv(CSV_PATH, header=True, inferSchema=True)

# COMMAND ----------
# MAGIC %md
# MAGIC ## Transformations: nothing is processed yet

# COMMAND ----------
filtered = df.filter(F.col("revenue") > 5000)                    # transformation
selected = filtered.select("order_id", "city", "revenue")        # transformation

# COMMAND ----------
# MAGIC %md
# MAGIC ## Inspect the plan

# COMMAND ----------
selected.explain(mode="formatted")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Action: now Spark runs the plan

# COMMAND ----------
print(selected.count())          # action
display(selected)                # action

# COMMAND ----------
# MAGIC %md
# MAGIC ### Questions to answer
# MAGIC 1. Which operations appear in the plan?
# MAGIC 2. Is the filter applied at the file scan (look for `PushedFilters`)?
# MAGIC 3. Add a `groupBy("city").count()` and run `explain()` again. Where is the **Exchange** (shuffle)?
