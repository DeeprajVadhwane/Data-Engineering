# Sample Data

[🏠 Home](../README.md)

Synthetic data created for teaching. It contains no real customers.

| File | Rows | Purpose |
| --- | --- | --- |
| [`sales_sample.csv`](sales_sample.csv) | 60 | Clean retail orders: analysis, exercises, the five management questions |
| [`sales_raw_dirty.csv`](sales_raw_dirty.csv) | 32 | Same schema with deliberate defects for the Bronze → Silver → Gold pipeline |

## Schema

| Column | Type | Description |
| --- | --- | --- |
| `order_id` | int | Unique order number |
| `order_date` | date | When the order was placed |
| `city` | string | Hyderabad, Mumbai, Bangalore, Delhi, Chennai |
| `category` | string | Electronics, Fashion, Home |
| `product` | string | Product name |
| `quantity` | int | Units ordered (1–3) |
| `unit_price` | int | Price per unit (₹) |
| `revenue` | int | `quantity × unit_price` |
| `promised_date` | date | Promised delivery date |
| `delivered_date` | date | Actual delivery date |

## Defects in `sales_raw_dirty.csv`

| Defect | Rows |
| --- | --- |
| Exact duplicate rows | orders 1003, 1006 |
| Missing city | order 1009 |
| Messy city text (`" mumbai "`, `"HYDERABAD"`) | two rows |
| Missing quantity | order 1022 |
| Negative revenue | order 1019 |

---

[🏠 Home](../README.md)
