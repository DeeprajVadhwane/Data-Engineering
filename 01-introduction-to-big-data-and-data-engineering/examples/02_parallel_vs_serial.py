"""Scale-out in miniature: split the work, run it on several CPU cores at once.

This is NOT Spark. It uses Python's multiprocessing to show the core idea
behind distributed systems: partition the data, process partitions in parallel,
combine the partial results.

Run:  python 02_parallel_vs_serial.py
"""
import time
from multiprocessing import Pool, cpu_count

N = 40_000_000


def work(bounds):
    """Process ONE partition: sum of squares over a range."""
    lo, hi = bounds
    total = 0
    for i in range(lo, hi):
        total += i * i
    return total


def partition(n, parts):
    step = n // parts
    chunks = [(i * step, (i + 1) * step) for i in range(parts)]
    chunks[-1] = (chunks[-1][0], n)          # last chunk takes the remainder
    return chunks


if __name__ == "__main__":
    workers = max(2, cpu_count())

    t0 = time.perf_counter()
    serial = work((0, N))                                   # 1 worker, all data
    t_serial = time.perf_counter() - t0

    t0 = time.perf_counter()
    with Pool(workers) as pool:                             # many workers
        parallel = sum(pool.map(work, partition(N, workers)))   # combine results
    t_parallel = time.perf_counter() - t0

    assert serial == parallel, "results must match"
    print(f"CPU cores used : {workers}")
    print(f"1 worker       : {t_serial:.2f} s")
    print(f"{workers} workers      : {t_parallel:.2f} s")
    print(f"Speed-up       : {t_serial / t_parallel:.1f}x   (same answer: {serial == parallel})")
    if workers < 4:
        print("Note: you have few CPU cores, so the speed-up will be small. Try a machine with 4+ cores.")
