"""A complete mini ETL pipeline using only the Python standard library.

Extract  : read raw CSV text (with typical real-world problems)
Transform: remove duplicates, drop invalid rows, standardise values, add a column
Load     : write into a SQLite table (our stand-in for a warehouse)

It is idempotent: running it twice gives the same result, with no duplicates.

Run:  python 05_simple_etl_pipeline.py
"""
import csv
import io
import sqlite3

RAW = """order_id,customer,region,quantity,unit_price
1001,Asha,south,2,50.0
1002,Ravi,NORTH,1,120.0
1002,Ravi,NORTH,1,120.0
1003,Meera, East ,-3,40.0
1004,Kiran,,4,25.0
1005,Diya,south,5,10.0
"""


def extract(text):
    return list(csv.DictReader(io.StringIO(text)))


def transform(rows):
    seen, clean, rejected = set(), [], []
    for r in rows:
        if r["order_id"] in seen:                      # 1. remove duplicates
            rejected.append((r["order_id"], "duplicate")); continue
        seen.add(r["order_id"])
        qty, price = int(r["quantity"]), float(r["unit_price"])
        if qty <= 0:                                   # 2. drop invalid rows
            rejected.append((r["order_id"], "invalid quantity")); continue
        clean.append({
            "order_id": int(r["order_id"]),
            "customer": r["customer"].strip(),
            "region": (r["region"].strip().upper() or "UNKNOWN"),   # 3. standardise
            "amount": round(qty * price, 2),                        # 4. derive a column
        })
    return clean, rejected


def load(rows, db):
    db.execute("""CREATE TABLE IF NOT EXISTS orders
                  (order_id INTEGER PRIMARY KEY, customer TEXT, region TEXT, amount REAL)""")
    db.executemany("INSERT OR REPLACE INTO orders VALUES (:order_id, :customer, :region, :amount)", rows)
    db.commit()


if __name__ == "__main__":
    raw = extract(RAW)
    clean, rejected = transform(raw)
    db = sqlite3.connect(":memory:")
    load(clean, db)
    load(clean, db)                                    # run twice on purpose: idempotent

    print(f"extracted {len(raw)} rows | loaded {len(clean)} | rejected {len(rejected)}: {rejected}")
    print("\nRevenue by region (the kind of question an analyst asks):")
    for region, total in db.execute("SELECT region, SUM(amount) FROM orders GROUP BY region ORDER BY region"):
        print(f"  {region:<8} {total:>8.2f}")
    print("\nRows in table after running the load twice:", db.execute("SELECT COUNT(*) FROM orders").fetchone()[0])
