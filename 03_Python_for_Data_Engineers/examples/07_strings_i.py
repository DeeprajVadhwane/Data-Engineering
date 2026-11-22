# Module 03, 07 · Strings I
# Every runnable example from the topic, in order.
# Run:  python 07_strings_i.py
# Note: the document ran input() with fixed answers; here you type them yourself.

region = "West"
city = 'Pune'
note = """Order held for review.
Customer called twice."""

print(region, city)
print(note)
print(type(region).__name__, len(region))

print("It's fine")
print('She said "ship it"')
print("Line one\nLine two")      # \n is a new line
print("Column A\tColumn B")      # \t is a tab
print("C:\\data\\orders.csv")    # \\ is one backslash
print(r"C:\data\orders.csv")     # r"..." is a raw string: backslashes stay as written

first = "Meera"
last = "Iyer"
print(first + " " + last)     # concatenation
print("-" * 20)               # repetition
print("West" in "North West") # membership test

code = "ORD-2025-1001"

print(code[0])      # first character
print(code[4])
print(code[-1])     # last character
print(code[-4:])    # last four characters

code = "ORD-2025-1001"

print(code[0:3])     # ORD
print(code[4:8])     # 2025
print(code[9:])      # from position 9 to the end
print(code[:3])      # from the start to position 3
print(code[::2])     # every second character
print(code[::-1])    # reversed

code = "ORD-2025-1001"
print(code[50:60] == "")      # a slice out of range gives an empty string
try:
    print(code[50])
except IndexError as error:
    print("IndexError:", error)

code = "ORD-2025-1001"
try:
    code[0] = "X"
except TypeError as error:
    print("TypeError:", error)

code = "X" + code[1:]         # build a new string instead
print(code)

text = "xyz Company west"

print(text.upper())
print(text.lower())
print(text.title())          # first letter of every word
print(text.capitalize())     # only the first letter of the string
print(text.swapcase())

raw = "   Meera Iyer \n"
print(repr(raw.strip()))      # both ends
print(repr(raw.lstrip()))     # left only
print(repr(raw.rstrip()))     # right only
print("**West**".strip("*"))  # strip given characters

email = "asha@xyzcompany.com"

print(email.find("@"))              # position, or -1 if missing
print(email.find("#"))
print(email.index("@"))             # like find, but raises ValueError if missing
print(email.count("a"))
print(email.startswith("asha"))
print(email.endswith(".com"))

print("1,200.50".replace(",", ""))

line = "1001,Meera Iyer,West,1200.50"
fields = line.split(",")
print(fields)

print("-".join(["2025", "12", "02"]))       # join a list of strings
print("a b  c".split())                      # no argument: split on any whitespace
print("one two three".split(" ", 1))         # at most one split

print("12345".isdigit())
print("12.5".isdigit())      # the dot is not a digit
print("West".isalpha())
print("West2".isalnum())
print("   ".isspace())
print("West".islower(), "WEST".isupper())

print("42".zfill(6))          # zero-pad to width 6
print("West".ljust(8) + "|")
print("West".rjust(8) + "|")
print("West".center(8, "*"))

raw_region = "  wEsT "
clean = raw_region.strip().capitalize()
print(repr(clean))

name = "Meera Iyer"
amount = 1200.5
orders = 7

print(f"{name} placed {orders} orders worth {amount}")
print(f"{amount:,.2f}")          # thousands separator, 2 decimals
print(f"{orders:03d}")           # zero-padded to 3 digits
print(f"{0.1834:.1%}")           # as a percentage
print(f"{name:<12}|{orders:>4}|")   # left and right aligned
print(f"{2 + 3 = }")             # shows the expression and its value (Python 3.8+)

print("{} placed {} orders".format("Meera", 7))
print("{0} placed {1} orders. {0} is in {2}".format("Meera", 7, "Pune"))
print("{name} owes {amount:,.2f}".format(name="Meera", amount=1200.5))

print("%s owes %.2f" % ("Meera", 1200.5))

name = input("Customer name: ")
amount_text = input("Order amount: ")

print(f"Name: {name!r}")
print(f"Amount: {amount_text!r}, type {type(amount_text).__name__}")

print(int("42") + 1)
print(float("1200.50") * 2)
print(str(99) + " items")
print(int(7.9))               # int() truncates, it does not round
print(round(7.9))
print(list("West"))           # a string becomes a list of characters

for text in ["42", "1,200", "12.5", "abc", ""]:
    try:
        print(f"{text!r:>8} -> {int(text)}")
    except ValueError as error:
        print(f"{text!r:>8} -> ValueError: {error}")

print(bool("False"), bool("0"), bool(""))

def to_amount(text):
    cleaned = text.strip().replace(",", "")
    if cleaned == "":
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None

for raw in [" 1,200.50 ", "800", "", "N/A"]:
    print(f"{raw!r:>14} -> {to_amount(raw)}")
