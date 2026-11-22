# Module 03, 11 · For-else, While-else and Comprehensions
# Every runnable example from the topic, in order.
# Run:  python 11_for_else_while_else_and_comprehensions.py

files = ["orders_1.csv", "orders_2.csv", "orders_3.csv"]

for name in files:
    if name.startswith("corrupt"):
        print("Found a corrupt file:", name)
        break
else:
    print("No corrupt files, batch is clean")

files = ["orders_1.csv", "corrupt_2.csv", "orders_3.csv"]

for name in files:
    if name.startswith("corrupt"):
        print("Found a corrupt file:", name)
        break
else:
    print("No corrupt files, batch is clean")

def is_prime(n):
    if n < 2:
        return False
    for divisor in range(2, int(n ** 0.5) + 1):
        if n % divisor == 0:
            return False          # a divisor was found
    else:
        return True               # no divisor found

print([n for n in range(2, 30) if is_prime(n)])

attempts = 0
max_attempts = 3
done = False

while attempts < max_attempts:
    attempts += 1
    print("Attempt", attempts)
    if attempts == 2:             # pretend the service answered
        done = True
        break
else:
    print("All attempts used, giving up")

print("done:", done)

amounts = [1200, -50, 800, 0, 300]

valid = []
for a in amounts:
    if a > 0:
        valid.append(a)

print(valid)

valid = [a for a in amounts if a > 0]
print(valid)

prices = [100, 250, 499, 999]

with_tax = [round(p * 1.18, 2) for p in prices]
labels = [f"INR {p}" for p in prices]

print(with_tax)
print(labels)

names = ["  meera iyer ", "RAHUL SHARMA", "", "anika gupta"]

clean = [n.strip().title() for n in names if n.strip()]
print(clean)

amounts = [1200, -50, 800, 0, 300]

flags = ["ok" if a > 0 else "invalid" for a in amounts]
print(flags)

regions = ["West", "East"]
quarters = ["Q3", "Q4"]

pairs = [(r, q) for r in regions for q in quarters]
print(pairs)

customers = [(1, "Meera Iyer"), (2, "Rahul Sharma"), (3, "Anika Gupta")]

by_id = {cid: name for cid, name in customers}
print(by_id)

revenue = {"West": 1500, "East": 1050, "North": 500, "South": 900}

large = {region: total for region, total in revenue.items() if total >= 900}
in_thousands = {region: total / 1000 for region, total in revenue.items()}

print(large)
print(in_thousands)

status_codes = {"completed": 1, "cancelled": 2, "pending": 3}
by_code = {code: status for status, code in status_codes.items()}
print(by_code)

words = ["load", "clean", "load", "publish", "clean", "load"]

counts = {w: words.count(w) for w in set(words)}
print(dict(sorted(counts.items())))

emails = ["a@xyz.com", "b@abc.org", "c@xyz.com", "d@abc.org"]

domains = {e.split("@")[1] for e in emails}
print(sorted(domains))

batches = [[1200, 800], [300], [500, 250, 100]]

all_amounts = [amount for batch in batches for amount in batch]
print(all_amounts)

orders = [
    {"region": "West",  "amount": 1200, "status": "completed"},
    {"region": "East",  "amount": 800,  "status": "completed"},
    {"region": "West",  "amount": 300,  "status": "cancelled"},
    {"region": "North", "amount": 500,  "status": "completed"},
    {"region": "West",  "amount": 250,  "status": "completed"},
]

regions = {o["region"] for o in orders}
revenue = {
    r: sum(o["amount"] for o in orders if o["region"] == r and o["status"] == "completed")
    for r in regions
}

for region, total in sorted(revenue.items(), key=lambda kv: kv[1], reverse=True):
    print(region, total)

customers = {1: "Meera Iyer", 2: "Rahul Sharma", 3: "Anika Gupta"}
orders = [(1001, 1, 1200), (1002, 3, 800), (1003, 9, 300)]

joined = [(oid, customers[cid], amt) for oid, cid, amt in orders if cid in customers]
orphans = [oid for oid, cid, _ in orders if cid not in customers]

print(joined)
print("orders with unknown customer:", orphans)

quarters = ["Q3", "Q4"]
regions = ["West", "East"]

grid = [[f"{r}-{q}" for q in quarters] for r in regions]
for row in grid:
    print(row)
