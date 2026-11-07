"""
Simulate MapReduce in plain Python (no Hadoop, no Spark).

Goal: total revenue per city, using the three MapReduce stages:
    Map  ->  Shuffle & Sort  ->  Reduce

Run:  python examples/local/mapreduce_simulation.py
"""
from collections import defaultdict

ORDERS = [
    (101, "Hyderabad", 500),
    (102, "Mumbai", 700),
    (103, "Hyderabad", 300),
    (104, "Bangalore", 800),
    (105, "Mumbai", 200),
    (106, "Hyderabad", 400),
]


def map_stage(records):
    """Emit one (key, value) pair per input record."""
    return [(city, revenue) for _order_id, city, revenue in records]


def shuffle_and_sort(pairs):
    """Group every value under its key (what the framework does for you)."""
    groups = defaultdict(list)
    for key, value in pairs:
        groups[key].append(value)
    return dict(sorted(groups.items()))


def reduce_stage(groups):
    """Combine each group's values into a single result."""
    return {key: sum(values) for key, values in groups.items()}


if __name__ == "__main__":
    pairs = map_stage(ORDERS)
    print("MAP output:")
    for p in pairs:
        print("  ", p)

    groups = shuffle_and_sort(pairs)
    print("\nSHUFFLE & SORT output:")
    for k, v in groups.items():
        print(f"   {k:<10} -> {v}")

    result = reduce_stage(groups)
    print("\nREDUCE output:")
    for k, v in result.items():
        print(f"   {k:<10} = {v}")
