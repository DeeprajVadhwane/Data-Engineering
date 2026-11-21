# Examples

Every example runs against the same deterministic **XYZ database**, built in memory by [`xyz_data.py`](xyz_data.py). The output shown in the topic documents was captured by running these files.

| File | Topic | What it shows |
|---|---|---|
| [`01_why_sql_still_matters.sql`](01_why_sql_still_matters.sql) | [01](../01-why-sql-still-matters.md) | The XYZ tables and a first revenue query |
| [`01_sql_vs_python_loop.py`](01_sql_vs_python_loop.py) | [01](../01-why-sql-still-matters.md) | The same question answered by a Python loop and by SQL |
| [`02_querying_fundamentals.sql`](02_querying_fundamentals.sql) | [02](../02-querying-fundamentals.md) | Filtering, `NULL`, `CASE`, dates |
| [`03_aggregation_and_grouping.sql`](03_aggregation_and_grouping.sql) | [03](../03-aggregation-and-grouping.md) | `GROUP BY`, `HAVING`, conditional aggregation |
| [`04_joins.sql`](04_joins.sql) | [04](../04-joins.md) | Join types, anti-joins, fan-out |
| [`05_subqueries_ctes_and_set_operations.sql`](05_subqueries_ctes_and_set_operations.sql) | [05](../05-subqueries-ctes-and-set-operations.md) | CTEs, recursive CTE, set operations |
| [`06_window_functions.sql`](06_window_functions.sql) | [06](../06-window-functions.md) | Ranking, `LAG`, running totals, frames |
| [`07_cleaning_and_validating_data.sql`](07_cleaning_and_validating_data.sql) | [07](../07-cleaning-and-validating-data.md) | Cleaning the raw feed, quality checks |
| [`08_modelling_and_loading_with_sql.sql`](08_modelling_and_loading_with_sql.sql) | [08](../08-modelling-and-loading-with-sql.md) | Star schema, SCD Type 2, upsert |
| [`08_incremental_elt_pipeline.py`](08_incremental_elt_pipeline.py) | [08](../08-modelling-and-loading-with-sql.md) | A rerunnable incremental pipeline with a quality gate |
| [`09_query_performance_and_execution.sql`](09_query_performance_and_execution.sql) | [09](../09-query-performance-and-execution.md) | `EXPLAIN QUERY PLAN`, indexes |
| [`09_index_demo.py`](09_index_demo.py) | [09](../09-query-performance-and-execution.md) | Timing a scan against an index on 400,000 rows |

Support files: [`run_sql.py`](run_sql.py) runs a `.sql` file and prints each result as a table, and [`xyz_data.py`](xyz_data.py) builds the data.

## Quick start

```bash
cd examples
python run_sql.py 02_querying_fundamentals.sql
python run_sql.py 07_cleaning_and_validating_data.sql --stage   # also loads the raw feed
python 08_incremental_elt_pipeline.py
```

Files from Topic 07 onwards use the raw feed table `raw_orders_stage`. Add `--stage` so the runner loads it.

## Notes

- The data uses a fixed generator, so you get the same rows and totals on every machine.
- Requires SQLite 3.25+ (window functions). `RIGHT` and `FULL JOIN` in Topic 04 need 3.39+.
- **Example 09** timings are machine dependent. The plans and the speed-up ratio are what matter.
- The `.sql` files run one topic's statements in order. Statements that change data, such as Topic 08's, build on each other, so run each file from the top.
