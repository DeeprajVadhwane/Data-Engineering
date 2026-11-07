# 10 · Common Misconceptions

**← Previous** [09 · Real-World Use Cases](09-real-world-use-cases.md) · [🏠 Home](../README.md) · **Next →** [11 · Knowledge Check](11-knowledge-check.md)

> Learners (and interviewers!) often trip over the same ideas. Read this before your first interview or lesson.

| # | Misconception | Reality |
| --- | --- | --- |
| 1 | Hadoop is only a storage technology | Hadoop includes distributed **storage (HDFS)** and **processing (MapReduce)** |
| 2 | HDFS and MapReduce are the same thing | HDFS **stores** data; MapReduce **processes** it |
| 3 | Spark completely replaced Hadoop | Spark can coexist with Hadoop storage and infrastructure |
| 4 | Spark always processes everything in RAM | Spark uses memory **and** disk depending on the plan and resources |
| 5 | PySpark is a different processing engine | PySpark is the **Python API** for Apache Spark |
| 6 | Every partition runs on its own machine | Partitions are **logical** slices; tasks are scheduled on available resources |
| 7 | Databricks is just a notebook | It is a broader data and AI platform: compute, governance, orchestration, analytics |
| 8 | PySpark is always faster than Pandas | Depends on data size, operations, overhead and resources. Small data is often faster in Pandas |
| 9 | `filter()` reads the data immediately | Transformations are **lazy**; an action triggers execution |
| 10 | More partitions is always better | Too many tiny partitions add scheduling overhead; too few leave cores idle |

## Quick self-test

Cover the right-hand column above and explain each misconception in one sentence. If you can do that for all ten, you understand the foundations.

---

**← Previous** [09 · Real-World Use Cases](09-real-world-use-cases.md) · [🏠 Home](../README.md) · **Next →** [11 · Knowledge Check](11-knowledge-check.md)
