# Module 03, 08 · Conditional Statements
# Every runnable example from the topic, in order.
# Run:  python 08_conditional_statements.py

amount = 6200

if amount > 5000:
    print("Flag for manual approval")

print("Record processed")

amount = 800

if amount > 5000:
    print("Flag for manual approval")

print("Record processed")

status = "cancelled"

if status == "completed":
    print("Include in revenue")
else:
    print("Exclude from revenue")

status = "pending"

if status == "completed":
    action = "load into revenue"
elif status == "cancelled":
    action = "load, exclude from revenue"
elif status == "pending":
    action = "hold until settled"
else:
    action = "reject: unknown status"

print(f"{status}: {action}")

amount = 6200
region = "West"

if amount > 0:
    if amount > 5000:
        if region == "West":
            print("Large West order: route to West approver")
        else:
            print("Large order: route to head office")
    else:
        print("Standard processing")
else:
    print("Reject: amount must be positive")

amount = 6200
region = "West"

if amount > 5000 and region == "West":
    print("Large West order: route to West approver")

record = {"order_id": 1004, "amount": -50, "region": "East"}

if record["amount"] <= 0:
    print("Reject: amount must be positive")
elif record["region"] == "":
    print("Send to review queue: region missing")
else:
    print("Process normally")

def order_tier(amount):
    if amount >= 10000:
        return "platinum"
    elif amount >= 5000:
        return "gold"
    elif amount >= 1000:
        return "silver"
    elif amount > 0:
        return "bronze"
    else:
        return "invalid"

for amount in [12000, 5000, 1200, 250, 0]:
    print(f"{amount:>6}  ->  {order_tier(amount)}")

def broken_tier(amount):
    if amount > 0:
        return "bronze"          # catches everything positive
    elif amount >= 1000:
        return "silver"          # never reached
    else:
        return "invalid"

print(broken_tier(12000))

for value in [0, 42, "", "West", [], [1], None]:
    if value:
        print(f"{value!r:<8} truthy")
    else:
        print(f"{value!r:<8} falsy")

region = ""
orders = []

if not region:
    print("Region is missing")
if not orders:
    print("No orders to process")

amount = 6200
label = "approval needed" if amount > 5000 else "auto"
print(label)

orders = [
    {"order_id": 1001, "amount": 1200.0,  "status": "completed", "region": "West"},
    {"order_id": 1002, "amount": -50.0,   "status": "completed", "region": "East"},
    {"order_id": 1003, "amount": 7400.0,  "status": "completed", "region": "North"},
    {"order_id": 1004, "amount": 300.0,   "status": "cancelled", "region": "South"},
    {"order_id": 1005, "amount": 900.0,   "status": "completed", "region": ""},
]

for o in orders:
    if o["amount"] is None or o["amount"] <= 0:
        route = "reject"
    elif not o["region"]:
        route = "review queue"
    elif o["status"] == "cancelled":
        route = "load, exclude from revenue"
    elif o["amount"] > 5000:
        route = "manual approval"
    else:
        route = "standard"
    print(f"{o['order_id']}  {route}")
