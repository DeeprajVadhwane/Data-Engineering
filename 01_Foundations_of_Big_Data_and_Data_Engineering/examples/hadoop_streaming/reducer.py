#!/usr/bin/env python3
"""Hadoop Streaming reducer: input arrives SORTED by key, so equal words are adjacent."""
import sys

current_word, current_count = None, 0
for line in sys.stdin:
    word, count = line.rstrip("\n").split("\t")
    if word == current_word:
        current_count += int(count)
    else:
        if current_word is not None:
            print(f"{current_word}\t{current_count}")
        current_word, current_count = word, int(count)
if current_word is not None:
    print(f"{current_word}\t{current_count}")
