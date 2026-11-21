"""Run a .sql file against the XYZ sample database and print every result.

Usage:   python run_sql.py 03_aggregation.sql
         python run_sql.py 03_aggregation.sql --stage     (also load raw_orders_stage)

Each statement runs in order against a fresh in-memory copy of the database, so
a file always starts from the same state. Statements that return rows print a
table; statements that change data (INSERT, UPDATE, CREATE ...) run silently.
Needs Python 3.8+ and SQLite 3.25+ (window functions). Check yours with:
    python -c "import sqlite3; print(sqlite3.sqlite_version)"
"""
import sqlite3
import sys
from pathlib import Path

import xyz_data


def split_statements(text):
    """Split a script into complete statements, keeping any leading comments."""
    statements, buffer = [], ""
    for line in text.splitlines(keepends=True):
        buffer += line
        if sqlite3.complete_statement(buffer):
            statements.append(buffer.strip())
            buffer = ""
    leftover = "\n".join(l for l in buffer.splitlines() if l.strip() and not l.strip().startswith("--"))
    if leftover:
        statements.append(buffer.strip())
    return statements


def _cell(value):
    if value is None:
        return "NULL"
    if isinstance(value, float):
        s = f"{value:.15g}"
        return s + ".0" if s.lstrip("-").isdigit() else s
    return str(value)


def format_table(columns, rows):
    """Render rows like the sqlite3 shell's column mode: numbers right-aligned."""
    cells = [[_cell(v) for v in row] for row in rows]
    numeric = [all(isinstance(r[i], (int, float)) or r[i] is None for r in rows) and
               any(r[i] is not None for r in rows) for i in range(len(columns))]
    widths = [max([len(columns[i])] + [len(c[i]) for c in cells]) for i in range(len(columns))]

    def fmt(values, header=False):
        out = []
        for i, v in enumerate(values):
            out.append(v.rjust(widths[i]) if numeric[i] and not header else v.ljust(widths[i]))
        return "  ".join(out).rstrip()

    lines = [fmt(columns, header=True), "  ".join("-" * w for w in widths)]
    lines += [fmt(c) for c in cells]
    return "\n".join(lines)


def format_plan(rows):
    """Render EXPLAIN QUERY PLAN rows (id, parent, notused, detail) as a tree."""
    children = {}
    for rid, parent, _, detail in rows:
        children.setdefault(parent, []).append((rid, detail))
    lines = ["QUERY PLAN"]

    def walk(parent, prefix):
        kids = children.get(parent, [])
        for i, (rid, detail) in enumerate(kids):
            last = i == len(kids) - 1
            lines.append(f"{prefix}{'`--' if last else '|--'}{detail}")
            walk(rid, prefix + ("   " if last else "|  "))

    walk(0, "")
    return "\n".join(lines)


def execute(db, statement):
    """Run one statement. Returns the text to display, or None if it returns no rows."""
    cur = db.execute(statement)
    if cur.description is None:
        return None
    rows = cur.fetchall()
    head = statement.lstrip()
    while head.startswith("--"):
        head = head.split("\n", 1)[1].lstrip() if "\n" in head else ""
    if head.upper().startswith("EXPLAIN QUERY PLAN"):
        return format_plan(rows)
    return format_table([d[0] for d in cur.description], rows)


def fresh_database(stage=True):
    db = xyz_data.build()
    if stage:
        xyz_data.load_staging(db)
    return db


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    path = Path(argv[1])
    db = fresh_database(stage=True)
    for n, statement in enumerate(split_statements(path.read_text(encoding="utf8")), start=1):
        result = execute(db, statement)
        if result is not None:
            title = next((l for l in statement.splitlines() if l.strip()), "")
            print(f"[{n}] {title.strip()[:70]}")
            print(result)
            print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
