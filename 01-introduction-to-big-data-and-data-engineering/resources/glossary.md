# Glossary

[Back to module home](../README.md)

## Big data foundations
| Term | Plain meaning |
|---|---|
| **Big data** | Data too large or fast for one computer to handle comfortably |
| **OLTP** | Many small transactions (orders, logins). What MySQL is built for |
| **OLAP** | Heavy analysis over lots of data. What analytics platforms are built for |
| **Scale up (vertical)** | Make one machine bigger |
| **Scale out (horizontal)** | Add more machines |
| **Cluster** | A group of machines working together as one |
| **Node** | One machine in a cluster |
| **Commodity hardware** | Ordinary, inexpensive servers |
| **Hadoop** | Open-source system for storing and processing big data on many machines |
| **HDFS** | Hadoop's distributed file system: splits files into blocks across machines |
| **MapReduce** | Hadoop's processing model: *map* on each machine, *reduce* to combine |
| **YARN** | Hadoop's resource manager that assigns work to machines |
| **Replication** | Keeping copies of data on several machines (Hadoop default: 3) |
| **Fault tolerance** | Continuing to work when a machine fails |
| **Spark** | Fast engine that processes big data in memory across many machines |
| **PySpark** | Spark used from Python |
| **DataFrame** | A table-like collection of data in Spark, split across the cluster |
| **Partition** | One chunk of a DataFrame |
| **Driver** | The Spark process that runs your code and plans the work |
| **Executor** | A Spark worker process that runs tasks |
| **Task** | Work on one partition |
| **Transformation** | A Spark step that builds a plan (`filter`, `select`, `groupBy`). Lazy |
| **Action** | A Spark step that runs the plan (`show`, `count`, `write`) |
| **Lazy evaluation** | Spark waits for an action before doing any work |
| **Shuffle** | Moving data between machines (caused by `groupBy`, `join`). Expensive |
| **Micro-batch** | Processing a stream as many tiny batches (how Spark streaming works) |

## Databricks platform
| Term | Plain meaning |
|---|---|
| **Databricks** | Managed, unified platform built around Spark and Delta Lake |
| **Workspace** | Your Databricks environment: notebooks, data, jobs, permissions |
| **Notebook** | A document of cells (Python, SQL, Markdown) you run one by one |
| **Control plane** | The part of Databricks run by Databricks: web app, scheduler, cluster manager |
| **Compute plane** | Where your code runs |
| **Compute** | The machines that run your code |
| **Serverless compute** | Compute that Databricks manages for you; starts in seconds |
| **Classic cluster** | Compute you configure yourself (size, runtime, libraries) |
| **Auto-termination** | A cluster setting that shuts it down when idle |
| **Photon** | Databricks' fast native query engine |
| **Data lake** | Cheap storage holding raw files of any type |
| **Data warehouse** | Reliable, fast, structured storage for analytics |
| **Lakehouse** | Lake storage + warehouse reliability on one platform |
| **Parquet** | A compressed, column-based file format |
| **Delta Lake** | Parquet files + a transaction log: ACID, time travel, MERGE |
| **ACID** | Transactions that are all-or-nothing and never leave half-written data |
| **Time travel** | Querying or restoring an older version of a Delta table |
| **Schema enforcement** | Rejecting data that doesn't match the table's structure |
| **MERGE** | Update matching rows and insert new ones in one operation (upsert) |
| **Unity Catalog** | Governance: access control, lineage, auditing, discovery |
| **Metastore** | The top-level container for Unity Catalog metadata (one per region) |
| **Catalog / Schema** | First and second level of the name `catalog.schema.table` |
| **Volume** | A governed folder for files in Unity Catalog |
| **Medallion architecture** | Bronze (raw) → Silver (clean) → Gold (business-ready) |
| **Job** | A scheduled run of one or more tasks (formerly "Workflow") |
| **Idempotent** | Safe to re-run: running twice gives the same result, with no duplicates |

## Data engineering
| Term | Plain meaning |
|---|---|
| **Data engineering** | Building and running the systems that move, store and prepare data |
| **Pipeline** | A series of automated steps that moves data from sources to consumers |
| **ETL** | Extract, Transform, Load: reshape data before loading it |
| **ELT** | Extract, Load, Transform: load raw data first, reshape inside the platform |
| **Batch processing** | Processing data in chunks on a schedule |
| **Stream processing** | Processing each event as it arrives |
| **Orchestration** | Scheduling and coordinating pipeline steps, with retries and dependencies |
| **Data quality** | How complete, unique, valid, consistent, timely and accurate data is |
| **Data lineage** | The record of where data came from and how it changed |
| **OLTP / OLAP** | Transaction processing vs analytical processing |
| **Sharding** | Splitting one dataset across several database servers |
| **Schema-on-write / read** | Apply structure before storing vs when reading |
| **Amdahl's law** | The speed-up from parallelism is limited by the sequential part of a job |
| **CAP theorem** | During a network partition, choose consistency or availability |
| **Data skew** | Uneven data across partitions that makes a few tasks very slow |
| **Lineage (Spark)** | The recorded chain of transformations used to recompute lost partitions |
| **DAG** | Directed acyclic graph: Spark's plan of steps |
| **Catalyst** | Spark SQL's query optimiser |
| **Py4J** | The bridge that lets Python control the JVM in PySpark |
