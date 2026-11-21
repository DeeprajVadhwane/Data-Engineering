"""The XYZ Company sample database used by every example in Module 02.

XYZ is the online retailer from Module 01. This file builds a small online-retail
database in SQLite. The data is generated with a fixed formula (no random module),
so you get exactly the same rows, and exactly the same query results, on every
machine and every run.

Tables
    customers    60 customers across four regions
    products     16 products in four categories
    orders       one row per order (July to December 2025)
    order_items  one row per product line inside an order
    returns      one row per returned order line
and, loaded separately with load_staging(), a deliberately messy table:
    raw_orders_stage   a raw feed with the problems real feeds have

Run:  python xyz_data.py
"""
import sqlite3
from datetime import date, timedelta

SCHEMA = """
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    city        TEXT,                    -- NULL when unknown
    region      TEXT NOT NULL,
    segment     TEXT,                    -- NULL when not yet classified
    signup_date TEXT NOT NULL            -- ISO date: YYYY-MM-DD
);
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    category   TEXT NOT NULL,
    list_price REAL NOT NULL
);
CREATE TABLE orders (
    order_id     INTEGER PRIMARY KEY,
    customer_id  INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date   TEXT NOT NULL,          -- ISO date: YYYY-MM-DD
    status       TEXT NOT NULL,          -- completed, cancelled or pending
    channel      TEXT NOT NULL,          -- web, app or marketplace
    shipping_fee REAL NOT NULL           -- charged once per order
);
CREATE TABLE order_items (
    order_id   INTEGER NOT NULL REFERENCES orders(order_id),
    line_no    INTEGER NOT NULL,
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity   INTEGER NOT NULL,
    unit_price REAL NOT NULL,            -- price actually charged on that day
    PRIMARY KEY (order_id, line_no)
);
CREATE TABLE returns (
    return_id   INTEGER PRIMARY KEY,
    order_id    INTEGER NOT NULL,
    line_no     INTEGER NOT NULL,
    return_date TEXT NOT NULL,
    reason      TEXT NOT NULL,
    FOREIGN KEY (order_id, line_no) REFERENCES order_items(order_id, line_no)
);
"""

REGIONS = {
    "North": ["Delhi", "Chandigarh", "Jaipur"],
    "South": ["Bengaluru", "Chennai", "Hyderabad"],
    "East": ["Kolkata", "Bhubaneswar", "Patna"],
    "West": ["Mumbai", "Pune", "Ahmedabad"],
}
FIRST = ["Asha", "Ravi", "Meera", "Kiran", "Diya", "Imran", "Sneha", "Tarun", "Anika", "Rohan",
         "Priya", "Vikram", "Neha", "Arjun", "Isha", "Karan", "Pooja", "Aditya", "Riya", "Sameer",
         "Divya", "Nikhil", "Tanvi", "Harsh", "Kavya", "Manish", "Shreya", "Yash", "Lakshmi", "Dev"]
LAST = ["Rao", "Shah", "Iyer", "Das", "Nair", "Khan", "Patil", "Menon", "Gupta", "Reddy", "Bose", "Joshi"]

PRODUCTS = [
    (1, "Wireless Earbuds", "Electronics", 2499.0), (2, "Smart Watch", "Electronics", 5999.0),
    (3, "Power Bank", "Electronics", 1499.0), (4, "Bluetooth Speaker", "Electronics", 3299.0),
    (5, "Air Fryer", "Home", 4499.0), (6, "Cotton Bedsheet", "Home", 1299.0),
    (7, "Steel Water Bottle", "Home", 599.0), (8, "LED Desk Lamp", "Home", 899.0),
    (9, "Running Shoes", "Fashion", 3499.0), (10, "Denim Jacket", "Fashion", 2799.0),
    (11, "Cotton T-Shirt", "Fashion", 599.0), (12, "Backpack", "Fashion", 1899.0),
    (13, "Basmati Rice 5kg", "Grocery", 749.0), (14, "Green Tea Box", "Grocery", 349.0),
    (15, "Almonds 500g", "Grocery", 599.0), (16, "Olive Oil 1L", "Grocery", 899.0),
]
RETURN_REASONS = {
    "Fashion": ["wrong size", "not as described", "changed mind"],
    "other": ["damaged", "not as described", "changed mind"],
}
CHANNELS = ["web", "web", "app", "app", "app", "marketplace"]

START, END = date(2025, 7, 1), date(2025, 12, 31)


class LCG:
    """A tiny, fixed pseudo-random sequence so the dataset never changes."""

    def __init__(self, seed):
        self.state = seed

    def rand(self, n):
        self.state = (self.state * 1103515245 + 12345) % 2147483648
        return (self.state >> 8) % n

    def pick(self, seq):
        return seq[self.rand(len(seq))]


def _customers(rng):
    rows = []
    for i in range(1, 61):
        region = rng.pick(list(REGIONS))
        city = None if i % 15 == 0 else rng.pick(REGIONS[region])
        segment = None if i % 10 == 0 else rng.pick(["Retail", "Premium", "Business"])
        signup = date(2024, 1, 1) + timedelta(days=rng.rand(600))
        name = f"{FIRST[(i * 7) % 30]} {LAST[(i * 5) % 12]}"
        rows.append((i, name, city, region, segment, signup.isoformat()))
    return rows


def build(path=":memory:"):
    """Create the XYZ database and return an open sqlite3 connection."""
    db = sqlite3.connect(path)
    db.executescript(SCHEMA)
    rng = LCG(2025)

    customers = _customers(rng)
    db.executemany("INSERT INTO customers VALUES (?,?,?,?,?,?)", customers)
    db.executemany("INSERT INTO products VALUES (?,?,?,?)", PRODUCTS)
    category = {p[0]: p[2] for p in PRODUCTS}
    price = {p[0]: p[3] for p in PRODUCTS}

    # Customers whose id is a multiple of 9 never order, which gives us
    # "customers with no orders" to find later.
    eligible = [c for c in customers if c[0] % 9 != 0]

    order_id, return_id = 0, 0
    orders, items, returns = [], [], []
    d = START
    while d <= END:
        q4 = d >= date(2025, 10, 1)
        count = 3 + rng.rand(3) + (2 if d.month == 11 else 0)
        buyers = []
        for _ in range(count):
            pool = [c for c in eligible if c[5] <= d.isoformat()]
            buyers.append(rng.pick(pool))
        if q4:  # the West region ramps up in the last quarter
            west = [c for c in eligible if c[3] == "West" and c[5] <= d.isoformat()]
            for _ in range(1 + rng.rand(2)):
                buyers.append(rng.pick(west))

        for cust in buyers:
            order_id += 1
            if d >= date(2025, 12, 30):
                status = "pending"
            else:
                status = "cancelled" if rng.rand(100) < 5 else "completed"
            channel = rng.pick(CHANNELS)

            chosen = []
            for _ in range(1 + rng.rand(3)):
                p = 1 + rng.rand(16)
                if p not in chosen:
                    chosen.append(p)
            total = 0.0
            for line_no, p in enumerate(chosen, start=1):
                qty = 1 + rng.rand(3 if price[p] < 1500 else 2)
                unit = price[p]
                if category[p] == "Fashion" and d.month == 11:
                    unit = round(unit * 0.9, 2)  # November fashion sale
                total += qty * unit
                items.append((order_id, line_no, p, qty, unit))
                chance = 14 if category[p] == "Fashion" else 4
                if status == "completed" and rng.rand(100) < chance:
                    when = d + timedelta(days=3 + rng.rand(15))
                    reasons = RETURN_REASONS["Fashion" if category[p] == "Fashion" else "other"]
                    reason = rng.pick(reasons)
                    if when <= END:
                        return_id += 1
                        returns.append((return_id, order_id, line_no, when.isoformat(), reason))
            fee = 79.0 if total < 1000 else (49.0 if total < 3000 else 0.0)
            orders.append((order_id, cust[0], d.isoformat(), status, channel, fee))
        d += timedelta(days=1)

    db.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?)", orders)
    db.executemany("INSERT INTO order_items VALUES (?,?,?,?,?)", items)
    db.executemany("INSERT INTO returns VALUES (?,?,?,?,?)", returns)
    db.commit()
    return db


STAGING_DDL = """
CREATE TABLE raw_orders_stage (
    order_ref TEXT, customer TEXT, region TEXT, order_ts TEXT,
    amount TEXT, status TEXT, loaded_at TEXT
);
"""

# A raw feed as it really arrives: everything is text, and nothing is clean.
STAGING_ROWS = [
    ("A-1001", "Asha Rao",     "south", "2025-12-01 10:15:00", "1,299.50", "COMPLETE",  "2025-12-02 01:00:00"),
    ("A-1002", "  Ravi Shah",  "NORTH", "2025-12-01 11:40:00", "499.00",   "completed", "2025-12-02 01:00:00"),
    ("A-1002", "Ravi Shah",    "North", "2025-12-01 11:40:00", "549.00",   "Completed", "2025-12-03 01:00:00"),
    ("A-1003", "Meera Iyer",   " East ", "2025-12-02 09:05:00", "",         "completed", "2025-12-03 01:00:00"),
    ("A-1004", "Kiran Das",    "",      "02/12/2025",          "250.00",   "cancelled", "2025-12-03 01:00:00"),
    ("A-1005", "Diya Nair",    "west",  "2025-12-03 18:22:00", "2,150.75", "COMPLETE",  "2025-12-04 01:00:00"),
    ("A-1006", "Imran Khan",   "North", "2025-12-03 19:00:00", "-120.00",  "completed", "2025-12-04 01:00:00"),
    ("A-1007", "Sneha Patil",  "WEST",  "2025-12-04 08:30:00", "899.00",   "shipped",   "2025-12-05 01:00:00"),
    ("A-1005", "Diya Nair",    "west",  "2025-12-03 18:22:00", "2,150.75", "COMPLETE",  "2025-12-05 01:00:00"),
    ("A-1008", "Tarun Menon",  "South", "2025-12-05 12:00:00", "abc",      "completed", "2025-12-06 01:00:00"),
]


def load_staging(db):
    """Add the messy raw_orders_stage table used in topics 07 and 08."""
    db.executescript(STAGING_DDL)
    db.executemany("INSERT INTO raw_orders_stage VALUES (?,?,?,?,?,?,?)", STAGING_ROWS)
    db.commit()
    return db


if __name__ == "__main__":
    conn = load_staging(build())
    for table in ["customers", "products", "orders", "order_items", "returns", "raw_orders_stage"]:
        n = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table:<18} {n:>6} rows")
    lo, hi = conn.execute("SELECT MIN(order_date), MAX(order_date) FROM orders").fetchone()
    print(f"\norders span {lo} to {hi}")
