# Examples

Six runnable examples that bring the topics to life. Every example prints real output, which is also shown in the topic documents.

| # | File | Topic | Needs | What it shows |
|---|---|---|---|---|
| 01 | [`01_capacity_calculator.py`](01_capacity_calculator.py) | [01](../01-the-data-problem.md) | Python | The maths of 100 GB a day, in rows and read time |
| 02 | [`02_parallel_vs_serial.py`](02_parallel_vs_serial.py) | [04](../04-distributed-computing-fundamentals.md) | Python | Partition, process in parallel, combine |
| 03 | [`03_mapreduce_word_count.py`](03_mapreduce_word_count.py) | [05](../05-hadoop-and-mapreduce.md) | Python | Map, shuffle and sort, reduce |
| - | [`hadoop_streaming/`](hadoop_streaming/) | [05](../05-hadoop-and-mapreduce.md) | Python, shell | A real Hadoop mapper and reducer |
| 04 | [`04_pyspark_quickstart.py`](04_pyspark_quickstart.py) | [06](../06-apache-spark.md), [07](../07-pyspark.md) | `pyspark`, Java 17+ | DataFrames, lazy evaluation, `explain()`, SQL, UDFs |
| 05 | [`05_simple_etl_pipeline.py`](05_simple_etl_pipeline.py) | [03](../03-what-is-data-engineering.md) | Python | A complete idempotent ETL pipeline |
| 06 | [`06_databricks_platform_tour.py`](06_databricks_platform_tour.py) | [09](../09-modern-data-platforms-and-databricks.md) | Databricks workspace | Partitions, catalogs, Delta time travel, volumes |

## Quick start

```bash
cd examples
python 01_capacity_calculator.py
python 03_mapreduce_word_count.py
python 05_simple_etl_pipeline.py

pip install pyspark            # requires Java 17+
python 04_pyspark_quickstart.py
```

## Notes

- **Example 02** measures real speed-up, which depends on your CPU. On machines with one or two cores the gain is small. Try it on four or more cores.
- **Example 06** is in Databricks *source format*: import it into a workspace (**Workspace → Import**) and it opens as a notebook with cells.
- Example 04 disables Adaptive Query Execution only to keep the printed plan simple to read.
