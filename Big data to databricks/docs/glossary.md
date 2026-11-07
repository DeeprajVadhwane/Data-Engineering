# Glossary

[🏠 Home](../README.md)

Plain-English definitions, alphabetical.

| Term | Meaning |
| --- | --- |
| **Action** | A Spark operation that triggers execution (`count`, `show`, `collect`, `write`, `display`) |
| **ACID** | Atomicity, Consistency, Isolation, Durability: guarantees for reliable transactions |
| **Block (HDFS)** | A fixed-size chunk of a file stored on a DataNode |
| **Bronze / Silver / Gold** | Medallion layers: raw → cleaned → business-ready |
| **Cluster** | A group of machines working together |
| **Cluster manager** | Allocates machines and resources to Spark applications |
| **DataFrame** | A distributed, table-like dataset with named columns |
| **DataNode** | HDFS machine that stores data blocks |
| **Delta Lake** | Storage layer adding ACID transactions, schema control and time travel to data lake files |
| **Distributed computing** | Splitting work across many machines |
| **Driver** | The Spark process that plans and coordinates an application |
| **Executor** | A process on a worker that runs tasks and can cache data |
| **HDFS** | Hadoop Distributed File System |
| **Horizontal scaling** | Adding more machines |
| **Lakehouse** | Data-lake flexibility combined with warehouse-style reliability and governance |
| **Lazy evaluation** | Spark records transformations and waits for an action before running |
| **MapReduce** | Hadoop's Map → Shuffle & Sort → Reduce processing model |
| **Medallion architecture** | Layered pipeline design (Bronze, Silver, Gold) |
| **NameNode** | HDFS master that holds metadata about files and blocks |
| **Node** | One machine in a cluster |
| **Parquet** | A columnar file format widely used for analytics |
| **Partition** | One slice of a dataset processed by one task |
| **PySpark** | The Python API for Apache Spark |
| **Replication** | Keeping multiple copies of each block for fault tolerance |
| **Shuffle** | Moving data between machines to regroup it (e.g. for `groupBy`, joins) |
| **SparkSession** | Entry point to Spark functionality (`spark`) |
| **Task** | A unit of work: one operation on one partition |
| **Transformation** | A lazy operation that defines a new DataFrame (`select`, `filter`, `groupBy`) |
| **Unity Catalog** | Databricks' central governance layer for data and AI assets |
| **Vertical scaling** | Making one machine more powerful |
| **Volume (Unity Catalog)** | Governed storage location for files such as CSVs |
| **Worker node** | A machine that provides resources for executors |

---

[🏠 Home](../README.md)
