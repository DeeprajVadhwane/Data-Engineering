# Module 03, 01 · Introduction to Python for Data Engineering
# Every runnable example from the topic, in order.
# Run:  python 01_introduction_to_python_for_data_engineering.py

orders = [
    {"order_id": 1001, "region": "West",  "amount": 1200.0},
    {"order_id": 1002, "region": "East",  "amount": 800.0},
    {"order_id": 1003, "region": "West",  "amount": 300.0},
    {"order_id": 1004, "region": "North", "amount": 500.0},
]

revenue = {}
for order in orders:
    region = order["region"]
    revenue[region] = revenue.get(region, 0) + order["amount"]

for region, total in sorted(revenue.items()):
    print(region, total)

print("Hello, XYZ Company")
print(2 + 3)

amount = 1200

if amount > 1000:
    print("Large order")        # inside the if block: indented
    print("Needs approval")     # same block
print("Done")                   # not indented: runs either way

# This whole line is a comment
price = 499        # a comment after code

"""
A triple-quoted string on its own is often used as a multi-line note.
"""
print(price)

a = 5; b = 7; print(a + b)        # semicolons allow several statements on one line (rarely used)

total = (1200 +
         800 +
         300)                      # brackets let a statement continue on the next line
print(total)

values = [42, 499.99, 3 + 2j, True, None, "West", [1, 2], (1, 2), {1, 2}, {"region": "West"}]

for value in values:
    print(f"{value!r:<20} {type(value).__name__}")

x = 10
print(x, type(x).__name__)

x = "ten"
print(x, type(x).__name__)

order = {
    "order_id": 1001,            # int
    "customer": "Meera Iyer",    # str
    "amount": 1200.50,           # float
    "is_paid": True,             # bool
    "coupon": None,              # None: no coupon used
    "items": ["Shoes", "Socks"], # list
}

for field, value in order.items():
    print(f"{field:<10} {type(value).__name__:<6} {value}")
