"""Time the same lookup with and without an index on a larger table.

Builds 400,000 deterministic order rows in memory, then for 200 customer lookups
compares a full scan with an indexed search. Timings depend on the machine, so
read the ratio, not the absolute numbers.

Run:  python 09_index_demo.py
"""
import sqlite3
import time

from xyz_data import LCG

ROWS = 400_000
LOOKUPS = 200


def build():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE big_orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, "
               "order_date TEXT, amount REAL)")
    rng = LCG(2025)
    rows = [(i, 1 + rng.rand(50_000), f"2025-{1 + rng.rand(12):02d}-{1 + rng.rand(28):02d}",
             100 + rng.rand(5000)) for i in range(1, ROWS + 1)]
    db.executemany("INSERT INTO big_orders VALUES (?,?,?,?)", rows)
    db.commit()
    return db


def timed_lookups(db):
    start = time.perf_counter()
    found = 0
    for customer_id in range(1, LOOKUPS + 1):
        found += len(db.execute("SELECT order_id, amount FROM big_orders WHERE customer_id = ?",
                                (customer_id,)).fetchall())
    return time.perf_counter() - start, found


def plan(db):
    return db.execute("EXPLAIN QUERY PLAN SELECT order_id, amount FROM big_orders WHERE customer_id = 1"
                      ).fetchone()[3]


if __name__ == "__main__":
    db = build()
    print(f"Table: {ROWS:,} rows, {LOOKUPS} lookups by customer_id\n")

    print("Without an index")
    print("  plan:", plan(db))
    scan_time, found = timed_lookups(db)
    print(f"  rows found: {found}")

    db.execute("CREATE INDEX idx_big_customer ON big_orders (customer_id)")
    print("\nWith an index on customer_id")
    print("  plan:", plan(db))
    index_time, found2 = timed_lookups(db)
    print(f"  rows found: {found2}")

    print(f"\nSame rows returned: {found == found2}")
    print(f"Indexed lookups were faster by a factor of {scan_time / index_time:,.0f} "
          f"(machine dependent; expect a large factor, not an exact number)")
