"""How big is the problem? A back-of-the-envelope calculator for the 100 GB/day scenario.

Run:  python 01_capacity_calculator.py
"""

GB_PER_DAY = 100          # data generated per day
BYTES_PER_ROW = 100       # assumption: a typical small record
EXCEL_ROW_LIMIT = 1_048_576
DISK_MB_PER_SEC = 150     # assumption: sequential read speed of one disk
MACHINES = 100

rows_per_day = GB_PER_DAY * 1024**3 / BYTES_PER_ROW
read_seconds_one = GB_PER_DAY * 1024 / DISK_MB_PER_SEC
read_seconds_many = read_seconds_one / MACHINES

print(f"Data per day     : {GB_PER_DAY} GB")
print(f"Data per month   : {GB_PER_DAY * 30 / 1024:.1f} TB")
print(f"Data per year    : {GB_PER_DAY * 365 / 1024:.1f} TB")
print(f"Rows per day     : {rows_per_day:,.0f}  (at {BYTES_PER_ROW} bytes per row)")
print(f"Excel row limit  : {EXCEL_ROW_LIMIT:,}")
print(f"One day / Excel  : {rows_per_day / EXCEL_ROW_LIMIT:,.0f}x the Excel limit")
print()
print(f"Read 100 GB on 1 machine   : {read_seconds_one:,.0f} s  ({read_seconds_one / 60:.1f} min)")
print(f"Read 100 GB on {MACHINES} machines : {read_seconds_many:,.1f} s  (ideal, no overhead)")
