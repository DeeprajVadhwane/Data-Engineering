# Module 03, 03 · Operators and Intro to Conditions
# Every runnable example from the topic, in order.
# Run:  python 03_operators_and_intro_conditions.py

print(7 + 2, 7 - 2, 7 * 2)
print(7 / 2, 8 / 2)           # / always returns a float
print(7 // 2, 7 % 2, 7 ** 2)
print(divmod(7, 2))            # quotient and remainder in one call

print(-7 // 2, -7 % 2)
print(int(-7 / 2))            # truncates toward zero: a different answer

lines = 1773
page_size = 500

full_pages, remainder = divmod(lines, page_size)
total_pages = full_pages + (1 if remainder else 0)

print(f"{full_pages} full pages, {remainder} lines left, {total_pages} pages in total")
print(-(-lines // page_size))     # a common ceiling-division trick: negate, floor-divide, negate

print("Order " + "1001")
print("-" * 20)
print([0] * 5)
print([1, 2] + [3])

try:
    print(100 / 0)
except ZeroDivisionError as error:
    print("ZeroDivisionError:", error)

revenue = 1000
revenue += 250        # add
revenue -= 50         # subtract
revenue *= 2          # multiply
print(revenue)

revenue //= 7
print(revenue)
revenue **= 2
print(revenue)

log = "start"
log += " > load"      # += also works on strings
print(log)

amount = 1200
print(amount == 1200, amount != 1200)
print(amount > 1000, amount < 1000)
print(amount >= 1200, amount <= 1000)

print("West" == "west")            # text comparison is case sensitive
print("Delhi" < "Pune")            # strings compare alphabetically, by character code
print(1 == 1.0)                    # numbers of different types compare by value
print(1 == "1")                    # different kinds of value are simply not equal

amount = 1200

print(1000 <= amount < 5000)               # a range test
print(1000 <= amount and amount < 5000)    # the long form: the same result

import math

computed = 0.1 + 0.2
print(computed == 0.3)
print(math.isclose(computed, 0.3))

amount = 1200
status = "completed"
is_paid = False

print(amount > 1000 and status == "completed")
print(amount > 5000 or status == "completed")
print(not is_paid)

orders = 0
total = 5000

print(orders != 0 and total / orders > 100)    # no ZeroDivisionError: the right side never runs

print("" or "unknown")             # first truthy value, or the last one
print("West" or "unknown")
print(0 and 5)                     # first falsy value, or the last one
print(None or 0 or "fallback")

region = ""
print(region or "UNASSIGNED")

amount = 1500
status = "pending"

# Intended rule: (amount > 1000 or amount < 0) AND status is completed
wrong = amount > 1000 or amount < 0 and status == "completed"
right = (amount > 1000 or amount < 0) and status == "completed"

print("as written :", wrong)
print("with brackets:", right)

a = [1001, 1002]
b = [1001, 1002]          # a different list with the same content
c = a                     # another name for the same list

print(a == b)             # same content
print(a is b)             # different objects
print(a is c)             # the same object
print(id(a) == id(c))     # id() is the object's identity

coupon = None

print(coupon is None)
print(coupon is not None)

allowed_status = ["completed", "pending", "cancelled"]

print("completed" in allowed_status)
print("teleported" not in allowed_status)
print("Pu" in "Pune")                   # also works on text

print(2 + 3 * 4)          # multiplication first
print((2 + 3) * 4)        # brackets first
print(-2 ** 2)            # ** binds tighter than the minus sign
print(2 ** 3 ** 2)        # ** groups right to left: 2 ** 9
print(10 - 2 - 3)         # other operators group left to right

amount = 1200

if amount > 1000:
    print("Large order: needs approval")

print("Checked")

amount = 450

if amount > 1000:
    print("Large order: needs approval")
else:
    print("Standard order")

status = "completed"
amount = 1200
coupon = None

if status == "completed" and amount >= 1000:
    print("High value completed order")

if coupon is None:
    print("No coupon used")

if status in ("cancelled", "pending"):
    print("Not yet revenue")
else:
    print("Counts as revenue")

amount = 1200
label = "large" if amount > 1000 else "standard"
print(label)
