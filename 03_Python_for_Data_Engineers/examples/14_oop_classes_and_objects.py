# Module 03, 14 · OOP: Classes and Objects
# Every runnable example from the topic, in order.
# Run:  python 14_oop_classes_and_objects.py

class Order:
    pass                       # an empty class: valid, and a starting point


first = Order()                # create an object: call the class like a function
second = Order()

print(type(first).__name__)
print(first is second)         # two different objects

class Order:
    def __init__(self, order_id, region, amount):
        self.order_id = order_id         # properties
        self.region = region
        self.amount = amount

    def total_with_tax(self, rate=0.18):   # a method
        return round(self.amount * (1 + rate), 2)

    def describe(self):
        return f"Order {self.order_id} ({self.region}): {self.amount}"


o1 = Order(1001, "West", 1200.0)
o2 = Order(1002, "East", 800.0)

print(o1.describe())
print(o2.describe())
print(o1.total_with_tax())
print(o2.total_with_tax(rate=0.05))

print(o1.region)                # read a property
o1.region = "North"             # change a property
print(o1.describe())

o1.coupon = "FIRST10"           # Python also lets you add new properties at any time
print(o1.coupon)
print(hasattr(o2, "coupon"))    # o2 was not affected

print(o1.describe())
print(Order.describe(o1))       # the same call, written out: self is o1

class Order:
    def __init__(self, order_id, region, amount, status="pending"):
        if amount < 0:
            raise ValueError(f"amount cannot be negative: {amount}")
        self.order_id = order_id
        self.region = region.strip().title()     # clean on the way in
        self.amount = amount
        self.status = status                     # default value


good = Order(1003, " east ", 450.0)
print(good.region, good.status)

try:
    Order(1004, "West", -10.0)
except ValueError as err:
    print("Rejected:", err)

class Order:
    tax_rate = 0.18                     # class variable: shared by every order
    orders_created = 0                  # class variable used as a counter

    def __init__(self, order_id, amount):
        self.order_id = order_id        # instance variables: one copy per object
        self.amount = amount
        Order.orders_created += 1       # update the shared counter through the class

    def total(self):
        tax = self.amount * Order.tax_rate     # 'tax' is a local variable
        return round(self.amount + tax, 2)


a = Order(1, 1000.0)
b = Order(2, 2000.0)

print(a.total(), b.total())
print(Order.orders_created)
print(Order.tax_rate, a.tax_rate, b.tax_rate)   # the same value everywhere

a.tax_rate = 0.05                       # creates an instance variable on a only
print(a.tax_rate, b.tax_rate, Order.tax_rate)

class Order:
    tax_rate = 0.18

    def __init__(self, order_id, region, amount):
        self.order_id = order_id
        self.region = region
        self.amount = amount

    def total(self):                                 # instance method
        return round(self.amount * (1 + self.tax_rate), 2)

    @classmethod
    def from_csv_line(cls, line):                    # class method: builds an Order from a text line
        order_id, region, amount = line.split(",")
        return cls(int(order_id), region, float(amount))

    @classmethod
    def set_tax_rate(cls, rate):                     # class method: changes class-wide data
        cls.tax_rate = rate

    @staticmethod
    def is_valid_region(region):                     # static method: needs neither object nor class
        return region in {"North", "South", "East", "West"}


order = Order.from_csv_line("1005,West,1500.0")
print(order.order_id, order.region, order.amount)
print(order.total())

Order.set_tax_rate(0.12)
print(order.total())

print(Order.is_valid_region("West"), Order.is_valid_region("Mars"))

class Customer:
    def __init__(self, name, email, card_token):
        self.name = name                    # public
        self._email = email                 # protected by convention: "please do not touch"
        self.__card_token = card_token      # private: name mangled

    def masked_token(self):
        return "****" + self.__card_token[-4:]


c = Customer("Meera Iyer", "meera@example.com", "tok_9f3a21c7")

print(c.name)
print(c._email)                  # works, but the underscore says "internal"
print(c.masked_token())

try:
    print(c.__card_token)
except AttributeError as err:
    print("AttributeError:", err)

print(c._Customer__card_token)   # the mangled name still works, so it is not real security

class Order:
    VALID_STATUS = {"pending", "shipped", "completed", "cancelled"}   # class variable (constant by convention)

    def __init__(self, order_id, region, amount, status="pending"):
        if status not in Order.VALID_STATUS:
            raise ValueError(f"invalid status: {status}")
        self.order_id = order_id
        self.region = region
        self.amount = amount
        self.status = status

    def __repr__(self):
        return f"Order(id={self.order_id}, region={self.region!r}, amount={self.amount}, status={self.status!r})"

    def is_revenue(self):
        return self.status == "completed"


rows = [(1001, "West", 1200.0, "completed"), (1002, "East", 800.0, "cancelled"),
        (1003, "West", 300.0, "completed"), (1004, "North", 500.0, "pending")]
orders = [Order(*row) for row in rows]

print(orders[0])
print(sum(o.amount for o in orders if o.is_revenue()))
