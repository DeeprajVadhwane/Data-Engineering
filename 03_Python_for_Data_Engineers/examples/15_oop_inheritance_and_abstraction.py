# Module 03, 15 · OOP: Inheritance and Abstraction
# Every runnable example from the topic, in order.
# Run:  python 15_oop_inheritance_and_abstraction.py

class Source:
    def __init__(self, name):
        self.name = name

    def log(self, message):
        print(f"[{self.name}] {message}")


class CsvSource(Source):                 # CsvSource inherits from Source
    def read(self):
        self.log("reading csv")          # uses the inherited method
        return ["row1", "row2"]


csv_source = CsvSource("partner_csv")
rows = csv_source.read()
print(rows)
print(isinstance(csv_source, CsvSource), isinstance(csv_source, Source))
print(issubclass(CsvSource, Source))

class JsonSource(Source):
    def __init__(self, name, path):
        super().__init__(name)           # run the parent's constructor first
        self.path = path                 # then add what is specific to JSON

    def read(self):
        self.log(f"reading json from {self.path}")
        return [{"order_id": 1}]


js = JsonSource("webshop_json", "/data/orders.json")
print(js.read())
print(js.name, js.path)

class Source:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return f"source {self.name}"


class FileSource(Source):                       # level 2
    def __init__(self, name, path):
        super().__init__(name)
        self.path = path

    def describe(self):
        return super().describe() + f" at {self.path}"


class CsvSource(FileSource):                    # level 3
    def __init__(self, name, path, delimiter=","):
        super().__init__(name, path)
        self.delimiter = delimiter

    def describe(self):
        return super().describe() + f" (csv, delimiter {self.delimiter!r})"


print(CsvSource("partner", "/data/orders.csv", ";").describe())

class Loggable:                                  # a mixin: only adds logging
    def log(self, message):
        print(f"[{type(self).__name__}] {message}")


class Retryable:                                 # another mixin: adds retry behaviour
    max_retries = 3

    def describe_retry(self):
        return f"up to {self.max_retries} retries"


class FileSource(Source):
    pass


class CsvSource(FileSource, Loggable, Retryable):   # inherits from three classes
    pass


s = CsvSource("partner")
s.log("started")
print(s.describe(), "|", s.describe_retry())

class Source:
    def __init__(self, name):
        self.name = name

    def read(self):
        raise NotImplementedError("subclasses must implement read()")


class CsvSource(Source):
    def read(self):
        return [("1001", "West", "1200.0")]


class JsonSource(Source):
    def read(self):
        return [{"order_id": 1001, "region": "West", "amount": 1200.0}]


for source in (CsvSource("csv"), JsonSource("json")):
    print(source.name, source.read())

class A:
    def who(self):
        return "A"


class B(A):
    def who(self):
        return "B"


class C(A):
    def who(self):
        return "C"


class D(B, C):                  # diamond: D inherits from B and C, which both inherit from A
    pass


print(D().who())

print([cls.__name__ for cls in D.__mro__])
print(D.mro() == list(D.__mro__))

class A:
    def setup(self):
        print("A setup")


class B(A):
    def setup(self):
        print("B setup")
        super().setup()


class C(A):
    def setup(self):
        print("C setup")
        super().setup()


class D(B, C):
    def setup(self):
        print("D setup")
        super().setup()


D().setup()

from abc import ABC, abstractmethod


class DataSource(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def read(self):
        """Return a list of order dictionaries."""

    def run(self):                              # a concrete method shared by all subclasses
        rows = self.read()
        print(f"[{self.name}] read {len(rows)} rows")
        return rows


class CsvSource(DataSource):
    def read(self):
        raw = ["1001,West,1200.0", "1002,East,800.0"]
        return [dict(zip(("order_id", "region", "amount"), line.split(","))) for line in raw]


class BrokenSource(DataSource):
    pass                                        # forgot to implement read()


print(CsvSource("partner_csv").run())

try:
    BrokenSource("oops")
except TypeError as err:
    print("TypeError:", err)

try:
    DataSource("abstract")
except TypeError as err:
    print("TypeError:", err)

class JsonSource(DataSource):
    def read(self):
        return [{"order_id": "1003", "region": "North", "amount": "500.0"}]


class DatabaseSource(DataSource):
    def __init__(self, name, query):
        super().__init__(name)
        self.query = query

    def read(self):
        return [{"order_id": "1004", "region": "South", "amount": "250.0"}]


def load_all(sources):
    """Works with any DataSource, whatever its type."""
    rows = []
    for source in sources:
        rows.extend(source.run())
    return rows


all_rows = load_all([CsvSource("partner_csv"), JsonSource("webshop_json"),
                     DatabaseSource("orders_db", "SELECT * FROM orders")])
print(len(all_rows), "rows in total")

class Sink(ABC):
    @property
    @abstractmethod
    def destination(self):
        """Where this sink writes."""

    @abstractmethod
    def write(self, rows):
        """Write the rows."""


class ConsoleSink(Sink):
    destination = "console"

    def write(self, rows):
        for row in rows:
            print("->", row)


sink = ConsoleSink()
print(sink.destination)
sink.write(all_rows[:2])

class Logger:
    def info(self, message):
        print("INFO", message)


class Pipeline:
    def __init__(self, source, logger):
        self.source = source              # a Pipeline HAS a source and HAS a logger
        self.logger = logger

    def run(self):
        rows = self.source.read()
        self.logger.info(f"loaded {len(rows)} rows")


Pipeline(CsvSource("partner_csv"), Logger()).run()
