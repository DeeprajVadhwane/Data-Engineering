"""MapReduce word count, simulated in plain Python.

Mirrors the diagram in docs/05: input splits -> map -> shuffle & sort -> reduce.
Real Hadoop runs each phase on many machines; here we run them in one process
so you can see exactly what each phase does.

Run:  python 03_mapreduce_word_count.py
"""
from collections import defaultdict

splits = ["big data", "big ideas", "data matters"]        # 1. input splits


def map_phase(line):
    """2. MAP: emit (word, 1) for every word."""
    return [(word, 1) for word in line.split()]


def shuffle_phase(mapped_outputs):
    """3. SHUFFLE & SORT: bring identical keys together."""
    groups = defaultdict(list)
    for pairs in mapped_outputs:
        for word, one in pairs:
            groups[word].append(one)
    return dict(sorted(groups.items()))


def reduce_phase(word, ones):
    """4. REDUCE: add up the 1s for one word."""
    return word, sum(ones)


mapped = [map_phase(s) for s in splits]
for i, m in enumerate(mapped, 1):
    print(f"map task {i}     : {m}")

grouped = shuffle_phase(mapped)
print(f"after shuffle   : {grouped}")

result = dict(reduce_phase(w, ones) for w, ones in grouped.items())
print(f"final output    : {result}")
