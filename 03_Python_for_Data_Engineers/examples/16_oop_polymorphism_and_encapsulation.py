# Module 03, 16 · OOP: Polymorphism and Encapsulation
# Every runnable example from the topic, in order.
# Run:  python 16_oop_polymorphism_and_encapsulation.py

print(len("West"), len([1, 2, 3]), len({"a": 1}))     # len() works on many types
print(3 + 4, "a" + "b", [1] + [2])                    # + means something different for each

class Sink:
    def write(self, rows):
        raise NotImplementedError

    def report(self, rows):
        self.write(rows)
        print(f"{type(self).__name__}: wrote {len(rows)} rows")


class ConsoleSink(Sink):
    def write(self, rows):                      # overrides Sink.write
        for row in rows:
            print("  ->", row)


class ListSink(Sink):
    def __init__(self):
        self.stored = []

    def write(self, rows):                      # overrides Sink.write differently
        self.stored.extend(rows)


rows = [{"order_id": 1001, "amount": 1200.0}, {"order_id": 1002, "amount": 800.0}]

for sink in (ConsoleSink(), ListSink()):        # the loop does not check types
    sink.report(rows)

class Order:
    def __init__(self, order_id, amount):
        self.order_id = order_id
        self.amount = amount

    def total(self):
        return self.amount


class ExportOrder(Order):
    def __init__(self, order_id, amount, duty_rate):
        super().__init__(order_id, amount)          # parent's setup
        self.duty_rate = duty_rate                  # extra data for the child

    def total(self):                                # overridden method
        return round(self.amount * (1 + self.duty_rate), 2)


orders = [Order(1, 1000.0), ExportOrder(2, 1000.0, 0.10)]
for o in orders:
    print(type(o).__name__, o.total())

class CsvWriter:
    def write(self, rows):
        print(f"csv: {len(rows)} rows")


class ApiClient:                                  # unrelated to CsvWriter: no common parent
    def write(self, rows):
        print(f"api: posted {len(rows)} rows")


def publish(target, rows):
    target.write(rows)                            # needs only a .write() method


for target in (CsvWriter(), ApiClient()):
    publish(target, rows)

try:
    publish("not a writer", rows)
except AttributeError as err:
    print("AttributeError:", err)

class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

    def __add__(self, other):                       # defines +
        if self.currency != other.currency:
            raise ValueError(f"cannot add {self.currency} and {other.currency}")
        return Money(self.amount + other.amount, self.currency)

    def __eq__(self, other):                        # defines ==
        return (self.amount, self.currency) == (other.amount, other.currency)

    def __lt__(self, other):                        # defines <
        return self.amount < other.amount

    def __repr__(self):                             # how the object prints
        return f"Money({self.amount}, {self.currency!r})"


a = Money(100, "INR")
b = Money(250, "INR")
print(a + b)
print(a == Money(100, "INR"), a < b)
print(sorted([b, a]))

try:
    a + Money(5, "USD")
except ValueError as err:
    print("ValueError:", err)

class Calculator:
    def total(self, a, b):
        return a + b

    def total(self, a, b, c):            # replaces the first definition
        return a + b + c


calc = Calculator()
try:
    calc.total(1, 2)
except TypeError as err:
    print("TypeError:", err)
print(calc.total(1, 2, 3))

class Calculator:
    def total(self, *values):            # accepts any number of arguments
        return sum(values)

    def price(self, amount, tax_rate=0.18, discount=0.0):    # optional parameters
        return round(amount * (1 + tax_rate) * (1 - discount), 2)


calc = Calculator()
print(calc.total(1, 2), calc.total(1, 2, 3, 4))
print(calc.price(1000), calc.price(1000, discount=0.1))

from functools import singledispatch


@singledispatch
def to_amount(value):
    raise TypeError(f"cannot convert {type(value).__name__}")


@to_amount.register
def _(value: int):
    return float(value)


@to_amount.register
def _(value: str):
    return float(value.replace(",", ""))


print(to_amount(1200), to_amount("1,200.50"))

class Order:
    def __init__(self, order_id, region="Unknown", amount=0.0):    # defaults: several ways to call
        self.order_id = order_id
        self.region = region
        self.amount = amount

    @classmethod
    def from_dict(cls, record):                                      # build from a dictionary
        return cls(record["order_id"], record["region"], record["amount"])

    @classmethod
    def from_csv_line(cls, line):                                    # build from a CSV line
        order_id, region, amount = line.split(",")
        return cls(int(order_id), region, float(amount))

    def __repr__(self):
        return f"Order({self.order_id}, {self.region!r}, {self.amount})"


print(Order(1))
print(Order(2, "West", 300.0))
print(Order.from_dict({"order_id": 3, "region": "East", "amount": 450.0}))
print(Order.from_csv_line("4,North,980.5"))

class Order:
    def __init__(self, order_id, amount, discount=0.0):
        self.order_id = order_id
        self.amount = amount
        self.discount = discount

    def payable(self):
        return round(self.amount * (1 - self.discount), 2)


o = Order(1, 1000.0)
o.discount = 5.0                 # nothing stops this
print(o.payable())

class Order:
    def __init__(self, order_id, amount, discount=0.0):
        self.order_id = order_id
        self.amount = amount
        self.discount = discount            # goes through the setter below

    @property
    def discount(self):                     # getter: runs on  order.discount
        return self._discount

    @discount.setter
    def discount(self, value):              # setter: runs on  order.discount = value
        if not 0 <= value <= 0.5:
            raise ValueError(f"discount must be between 0 and 0.5, got {value}")
        self._discount = value

    def payable(self):
        return round(self.amount * (1 - self._discount), 2)


o = Order(1, 1000.0)
o.discount = 0.2
print(o.discount, o.payable())

try:
    o.discount = 5.0
except ValueError as err:
    print("ValueError:", err)

try:
    Order(2, 500.0, discount=0.9)
except ValueError as err:
    print("ValueError:", err)

class Order:
    def __init__(self, order_id, quantity, unit_price):
        self._order_id = order_id
        self.quantity = quantity
        self.unit_price = unit_price

    @property
    def order_id(self):                      # read-only: no setter
        return self._order_id

    @property
    def amount(self):                        # calculated from other data
        return self.quantity * self.unit_price


o = Order(7, 3, 250.0)
print(o.order_id, o.amount)

o.quantity = 4
print(o.amount)                              # recalculated automatically

try:
    o.order_id = 8
except AttributeError as err:
    print("AttributeError:", err)

class Order:
    def __init__(self, order_id, amount, currency="INR"):
        self.order_id = order_id
        self.price = Money(amount, currency)

    @property
    def amount(self):
        return self.price.amount


orders = [Order(1001, 1200.0), Order(1002, 800.0), Order(1003, 300.0)]

total = Money(0, "INR")
for order in orders:
    total = total + order.price                 # operator overloading

print("Total:", total)

for sink in (ConsoleSink(), ListSink()):         # polymorphism
    sink.report([{"order_id": o.order_id, "amount": o.amount} for o in orders])
