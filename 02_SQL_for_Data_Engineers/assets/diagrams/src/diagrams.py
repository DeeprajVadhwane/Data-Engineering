"""Module 02 diagrams (SVG). Palette: blue foundations, orange engines, green results, red problems."""
from lib import S, P


def box(s, x, y, w, h, lines, fill, stroke, size=17, fg=None, bold_first=True):
    s.rect(x, y, w, h, fill, stroke, 2, 12)
    n = len(lines)
    top = y + h / 2 - (n - 1) * size * 0.68 + size * 0.33
    for i, l in enumerate(lines):
        s.text(x + w / 2, top + i * size * 1.35, l, size, fg or P["ink"],
               "bold" if (i == 0 and bold_first) else "normal", "middle")


def table(s, x, y, cols, rows, cw, rh=30, head=None, size=15, hl=None):
    head = head or P["blue"]
    w = cw * len(cols)
    s.rect(x, y, w, rh, head, P["navy"], 1.5, 4)
    for j, c in enumerate(cols):
        s.text(x + j * cw + cw / 2, y + rh * 0.68, c, size, "#FFFFFF", "bold", "middle")
    for i, r in enumerate(rows):
        fill = P["lorange"] if hl and i in hl else "#FFFFFF"
        s.rect(x, y + rh * (i + 1), w, rh, fill, P["navy"], 1, 0)
        for j, c in enumerate(r):
            s.text(x + j * cw + cw / 2, y + rh * (i + 1) + rh * 0.68, c, size, P["ink"], "normal", "middle")
    return y + rh * (len(rows) + 1)


def d00_banner(path):
    s = S(1200, 320)
    s.text(60, 120, "SQL for Data Engineers", 54, P["navy"], "bold")
    s.add(f'<rect x="60" y="140" width="110" height="7" rx="3.5" fill="{P["orange"]}"/>')
    s.text(60, 192, "From a business question to a rerunnable pipeline", 24, P["grey"])
    s.text(60, 240, "Module 02  |  10 topics  |  SQLite and Spark SQL", 20, P["blue"], "bold")
    s.grid(800, 70, 300, 180, 4, 4, P["lblue"])
    s.chip(830, 270, 100, 30, "SELECT", P["blue"], size=14)
    s.chip(940, 270, 90, 30, "JOIN", P["orange"], size=14)
    s.chip(1040, 270, 100, 30, "WINDOW", P["green"], size=14)
    s.save(path)


def d00_roadmap(path):
    s = S(1200, 470, "Learning roadmap", "Each topic answers a problem the previous one exposed")
    items = [("01", "Why SQL", P["blue"]), ("02", "Querying", P["blue"]), ("03", "Aggregation", P["blue"]),
             ("04", "Joins", P["blue"]), ("05", "CTEs", P["orange"]), ("06", "Windows", P["orange"]),
             ("07", "Cleaning", P["green"]), ("08", "Modelling", P["green"]), ("09", "Performance", P["green"]),
             ("10", "Review", P["grey"])]
    for i, (n, t, c) in enumerate(items):
        row, col = divmod(i, 5)
        x, y = 50 + col * 224, 150 + row * 150
        s.rect(x, y, 190, 100, "#FFFFFF", c, 3, 14)
        s.badge(x + 30, y + 32, n, c, 20)
        s.text(x + 95, y + 70, t, 20, P["navy"], "bold", "middle")
        if col < 4:
            s.arrow(x + 192, y + 50, x + 222, y + 50, P["navy"], 2)
    s.chip(50, 420, 190, 30, "Language", P["blue"], size=14)
    s.chip(250, 420, 190, 30, "Thinking in steps", P["orange"], size=14)
    s.chip(450, 420, 270, 30, "Production data work", P["green"], size=14)
    s.save(path)


def d01_problem(path):
    s = S(1200, 430, "The business question", "XYZ Company, one analyst, one question")
    s.person(60, 150, 70, P["blue"])
    s.text(95, 250, "Asha, analyst", 17, P["navy"], "bold", "middle")
    box(s, 190, 140, 380, 100, ["Which regions grew fastest", "last quarter, and which", "products are returned most?"],
        P["lgold"], P["gold"], 18)
    s.arrow(130, 190, 188, 190)
    for i, (t, sub) in enumerate([("orders", "916 rows"), ("order_items", "1,773 rows"), ("customers", "60 rows"),
                                  ("products", "16 rows"), ("returns", "119 rows")]):
        s.db(630 + (i % 3) * 190, 120 + (i // 3) * 130, 50, 60, P["lblue"])
        s.text(655 + (i % 3) * 190, 205 + (i // 3) * 130, t, 15, P["navy"], "bold", "middle")
        s.text(655 + (i % 3) * 190, 223 + (i // 3) * 130, sub, 13, P["grey"], "normal", "middle")
    s.arrow(572, 190, 625, 190)
    s.text(60, 380, "Today: spreadsheets and loops, different answers each time.", 18, P["red"], "bold")
    s.text(60, 408, "Goal: one repeatable SQL answer, then a pipeline that produces it daily.", 18, P["green"], "bold")
    s.save(path)


def d01_pipeline(path):
    s = S(1200, 400, "Where SQL sits in a data platform", "Most pipeline steps are SQL queries over layered tables")
    cols = [("Sources", ["App database", "Files, APIs"], P["lgrey"], P["grey"]),
            ("Bronze", ["Raw, as received"], P["lorange"], P["orange"]),
            ("Silver", ["Cleaned,", "deduplicated"], P["lblue"], P["blue"]),
            ("Gold", ["Star schema,", "aggregates"], P["lgreen"], P["green"]),
            ("Consumers", ["Dashboards", "ML, reports"], P["lgold"], P["gold"])]
    for i, (h, ls, f, c) in enumerate(cols):
        x = 40 + i * 230
        s.card(x, 150, 190, 130, h, f, c, hh=40)
        s.lines(x + 95, 215, ls, 16, P["ink"], anchor="middle")
        if i < 4:
            s.arrow(x + 192, 215, x + 228, 215, P["navy"], 3)
    for i in (1, 2, 3):
        s.chip(40 + i * 230 + 5, 305, 180, 32, "SQL transform", P["navy"], size=14)
    s.text(40, 378, "SQL runs the transform steps (ELT): load first, then transform inside the engine.", 17, P["grey"])
    s.save(path)


def d01_schema(path):
    s = S(1200, 520, "The XYZ database", "Five tables, one-to-many relationships")
    spec = {"customers": (60, 140, ["customer_id PK", "name", "city", "region", "segment"]),
            "orders": (350, 140, ["order_id PK", "customer_id FK", "order_date", "status", "shipping_fee"]),
            "order_items": (640, 140, ["order_id FK", "line_no", "product_id FK", "quantity", "unit_price"]),
            "products": (930, 140, ["product_id PK", "name", "category"]),
            "returns": (640, 360, ["return_id PK", "order_id FK", "product_id FK", "reason"])}
    for name, (x, y, cols) in spec.items():
        h = 40 + 30 * len(cols)
        s.card(x, y, 230, h, name, "#FFFFFF", P["blue"], hh=38)
        for i, c in enumerate(cols):
            s.text(x + 16, y + 38 + 23 + i * 30, c, 15, P["red"] if "FK" in c else P["ink"],
                   "bold" if "PK" in c else "normal")
    s.arrow(290, 200, 348, 200, P["navy"], 2)
    s.arrow(580, 200, 638, 200, P["navy"], 2)
    s.arrow(870, 200, 928, 200, P["navy"], 2)
    s.arrow(755, 322, 755, 358, P["navy"], 2)
    s.text(60, 440, "customer 1 : N orders", 16, P["grey"]); s.text(60, 466, "order 1 : N order_items", 16, P["grey"])
    s.text(60, 492, "order_items N : 1 product", 16, P["grey"])
    s.save(path)


def d02_order(path):
    s = S(1200, 560, "Logical order of a query", "The order you write is not the order the engine reasons in")
    steps = [("1", "FROM / JOIN", "Pick and combine tables", P["blue"]),
             ("2", "WHERE", "Filter rows", P["blue"]),
             ("3", "GROUP BY", "Form groups", P["orange"]),
             ("4", "HAVING", "Filter groups", P["orange"]),
             ("5", "SELECT", "Compute columns, aliases", P["green"]),
             ("6", "DISTINCT", "Drop duplicate rows", P["green"]),
             ("7", "ORDER BY", "Sort", P["grey"]),
             ("8", "LIMIT", "Keep first N rows", P["grey"])]
    for i, (n, t, d, c) in enumerate(steps):
        y = 130 + i * 52
        s.rect(60, y, 420, 42, "#FFFFFF", c, 2.5, 10)
        s.badge(84, y + 21, n, c, 14)
        s.text(112, y + 28, t, 18, P["navy"], "bold")
        s.text(250, y + 28, d, 15, P["grey"])
        if i < 7:
            s.arrow(270, y + 43, 270, y + 51, P["navy"], 2)
    s.card(560, 140, 580, 150, "What follows from the order", P["lgold"], P["gold"], P["navy"])
    s.lines(580, 205, ["WHERE cannot use a SELECT alias: it runs earlier",
                       "HAVING can filter aggregates, WHERE cannot",
                       "Window functions run after HAVING: filter them",
                       "in an outer query or CTE, not in WHERE"], 16)
    s.card(560, 320, 580, 150, "Aggregates versus rows", P["lblue"], P["blue"])
    s.lines(580, 385, ["WHERE removes rows before groups exist", "HAVING removes groups after they are computed",
                       "ORDER BY may use aliases: it runs after SELECT"], 16)
    s.save(path)


def d03_group(path):
    s = S(1200, 460, "GROUP BY collapses rows into groups", "Each group becomes one output row")
    rows = [("West", "1200"), ("East", "800"), ("West", "300"), ("North", "500"), ("East", "250")]
    s.text(60, 150, "orders (input)", 17, P["navy"], "bold")
    table(s, 60, 165, ["region", "amount"], rows, 120, 34)
    cols = {"West": P["orange"], "East": P["blue"], "North": P["green"]}
    for i, (r, _) in enumerate(rows):
        s.circle(330, 165 + 34 * (i + 1) + 17, 8, cols[r])
    s.text(430, 150, "groups", 17, P["navy"], "bold")
    for i, (r, sm) in enumerate([("West", "1500"), ("East", "1050"), ("North", "500")]):
        y = 175 + i * 80
        s.rect(430, y, 200, 62, "#FFFFFF", cols[r], 3, 12)
        s.text(530, y + 38, f"{r}: {sm}", 20, P["navy"], "bold", "middle")
    s.arrow(345, 250, 425, 250, P["navy"], 3)
    s.arrow(640, 250, 740, 250, P["navy"], 3)
    s.text(750, 150, "result", 17, P["navy"], "bold")
    table(s, 750, 165, ["region", "SUM(amount)"], [("West", "1500"), ("East", "1050"), ("North", "500")], 160, 34,
          head=P["green"])
    s.text(60, 430, "SELECT region, SUM(amount) FROM orders GROUP BY region", 17, P["grey"])
    s.save(path)


def d04_join_types(path):
    s = S(1200, 520, "Join types", "A = customers, B = orders. Shaded area is what the result keeps")
    kinds = [("INNER", "matches only", 1, 1, 1), ("LEFT", "all A + matches", 1, 1, 0),
             ("RIGHT", "all B + matches", 0, 1, 1), ("FULL", "everything", 1, 1, 1)]
    for i, (t, d, a, m, b) in enumerate(kinds):
        cx = 170 + i * 280
        cy = 270
        s.circle(cx - 35, cy, 70, P["lblue"] if (t in ("LEFT", "FULL")) else "#FFFFFF", P["blue"], 3)
        s.circle(cx + 35, cy, 70, P["lorange"] if (t in ("RIGHT", "FULL")) else "#FFFFFF", P["orange"], 3)
        s.add(f'<clipPath id="c{i}"><circle cx="{cx-35}" cy="{cy}" r="70"/></clipPath>')
        s.add(f'<circle clip-path="url(#c{i})" cx="{cx+35}" cy="{cy}" r="70" fill="{P["green"]}" opacity="0.85"/>')
        s.circle(cx - 35, cy, 70, "none", P["blue"], 3); s.circle(cx + 35, cy, 70, "none", P["orange"], 3)
        s.text(cx - 70, cy + 6, "A", 20, P["navy"], "bold", "middle"); s.text(cx + 70, cy + 6, "B", 20, P["navy"], "bold", "middle")
        s.text(cx, cy + 118, t + " JOIN", 20, P["navy"], "bold", "middle")
        s.text(cx, cy + 144, d, 15, P["grey"], "normal", "middle")
    s.text(60, 475, "Unmatched columns are filled with NULL. Anti-join: LEFT JOIN ... WHERE B.key IS NULL.", 16, P["grey"])
    s.save(path)


def d04_fan_out(path):
    s = S(1200, 520, "Join fan-out", "A one-to-many join repeats the parent row, so parent measures are summed more than once")
    s.text(60, 150, "orders", 17, P["navy"], "bold")
    table(s, 60, 165, ["order_id", "shipping_fee"], [("1001", "50")], 130, 34)
    s.text(60, 290, "order_items", 17, P["navy"], "bold")
    table(s, 60, 305, ["order_id", "product"], [("1001", "Shoes"), ("1001", "Socks"), ("1001", "Cap")], 130, 34)
    s.arrow(340, 300, 440, 300, P["navy"], 3)
    s.text(460, 150, "after the join", 17, P["navy"], "bold")
    table(s, 460, 165, ["order_id", "shipping_fee", "product"], [("1001", "50", "Shoes"), ("1001", "50", "Socks"),
                                                               ("1001", "50", "Cap")], 130, 34, head=P["red"],
          hl=[0, 1, 2])
    box(s, 880, 165, 260, 120, ["SUM(shipping_fee)", "= 150", "true value: 50"], P["lorange"], P["red"], 18)
    s.card(460, 330, 680, 140, "How to avoid it", P["lgreen"], P["green"])
    s.lines(480, 395, ["Aggregate the many side first, then join (one row per order)",
                       "Or sum at the right grain: use order-level data once",
                       "Check: row count and totals before and after the join"], 16)
    s.save(path)


def d05_cte(path):
    s = S(1200, 400, "A query as a pipeline of named steps", "Each CTE is one readable stage; the final SELECT reads the last one")
    names = [("quarterly", "Revenue by region and quarter", P["blue"]), ("pivoted", "Q3 and Q4 side by side", P["blue"]),
             ("growth", "Percent change", P["orange"]), ("final SELECT", "Rank and present", P["green"])]
    for i, (t, d, c) in enumerate(names):
        x = 50 + i * 285
        s.card(x, 150, 240, 120, t, "#FFFFFF", c, hh=40)
        s.lines(x + 120, 218, [d], 15, P["ink"], anchor="middle")
        if i < 3:
            s.arrow(x + 242, 210, x + 283, 210, P["navy"], 3)
    s.text(50, 330, "WITH quarterly AS (...), pivoted AS (...), growth AS (...)", 17, P["grey"])
    s.text(50, 358, "SELECT ... FROM growth ORDER BY growth_pct DESC;", 17, P["grey"])
    s.save(path)


def d06_window(path):
    s = S(1200, 500, "Window function versus GROUP BY", "GROUP BY collapses rows. A window keeps them and adds a calculation")
    data = [("West", "1200"), ("West", "300"), ("East", "800"), ("East", "250")]
    s.card(60, 140, 480, 300, "GROUP BY region", P["lblue"], P["blue"])
    table(s, 100, 205, ["region", "SUM(amount)"], [("West", "1500"), ("East", "1050")], 190, 36)
    s.text(100, 345, "2 rows out: detail is gone", 17, P["red"], "bold")
    s.card(660, 140, 480, 300, "SUM() OVER (PARTITION BY region)", P["lgreen"], P["green"])
    table(s, 690, 205, ["region", "amount", "region_total"],
          [(r, a, "1500" if r == "West" else "1050") for r, a in data], 140, 36, head=P["green"])
    s.text(690, 420, "4 rows out: detail kept, total added", 17, P["green"], "bold")
    s.save(path)


def d07_clean(path):
    s = S(1200, 520, "From raw feed to trusted tables", "Standardise, deduplicate, validate, and never lose a row silently")
    box(s, 40, 170, 190, 110, ["raw_orders_stage", "10 messy rows"], P["lorange"], P["orange"])
    for i, t in enumerate(["Standardise", "Deduplicate", "Validate"]):
        x = 290 + i * 215
        s.arrow(x - 55, 225, x - 5, 225, P["navy"], 3)
        box(s, x, 190, 170, 70, [t], P["lblue"], P["blue"], 18)
    s.arrow(895, 225, 945, 225, P["navy"], 3)
    box(s, 950, 140, 210, 80, ["orders_clean"], P["lgreen"], P["green"], 18)
    box(s, 950, 260, 210, 80, ["orders_rejected", "with a reason"], P["lred"] if "lred" in P else P["lorange"], P["red"], 17)
    s.line(895, 225, 935, 180, P["navy"], 3); s.line(895, 225, 935, 300, P["navy"], 3)
    s.card(40, 390, 1120, 100, "Quality gate", P["lgold"], P["gold"], P["navy"], hh=34, size=17)
    s.text(60, 465, "Checks return violation counts (zero = pass). Raw = clean + rejected. Any failure stops the run.", 16)
    s.save(path)


def d08_star(path):
    s = S(1200, 560, "Star schema", "One fact table at a declared grain, surrounded by dimensions")
    s.card(430, 220, 340, 210, "fact_sales (one row per order line)", P["lorange"], P["orange"], hh=44, size=16)
    s.lines(450, 292, ["order_id, line_no", "order_date_key  ->  dim_date", "customer_key  ->  dim_customer",
                       "product_key  ->  dim_product", "quantity, unit_price, line_amount"], 15)
    for (x, y, t, ls, ax, ay) in [(60, 150, "dim_date", ["date_key", "year, quarter, month", "is_weekend"], 430, 280),
                                  (60, 350, "dim_product", ["product_key", "name, category"], 430, 380),
                                  (870, 150, "dim_customer", ["customer_key", "city, region", "valid_from, valid_to"], 770, 280),
                                  (870, 350, "other dimensions", ["added the same way"], 770, 380)]:
        s.card(x, y, 270, 130, t, P["lblue"], P["blue"], hh=38, size=17)
        s.lines(x + 135, y + 78, ls, 15, anchor="middle")
        s.arrow(x + 270 if x < 400 else x, y + 65, ax, ay, P["navy"], 2.5)
    s.text(60, 530, "Facts: events and measures. Dimensions: who, what, when, where.", 16, P["grey"])
    s.save(path)


def d08_scd(path):
    s = S(1200, 500, "SCD Type 2: keep every version", "Customer 3 moves from Pune to Delhi on 15 November")
    s.text(60, 145, "Type 1 (overwrite): history lost", 18, P["red"], "bold")
    table(s, 60, 160, ["key", "city", "region"], [("3", "Delhi", "North")], 130, 34, head=P["red"])
    s.text(60, 265, "Past orders now report under North", 15, P["red"])
    s.text(60, 315, "Type 2 (new row): history kept", 18, P["green"], "bold")
    table(s, 60, 330, ["key", "city", "valid_from", "valid_to", "current"],
          [("3", "Pune", "2025-07-01", "2025-11-15", "0"), ("61", "Delhi", "2025-11-15", "9999-12-31", "1")],
          160, 36, head=P["green"])
    s.text(900, 180, "Fact rows point to the version", 16, P["navy"], "bold")
    s.text(900, 205, "valid on the order date:", 16, P["navy"], "bold")
    s.lines(900, 240, ["order on 2025-10-20 -> key 3", "order on 2025-12-02 -> key 61"], 16)
    s.save(path)


def d09_lifecycle(path):
    s = S(1200, 380, "Life of a query", "SQL says what. The optimiser decides how")
    steps = [("Parse", "syntax to tree", P["blue"]), ("Analyse", "names and types", P["blue"]),
             ("Optimise", "pick cheapest plan", P["orange"]), ("Execute", "scan, join, aggregate", P["green"]),
             ("Result", "rows returned", P["gold"])]
    for i, (t, d, c) in enumerate(steps):
        x = 40 + i * 230
        s.card(x, 140, 190, 110, t, "#FFFFFF", c, hh=40)
        s.text(x + 95, 215, d, 15, P["ink"], "normal", "middle")
        if i < 4:
            s.arrow(x + 192, 195, x + 228, 195, P["navy"], 3)
    s.chip(450, 275, 190, 30, "statistics + indexes", P["orange"], size=14)
    s.arrow(545, 273, 545, 252, P["orange"], 2.5)
    s.text(40, 345, "EXPLAIN shows the plan the optimiser chose.", 17, P["grey"])
    s.save(path)


def d09_index(path):
    s = S(1200, 480, "Full scan versus index search", "Looking for customer_id = 17")
    s.card(50, 140, 500, 290, "Full scan: read every row", P["lred"] if "lred" in P else P["lorange"], P["red"])
    for i in range(30):
        x, y = 80 + (i % 10) * 45, 205 + (i // 10) * 50
        s.rect(x, y, 38, 38, P["lorange"] if i != 17 else P["red"], P["red"], 1.5, 6)
    s.text(300, 395, "work grows with table size", 16, P["red"], "bold", "middle")
    s.card(650, 140, 500, 290, "Index: seek then read matches", P["lgreen"], P["green"])
    box(s, 830, 190, 140, 44, ["root"], "#FFFFFF", P["green"], 15)
    for i, t in enumerate(["1-12", "13-24", "25-36"]):
        box(s, 690 + i * 150, 270, 130, 44, [t], "#FFFFFF", P["green"], 15)
    s.line(900, 234, 765, 270, P["green"], 2); s.arrow(900, 234, 915, 268, P["green"], 2.5); s.line(900, 234, 1065, 270, P["green"], 2)
    box(s, 840, 350, 120, 40, ["row 17"], P["green"], P["green"], 15, "#FFFFFF")
    s.arrow(915, 316, 900, 348, P["green"], 2.5)
    s.text(900, 415, "work grows with matches, not table size", 16, P["green"], "bold", "middle")
    s.save(path)


ALL = [("00-module-banner", d00_banner), ("00-learning-roadmap", d00_roadmap), ("01-business-problem", d01_problem),
       ("01-sql-in-the-pipeline", d01_pipeline), ("01-xyz-schema", d01_schema), ("02-logical-order", d02_order),
       ("03-group-by", d03_group), ("04-join-types", d04_join_types), ("04-join-fan-out", d04_fan_out),
       ("05-cte-pipeline", d05_cte), ("06-window-vs-group-by", d06_window), ("07-raw-to-clean", d07_clean),
       ("08-star-schema", d08_star), ("08-scd-type-2", d08_scd), ("09-query-lifecycle", d09_lifecycle),
       ("09-index-vs-scan", d09_index)]
