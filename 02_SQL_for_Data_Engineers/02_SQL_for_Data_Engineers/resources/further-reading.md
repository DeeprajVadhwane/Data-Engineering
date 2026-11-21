# Further reading

Official documentation first. Topics link to the specific pages they use.

## SQLite (the engine used for the runnable examples)

- [SQL language reference](https://www.sqlite.org/lang.html)
- [SELECT](https://www.sqlite.org/lang_select.html) · [Expressions](https://www.sqlite.org/lang_expr.html) · [Core functions](https://www.sqlite.org/lang_corefunc.html) · [Date and time functions](https://www.sqlite.org/lang_datefunc.html)
- [Aggregate functions](https://www.sqlite.org/lang_aggfunc.html) · [Window functions](https://www.sqlite.org/windowfunctions.html)
- [WITH clause (CTEs)](https://www.sqlite.org/lang_with.html) · [UPSERT](https://www.sqlite.org/lang_upsert.html)
- [NULL handling](https://www.sqlite.org/nulls.html) · [Datatypes](https://www.sqlite.org/datatype3.html)
- [Query planner](https://www.sqlite.org/queryplanner.html) · [EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html) · [Optimizer overview](https://www.sqlite.org/optoverview.html)

## Spark SQL and Databricks

- [Spark SQL reference](https://spark.apache.org/docs/latest/sql-ref.html)
- [Null semantics](https://spark.apache.org/docs/latest/sql-ref-null-semantics.html) · [ANSI compliance](https://spark.apache.org/docs/latest/sql-ref-ansi-compliance.html)
- [Performance tuning](https://spark.apache.org/docs/latest/sql-performance-tuning.html) · [Join hints](https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-hints.html)
- [Databricks SQL language reference](https://docs.databricks.com/aws/en/sql/language-manual/)
- [Delta Lake documentation](https://docs.delta.io/latest/index.html)

## PostgreSQL (the reference dialect many teams use)

- [Documentation](https://www.postgresql.org/docs/current/) · [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html) · [MERGE](https://www.postgresql.org/docs/current/sql-merge.html)

## Books and articles

- Ralph Kimball and Margy Ross, *The Data Warehouse Toolkit* (dimensional modelling, SCD types)
- Markus Winand, *SQL Performance Explained*, and the free site [Use The Index, Luke](https://use-the-index-luke.com/)
- Joe Reis and Matt Housley, *Fundamentals of Data Engineering*
- [Kimball Group: dimensional modelling techniques](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/)

## Practice

- Rewrite each Topic 10 exercise in Spark SQL on a Databricks workspace
- Port the Topic 08 pipeline to PostgreSQL using `MERGE`
