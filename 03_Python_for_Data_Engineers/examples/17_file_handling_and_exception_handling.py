# Module 03, 17 · File Handling and Exception Handling
# Every runnable example from the topic, in order.
# Run:  python 17_file_handling_and_exception_handling.py

import json
import tempfile
from pathlib import Path

workdir = Path(tempfile.mkdtemp())          # a temporary folder, so this runs anywhere
path = workdir / "orders.txt"

with open(path, "w", encoding="utf-8") as f:        # write: creates or erases the file
    f.write("1001,West,1200.0\n")
    f.write("1002,East,800.0\n")

with open(path, "a", encoding="utf-8") as f:        # append: adds to the end
    f.write("1003,North,500.0\n")

print(f.closed)       # True: 'with' closed it for us

with open(path, encoding="utf-8") as f:
    whole = f.read()                     # the entire file as one string
print(repr(whole))

with open(path, encoding="utf-8") as f:
    first = f.readline()                 # one line
    rest = f.readlines()                 # the remaining lines, as a list
print(repr(first), len(rest))

with open(path, encoding="utf-8") as f:
    for line in f:                       # best for large files: one line at a time, little memory
        order_id, region, amount = line.strip().split(",")
        print(order_id, region, float(amount))

rows = ["1004,South,250.0", "1005,West,980.5"]

with open(path, "a", encoding="utf-8") as f:
    f.writelines(line + "\n" for line in rows)

with open(path, encoding="utf-8") as f:
    print(sum(1 for _ in f), "lines")

base = Path("data") / "raw" / "orders_2025-12-01.csv"      # the / operator joins path parts

print(base.name)              # file name
print(base.stem)              # name without extension
print(base.suffix)            # extension
print(base.parent)            # folder
print(base.with_suffix(".parquet"))

print(path.exists(), path.is_file(), path.stat().st_size > 0)
print([p.name for p in workdir.glob("*.txt")])             # find files by pattern

import csv

csv_path = workdir / "partner_orders.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as f:       # newline="" is required with csv
    writer = csv.writer(f)
    writer.writerow(["order_id", "region", "amount", "note"])
    writer.writerow([1001, "West", 1200.0, "gift, wrapped"])        # the comma inside is handled
    writer.writerow([1002, "East", 800.0, 'said "urgent"'])

print(csv_path.read_text(encoding="utf-8"))

with open(csv_path, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row["order_id"], row["region"], float(row["amount"]), "|", row["note"])

orders = [
    {"order_id": 1001, "region": "West", "amount": 1200.0, "items": ["Shoes", "Socks"], "coupon": None},
    {"order_id": 1002, "region": "East", "amount": 800.0, "items": ["Backpack"], "coupon": "FIRST10"},
]

json_path = workdir / "orders.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(orders, f, indent=2)                      # object to file

with open(json_path, encoding="utf-8") as f:
    loaded = json.load(f)                               # file to object

print(loaded == orders)
print(json.dumps(orders[1]))                            # object to string
print(json.loads('{"order_id": 7, "paid": true, "coupon": null}'))   # string to object

try:
    amount = float("abc")
except ValueError as err:
    print("Caught:", err)
print("The program carries on")

def load_amount(text):
    try:
        amount = float(text)
    except ValueError:
        print(f"  {text!r}: not a number")
        return None
    else:
        print(f"  {text!r}: parsed")             # only when no exception happened
        return amount
    finally:
        print("  (done with this value)")        # always runs


for value in ["1200.50", "abc"]:
    print(load_amount(value))

def read_first_line(file_path):
    try:
        with open(file_path, encoding="utf-8") as f:
            return f.readline().strip()
    except FileNotFoundError:
        return "file not found"
    except PermissionError:
        return "no permission"
    except (UnicodeDecodeError, OSError) as err:         # a tuple handles several types the same way
        return f"cannot read: {type(err).__name__}"


print(read_first_line(workdir / "orders.txt"))
print(read_first_line(workdir / "missing.txt"))

def check_order(order):
    if order["amount"] < 0:
        raise ValueError(f"order {order['order_id']}: negative amount {order['amount']}")
    return order


try:
    check_order({"order_id": 1005, "amount": -50.0})
except ValueError as err:
    print("Rejected:", err)

class DataQualityError(Exception):
    """Raised when a file has too many bad rows to trust."""


def gate(rejected, total, limit=0.5):
    ratio = rejected / total
    if ratio > limit:
        raise DataQualityError(f"{ratio:.0%} of rows rejected, limit is {limit:.0%}")


try:
    gate(rejected=4, total=5)
except DataQualityError as err:
    print("Stopping the run:", err)

def parse_amount(text):
    try:
        return float(text)
    except ValueError as err:
        raise DataQualityError(f"bad amount {text!r}") from err


try:
    parse_amount("12,5")
except DataQualityError as err:
    print(err, "| caused by:", repr(err.__cause__))

import time

calls = {"count": 0}


def flaky_read():
    calls["count"] += 1
    if calls["count"] < 3:
        raise ConnectionError("share temporarily unavailable")
    return "file contents"


def retry(func, attempts=4, delay=0.01):
    for attempt in range(1, attempts + 1):
        try:
            return func()
        except (ConnectionError, TimeoutError) as err:       # transient errors only
            print(f"attempt {attempt} failed: {err}")
            if attempt == attempts:
                raise                                         # out of attempts: let the caller know
            time.sleep(delay * 2 ** (attempt - 1))            # exponential backoff: 0.01, 0.02, 0.04 ...


print(retry(flaky_read))

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(levelname)-7s %(name)s: %(message)s")
log = logging.getLogger("orders")

log.debug("not shown: below the INFO level")
log.info("read %d rows", 6)
log.warning("%d rows rejected", 3)

try:
    float("abc")
except ValueError:
    log.exception("conversion failed")       # logs at ERROR level and includes the traceback

import shutil

shutil.rmtree(workdir)
print(workdir.exists())
