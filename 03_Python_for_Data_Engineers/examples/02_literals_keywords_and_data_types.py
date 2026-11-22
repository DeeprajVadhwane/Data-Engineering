# Module 03, 02 · Literals, Keywords and Data Types
# Every runnable example from the topic, in order.
# Run:  python 02_literals_keywords_and_data_types.py
# Note: the document ran input() with fixed answers; here you type them yourself.

print(1_000_000)        # underscores make large numbers readable
print(0b1010, 0o17, 0xFF)   # binary, octal and hexadecimal: all print as decimal
print(1.5e3)            # scientific notation
print(type(3 + 2j).__name__)
print("It's fine", 'She said "hello"')    # quote one kind inside the other

order_total = 1200
print(order_total)

import keyword

candidates = ["order_total", "region2", "_temp", "2nd_region", "order-total", "order total", "class", "Total"]

for name in candidates:
    ok = name.isidentifier() and not keyword.iskeyword(name)
    print(f"{name!r:<14} valid: {ok}")

import keyword
import textwrap

print(textwrap.fill(" ".join(keyword.kwlist), width=70))

amounts = [1200, 800, 300]
print(sum(amounts))

sum = 99                       # shadows the built-in function for the rest of the program
try:
    print(sum(amounts))
except TypeError as error:
    print("TypeError:", error)

del sum                        # remove our name, and the built-in is visible again
print(sum(amounts))

region = "West"           # str
quantity = 3              # int
unit_price = 499.99       # float
is_paid = True            # bool
coupon = None             # NoneType

print(region, quantity, unit_price, is_paid, coupon)
print(type(region).__name__, type(quantity).__name__, type(unit_price).__name__)

a = b = c = 0                     # the same value to three names
region, city = "West", "Pune"    # one value for each name, in order
first, second = 10, 20
first, second = second, first    # swap without a temporary variable

print(a, b, c)
print(region, city)
print(first, second)

value = 42
print(type(value).__name__)
value = "forty-two"
print(type(value).__name__)

print(isinstance(42, int), isinstance(42, (int, float)), isinstance("42", int))

print(2 ** 100)                 # big integers just work
print(0.1 + 0.2)                # a float surprise
print(0.1 + 0.2 == 0.3)
print(round(0.1 + 0.2, 2) == 0.3)

from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))     # exact decimal arithmetic

print(True + True, False + 5)
print(isinstance(True, int))

coupon = None
print(coupon is None, coupon == 0, coupon == "")

for value in [0, 0.0, "", [], {}, None, "0", [0], -1]:
    print(f"{value!r:<6} -> {bool(value)}")

print(int("42") + 1)
print(float("499.99"))
print(str(1200) + " INR")
print(int(7.9), int(-7.9))        # int() truncates toward zero, it does not round
print(int(True), float(3))

try:
    int("12.5")
except ValueError as error:
    print("ValueError:", error)

print("West", 1200, True)
print("West", 1200, "Q4", sep=" | ")
print("Loading", end="...")
print("done")

print("Region:\tWest")                # \t is a tab
print("Line one\nLine two")            # \n is a new line
print("A backslash: \\")
print(r"C:\data\orders.csv")           # r"" is a raw string: backslashes stay as written

region = "West"
revenue = 1197802.8
growth = 2.25

print(f"{region} revenue: {revenue:,.2f}")
print(f"{region} growth: {growth:.1%}")
print(f"{region=}")                    # prints the name and value: handy when debugging

customer = input("Customer name: ")
amount = input("Order amount: ")

print(f"Read {customer!r} of type {type(customer).__name__}")
print(f"Read {amount!r} of type {type(amount).__name__}")

amount = "1200"
try:
    total = amount + 100
except TypeError as error:
    print("TypeError:", error)

total = int(amount) + 100        # convert first
print(total)

raw = input("Order amount: ")

try:
    amount = float(raw)
    print(f"Accepted {amount:.2f}")
except ValueError:
    print(f"{raw!r} is not a valid amount")

region, amount, quantity = input("region,amount,quantity: ").split(",")
print(region, int(amount) * int(quantity))
