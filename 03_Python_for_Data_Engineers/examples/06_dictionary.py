# Module 03, 06 · Dictionary
# Every runnable example from the topic, in order.
# Run:  python 06_dictionary.py

order = {"order_id": 1001, "customer": "Meera Iyer", "region": "West", "amount": 1200.0}
print(order)
print(len(order), type(order).__name__)

empty = {}
print(empty)

print(dict(region="West", amount=1200.0))                       # keyword arguments (keys must be valid names)
print(dict([("West", 1), ("East", 2)]))                          # from a list of key-value pairs
print(dict(zip(["West", "East"], [1200.0, 800.0])))              # from two lists
print(dict.fromkeys(["completed", "pending"], 0))                # the same value for every key

order = {
    "order_id": 1001,
    "customer": {"name": "Meera Iyer", "city": "Pune"},
    "items": [
        {"product": "Running Shoes", "qty": 1, "price": 3200.0},
        {"product": "Cotton T-Shirt", "qty": 2, "price": 450.0},
    ],
}

print(order["customer"]["city"])
print(order["items"][1]["product"])

order = {"order_id": 1001, "region": "West", "amount": 1200.0}

print(order["region"])

try:
    print(order["coupon"])
except KeyError as error:
    print("KeyError:", error)

print(order.get("coupon"))
print(order.get("coupon", "none"))
print(order.get("region", "unknown"))
print("coupon" in order, "region" in order)       # `in` tests the KEYS

order["coupon"] = "FEST10"        # new key: added
order["amount"] = 1250.0          # existing key: replaced
print(order)

order.update({"status": "completed", "amount": 1300.0})     # several at once
print(order)

removed = order.pop("coupon")             # remove a key and return its value
print(removed)

print(order.pop("coupon", "not there"))   # a default avoids a KeyError

del order["status"]                       # remove without returning
print(order)

groups = {}
groups.setdefault("West", []).append(1001)
groups.setdefault("West", []).append(1003)
groups.setdefault("East", []).append(1002)
print(groups)

revenue = {"West": 1500.0, "East": 1050.0, "North": 500.0}

print(revenue.keys())
print(revenue.values())
print(revenue.items())
print(list(revenue))                      # looping or listing a dictionary gives its keys

for region in revenue:                           # keys
    print(region)

print("--")
for region, total in revenue.items():            # key and value together (the most common form)
    print(f"{region:<6} {total:>8,.1f}")

print("--")
print(sum(revenue.values()), max(revenue.values()))
print(max(revenue, key=revenue.get))             # the key with the largest value

by_value = sorted(revenue.items(), key=lambda pair: pair[1], reverse=True)
print(by_value)

print(dict(by_value))                      # back to a dictionary, in the new order

defaults = {"retries": 3, "timeout": 30, "format": "csv"}
overrides = {"timeout": 60}

merged = defaults | overrides              # Python 3.9+: the right side wins
print(merged)

print({**defaults, **overrides})           # the same, for older versions

statuses = ["completed", "completed", "pending", "cancelled", "completed", "pending"]

counts = {}
for status in statuses:
    counts[status] = counts.get(status, 0) + 1

print(counts)

from collections import Counter

print(Counter(statuses))
print(Counter(statuses).most_common(1))

status_labels = {"C": "completed", "P": "pending", "X": "cancelled"}

for code in ["C", "X", "Z"]:
    print(code, "->", status_labels.get(code, "UNKNOWN CODE"))

orders = [
    {"order_id": 1001, "region": "West",  "amount": 1200.0},
    {"order_id": 1002, "region": "East",  "amount": 800.0},
    {"order_id": 1003, "region": "West",  "amount": 300.0},
    {"order_id": 1004, "region": "North", "amount": 500.0},
]

revenue = {}
for order in orders:
    revenue[order["region"]] = revenue.get(order["region"], 0) + order["amount"]
print(revenue)

import json

order = {"order_id": 1001, "region": "West", "amount": 1200.0, "coupon": None, "paid": True}
text = json.dumps(order)
print(text)
print(json.loads(text) == order)

text = "West"
print(id(text) == id(text + "!"))         # a new string every time

name = text
text += " region"                         # builds a new string and re-binds the name
print(name, "|", text)                    # `name` still refers to the old string

amounts = [1, 2]
before = id(amounts)
amounts.append(3)                         # modifies the same list
print(before == id(amounts), amounts)

config = {"retries": 3, "timeout": 30}
backup = config                           # another name, not a copy

config["retries"] = 10
print(backup)                             # also changed
print(backup is config)

config = {"retries": 3, "timeout": 30}
backup = config.copy()

config["retries"] = 10
print(config)
print(backup)                             # unaffected

job = {"name": "load_orders", "tags": ["daily", "critical"]}
shallow = job.copy()

job["tags"].append("finance")
print(job["tags"])
print(shallow["tags"])                    # changed too: the inner list is shared
print(job["tags"] is shallow["tags"])

import copy

job = {"name": "load_orders", "tags": ["daily", "critical"]}
deep = copy.deepcopy(job)

job["tags"].append("finance")
print(job["tags"])
print(deep["tags"])                       # independent
