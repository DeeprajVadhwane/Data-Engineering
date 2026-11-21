# Glossary

Terms used in Module 02, in alphabetical order, with the topic where each is explained.

| Term | Meaning | Topic |
|---|---|---|
| **Adaptive Query Execution (AQE)** | Spark 3+ feature that re-optimises a query at run time: coalesces small shuffle partitions, switches join strategy, splits skewed partitions | [09](../09-query-performance-and-execution.md) |
| **Aggregate function** | A function that reduces many rows to one value: `SUM`, `COUNT`, `AVG`, `MIN`, `MAX` | [03](../03-aggregation-and-grouping.md) |
| **Anti-join** | Rows in one table with no match in another, written with `LEFT JOIN ... IS NULL` or `NOT EXISTS` | [04](../04-joins.md) |
| **Broadcast join** | A join in which the small table is copied to every executor so the large table is not shuffled | [09](../09-query-performance-and-execution.md) |
| **B-tree** | A sorted, balanced tree structure used by most indexes | [09](../09-query-performance-and-execution.md) |
| **CTE (common table expression)** | A named query step introduced with `WITH`, readable by the query that follows | [05](../05-subqueries-ctes-and-set-operations.md) |
| **Covering index** | An index that contains every column a query needs, so the table is not read | [09](../09-query-performance-and-execution.md) |
| **Declarative** | Stating the result you want and leaving the method to the engine | [01](../01-why-sql-still-matters.md) |
| **Dimension table** | A table of descriptive attributes (customer, product, date) used to filter and group facts | [08](../08-modelling-and-loading-with-sql.md) |
| **Fact table** | A table of measurable events at a declared grain | [08](../08-modelling-and-loading-with-sql.md) |
| **Fan-out** | Row multiplication caused by joining to a table with several matches per row, which inflates sums | [04](../04-joins.md) |
| **Frame** | The set of rows around the current row that a window function reads (`ROWS` or `RANGE`) | [06](../06-window-functions.md) |
| **Grain** | What one row of a table represents, such as one order line | [08](../08-modelling-and-loading-with-sql.md) |
| **Idempotent** | Giving the same result when run once or many times | [08](../08-modelling-and-loading-with-sql.md) |
| **Index** | A separate sorted structure that lets the engine seek rows instead of scanning | [09](../09-query-performance-and-execution.md) |
| **Logical order of execution** | The order in which a query's clauses are evaluated, which differs from the order they are written | [02](../02-querying-fundamentals.md) |
| **MERGE** | A statement that inserts, updates or deletes target rows from a source in one operation | [08](../08-modelling-and-loading-with-sql.md) |
| **Medallion architecture** | Bronze (raw), silver (cleaned) and gold (business-ready) table layers | [01](../01-why-sql-still-matters.md) |
| **NULL** | A marker for missing or unknown. Comparisons with it are neither true nor false | [02](../02-querying-fundamentals.md) |
| **Optimiser** | The engine component that chooses an execution plan from statistics and available indexes | [09](../09-query-performance-and-execution.md) |
| **Partition pruning** | Skipping data folders that cannot match a filter on the partition column | [09](../09-query-performance-and-execution.md) |
| **Predicate pushdown** | Applying a filter at the storage layer so unneeded data is never read | [09](../09-query-performance-and-execution.md) |
| **Query plan** | The steps the engine will take to run a query, shown by `EXPLAIN` | [09](../09-query-performance-and-execution.md) |
| **Reject pattern** | Routing invalid rows to a separate table with a reason instead of dropping them | [07](../07-cleaning-and-validating-data.md) |
| **SCD (slowly changing dimension)** | A policy for handling changes in dimension attributes. Type 1 overwrites, Type 2 keeps versions | [08](../08-modelling-and-loading-with-sql.md) |
| **Shuffle** | Redistributing rows across a cluster so rows with the same key meet | [09](../09-query-performance-and-execution.md) |
| **Skew** | Uneven key distribution that overloads one partition or task | [09](../09-query-performance-and-execution.md) |
| **Star schema** | A fact table joined to surrounding dimension tables | [08](../08-modelling-and-loading-with-sql.md) |
| **Surrogate key** | A generated, meaningless key for a dimension row, separate from the source key | [08](../08-modelling-and-loading-with-sql.md) |
| **Three-valued logic** | SQL's true, false and unknown, caused by `NULL` | [02](../02-querying-fundamentals.md) |
| **Upsert** | Insert a row if its key is new, otherwise update it | [08](../08-modelling-and-loading-with-sql.md) |
| **Watermark** | A stored high-water mark (such as the last `loaded_at`) used to read only new data | [08](../08-modelling-and-loading-with-sql.md) |
| **Window function** | A calculation across related rows that keeps every input row | [06](../06-window-functions.md) |
