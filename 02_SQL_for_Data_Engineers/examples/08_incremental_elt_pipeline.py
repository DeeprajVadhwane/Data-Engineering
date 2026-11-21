"""A small incremental ELT pipeline written as SQL steps driven from Python.

The raw feed from Topic 07 arrives one day at a time. Each run:
    1. reads only rows newer than the stored watermark       (incremental)
    2. standardises, deduplicates and validates them          (Topic 07 rules)
    3. upserts clean rows and rejected rows by key            (idempotent)
    4. runs quality checks and rolls back if any fails        (a gate)
    5. advances the watermark                                 (only after success)
Everything for one run happens in a single transaction, so a failure leaves the
tables exactly as they were.

Run:  python 08_incremental_elt_pipeline.py
"""
import sqlite3
from collections import defaultdict

from run_sql import format_table
from xyz_data import STAGING_DDL, STAGING_ROWS

SCHEMA = STAGING_DDL + """
CREATE TABLE orders_clean (
    order_ref TEXT PRIMARY KEY, customer TEXT NOT NULL, region TEXT NOT NULL,
    order_date TEXT NOT NULL, status TEXT NOT NULL, amount REAL NOT NULL, loaded_at TEXT NOT NULL
);
CREATE TABLE orders_rejected (
    order_ref TEXT PRIMARY KEY, reject_reason TEXT NOT NULL, loaded_at TEXT NOT NULL
);
CREATE TABLE etl_watermark (pipeline TEXT PRIMARY KEY, last_loaded_at TEXT NOT NULL);
INSERT INTO etl_watermark VALUES ('orders', '');
CREATE TEMP TABLE batch (
    order_ref TEXT, customer TEXT, region TEXT, order_date TEXT, status TEXT,
    amount REAL, loaded_at TEXT, reject_reason TEXT
);
"""

# Step 1-2: new rows only, standardised, latest delivery per order, validated.
BATCH_SQL = """
INSERT INTO batch
WITH new_rows AS (
    SELECT * FROM raw_orders_stage WHERE loaded_at > :watermark
),
standardised AS (
    SELECT order_ref,
           TRIM(customer) AS customer,
           CASE WHEN TRIM(region) = '' THEN NULL
                ELSE UPPER(SUBSTR(TRIM(region), 1, 1)) || LOWER(SUBSTR(TRIM(region), 2)) END AS region,
           CASE WHEN order_ts GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]*' THEN date(order_ts)
                WHEN order_ts GLOB '[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]'
                     THEN SUBSTR(order_ts, 7, 4) || '-' || SUBSTR(order_ts, 4, 2) || '-' || SUBSTR(order_ts, 1, 2)
           END AS order_date,
           NULLIF(REPLACE(TRIM(amount), ',', ''), '') AS amount_text,
           CASE LOWER(TRIM(status)) WHEN 'complete' THEN 'completed' ELSE LOWER(TRIM(status)) END AS status,
           loaded_at
    FROM new_rows
),
latest AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY order_ref ORDER BY loaded_at DESC) AS rn
    FROM standardised
)
SELECT order_ref, customer, region, order_date, status,
       CASE WHEN amount_text NOT GLOB '*[^0-9.-]*' THEN CAST(amount_text AS REAL) END AS amount,
       loaded_at,
       CASE WHEN amount_text IS NULL            THEN 'amount missing'
            WHEN amount_text GLOB '*[^0-9.-]*'  THEN 'amount not a number'
            WHEN CAST(amount_text AS REAL) < 0  THEN 'amount negative'
            WHEN region IS NULL                 THEN 'region missing'
            WHEN order_date IS NULL             THEN 'order date unreadable'
       END AS reject_reason
FROM latest
WHERE rn = 1
"""

# Step 3: upsert by key. The WHERE stops an older delivery overwriting a newer one.
UPSERT_CLEAN = """
INSERT INTO orders_clean (order_ref, customer, region, order_date, status, amount, loaded_at)
SELECT order_ref, customer, region, order_date, status, amount, loaded_at
FROM batch
WHERE reject_reason IS NULL
ON CONFLICT (order_ref) DO UPDATE SET
    customer = excluded.customer, region = excluded.region, order_date = excluded.order_date,
    status = excluded.status, amount = excluded.amount, loaded_at = excluded.loaded_at
WHERE excluded.loaded_at > orders_clean.loaded_at
"""
UPSERT_REJECTED = """
INSERT INTO orders_rejected (order_ref, reject_reason, loaded_at)
SELECT order_ref, reject_reason, loaded_at
FROM batch
WHERE reject_reason IS NOT NULL
ON CONFLICT (order_ref) DO UPDATE SET
    reject_reason = excluded.reject_reason, loaded_at = excluded.loaded_at
WHERE excluded.loaded_at > orders_rejected.loaded_at
"""
# An order that was rejected earlier and now arrives corrected leaves the rejects table.
CLEAR_FIXED_REJECTS = "DELETE FROM orders_rejected WHERE order_ref IN (SELECT order_ref FROM orders_clean)"

# Step 4: every check returns the number of violations. Zero means pass.
CHECKS = {
    "region missing": "SELECT COUNT(*) FROM orders_clean WHERE TRIM(region) = ''",
    "amount not positive": "SELECT COUNT(*) FROM orders_clean WHERE amount <= 0",
    "status outside allowed set":
        "SELECT COUNT(*) FROM orders_clean WHERE status NOT IN ('completed', 'cancelled', 'shipped', 'pending')",
    "order in both clean and rejected":
        "SELECT COUNT(*) FROM orders_rejected WHERE order_ref IN (SELECT order_ref FROM orders_clean)",
    "orders lost (raw minus clean and rejected)":
        """SELECT (SELECT COUNT(DISTINCT order_ref) FROM raw_orders_stage WHERE loaded_at <= :high)
                  - (SELECT COUNT(*) FROM orders_clean) - (SELECT COUNT(*) FROM orders_rejected)""",
}


def run_pipeline(db):
    """One incremental run. Returns (rows_read, clean, rejected)."""
    with db:  # one transaction: commit on success, roll back on any exception
        watermark = db.execute("SELECT last_loaded_at FROM etl_watermark WHERE pipeline = 'orders'").fetchone()[0]
        read, high = db.execute("SELECT COUNT(*), MAX(loaded_at) FROM raw_orders_stage WHERE loaded_at > ?",
                                (watermark,)).fetchone()
        if read == 0:
            return 0, 0, 0
        db.execute("DELETE FROM batch")
        db.execute(BATCH_SQL, {"watermark": watermark})
        clean = db.execute("SELECT COUNT(*) FROM batch WHERE reject_reason IS NULL").fetchone()[0]
        rejected = db.execute("SELECT COUNT(*) FROM batch WHERE reject_reason IS NOT NULL").fetchone()[0]
        db.execute(UPSERT_CLEAN)
        db.execute(UPSERT_REJECTED)
        db.execute(CLEAR_FIXED_REJECTS)
        for name, sql in CHECKS.items():
            failed = db.execute(sql, {"high": high}).fetchone()[0] if ":high" in sql else db.execute(sql).fetchone()[0]
            if failed:
                raise RuntimeError(f"quality check failed: {name} ({failed} rows)")
        db.execute("UPDATE etl_watermark SET last_loaded_at = ? WHERE pipeline = 'orders'", (high,))
        return read, clean, rejected


def snapshot(db):
    return (db.execute("SELECT * FROM orders_clean ORDER BY order_ref").fetchall(),
            db.execute("SELECT * FROM orders_rejected ORDER BY order_ref").fetchall())


def totals(db):
    c = db.execute("SELECT COUNT(*) FROM orders_clean").fetchone()[0]
    r = db.execute("SELECT COUNT(*) FROM orders_rejected").fetchone()[0]
    return f"orders_clean={c}  orders_rejected={r}"


if __name__ == "__main__":
    db = sqlite3.connect(":memory:")
    db.executescript(SCHEMA)

    # The feed, split into the daily deliveries it arrived in. Day 6 adds a correction
    # for the order that was rejected for a missing amount, plus one brand-new order.
    deliveries = defaultdict(list)
    for row in STAGING_ROWS:
        deliveries[row[6][:10]].append(row)
    deliveries["2025-12-07"] = [
        ("A-1003", "Meera Iyer", " East ", "2025-12-02 09:05:00", "1,180.00", "completed", "2025-12-07 01:00:00"),
        ("A-1009", "Anika Gupta", "north", "2025-12-06 15:45:00", "640.00", "completed", "2025-12-07 01:00:00"),
    ]

    print("Daily runs")
    for n, day in enumerate(sorted(deliveries), start=1):
        db.executemany("INSERT INTO raw_orders_stage VALUES (?,?,?,?,?,?,?)", deliveries[day])
        db.commit()  # loading raw data is its own committed step, separate from the pipeline run
        read, clean, rejected = run_pipeline(db)
        print(f"  day {n} ({day}): read {read}, clean {clean}, rejected {rejected}  ->  {totals(db)}")

    before = snapshot(db)
    read, _, _ = run_pipeline(db)
    print(f"\nRun again with no new data: read {read} rows, tables unchanged: {snapshot(db) == before}")

    db.execute("UPDATE etl_watermark SET last_loaded_at = ''")  # force a full replay from the start
    db.commit()
    read, clean, rejected = run_pipeline(db)
    print(f"Replay everything from the start: read {read}, tables unchanged: {snapshot(db) == before}")

    print("\norders_clean")
    cols = ["order_ref", "customer", "region", "order_date", "status", "amount", "loaded_at"]
    print(format_table(cols, db.execute("SELECT * FROM orders_clean ORDER BY order_ref").fetchall()))
    print("\norders_rejected")
    print(format_table(["order_ref", "reject_reason", "loaded_at"],
                       db.execute("SELECT * FROM orders_rejected ORDER BY order_ref").fetchall()))

    # A failed check rolls everything back. Force one with an invalid status.
    db.execute("INSERT INTO raw_orders_stage VALUES "
               "('A-1010','Test User','South','2025-12-08 10:00:00','100.00','teleported','2025-12-08 01:00:00')")
    db.commit()
    state_before = snapshot(db)
    try:
        run_pipeline(db)
    except RuntimeError as err:
        print(f"\nGate: {err}")
        raw_rows = db.execute("SELECT COUNT(*) FROM raw_orders_stage").fetchone()[0]
        print("Rolled back, tables unchanged:", snapshot(db) == state_before)
        print(f"Raw feed still holds all {raw_rows} rows, and the watermark did not move, "
              "so the next run retries the batch.")
