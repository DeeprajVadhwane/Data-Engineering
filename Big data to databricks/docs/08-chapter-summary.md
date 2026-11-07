# 08 · Chapter Summary

**← Previous** [07 · Databricks, Lakehouse and Medallion](07-databricks-lakehouse-medallion.md) · [🏠 Home](../README.md) · **Next →** [09 · Common Misconceptions](09-common-misconceptions.md)

> A one-stop revision page for the concept chapters (01–07).

## Table of contents

- [Technology evolution at a glance](#technology-evolution-at-a-glance)
- [Important terminology](#important-terminology)
- [Interview questions](#interview-questions)
- [Practical exercises](#practical-exercises)
- [Official references](#official-references)
- [Final learning perspective](#final-learning-perspective)

---

## Technology evolution at a glance

| Technology | Main purpose |
| --- | --- |
| Traditional computing | Single-machine processing |
| Vertical scaling | Increasing resources on one machine |
| Horizontal scaling | Adding multiple machines |
| Distributed computing | Coordinating processing across machines |
| Hadoop | Distributed storage and processing ecosystem |
| HDFS | Distributed file storage |
| MapReduce | Distributed batch processing |
| Apache Spark | Distributed processing engine |
| PySpark | Python API for Spark |
| Databricks | Unified data and AI platform |
| Delta Lake | Reliable data-lake table storage |
| Lakehouse | Unified data architecture |

## Important terminology

| Term | Definition |
| --- | --- |
| Node | An individual machine in a distributed system |
| Cluster | A group of connected computing resources |
| HDFS | Hadoop Distributed File System |
| NameNode | HDFS metadata manager |
| DataNode | HDFS data-block storage component |
| MapReduce | Distributed processing model |
| Driver | Coordinates a Spark application |
| Executor | Executes Spark tasks |
| Partition | Logical division of a dataset |
| Transformation | Operation that creates a new dataset |
| Action | Operation that triggers computation |
| Lazy evaluation | Delayed execution of transformations |
| DataFrame | Structured distributed dataset |
| Delta Lake | Storage framework with transaction capabilities |
| Medallion architecture | Bronze, Silver and Gold data layers |

More in the [glossary](glossary.md).

## Interview questions

<details><summary><strong>Big Data and scaling</strong> (questions 1–5)</summary>

1. What is Big Data, and why do organisations need Big Data technologies?
2. Explain the five Vs of Big Data.
3. What is the difference between vertical and horizontal scaling?
4. What is distributed computing?
5. Differentiate parallel processing and distributed processing.

</details>

<details><summary><strong>Hadoop</strong> (questions 6–11)</summary>

6. What is Apache Hadoop?
7. Explain HDFS architecture.
8. What are the NameNode and DataNode?
9. What is block replication?
10. Explain MapReduce with an example.
11. What is the difference between Map, Shuffle and Reduce?

</details>

<details><summary><strong>Spark and PySpark</strong> (questions 12–19)</summary>

12. Why was Apache Spark introduced?
13. Explain Spark architecture.
14. What is the responsibility of the Driver?
15. What is an Executor?
16. What are partitions in Spark?
17. What is PySpark?
18. Differentiate Pandas and PySpark.
19. Explain lazy evaluation.

</details>

<details><summary><strong>Databricks and the lakehouse</strong> (questions 20–23)</summary>

20. What is Databricks?
21. What is Delta Lake?
22. Explain lakehouse architecture.
23. What is Medallion architecture?

</details>

Practise these with the [knowledge check](10-knowledge-check.md).

## Practical exercises

These eight tasks are done in the hands-on part. Each links to the place where it is explained.

| # | Task | Where |
| --- | --- | --- |
| 1 | Create a Spark DataFrame from a list of tuples | [Hands-On, Step 1](11-hands-on-guide.md#step-1-create-a-dataframe) |
| 2 | Display the DataFrame schema | [Hands-On, Step 1](11-hands-on-guide.md#step-1-create-a-dataframe) |
| 3 | Count the total number of records | [Hands-On, Step 1](11-hands-on-guide.md#step-1-create-a-dataframe) |
| 4 | Filter orders with revenue greater than 500 | [Hands-On, Step 3](11-hands-on-guide.md#step-3-transform-the-data) |
| 5 | Calculate total revenue by city | [Hands-On, Step 3](11-hands-on-guide.md#step-3-transform-the-data) |
| 6 | Repartition the DataFrame into three partitions | [Hands-On, Step 2](11-hands-on-guide.md#step-2-look-at-partitions) |
| 7 | Inspect the execution plan with `explain()` | [Hands-On, Step 5](11-hands-on-guide.md#step-5-read-the-execution-plan) |
| 8 | Save the DataFrame as a Delta table | [Hands-On, pipeline](11-hands-on-guide.md#bronze--silver--gold-pipeline) |

Extra practice: [exercises/](../exercises/README.md).

## Official references

| Resource | Link |
| --- | --- |
| Apache Hadoop | [hadoop.apache.org](https://hadoop.apache.org/) |
| HDFS architecture | [HDFS Design](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html) |
| Apache Spark | [Spark documentation](https://spark.apache.org/docs/latest/) |
| Spark architecture | [Cluster overview](https://spark.apache.org/docs/latest/cluster-overview.html) |
| PySpark | [PySpark API](https://spark.apache.org/docs/latest/api/python/) |
| Databricks | [Databricks documentation](https://docs.databricks.com/) |
| Delta Lake | [Delta Lake documentation](https://docs.delta.io/) |
| Medallion architecture | [Databricks medallion guide](https://docs.databricks.com/aws/en/lakehouse/medallion) |

## Final learning perspective

The evolution of data engineering is not just the evolution of languages or tools. It is the evolution of how organisations **store, manage, process and extract value from data**:

```text
Traditional computing → Distributed computing → Hadoop → Apache Spark → PySpark → Databricks → Production data engineering
```

The goal is to move beyond writing individual SQL queries or scripts, and to design **scalable, reliable, production-ready data pipelines**.

> ℹ️ Examples use illustrative data and simplified architectures. Real cluster configurations, storage behaviour and execution plans depend on the deployment environment and workload.

**Next:** test yourself in [09 · Common Misconceptions](09-common-misconceptions.md) and [10 · Knowledge Check](10-knowledge-check.md), then start coding in [11 · Hands-On Guide](11-hands-on-guide.md).

---

**← Previous** [07 · Databricks, Lakehouse and Medallion](07-databricks-lakehouse-medallion.md) · [🏠 Home](../README.md) · **Next →** [09 · Common Misconceptions](09-common-misconceptions.md)
