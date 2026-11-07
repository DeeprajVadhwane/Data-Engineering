# 90-Minute Session Plan

[🏠 Home](../README.md)

**Title:** From the Big Data problem to your first PySpark DataFrame
**Audience:** learners with basic Python/SQL · **Tools:** Databricks workspace (or local PySpark)

> 🎯 **Principle:** don't open with `StructType` or `select()`. Start with the business problem and build the technical understanding step by step.

| Time | Segment | Content | Materials |
| --- | --- | --- | --- |
| 0–15 min | **The Big Data problem** | 10 TB/day scenario; single machine; vertical vs horizontal scaling | [Ch 01](../docs/01-big-data-problem.md), [Ch 02](../docs/02-distributed-computing.md) |
| 15–30 min | **Hadoop and MapReduce** | HDFS, NameNode, DataNode, Map → Shuffle → Reduce | [Ch 03](../docs/03-hadoop.md), [`mapreduce_simulation.py`](../examples/local/mapreduce_simulation.py) |
| 30–45 min | **Apache Spark** | Driver, executors, partitions, parallel processing | [Ch 04](../docs/04-apache-spark.md) |
| 45–55 min | **PySpark** | Why Python developers use Spark; Pandas vs PySpark | [Ch 05](../docs/05-pyspark.md) |
| 55–75 min | **Databricks practical** | Create a DataFrame, inspect partitions, aggregate | [Ch 08](../docs/08-hands-on-guide.md), [notebook 01](../notebooks/01_first_dataframe.py) |
| 75–90 min | **Discussion and exercises** | Explain the execution flow; solve a small aggregation | [Exercises](../exercises/README.md), [Knowledge check](../docs/11-knowledge-check.md) |

## Facilitation tips

- **Draw before you code.** Sketch the four-machine example on a whiteboard.
- **Ask, don't tell.** Before showing `explain()`, ask: *"Has Spark processed anything yet?"*
- **Surface misconceptions** from [Chapter 10](../docs/10-common-misconceptions.md) with quick polls.
- **Show failure.** Run the pure-Python MapReduce, then ask what happens if one "machine" dies.

## Assessment

- Exit ticket: the six questions in the [knowledge check](../docs/11-knowledge-check.md).
- Homework: Exercises 1–4, then the Bonus challenges.

## Follow-up sessions

See the [learning roadmap](../docs/12-learning-roadmap.md) for modules 2–8.

---

[🏠 Home](../README.md)
