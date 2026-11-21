# 10 · Module Review and Interview Preparation

> **Module 02 · Topic 10 of 10** &nbsp;|&nbsp; Reading time: ~45 min &nbsp;|&nbsp; Level: Review

[Module home](README.md) &nbsp;·&nbsp; [← Previous: Query Performance and Execution](09-query-performance-and-execution.md)

## What you will do

- Review the whole module on one page
- Keep a **cheat sheet** of the patterns you will use every week
- Practise **rapid-fire** and **scenario** interview questions
- Work through **exercises** on the XYZ database
- Check yourself against a **self-assessment list**

---

## 1. The module on one page

Asha began with a business question: *which regions grew fastest last quarter, and which products are returned most often?* She finished with a rerunnable pipeline that answers it every day. This is the route she took.

| Topic | The problem it solved | The key idea |
|---|---|---|
| [01 Why SQL still matters](01-why-sql-still-matters.md) | A Python loop answered the question slowly and differently each time | SQL is **declarative**: you state the result, the engine plans the work |
| [02 Querying fundamentals](02-querying-fundamentals.md) | Wrong filters and surprising `NULL` results | The **logical order** of execution, and **three-valued logic** |
| [03 Aggregation and grouping](03-aggregation-and-grouping.md) | Totals that did not add up | `GROUP BY`, `HAVING`, conditional aggregation, and the average-of-averages trap |
| [04 Joins](04-joins.md) | Revenue doubled after a join | Join types, **fan-out**, and `ON` versus `WHERE` in a `LEFT JOIN` |
| [05 Subqueries, CTEs and set operations](05-subqueries-ctes-and-set-operations.md) | A 60-line query nobody could read | Name each step with a **CTE**. Beware `NOT IN` with `NULL` |
| [06 Window functions](06-window-functions.md) | Top product per region, and growth versus last month | Calculate across related rows **without collapsing them** |
| [07 Cleaning and validating data](07-cleaning-and-validating-data.md) | A messy feed with duplicates and bad values | Standardise, dedupe, **reject with reasons**, and test with SQL checks |
| [08 Modelling and loading with SQL](08-modelling-and-loading-with-sql.md) | History rewritten, and double-counted reloads | **Star schema**, **SCD Type 2**, **idempotent** incremental loads |
| [09 Query performance and execution](09-query-performance-and-execution.md) | Slow lookups and stuck Spark tasks | Read the plan. Indexes, pruning, **shuffle**, broadcast and skew |

The answer to the business question, from Topic 08: **West grew 225.0% from Q3 to Q4**, while North and South grew about 8% and East fell 2.3%. Fashion products, such as Running Shoes (17.1%) and Cotton T-Shirt (17.0%), have the highest return rates.

---

## 2. Cheat sheet

### Logical order of a query

```text
FROM / JOIN  ->  WHERE  ->  GROUP BY  ->  HAVING  ->  window functions  ->  SELECT  ->  DISTINCT  ->  ORDER BY  ->  LIMIT
```

You cannot use a `SELECT` alias in `WHERE`. You cannot filter on a window function in `WHERE`: compute it in a CTE, then filter.

### Patterns

| Task | Pattern |
|---|---|
| Revenue by group | `SELECT g, SUM(x) FROM t GROUP BY g` |
| Filter on an aggregate | `HAVING SUM(x) > 100` |
| Conditional totals | `SUM(CASE WHEN status = 'completed' THEN amount END)` or `SUM(amount) FILTER (WHERE ...)` |
| Rows with no match | `LEFT JOIN ... WHERE right.key IS NULL`, or `NOT EXISTS (...)` |
| Keep unmatched rows when filtering the right table | Put the filter in `ON`, not `WHERE` |
| Top N per group | `ROW_NUMBER() OVER (PARTITION BY g ORDER BY x DESC)` in a CTE, then `WHERE rn <= N` |
| Latest row per key | `ROW_NUMBER() OVER (PARTITION BY k ORDER BY updated_at DESC) = 1` |
| Change vs previous period | `x - LAG(x) OVER (ORDER BY period)` |
| Running total | `SUM(x) OVER (ORDER BY d ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)` |
| Share of total | `x * 1.0 / SUM(x) OVER ()` |
| Remove duplicates | `ROW_NUMBER()` over the business key, keep `rn = 1` |
| Safe default for NULL | `COALESCE(x, 0)` |
| Avoid divide by zero | `x * 1.0 / NULLIF(y, 0)` |
| Idempotent load (SQLite, PostgreSQL) | `INSERT ... ON CONFLICT (key) DO UPDATE SET ...` |
| Idempotent load (Delta, PostgreSQL 15+) | `MERGE INTO t USING s ON ... WHEN MATCHED ... WHEN NOT MATCHED ...` |

### Traps

| Trap | Remember |
|---|---|
| `NULL = NULL` is not true | Use `IS NULL`, or `IS NOT` in SQLite for a NULL-safe comparison |
| `COUNT(*)` vs `COUNT(col)` vs `COUNT(DISTINCT col)` | Rows, non-NULL values, distinct non-NULL values |
| `NOT IN` with a `NULL` in the list | Returns nothing. Use `NOT EXISTS` |
| Join to a one-to-many table, then `SUM` | **Fan-out**. Aggregate before joining, or join at the right grain |
| `LEFT JOIN` + `WHERE` on the right table | Silently becomes an inner join |
| Average of averages | Weight by the underlying counts |
| `UNION` vs `UNION ALL` | `UNION` removes duplicates and costs a sort or hash |
| `LAST_VALUE` with the default frame | Stops at the current row. Set the frame explicitly |
| Function on a filter column | Defeats indexes and partition pruning |
| SQLite `CAST('abc' AS INTEGER)` | Returns 0 silently. Validate before casting |
| Plain `INSERT` in a retried job | Duplicates. Use an upsert or replace the partition |

### Dialects at a glance

| Feature | SQLite | PostgreSQL | Spark SQL / Databricks |
|---|---|---|---|
| Dates | ISO text, `date()`, `strftime()` | `DATE`, `TIMESTAMP`, `date_trunc` | `DATE`, `TIMESTAMP`, `date_format`, `date_trunc` |
| Type checking | Dynamic | Strict | Strict, with ANSI mode options |
| Window functions | 3.25+ | Yes | Yes |
| `QUALIFY` | No | No | Yes (Databricks) |
| Upsert | `ON CONFLICT` | `ON CONFLICT`, `MERGE` (15+) | `MERGE INTO` (Delta) |
| Plan | `EXPLAIN QUERY PLAN` | `EXPLAIN [ANALYZE]` | `EXPLAIN [FORMATTED]`, Spark UI |

---

## 3. Rapid-fire questions

Answer each in one or two sentences before opening the answer.

<details><summary><b>R1.</b> Declarative vs imperative?</summary>

Declarative code states the result wanted and leaves the method to the engine, which is SQL. Imperative code spells out the steps, as a Python loop does.
</details>

<details><summary><b>R2.</b> In what order does a query run logically?</summary>

`FROM`/`JOIN`, `WHERE`, `GROUP BY`, `HAVING`, window functions, `SELECT`, `DISTINCT`, `ORDER BY`, `LIMIT`.
</details>

<details><summary><b>R3.</b> <code>WHERE</code> vs <code>HAVING</code>?</summary>

`WHERE` filters rows before grouping. `HAVING` filters groups after aggregation.
</details>

<details><summary><b>R4.</b> What do <code>COUNT(*)</code> and <code>COUNT(col)</code> return?</summary>

All rows in the group, and the rows where `col` is not NULL.
</details>

<details><summary><b>R5.</b> What does <code>NULL = NULL</code> evaluate to?</summary>

Unknown (NULL), which a `WHERE` treats as false. Use `IS NULL`.
</details>

<details><summary><b>R6.</b> INNER vs LEFT JOIN?</summary>

Inner keeps only rows with matches on both sides. Left keeps every left row, with NULLs where the right side has no match.
</details>

<details><summary><b>R7.</b> How do you find customers who never ordered?</summary>

`LEFT JOIN` orders and keep rows where the order key is NULL, or use `NOT EXISTS`.
</details>

<details><summary><b>R8.</b> What is join fan-out?</summary>

A join to a table with several matches per row multiplies the rows, so sums over the other table's columns are inflated.
</details>

<details><summary><b>R9.</b> <code>UNION</code> vs <code>UNION ALL</code>?</summary>

`UNION` removes duplicate rows. `UNION ALL` keeps everything and is cheaper.
</details>

<details><summary><b>R10.</b> CTE vs subquery?</summary>

Both give the same result. A CTE names a step, so the query reads top to bottom and a step can be referenced more than once. Recursive CTEs can walk hierarchies or generate series.
</details>

<details><summary><b>R11.</b> <code>ROW_NUMBER</code> vs <code>RANK</code> vs <code>DENSE_RANK</code> on ties?</summary>

`ROW_NUMBER` gives unique numbers. `RANK` gives ties the same number and skips the next. `DENSE_RANK` gives ties the same number without gaps.
</details>

<details><summary><b>R12.</b> How is a window function different from <code>GROUP BY</code>?</summary>

It calculates across related rows but keeps every input row, so you can show a detail row next to its group total.
</details>

<details><summary><b>R13.</b> How do you deduplicate and keep the latest record?</summary>

`ROW_NUMBER() OVER (PARTITION BY business_key ORDER BY updated_at DESC)` in a CTE, then keep `rn = 1`.
</details>

<details><summary><b>R14.</b> What is a surrogate key?</summary>

A system-generated, meaningless key for a dimension row. It lets the dimension keep several versions of one entity.
</details>

<details><summary><b>R15.</b> SCD Type 1 vs Type 2?</summary>

Type 1 overwrites the value and loses history. Type 2 adds a new versioned row with validity dates and keeps it.
</details>

<details><summary><b>R16.</b> What makes a load idempotent?</summary>

Running it twice gives the same result as once. Use keyed upserts or replace a partition in a transaction.
</details>

<details><summary><b>R17.</b> What does a watermark do?</summary>

It records how far the last run processed, so the next run reads only newer rows.
</details>

<details><summary><b>R18.</b> Why can <code>WHERE YEAR(d) = 2025</code> be slow?</summary>

The function on the column prevents an index seek or partition pruning. Use a date range instead.
</details>

<details><summary><b>R19.</b> What is a shuffle?</summary>

Redistribution of rows across a cluster so rows with the same key meet, which costs network and disk.
</details>

<details><summary><b>R20.</b> How do you reduce data skew?</summary>

Isolate heavy keys (for example NULL), broadcast the smaller side, salt the key, or rely on Adaptive Query Execution.
</details>

---

## 4. Scenario questions

Each scenario is how interviewers test judgment. Think about your approach first, then compare.

<details><summary><b>S1.</b> A dashboard shows revenue 40% higher than finance's report. How do you investigate?</summary>

Reconcile at the lowest grain first. Compare row counts and totals between the source and the report table (Topic 07 and 08 checks). Look for **join fan-out**: a join to a one-to-many table before the `SUM` (Topic 04 saw 13,010.0 become 16,108.0 this way). Then check status filters (cancelled and pending orders included?), duplicate loads, and time zone or date-boundary differences. Fix at the cause, then add a reconciliation check so it cannot return silently.
</details>

<details><summary><b>S2.</b> The nightly job failed at 3 a.m., was rerun, and now yesterday's totals are doubled. What went wrong and what do you change?</summary>

The load was a plain append, so the retry inserted the same rows again. Make the write idempotent: a primary key with an upsert/`MERGE`, or delete and insert the day's partition in one transaction. Wrap the run in a transaction with a quality gate, as in the Topic 08 pipeline, so a failure leaves no partial data. Add a duplicate-key check and a row-count reconciliation.
</details>

<details><summary><b>S3.</b> A customer moved region. Last quarter's regional report changed overnight. How do you keep history stable?</summary>

The dimension was overwritten (Type 1). Use **SCD Type 2**: add a new customer version with validity dates, and load facts against the version valid on the order date. Topic 08 shows the effect: Q4 West differs by about 35,000 between "as was" and "as is". Decide with the business which view each report needs.
</details>

<details><summary><b>S4.</b> Support says a customer lookup takes 40 seconds. What do you do?</summary>

Get the exact query and run `EXPLAIN`. Expect a full scan. Check whether the filter column is indexed, and whether a function, cast or leading wildcard prevents its use. Add or fix the index (consider a composite or covering index for the exact query), refresh statistics, and measure before and after. Mention the write cost of the index.
</details>

<details><summary><b>S5.</b> A Spark job's stage has 199 tasks finished in two minutes, and one task has run for an hour. What is it and how do you fix it?</summary>

Skew: one key owns most of the rows in the shuffle. Confirm with a count per key. Typical culprits are NULL or default keys. Isolate or filter that key, broadcast the smaller side if possible, salt the key, and check that Adaptive Query Execution's skew handling is enabled.
</details>

<details><summary><b>S6.</b> The feed has duplicates, bad dates and negative amounts. How do you design the cleaning step?</summary>

Land the raw data untouched (bronze). In the silver step standardise text and types, parse dates explicitly, deduplicate with `ROW_NUMBER` on the business key and the latest load time, and **reject rows with a reason** instead of dropping them silently. Run SQL checks where zero rows means pass, reconcile raw against clean plus rejected, and keep the whole run idempotent and atomic.
</details>

<details><summary><b>S7.</b> Write a query for the top 3 products by revenue in each region.</summary>

Aggregate revenue by region and product, rank inside a CTE with `ROW_NUMBER()` or `RANK()` (choose based on how ties should behave) over `PARTITION BY region ORDER BY revenue DESC`, then filter `rank <= 3` in the outer query, since window functions cannot be filtered in `WHERE`. State the tie rule and the status filter you applied.
</details>

<details><summary><b>S8.</b> The same SQL returns different numbers in SQLite and in Databricks. What do you check?</summary>

Type behaviour (integer division, implicit casts, text-stored dates), `NULL` and collation handling in sorting and comparisons, date function differences, ANSI mode settings in Spark that turn silent casts into errors, and whether results depend on an unstated sort order. Compare row counts first, then totals, then individual keys.
</details>

---

## 5. Exercises

Run them on the XYZ database. Build it with `python run_sql.py` or load it from `xyz_data.py`. Answers are not given on purpose: write the query, then compare it against the matching example file.

| # | Exercise | Skills | Look at |
|---|---|---|---|
| 1 | List cancelled orders over 5,000 sorted by value, with the customer's name | Filters, sorting, joins | `02_querying_fundamentals.sql` |
| 2 | Revenue and order count per month, only for completed orders, and the share of the total each month holds | `GROUP BY`, window share | `03_aggregation_and_grouping.sql`, `06_window_functions.sql` |
| 3 | Customers who have **never** ordered, written two ways (`LEFT JOIN` and `NOT EXISTS`) | Anti-joins | `04_joins.sql` |
| 4 | Total shipping fees per region **without** fan-out | Grain, CTEs | `04_joins.sql`, `05_subqueries_ctes_and_set_operations.sql` |
| 5 | The best-selling product in every category | `ROW_NUMBER` | `06_window_functions.sql` |
| 6 | Each customer's first and most recent order date, and the days between | `FIRST_VALUE`, `LAG`, dates | `06_window_functions.sql` |
| 7 | Return rate by product, and products above the average rate | Ratios, subqueries | `05_subqueries_ctes_and_set_operations.sql` |
| 8 | Write five quality checks for `orders` (zero rows = pass) | Validation | `07_cleaning_and_validating_data.sql` |
| 9 | Move a second customer to a new region with SCD Type 2 and prove the totals still reconcile | Dimensions | Topic 08 |
| 10 | Rewrite a `strftime(...) = ...` filter as a range, and compare the plans | Indexes | Topic 09, `09_index_demo.py` |

Run the whole pipeline example any time to see the pieces together:

```bash
python 08_incremental_elt_pipeline.py
```

---

## 6. Self-assessment

You are ready for the next module when you can do each of these without notes.

- [ ] Explain why SQL is declarative, and what the optimiser does for you
- [ ] Write a query using `WHERE`, `GROUP BY`, `HAVING` and `ORDER BY` in the right order, and explain why
- [ ] Predict the result of a comparison, `COUNT` or `NOT IN` involving `NULL`
- [ ] Choose the correct join type, and spot and fix a fan-out
- [ ] Break a long query into CTEs
- [ ] Use `ROW_NUMBER`, `LAG` and a running total
- [ ] Clean a messy feed and reject bad rows with reasons
- [ ] Write a data quality check and a reconciliation
- [ ] Describe a star schema, its grain, and SCD Type 2
- [ ] Make a load idempotent
- [ ] Read a query plan and say whether it scans or seeks
- [ ] Explain shuffle, broadcast and skew

## 7. What comes next

Module 02 gave you the language of data work. The next steps build on it:

- **Python for Data Engineering:** the same pipeline steps, driven from code, with files, APIs and testing
- **Spark and the lakehouse:** the engines behind the Spark SQL notes in this module
- **Orchestration:** scheduling the pipeline from Topic 08 with retries and alerts

---

## Official documentation

- [SQLite documentation](https://www.sqlite.org/docs.html) · [SQL language reference](https://www.sqlite.org/lang.html)
- [Spark SQL reference](https://spark.apache.org/docs/latest/sql-ref.html)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [Databricks SQL language reference](https://docs.databricks.com/aws/en/sql/language-manual/)

---

| Previous | Contents | Next |
|:---|:---:|:---|
| [← Query Performance and Execution](09-query-performance-and-execution.md) | [Module home](README.md#topics-covered) | Module 03 (coming next) |
