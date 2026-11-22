# Module 03, 19 · Module Review and Interview Preparation
# Every runnable example from the topic, in order.
# Run:  python 19_module_review_and_interview_prep.py

raw_lines = [
    "1001, Meera Iyer , west , 1,200.50 , completed",
    "1002,Rohan Shah,EAST,800,completed",
    "1003,Anika Gupta,North,,completed",
    "1004,Dev Patel,south,abc,completed",
    "1005,Isha Nair, West ,300,cancelled",
    "1006,Karan Mehta,East,650,Completed",
]


def parse_line(line):
    """Return a clean record, or raise ValueError with the reason."""
    parts = [part.strip() for part in line.split(",")]
    order_id, customer, region, status = parts[0], parts[1], parts[2], parts[-1]
    amount_text = ",".join(parts[3:-1])      # rejoin: "1,200.50" was split at its thousands comma
    if amount_text == "":
        raise ValueError("amount missing")
    try:
        amount = float(amount_text.replace(",", ""))
    except ValueError:
        raise ValueError("amount not a number")
    return {"order_id": int(order_id), "customer": customer, "region": region.capitalize(),
            "amount": amount, "status": status.lower()}


clean, rejected = [], []
for line in raw_lines:
    try:
        clean.append(parse_line(line))
    except ValueError as reason:
        rejected.append((line.split(",")[0], str(reason)))

print(f"clean: {len(clean)}   rejected: {len(rejected)}")
for order_id, reason in rejected:
    print(f"  rejected {order_id}: {reason}")

revenue = {}
for record in clean:
    if record["status"] == "completed":
        revenue[record["region"]] = revenue.get(record["region"], 0) + record["amount"]

print()
for region, total in sorted(revenue.items(), key=lambda item: item[1], reverse=True):
    print(f"{region:<6} {total:>10,.2f}")
