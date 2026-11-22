"""A small, robust file pipeline: read a partner CSV, validate, write clean JSON and a rejects CSV.

Shows, in one script, everything from Topic 17:
    * files opened with `with`, csv, json and pathlib
    * a custom exception, and try / except / else / finally
    * a retry for a transient failure (and no retry for a permanent one)
    * logging instead of print
    * rejecting bad rows with a reason, never dropping them silently

Run:  python 17_robust_file_pipeline.py
"""
import csv
import json
import logging
import sys
import tempfile
from pathlib import Path

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(levelname)-7s %(message)s")
log = logging.getLogger("pipeline")

RAW_ROWS = [
    ["order_id", "region", "amount", "status"],
    ["1001", "west", "1200.00", "completed"],
    ["1002", "East", "800.00", "completed"],
    ["1003", "", "450.00", "completed"],          # region missing
    ["1004", "North", "abc", "pending"],          # amount not a number
    ["1005", "South", "-50.00", "completed"],     # negative amount
    ["1006", "North", "500.00", "cancelled"],
]


class DataQualityError(Exception):
    """Raised when too many rows fail validation to trust the file."""


_CALLS = {"count": 0}     # counts calls, to simulate a failure that clears up by itself


def read_csv(path, flaky_attempts=0):
    """Read a CSV. `flaky_attempts` simulates a transient failure (a busy network share)."""
    _CALLS["count"] += 1
    if _CALLS["count"] <= flaky_attempts:
        raise ConnectionError("share temporarily unavailable")
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def with_retry(func, attempts=3, transient=(ConnectionError, TimeoutError), **kwargs):
    """Retry transient errors only. A missing file will not fix itself, so it is raised at once."""
    for attempt in range(1, attempts + 1):
        try:
            return func(**kwargs)
        except transient as err:
            log.warning("attempt %d of %d failed: %s", attempt, attempts, err)
            if attempt == attempts:
                raise
    return None


def validate(row):
    """Return (clean_row, None) or (None, reason)."""
    region = row["region"].strip().title()
    if not region:
        return None, "region missing"
    try:
        amount = float(row["amount"])
    except ValueError:
        return None, "amount not a number"
    if amount < 0:
        return None, "amount negative"
    return {"order_id": int(row["order_id"]), "region": region, "amount": amount,
            "status": row["status"]}, None


def run(workdir, max_reject_ratio=0.5):
    source = Path(workdir) / "partner_orders.csv"
    clean_path = Path(workdir) / "orders_clean.json"
    reject_path = Path(workdir) / "orders_rejected.csv"

    with open(source, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(RAW_ROWS)

    log.info("reading %s", source.name)
    rows = with_retry(read_csv, path=source, flaky_attempts=2)
    log.info("read %d rows", len(rows))

    clean, rejected = [], []
    for row in rows:
        good, reason = validate(row)
        if good:
            clean.append(good)
        else:
            rejected.append({**row, "reject_reason": reason})

    ratio = len(rejected) / len(rows)
    if ratio > max_reject_ratio:
        raise DataQualityError(f"{ratio:.0%} of rows rejected, limit is {max_reject_ratio:.0%}")

    with open(clean_path, "w", encoding="utf-8") as f:
        json.dump(clean, f, indent=2)
    with open(reject_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["order_id", "region", "amount", "status", "reject_reason"])
        writer.writeheader()
        writer.writerows(rejected)

    log.info("wrote %d clean rows to %s and %d rejected rows to %s",
             len(clean), clean_path.name, len(rejected), reject_path.name)
    return clean_path, reject_path


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as workdir:
        print("Run 1: normal run, with a transient failure on the way")
        clean_path, reject_path = run(workdir)
        print("\norders_clean.json")
        print(clean_path.read_text(encoding="utf-8"))
        print("orders_rejected.csv")
        print(reject_path.read_text(encoding="utf-8").replace("\r\n", "\n").rstrip())

        print("\nRun 2: a permanent failure (file missing) is not retried")
        try:
            with_retry(read_csv, path=Path(workdir) / "does_not_exist.csv")
        except FileNotFoundError as err:
            log.error("giving up, file not found: %s", Path(err.filename).name)

        print("\nRun 3: a file that is mostly bad is refused, not loaded")
        try:
            run(workdir, max_reject_ratio=0.2)
        except DataQualityError as err:
            log.error("quality gate failed: %s", err)
        finally:
            print("cleanup done")
