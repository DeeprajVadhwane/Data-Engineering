# 11 · Knowledge Check

**← Previous** [10 · Common Misconceptions](10-common-misconceptions.md) · [🏠 Home](../README.md) · **Next →** [12 · Learning Roadmap](12-learning-roadmap.md)

> Try each question before opening the answer. Hands-on practice lives in [`exercises/`](../exercises/README.md).

## Table of contents

- [Questions](#questions)
- [Practice challenge](#practice-challenge)

---

## Questions

**1. What is the main limitation of vertical scaling?**

- A. It cannot increase CPU power
- B. Hardware and resource limits of a single machine
- C. It does not support Python

<details><summary>Show answer</summary>

**B.** One machine has a physical ceiling, grows expensive quickly, and remains a single point of failure.

</details>

**2. Which Hadoop component handles distributed storage?**

- A. MapReduce
- B. NameNode alone
- C. HDFS

<details><summary>Show answer</summary>

**C.** HDFS (NameNode + DataNodes) stores data. MapReduce processes it; the NameNode alone only holds metadata.

</details>

**3. What is the main job of MapReduce?**

- A. Distributed data processing
- B. Managing user access
- C. Creating dashboards

<details><summary>Show answer</summary>

**A.** It distributes the computation (Map → Shuffle & Sort → Reduce).

</details>

**4. What is PySpark?**

- A. A replacement for Python
- B. The Python API for Apache Spark
- C. A database

<details><summary>Show answer</summary>

**B.** It lets you drive the Spark engine from Python.

</details>

**5. What triggers execution of lazy DataFrame transformations?**

- A. Defining a variable
- B. Importing a library
- C. An action

<details><summary>Show answer</summary>

**C.** Actions such as `count()`, `show()`, `collect()`, `display()` or a write trigger the plan to run.

</details>

**6. What does a Spark executor do?**

- A. Coordinates the entire application
- B. Runs tasks and can cache application data
- C. Manages the Databricks workspace

<details><summary>Show answer</summary>

**B.** The driver coordinates; executors do the distributed work.

</details>

**7. Why does a Bronze layer exist?**

- A. To make dashboards faster
- B. To keep raw data so downstream layers can be rebuilt
- C. To store only aggregated data

<details><summary>Show answer</summary>

**B.** Bronze preserves data as ingested. If cleaning rules change, rebuild Silver and Gold from Bronze.

</details>

**8. Your DataFrame has 3 partitions. How many machines process it?**

- A. Exactly 3
- B. Exactly 1
- C. It depends on available executors and scheduling

<details><summary>Show answer</summary>

**C.** Partitions are logical slices. Tasks run on whatever executor resources are available.

</details>

## Practice challenge

Using the six-row dataset from [Chapter 08](08-hands-on-guide.md#step-1-create-a-dataframe), write PySpark code to:

1. find the city with the highest total revenue, and
2. count orders per city.

Then run `explain()` on one of them and point out the **Exchange** (shuffle) step. Reference solutions are in [`exercises/solutions/`](../exercises/solutions/solutions.py).

---

**← Previous** [10 · Common Misconceptions](10-common-misconceptions.md) · [🏠 Home](../README.md) · **Next →** [12 · Learning Roadmap](12-learning-roadmap.md)
