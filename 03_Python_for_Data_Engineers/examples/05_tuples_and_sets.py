# Module 03, 05 · Tuples and Sets
# Every runnable example from the topic, in order.
# Run:  python 05_tuples_and_sets.py

region = ("W", "West", "Pune")            # round brackets
point = 18.52, 73.85                      # the commas make the tuple: brackets are optional
empty = ()
single = (5,)                             # a single item needs a trailing comma
not_a_tuple = (5)                         # without it, this is just the number 5

print(region, type(region).__name__)
print(point)
print(single, type(single).__name__, "|", not_a_tuple, type(not_a_tuple).__name__)
print(tuple([1, 2, 3]), tuple("abc"))     # convert from another iterable
print(len(region), len(empty))

order = (1001, "Meera Iyer", "West", 1200.0, "completed")

print(order[0])
print(order[-1])
print(order[1:3])          # a slice of a tuple is a tuple
print(order[::-1])
print("West" in order)

try:
    order[3] = 1300.0
except TypeError as error:
    print("TypeError:", error)

new_order = order[:3] + (1300.0,) + order[4:]
print(new_order)
print(order)                 # unchanged

statuses = ("completed", "pending", "completed", "cancelled")

print(statuses.count("completed"))
print(statuses.index("pending"))

order = (1001, "Meera Iyer", "West", 1200.0, "completed")

order_id, customer, region, amount, status = order
print(order_id, customer, amount)

first, *middle, last = order        # * collects the rest into a list
print(first, middle, last)

order_id, _, region, *_ = order     # _ is a convention for "I don't need this"
print(order_id, region)

def summarise(amounts):
    return sum(amounts), len(amounts)        # a tuple

total, count = summarise([1200.0, 800.0, 300.0])
print(total, count)
print(summarise([5.0, 5.0]))

revenue = {
    ("West", "Q3"): 368579.0,
    ("West", "Q4"): 1197802.8,
}
print(revenue[("West", "Q4")])

try:
    revenue[["West", "Q4"]] = 1.0
except TypeError as error:
    print("TypeError:", error)

rows = [(1001, "West", 1200.0), (1002, "East", 800.0), (1003, "West", 300.0)]

for order_id, region, amount in rows:      # unpack each row in the loop header
    print(order_id, region, amount)

record = ("O-1", [100.0, 200.0])
record[1].append(300.0)             # allowed: we changed the list inside, not the tuple
print(record)

customers = {1, 2, 3, 3, 2, 1}               # duplicates are dropped
print(customers)

regions = set(["West", "East", "West"])      # from any iterable
print(sorted(regions))

letters = set("analytics")                   # from text: its unique characters
print(sorted(letters))

empty = set()                                # {} creates an empty DICTIONARY, not a set
print(type(empty).__name__, type({}).__name__)

try:
    bad = {[1, 2], 3}
except TypeError as error:
    print("TypeError:", error)

order_ids = [1001, 1002, 1002, 1003, 1001, 1004]

unique_ids = set(order_ids)
print(len(order_ids), len(unique_ids))
print(sorted(unique_ids))

print(list(dict.fromkeys(order_ids)))      # keeps the original order (dictionaries keep insertion order)

statuses = {"completed", "pending"}

statuses.add("cancelled")
statuses.add("completed")              # already there: no change
statuses.update(["shipped", "returned"])
print(sorted(statuses))

statuses.discard("returned")
statuses.discard("teleported")         # not present: silently ignored
print(sorted(statuses))

try:
    statuses.remove("teleported")
except KeyError as error:
    print("KeyError:", error)

statuses = {"completed", "pending", "cancelled"}

print("completed" in statuses)
print(len(statuses))

for status in sorted(statuses):          # sorted() gives a fixed, readable order
    print(status)

try:
    print(statuses[0])
except TypeError as error:
    print("TypeError:", error)

q3 = {1, 2, 3, 5, 8}      # customer IDs who ordered in Q3
q4 = {2, 3, 4, 5, 9}      # customer IDs who ordered in Q4

print("Ordered in either quarter :", sorted(q3 | q4))
print("Retained (both)           :", sorted(q3 & q4))
print("Lost (Q3 only)            :", sorted(q3 - q4))
print("New (Q4 only)             :", sorted(q4 - q3))
print("In exactly one quarter    :", sorted(q3 ^ q4))

allowed = {"completed", "pending", "cancelled", "shipped"}
seen = {"completed", "pending"}
bad_feed = {"completed", "teleported"}

print(seen <= allowed)                       # all statuses seen are valid
print(bad_feed <= allowed)
print(sorted(bad_feed - allowed))            # which ones are not valid?
print({1, 2}.isdisjoint({3, 4}))

active = {1, 2, 3, 4}
active.intersection_update({2, 3, 9})     # keep only items also in the other set
print(sorted(active))

active.difference_update({3})
print(sorted(active))

pair = frozenset({"West", "East"})
routes = {pair: "inter-region"}
print(routes[frozenset({"East", "West"})])      # order does not matter
