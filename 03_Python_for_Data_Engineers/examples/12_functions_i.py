# Module 03, 12 · Functions-I
# Every runnable example from the topic, in order.
# Run:  python 12_functions_i.py

def greet():
    print("Hello from a function")

print("Before the call")
greet()
greet()

def add_tax(price, rate):
    """Return the price including tax."""
    return price * (1 + rate)

print(add_tax(100, 0.18))
print(add_tax(250, 0.05))

amount = add_tax(1000, 0.18)
print("Stored result:", amount)

def clean_id(raw):
    """Keep letters and digits, in upper case."""
    return "".join(ch for ch in raw if ch.isalnum()).upper()

def clean_batch(raw_ids):
    """Clean every ID in a list."""
    return [clean_id(r) for r in raw_ids]

print(clean_batch([" ab-1042 ", "cd 2210", "ef_3301"]))

def describe_order(order_id, region, amount):
    return f"Order {order_id} from {region}: {amount}"

print(describe_order(1001, "West", 1200))
print(describe_order("West", 1001, 1200))       # wrong order: Python cannot tell

print(describe_order(amount=1200, region="West", order_id=1001))

print(describe_order(1001, amount=1200, region="West"))

def add_tax(price, rate=0.18):
    return round(price * (1 + rate), 2)

print(add_tax(100))               # uses the default rate
print(add_tax(100, 0.05))         # overrides it
print(add_tax(100, rate=0.28))    # overrides it by name

def load_orders(path, delimiter=",", has_header=True, encoding="utf-8"):
    return f"read {path} sep={delimiter!r} header={has_header} enc={encoding}"

print(load_orders("orders.csv"))
print(load_orders("orders.tsv", delimiter="\t"))
print(load_orders("legacy.csv", encoding="latin-1", has_header=False))

def add_record(record, batch=[]):          # shared list!
    batch.append(record)
    return batch

print(add_record("a"))
print(add_record("b"))                     # surprise: "a" is still there

def add_record(record, batch=None):
    if batch is None:
        batch = []
    batch.append(record)
    return batch

print(add_record("a"))
print(add_record("b"))

def revenue_share(part, total):
    """Return `part` as a percentage of `total`, rounded to 1 decimal place.

    Returns 0.0 when `total` is zero, to avoid a division error.
    """
    if total == 0:
        return 0.0
    return round(part / total * 100, 1)

print(revenue_share(1500, 3050))
print(revenue_share(10, 0))
print(revenue_share.__doc__.splitlines()[0])

def validate_order(order, max_amount=100000):
    """Return a list of problems found in an order. An empty list means valid."""
    problems = []
    if order.get("amount") is None or order["amount"] <= 0:
        problems.append("amount must be positive")
    elif order["amount"] > max_amount:
        problems.append("amount above limit")
    if not order.get("region"):
        problems.append("region missing")
    return problems

orders = [
    {"order_id": 1001, "amount": 1200, "region": "West"},
    {"order_id": 1002, "amount": -50,  "region": "East"},
    {"order_id": 1003, "amount": 900,  "region": ""},
    {"order_id": 1004, "amount": 250000, "region": "North"},
]

for order in orders:
    issues = validate_order(order)
    print(order["order_id"], "OK" if not issues else issues)

print("with a higher limit:", validate_order(orders[3], max_amount=500000))
