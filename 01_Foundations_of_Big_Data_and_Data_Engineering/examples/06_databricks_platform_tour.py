# Databricks notebook source
# MAGIC %md
# MAGIC # Platform Tour
# MAGIC A 20-minute hands-on tour of everything from Modules 01 and 02. **Run the cells one at a time** and read the output.
# MAGIC
# MAGIC You need: a Databricks workspace (Free Edition is fine) and serverless or any cluster.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 0 · Where am I?
# MAGIC `spark` is the Spark session. Databricks creates it for you in every notebook.

# COMMAND ----------

print("Spark version:", spark.version)
spark.sql("SELECT current_catalog() AS catalog, current_schema() AS schema").show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1 · Why we need distributed computing
# MAGIC Excel stops at 1,048,576 rows. Let's make 50 million rows. Nothing is computed yet: this line only builds a **plan**.

# COMMAND ----------

from pyspark.sql import functions as F

df = spark.range(0, 50_000_000)          # a DataFrame with one column, "id"
print("Plan built. Nothing has run yet.")

# COMMAND ----------

# MAGIC %md
# MAGIC `count()` is an **action**, so now Spark runs the plan.

# COMMAND ----------

print("Excel row limit :", f"{1_048_576:,}")
print("Rows in our data:", f"{df.count():,}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2 · Partitions: the data is split into chunks
# MAGIC Each partition is processed by one **task**, many tasks at the same time.

# COMMAND ----------

(df.withColumn("partition_id", F.spark_partition_id())
   .groupBy("partition_id").count()
   .orderBy("partition_id")
   .show(20))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3 · Lazy evaluation: transformations vs actions
# MAGIC Predict which cells run work immediately, then run them.

# COMMAND ----------

step1 = df.filter(F.col("id") % 2 == 0)                  # transformation
step2 = step1.withColumn("bucket", F.col("id") % 10)     # transformation
step3 = step2.groupBy("bucket").count()                  # transformation
print("No work done so far.")

# COMMAND ----------

step3.orderBy("bucket").show()                           # ACTION: runs everything above

# COMMAND ----------

# MAGIC %md
# MAGIC `explain()` prints the plan Spark made. Look for **Exchange**: that is a **shuffle** (data moving between machines), caused by `groupBy`.

# COMMAND ----------

step3.explain()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4 · Explore Unity Catalog
# MAGIC The three-level name is `catalog.schema.object`.

# COMMAND ----------

spark.sql("SHOW CATALOGS").show()

# COMMAND ----------

spark.sql("SHOW SCHEMAS").show()

# COMMAND ----------

# MAGIC %md
# MAGIC Now open **Catalog** in the left sidebar and find the same catalogs and schemas in the explorer.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5 · Create a Delta table
# MAGIC Tables created in Databricks are Delta by default. Every change creates a new **version**.

# COMMAND ----------

small = spark.range(1, 11).withColumn("amount", F.col("id") * 100)
small.write.mode("overwrite").saveAsTable("tour_amounts")
spark.sql("SELECT * FROM tour_amounts ORDER BY id").show()

# COMMAND ----------

spark.sql("DESCRIBE DETAIL tour_amounts").select("format", "numFiles", "location").show(truncate=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Change the table, then time travel

# COMMAND ----------

spark.sql("UPDATE tour_amounts SET amount = 0 WHERE id > 5")
spark.sql("SELECT * FROM tour_amounts ORDER BY id").show()

# COMMAND ----------

spark.sql("DESCRIBE HISTORY tour_amounts").select("version", "timestamp", "operation").show(truncate=False)

# COMMAND ----------

# the table as it was BEFORE the update
spark.sql("SELECT * FROM tour_amounts VERSION AS OF 0 ORDER BY id").show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6 · Files go in a volume
# MAGIC A **volume** is a governed folder for files. We create one, write a CSV into it, and list it.

# COMMAND ----------

spark.sql("CREATE VOLUME IF NOT EXISTS tour_files")
catalog, schema = spark.sql("SELECT current_catalog(), current_schema()").first()
vol_path = f"/Volumes/{catalog}/{schema}/tour_files"
print("Volume path:", vol_path)

small.coalesce(1).write.mode("overwrite").option("header", True).csv(f"{vol_path}/amounts_csv")
for f in dbutils.fs.ls(f"{vol_path}/amounts_csv"):
    print(f.name, f.size)

# COMMAND ----------

spark.read.option("header", True).csv(f"{vol_path}/amounts_csv").show(3)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7 · Clean up (optional)

# COMMAND ----------

spark.sql("DROP TABLE IF EXISTS tour_amounts")
spark.sql("DROP VOLUME IF EXISTS tour_files")

# COMMAND ----------

# MAGIC %md
# MAGIC ## What you just saw
# MAGIC | You did | Concept |
# MAGIC |---|---|
# MAGIC | 50 million rows | Far beyond Excel; Spark handles it by splitting into partitions |
# MAGIC | Nothing ran until `count()` / `show()` | Lazy evaluation |
# MAGIC | `Exchange` in `explain()` | Shuffle: data moving between machines |
# MAGIC | `catalog.schema.table` | Unity Catalog namespace |
# MAGIC | `VERSION AS OF 0` | Delta Lake time travel |
# MAGIC | `/Volumes/...` | Volumes hold files |
