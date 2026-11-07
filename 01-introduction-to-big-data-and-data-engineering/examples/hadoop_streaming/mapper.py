#!/usr/bin/env python3
"""Hadoop Streaming mapper: read lines from stdin, emit 'word<TAB>1' for every word."""
import sys

for line in sys.stdin:
    for word in line.strip().lower().split():
        print(f"{word}\t1")
