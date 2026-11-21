"""The same question answered two ways: a Python loop and one SQL query.

Question: what is the revenue of completed orders in each region?

The loop tells the computer HOW to get the answer, step by step.
The SQL query tells the engine WHAT answer we want and lets it choose the steps.

Run:  python 01_sql_vs_python_loop.py
"""
from xyz_data import build

SQL = """
SELECT c.region,
       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
FROM orders AS o
JOIN customers AS c    ON c.customer_id = o.customer_id
JOIN order_items AS oi ON oi.order_id   = o.order_id
WHERE o.status = 'completed'
GROUP BY c.region
"""


def revenue_with_a_loop(db):
    region_of = dict(db.execute("SELECT customer_id, region FROM customers"))
    order_info = {oid: (cid, status)
                  for oid, cid, status in db.execute("SELECT order_id, customer_id, status FROM orders")}
    totals = {}
    for order_id, qty, price in db.execute("SELECT order_id, quantity, unit_price FROM order_items"):
        customer_id, status = order_info[order_id]
        if status != "completed":
            continue
        region = region_of[customer_id]
        totals[region] = totals.get(region, 0.0) + qty * price
    return {region: round(total, 2) for region, total in totals.items()}


def revenue_with_sql(db):
    return dict(db.execute(SQL))


if __name__ == "__main__":
    db = build()
    by_loop, by_sql = revenue_with_a_loop(db), revenue_with_sql(db)
    print(f"{'region':<8} {'python loop':>13} {'sql':>13}")
    for region in sorted(by_sql):
        print(f"{region:<8} {by_loop[region]:>13,.2f} {by_sql[region]:>13,.2f}")
    print("\nSame answer:", by_loop == by_sql)
