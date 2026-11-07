# 90-Minute Session Plan

[🏠 Home](../README.md)

**Title:** From the Big Data problem to your first PySpark DataFrame
**Audience:** learners with basic Python/SQL · **Tools:** Databricks workspace (or local PySpark)

> 🎯 **Principle:** concepts first, code last. Spend the first hour on *why*, then let learners see the same ideas run.

| Time | Segment | Content | Materials |
| --- | --- | --- | --- |
| 0–10 min | **Why Big Data?** | 9 TB/day scenario, the 5 Vs | [Ch 01](../docs/01-introduction-to-big-data.md) |
| 10–25 min | **Traditional vs modern** | Compare the two approaches; the evolution timeline | [Ch 02](../docs/02-traditional-vs-modern-approach.md), [Ch 03](../docs/03-scaling-and-distributed-computing.md) |
| 25–40 min | **Hadoop and MapReduce** | HDFS, NameNode, DataNode, Map → Shuffle → Reduce on the whiteboard | [Ch 04](../docs/04-apache-hadoop.md) |
| 40–55 min | **Spark and PySpark** | Driver, executors, partitions, lazy evaluation; Pandas vs PySpark | [Ch 05](../docs/05-apache-spark.md), [Ch 06](../docs/06-pyspark.md) |
| 55–65 min | **Databricks and lakehouse** | Platform components, Delta Lake, Medallion | [Ch 07](../docs/07-databricks-lakehouse-medallion.md) |
| 65–85 min | **Hands-on** | Create a DataFrame, partitions, aggregation, `explain()` | [Ch 11](../docs/11-hands-on-guide.md), [notebook 01](../notebooks/01_first_dataframe.py) |
| 85–90 min | **Wrap-up** | Exit ticket | [Knowledge check](../docs/10-knowledge-check.md) |

## Facilitation tips

- **Draw before you code.** Sketch the four-machine example on a whiteboard.
- **Ask, don't tell.** Before showing `explain()`, ask: *"Has Spark processed anything yet?"*
- **Surface misconceptions** from [Chapter 09](../docs/09-common-misconceptions.md) with quick polls.
- **Compare approaches.** Have learners fill in the traditional vs modern table from [Chapter 02](../docs/02-traditional-vs-modern-approach.md) from memory.

## Assessment

- Exit ticket: the [knowledge check](../docs/10-knowledge-check.md).
- Homework: [Exercises](../exercises/README.md) 1–4, then the bonus challenges.

## Follow-up sessions

See the [learning roadmap](../docs/13-learning-roadmap.md) for modules 2–8.

---

[🏠 Home](../README.md)
