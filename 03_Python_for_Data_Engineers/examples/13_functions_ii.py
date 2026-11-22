# Module 03, 13 · Functions-II
# Every runnable example from the topic, in order.
# Run:  python 13_functions_ii.py

def log_event(message):
    print("[LOG]", message)

result = log_event("load started")
print("returned:", result)

def net_amount(amount, discount=0.0):
    if amount <= 0:
        return 0.0                  # early exit
    return round(amount * (1 - discount), 2)
    print("never reached")          # unreachable

print(net_amount(1000, 0.1))
print(net_amount(-5))

def summarise(amounts):
    return min(amounts), max(amounts), sum(amounts) / len(amounts)

low, high, average = summarise([1200, 800, 300, 500])
print(low, high, average)

print(summarise([10, 20]))          # the raw tuple

def parse_amount(text):
    cleaned = text.replace(",", "").strip()
    if not cleaned.replace(".", "", 1).isdigit():
        return None, f"not a number: {text!r}"
    return float(cleaned), None

for raw in ["1,200.50", "abc", " 300 "]:
    value, error = parse_amount(raw)
    print(raw.ljust(10), value, error)

def make_tax_calculator(rate):
    def calculate(price):
        return round(price * (1 + rate), 2)
    return calculate

gst18 = make_tax_calculator(0.18)
gst5 = make_tax_calculator(0.05)
print(gst18(1000), gst5(1000))

square = lambda x: x * x
add_tax = lambda price, rate=0.18: round(price * (1 + rate), 2)

print(square(7))
print(add_tax(1000))

orders = [("O-3", 800), ("O-1", 1200), ("O-2", 300)]

print(sorted(orders, key=lambda o: o[1]))                 # by amount, ascending
print(sorted(orders, key=lambda o: o[1], reverse=True))   # descending
print(max(orders, key=lambda o: o[1]))                    # the largest

customers = [
    {"name": "Meera", "region": "West",  "spend": 5000},
    {"name": "Rahul", "region": "East",  "spend": 1200},
    {"name": "Anika", "region": "West",  "spend": 7000},
]

by_region_then_spend = sorted(customers, key=lambda c: (c["region"], -c["spend"]))
for c in by_region_then_spend:
    print(c["region"], c["name"], c["spend"])

prices = [100, 250, 499, 999]

with_tax = list(map(lambda p: round(p * 1.18, 2), prices))
print(with_tax)

names = ["  meera ", "RAHUL", " anika"]
print(list(map(str.strip, names)))              # an existing function works too
print(list(map(lambda n: n.strip().title(), names)))

quantities = [2, 1, 3]
unit_prices = [100, 250, 400]
print(list(map(lambda q, p: q * p, quantities, unit_prices)))

amounts = [1200, -50, 800, 0, 300]

positive = list(filter(lambda a: a > 0, amounts))
print(positive)

print(list(filter(None, ["West", "", "East", ""])))      # None keeps truthy items

from functools import reduce

amounts = [1200, 800, 300, 500]

total = reduce(lambda acc, x: acc + x, amounts)
print(total)

largest = reduce(lambda a, b: a if a > b else b, amounts)
print(largest)

print(reduce(lambda acc, x: acc + x, amounts, 1000))      # with a starting value

batches = [{"West": 100, "East": 50}, {"West": 30, "North": 20}, {"East": 5}]

def merge(acc, batch):
    result = dict(acc)
    for region, value in batch.items():
        result[region] = result.get(region, 0) + value
    return result

print(reduce(merge, batches, {}))

amounts = [1200, -50, 800, 0, 300]

print(list(map(lambda a: a * 2, filter(lambda a: a > 0, amounts))))
print([a * 2 for a in amounts if a > 0])               # the same, as a comprehension

rate = 0.18                        # global

def show():
    local_note = "inside the function"   # local
    print(rate, local_note)

show()

def compute():
    total = 500
    return total

compute()
try:
    print(total)
except NameError as e:
    print("NameError:", e)

count = 10

def reset():
    count = 0                      # a new local variable, not the global one
    print("inside:", count)

reset()
print("outside:", count)

counter = 0

def increment():
    counter += 1                   # tries to read a local that has no value yet

try:
    increment()
except UnboundLocalError as e:
    print("UnboundLocalError:", e)

processed = 0

def mark_processed():
    global processed
    processed += 1

mark_processed()
mark_processed()
print(processed)

def mark_processed(count):
    return count + 1

processed = 0
processed = mark_processed(processed)
processed = mark_processed(processed)
print(processed)

def make_counter():
    count = 0
    def next_value():
        nonlocal count
        count += 1
        return count
    return next_value

counter = make_counter()
print(counter(), counter(), counter())

another = make_counter()          # its own separate count
print(another())

value = "global"

def outer():
    value = "enclosing"
    def inner():
        value = "local"
        return value
    return inner(), value

print(outer(), value)

def total_amount(*amounts):
    print("received:", amounts)
    return sum(amounts)

print(total_amount(1200, 800))
print(total_amount(1200, 800, 300, 500))

def describe(order_id, **details):
    print("order", order_id, details)

describe(1001, region="West", amount=1200)
describe(1002)

def log(level, *messages, **context):
    print(level, "|", " ".join(messages), "|", context)

log("INFO", "load", "finished", rows=916, seconds=4)

values = [1200, 800, 300]
options = {"level": "WARN"}
print(total_amount(*values))              # * unpacks a list into positional arguments
log(*["INFO", "from", "list"], **{"source": "api"})   # ** unpacks a dict into keywords

from functools import reduce

def strip_text(value):
    return value.strip()

def collapse_spaces(value):
    return " ".join(value.split())

def title_case(value):
    return value.title()

def apply_steps(value, steps):
    return reduce(lambda acc, step: step(acc), steps, value)

name_steps = [strip_text, collapse_spaces, title_case]

raw_names = ["  meera    iyer ", "RAHUL  sharma", " anika gupta"]
print([apply_steps(n, name_steps) for n in raw_names])

print(apply_steps("  ab  cd ", [strip_text, collapse_spaces]))     # a different recipe, same engine
