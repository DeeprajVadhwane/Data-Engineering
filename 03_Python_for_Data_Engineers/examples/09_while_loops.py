# Module 03, 09 · While Loops
# Every runnable example from the topic, in order.
# Run:  python 09_while_loops.py
# Note: the document ran input() with fixed answers; here you type them yourself.

count = 1

while count <= 5:
    print("Pass", count)
    count += 1

print("Loop finished, count is", count)

amounts = [1200, 800, 300, 500, 250]
budget = 2000
spent = 0
index = 0

while index < len(amounts) and spent + amounts[index] <= budget:
    spent += amounts[index]
    index += 1

print("Processed", index, "orders, total", spent)

files = ["a.csv", "b.csv", "corrupt.csv", "d.csv"]

index = 0
while index < len(files):
    name = files[index]
    if name.startswith("corrupt"):
        print("Found a corrupt file, stopping:", name)
        break
    print("Loaded", name)
    index += 1

amounts = [1200, -50, 800, 0, 300]

i = 0
total = 0
while i < len(amounts):
    value = amounts[i]
    i += 1                       # update first, so continue cannot cause an infinite loop
    if value <= 0:
        continue                 # skip invalid values
    total += value

print("Valid total:", total)

n = 0
while n < 3:
    if n == 1:
        pass                     # TODO: handle this case later
    n += 1
print("n =", n)

attempts = 0

while True:
    attempts += 1
    if attempts == 3:
        print("Succeeded on attempt", attempts)
        break

while True:
    text = input("Enter order amount: ")
    if not text.replace(".", "", 1).isdigit():
        print("Not a positive number, try again")
        continue
    amount = float(text)
    break

print("Accepted:", amount)

calls = {"count": 0}

def call_partner_api():
    """Simulated service: fails on the first two calls, then succeeds."""
    calls["count"] += 1
    return calls["count"] >= 3

max_attempts = 5
attempt = 1
success = False

while attempt <= max_attempts and not success:
    success = call_partner_api()
    if success:
        print(f"Attempt {attempt}: success")
    else:
        print(f"Attempt {attempt}: failed, retrying")
        attempt += 1

if not success:
    print("Giving up: alert the on-call engineer")

rows = 5
row = 1
while row <= rows:
    print("*" * row)
    row += 1

rows = 5
row = 1
while row <= rows:
    col = 1
    while col <= row:
        print("*", end=" ")
        col += 1
    print()                      # end the line
    row += 1

n = 5
while n >= 1:
    print(" ".join(str(k) for k in range(1, n + 1)))
    n -= 1

rows = 4
row = 1
while row <= rows:
    print(" " * (rows - row) + "*" * (2 * row - 1))
    row += 1

data = [("West", 1500), ("East", 1050), ("North", 500)]
largest = max(v for _, v in data)

i = 0
while i < len(data):
    region, value = data[i]
    bar = "#" * (value * 20 // largest)
    print(f"{region:<6} {bar:<20} {value}")
    i += 1
