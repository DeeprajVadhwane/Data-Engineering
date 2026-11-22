# Module 03, 04 · Lists and Intro to For Loops
# Every runnable example from the topic, in order.
# Run:  python 04_lists_and_intro_to_for_loops.py

amounts = [1200.0, 800.0, 300.0, 500.0, 250.0, 1800.0, 950.0]
regions = ["West", "East", "West", "North", "East", "West", "South"]
empty = []
mixed = [1001, "Meera Iyer", 1200.5, True, None]

print(amounts)
print(len(amounts), len(empty), len(mixed))
print(type(amounts).__name__)

print(list("West"))                 # from any iterable, such as text
print(list(range(5)))               # 0 to 4
print(list(range(1001, 1006)))      # start and stop (stop is not included)
print(list(range(0, 10, 3)))        # start, stop, step
print([0] * 4)                      # a list repeated
print([[1, 2], [3, 4]])             # a list of lists: a small table

amounts = [1200.0, 800.0, 300.0, 500.0, 250.0, 1800.0, 950.0]

print(amounts[0])        # first
print(amounts[2])
print(amounts[-1])       # last
print(amounts[-2])       # second from last

try:
    print(amounts[7])
except IndexError as error:
    print("IndexError:", error)

table = [[1001, "West"], [1002, "East"]]
print(table[1])
print(table[1][1])

amounts = [1200.0, 800.0, 300.0, 500.0, 250.0, 1800.0, 950.0]

print(amounts[1:4])      # indexes 1, 2, 3
print(amounts[:3])       # the first three
print(amounts[4:])       # from index 4 to the end
print(amounts[-3:])      # the last three
print(amounts[::2])      # every second item
print(amounts[1::2])     # every second item, starting at index 1
print(amounts[::-1])     # reversed
print(amounts[:])        # a full copy

print(amounts[5:100])
print(amounts[10:])

amounts = [1200.0, 800.0, 300.0, 500.0]

amounts[1] = 850.0                 # replace one item
print(amounts)

amounts[0:2] = [1300.0, 900.0, 100.0]     # replace a slice, and the size may change
print(amounts)

del amounts[-1]                    # delete by index
print(amounts)

orders = ["O-1", "O-2"]

orders.append("O-3")
print(orders)

orders.extend(["O-4", "O-5"])
print(orders)

orders.insert(0, "O-0")
print(orders)

orders.remove("O-2")
print(orders)

last = orders.pop()
print(last, orders)

print(orders.index("O-3"), orders.count("O-3"))

amounts = [1200.0, 800.0, 300.0, 500.0, 250.0]

print(sorted(amounts))                    # sorted() returns a NEW list
print(amounts)                            # the original is unchanged

amounts.sort(reverse=True)                # sort() changes the list in place
print(amounts)

regions = ["West", "east", "North", "South"]
print(sorted(regions))                            # capital letters sort before lowercase
print(sorted(regions, key=str.lower))             # key= changes what is compared

amounts = [300.0, 100.0, 200.0]
result = amounts.sort()
print(result)                 # None: sort() changes the list and returns nothing
print(amounts)

amounts = [1200.0, 800.0, 300.0, 500.0, 250.0, 1800.0, 950.0]

print(len(amounts), sum(amounts), min(amounts), max(amounts))
print(f"average: {sum(amounts) / len(amounts):.2f}")
print(500.0 in amounts, 999.0 in amounts)

original = [1, 2, 3]
alias = original              # a second name for the same list
copy = original.copy()        # a new list

alias.append(4)
print(original)               # changed: alias is the same object
print(copy)                   # unaffected

amounts = [1200.0, 800.0, 300.0]

for amount in amounts:
    print("Order amount:", amount)

print("Loop finished")      # not indented: runs once, after the loop

amounts = [1200.0, 800.0, 300.0, 500.0, 250.0, 1800.0, 950.0]

total = 0
large_orders = 0

for amount in amounts:
    total += amount
    if amount > 1000:
        large_orders += 1

print(f"total {total:,.1f}, large orders: {large_orders}")

for number in range(3):
    print("Retry attempt", number + 1)

regions = ["West", "East", "North"]

for i in range(len(regions)):
    print(i, regions[i])

for position, region in enumerate(regions):
    print(position, region)

print("--")
for number, region in enumerate(regions, start=1):      # start counting at 1 for people
    print(f"Row {number}: {region}")

ids = [1001, 1002, 1003]
amounts = [1200.0, 800.0, 300.0]

for order_id, amount in zip(ids, amounts):
    print(order_id, amount)

amounts = [1200.0, 800.0, 300.0, 500.0, 250.0, 1800.0, 950.0]

print("Even index, with a loop:")
for i in range(len(amounts)):
    if i % 2 == 0:
        print(" ", i, amounts[i])

print("Even index, with slicing :", amounts[::2])
print("Odd index, with slicing  :", amounts[1::2])

large = []
for amount in amounts:
    if amount >= 900:
        large.append(amount)

print(large)

largest = max(amounts)
position = amounts.index(largest)
print(f"Largest order {largest} is at index {position}")

regions = ["West", "East", "West", "North", "East", "West", "South"]

for region in ["West", "East", "North", "South"]:
    print(f"{region:<6} {regions.count(region)}")

order_ids = [1001, 1002, 1002, 1003, 1001, 1004]

unique = []
for order_id in order_ids:
    if order_id not in unique:
        unique.append(order_id)

print(unique)

amounts = [100.0, 0.0, 0.0, 250.0, 0.0]

for amount in amounts:
    if amount == 0.0:
        amounts.remove(amount)       # removing shifts the later items left, so the loop skips one

print(amounts)

amounts = [100.0, 0.0, 0.0, 250.0, 0.0]
amounts = [a for a in amounts if a != 0.0]      # a list comprehension: Topic 11
print(amounts)
