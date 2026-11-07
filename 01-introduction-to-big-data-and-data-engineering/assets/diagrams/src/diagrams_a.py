"""Diagrams for topics 00-03: banner, roadmap, problem, big data, data engineering."""
import extras
from lib import S, P
from extras import wrap


def banner(out):
    s = S(1280, 340)
    s.rect(0, 0, 1280, 340, P["navy"], None, 0, 16)
    s.rect(0, 0, 14, 340, P["orange"], None, 0, 0)
    s.chip(60, 52, 150, 32, "MODULE 01", P["orange"], size=16)
    s.text(60, 140, "Introduction to Big Data", 50, "#FFFFFF", "bold")
    s.text(60, 200, "& Data Engineering", 50, "#FFFFFF", "bold")
    s.text(60, 252, "From a single machine to Hadoop, Spark and PySpark", 22, "#9FB4C2")
    s.text(60, 296, "Concepts  ·  Architecture  ·  Hands-on examples  ·  Interview prep", 17, "#6F8798")
    s.db(790, 120, 74, 92, P["lblue"])
    s.arrow(880, 166, 930, 166, P["orange"], 4)
    for i in range(3):
        s.server(944, 70 + i * 82, 120, 62)
        s.arrow(1070, 100 + i * 82, 1120, 150 + i * 10, P["orange"], 3)
    s.grid(1126, 126, 110, 80, 3, 4, P["blue"])
    s.text(827, 244, "DATA", 15, "#9FB4C2", "bold", "middle")
    s.text(1004, 318, "DISTRIBUTED PROCESSING", 15, "#9FB4C2", "bold", "middle")
    s.text(1181, 244, "INSIGHTS", 15, "#9FB4C2", "bold", "middle")
    s.save(out)


def repo_banner(out):
    s = S(1280, 280)
    s.rect(0, 0, 1280, 280, P["navy"], None, 0, 16)
    s.rect(0, 0, 14, 280, P["orange"], None, 0, 0)
    s.text(60, 120, "Data Engineering", 64, "#FFFFFF", "bold")
    s.text(60, 175, "A complete, hands-on learning resource", 26, "#9FB4C2")
    s.text(60, 225, "Concepts  ·  Architecture  ·  Code  ·  Interview prep", 18, "#6F8798")
    for i, (c, t) in enumerate([(P["blue"], "SQL"), (P["green"], "Python"), (P["orange"], "Spark"), (P["purple"], "Cloud")]):
        s.chip(820 + (i % 2) * 190, 80 + (i // 2) * 70, 170, 46, t, c, size=20)
    s.save(out)


def roadmap(out):
    s = S(1200, 640, "Module Roadmap", "Ten short topics. Each one builds on the one before.")
    items = [("01", "The Data Problem", "Why Excel and MySQL fail", P["blue"]),
             ("02", "What Is Big Data?", "The 5 Vs and data types", P["blue"]),
             ("03", "What Is Data Engineering?", "Role, pipelines, ETL vs ELT", P["blue"]),
             ("04", "Distributed Computing", "Scale out, partition, replicate", P["orange"]),
             ("05", "Hadoop & MapReduce", "HDFS, YARN, MapReduce", P["orange"]),
             ("06", "Apache Spark", "In-memory, DAG, lazy evaluation", P["orange"]),
             ("07", "PySpark", "Spark driven by Python", P["orange"]),
             ("08", "Evolution of Processing", "Timeline and comparison", P["green"]),
             ("09", "Modern Data Platforms", "Lakehouse and Databricks", P["green"]),
             ("10", "Review & Interview Prep", "Cheat sheet, scenarios", P["green"])]
    pos = []
    for i, (n, t, d, c) in enumerate(items):
        col, row = i % 5, i // 5
        x, y = 40 + col * 232, 140 + row * 220
        pos.append((x, y))
        s.rect(x, y, 208, 160, "#FFFFFF", c, 3, 14)
        s.rect(x, y, 208, 8, c, None, 0, 4)
        s.chip(x + 14, y + 22, 52, 28, n, c, size=15)
        for k, l in enumerate(wrap(t, 20)):
            s.text(x + 14, y + 78 + k * 20, l, 16, P["navy"], "bold")
        for k, l in enumerate(wrap(d, 26)):
            s.text(x + 14, y + 78 + len(wrap(t, 20)) * 20 + 4 + k * 17, l, 13, P["grey"])
    for i in range(9):
        if i == 4:
            s.line(40 + 4 * 232 + 104, 300, 40 + 4 * 232 + 104, 330, P["navy"], 3)
            s.line(40 + 4 * 232 + 104, 330, 144, 330, P["navy"], 3)
            s.arrow(144, 330, 144, 356, P["navy"], 3)
        else:
            x, y = pos[i]
            s.arrow(x + 210, y + 65, x + 228, y + 65, P["navy"], 3)
    for i, (c, t) in enumerate([(P["blue"], "Foundations"), (P["orange"], "The processing engines"), (P["green"], "Putting it together")]):
        s.rect(40 + i * 270, 600, 16, 16, c, None, 0, 4)
        s.text(64 + i * 270, 614, t, 15, P["navy"], "bold")
    s.save(out)


def oltp_olap(out):
    s = S(1200, 660, "Two Kinds of Database Work: OLTP vs OLAP", "Excel and MySQL were designed for the left side. Big data analytics lives on the right.")
    cards = [(40, "OLTP", "Run the business", P["blue"],
              [("Purpose", "Record transactions"), ("Typical query", "INSERT order #1001"), ("Rows touched", "A handful"),
               ("Speed goal", "Milliseconds"), ("Storage layout", "Row-oriented"), ("Examples", "MySQL, PostgreSQL")], dict(hl_row=1), "reads or writes one whole row"),
             (620, "OLAP", "Understand the business", P["orange"],
              [("Purpose", "Analyse history"), ("Typical query", "Revenue by region, 2 yrs"), ("Rows touched", "Millions to billions"),
               ("Speed goal", "Seconds to minutes"), ("Storage layout", "Column-oriented"), ("Examples", "Warehouses, Spark")], dict(hl_col=2), "reads only the columns it needs")]
    for x, name, sub, c, rows, hl, cap in cards:
        s.card(x, 120, 540, 410, f"{name}: {sub}", "#FFFFFF", c)
        for i, (a, b) in enumerate(rows):
            y = 200 + i * 38
            s.text(x + 24, y, a, 14, P["grey"], "bold")
            s.text(x + 170, y, b, 17, P["navy"], "bold")
            if i < 5: s.line(x + 24, y + 14, x + 516, y + 14, P["lgrey"], 1)
        s.table_icon(x + 24, 440, 150, 70, 4, 4, **hl)
        s.text(x + 195, 480, cap, 15, c, "bold")
    s.rect(40, 555, 1120, 70, P["navy"], None, 0, 14)
    s.text(600, 598, "100 GB a day of history to analyse is an OLAP problem at scale.", 21, "#FFFFFF", "bold", "middle")
    s.save(out)


def five_vs(out):
    s = S(1200, 660, "The 5 Vs of Big Data", "Data is 'big' when it is hard to handle on one machine because of one or more of these.")
    cards = [("Volume", "How much?", "100 GB a day, terabytes a year", P["blue"]),
             ("Velocity", "How fast?", "Card swipes, ride requests and clicks arrive every second", P["orange"]),
             ("Variety", "What forms?", "Tables, JSON, logs, images, video, text", P["green"]),
             ("Veracity", "How trustworthy?", "Duplicates, missing values, typos, bad sensors", P["red"]),
             ("Value", "Why bother?", "Insights that change decisions and revenue", P["purple"])]
    for i, (n, q, ex, c) in enumerate(cards):
        x = 40 + i * 227
        s.rect(x, 130, 212, 400, "#FFFFFF", c, 3, 16)
        s.rect(x, 130, 212, 96, c, None, 0, 16)
        s.rect(x, 180, 212, 46, c, None, 0, 0)
        s.text(x + 106, 200, "V", 56, "#FFFFFF", "bold", "middle")
        s.text(x + 106, 258, n, 24, c, "bold", "middle")
        s.text(x + 106, 284, q, 15, P["grey"], anchor="middle", italic=True)
        cx = x + 106
        if i == 0:
            for k in range(3): s.db(cx - 28 + k * 8, 312 + k * 8, 56, 64, P["lblue"])
        elif i == 1: s.gauge(cx, 372, 44, P["orange"])
        elif i == 2:
            s.table_icon(x + 30, 322, 44, 44, 3, 3); s.doc(cx - 14, 318, 36, 50); s.photo(x + 130, 326, 52, 40)
        elif i == 3:
            s.tick(cx - 36, 346, 14); s.cross(cx + 36, 346, 13)
            s.rect(cx - 12, 326, 24, 40, "none", None, 0, 0)
        else:
            s.circle(cx, 346, 34, P["lgold"], P["gold"], 4); s.text(cx, 360, "$", 40, P["gold"], "bold", "middle")
        for k, l in enumerate(wrap(ex, 22)):
            s.text(x + 106, 430 + k * 22, l, 16, P["navy"], anchor="middle")
    s.rect(40, 555, 1120, 70, P["lgold"], None, 0, 14)
    s.text(600, 586, "Volume, Velocity and Variety (the '3 Vs') were described by analyst Doug Laney in 2001.", 17, P["navy"], "bold", "middle")
    s.text(600, 610, "Veracity and Value were added later as the field matured.", 16, P["grey"], anchor="middle")
    s.save(out)


def data_types(out):
    s = S(1200, 620, "Three Shapes of Data", "The shape decides how you store it and how you query it.")
    cols = [("Structured", "Fixed columns, every row the same shape", P["blue"], ["Sales table", "Bank transactions", "Customer records"], "SQL works directly"),
            ("Semi-structured", "Has structure, but flexible and nested", P["green"], ["JSON events", "XML, logs", "API responses"], "Parse, then SQL / DataFrames"),
            ("Unstructured", "No predefined structure", P["orange"], ["Images, video, audio", "PDFs, emails", "Free text"], "Needs ML or text processing")]
    for i, (n, d, c, ex, how) in enumerate(cols):
        x = 40 + i * 380
        s.card(x, 120, 360, 420, n, "#FFFFFF", c)
        if i == 0:
            s.table_icon(x + 110, 180, 140, 90, 4, 3)
            for k, h in enumerate(["id", "item", "qty"]): s.text(x + 110 + k * 47 + 23, 202, h, 11, P["navy"], "bold", "middle")
        elif i == 1:
            s.rect(x + 70, 176, 220, 100, P["navy"], None, 0, 8)
            s.mono(x + 84, 202, [("{ ", "#FFFFFF"), ('"user"', "#7CD6A5"), (": 42,", "#FFFFFF")], 14)
            s.mono(x + 84, 226, [('  "event"', "#7CD6A5"), (': "click",', "#FFFFFF")], 14)
            s.mono(x + 84, 250, [('  "tags"', "#7CD6A5"), (': ["new"] }', "#FFFFFF")], 14)
        else:
            s.photo(x + 70, 190, 90, 66); s.doc(x + 190, 182, 64, 80)
        for k, l in enumerate(wrap(d, 34)):
            s.text(x + 180, 312 + k * 22, l, 16, P["grey"], anchor="middle")
        s.text(x + 24, 372, "Examples", 14, c, "bold")
        for k, e in enumerate(ex):
            s.circle(x + 32, 396 + k * 28 - 5, 4, c); s.text(x + 46, 396 + k * 28, e, 17, P["navy"])
        s.rect(x + 20, 486, 320, 38, P["lgrey"], None, 0, 10)
        s.text(x + 180, 511, how, 15, P["navy"], "bold", "middle")
    s.text(600, 580, "Big data platforms must handle all three, often in the same pipeline.", 19, P["navy"], "bold", "middle")
    s.save(out)


def scale_ladder(out):
    s = S(1200, 720, "The Data Scale Ladder", "A rough guide to where each class of tool starts to struggle.")
    units = [("KB", "an email"), ("MB", "a photo or song"), ("GB", "a feature film"), ("TB", "100,000s of photos"), ("PB", "1,000 TB: large platforms"), ("EB", "global internet services")]
    cols = [P["mid"], P["mid"], P["blue"], P["blue"], P["orange"], P["orange"]]
    for i, (u, e) in enumerate(units):
        x = 60 + i * 185; h = 70 + i * 48; y = 600 - h
        s.rect(x, y, 160, h, cols[i], None, 0, 10)
        s.text(x + 80, y + 42, u, 30, "#FFFFFF", "bold", "middle")
        s.text(x + 80, 632, e, 15, P["navy"], anchor="middle")
    s.rect(60, 128, 345, 34, P["green"], None, 0, 17); s.text(232, 151, "Spreadsheet: up to ~1M rows", 15, "#FFFFFF", "bold", "middle")
    s.rect(245, 172, 530, 34, P["blue"], None, 0, 17); s.text(510, 195, "Single-server database: MBs to low TBs", 15, "#FFFFFF", "bold", "middle")
    s.rect(615, 216, 545, 34, P["orange"], None, 0, 17); s.text(887, 239, "Distributed systems: TBs to PBs and beyond", 15, "#FFFFFF", "bold", "middle")
    s.text(600, 680, "Our scenario, 100 GB a day, is about 36 TB a year: firmly in distributed territory.", 19, P["navy"], "bold", "middle")
    s.save(out)


def industry(out):
    s = S(1200, 640, "Where Big Data Comes From: Five Everyday Scenarios", "Illustrative examples of the data a typical business produces and the engineering challenge it creates.")
    cards = [("Online retail", "Clicks, carts, orders, stock levels", "Peak-day traffic and real-time recommendations", P["blue"], "grid"),
             ("Ride-hailing", "GPS pings, ride requests, payments", "Match riders to drivers in seconds", P["orange"], "gauge"),
             ("Banking", "Card swipes, transfers, logins", "Spot fraud in milliseconds; audit everything", P["red"], "db"),
             ("Streaming media", "Plays, pauses, searches, ratings", "Personalise for millions of viewers", P["purple"], "photo"),
             ("Healthcare & IoT", "Sensor readings, device logs", "Continuous data under strict privacy rules", P["green"], "server")]
    for i, (n, d, ch, c, ic) in enumerate(cards):
        x = 40 + i * 227
        s.card(x, 140, 212, 420, n, "#FFFFFF", c, size=17)
        cx = x + 106
        if ic == "grid": s.table_icon(cx - 38, 205, 76, 60, 3, 3)
        elif ic == "gauge": s.gauge(cx, 262, 36, P["orange"])
        elif ic == "db": s.db(cx - 28, 196, 56, 70, P["lblue"])
        elif ic == "photo": s.photo(cx - 34, 208, 68, 54)
        else: s.server(cx - 40, 204, 80, 58)
        s.text(x + 18, 316, "DATA PRODUCED", 12, c, "bold")
        for k, l in enumerate(wrap(d, 22)): s.text(x + 18, 340 + k * 21, l, 16, P["navy"], "bold")
        s.text(x + 18, 420, "THE CHALLENGE", 12, c, "bold")
        for k, l in enumerate(wrap(ch, 22)): s.text(x + 18, 444 + k * 21, l, 16, P["navy"])
    s.text(600, 600, "Different industries, same problem: more data, arriving faster, in more shapes.", 19, P["navy"], "bold", "middle")
    s.save(out)


def de_role(out):
    s = S(1200, 640, "What a Data Engineer Does", "Builds and runs the data highway between raw sources and the people who use data.")
    s.text(40, 150, "SOURCES", 14, P["grey"], "bold")
    for i, t in enumerate(["Apps & websites", "Databases", "IoT sensors", "Logs & events", "SaaS tools"]):
        s.chip(40, 166 + i * 62, 190, 44, t, P["lgrey"], P["navy"], 16, P["mid"])
        s.arrow(234, 188 + i * 62, 300, 300, P["grey"], 2)
    s.rect(300, 130, 600, 330, P["lblue"], P["blue"], 3, 18)
    s.text(600, 166, "THE DATA ENGINEER BUILDS AND RUNS", 15, P["blue"], "bold", "middle")
    steps = [("Ingest", "collect"), ("Clean", "fix & validate"), ("Transform", "join & shape"), ("Store", "organise & secure")]
    for i, (a, b) in enumerate(steps):
        x = 322 + i * 144
        s.rect(x, 210, 124, 120, "#FFFFFF", P["blue"], 2.5, 12)
        s.badge(x + 62, 240, str(i + 1), P["blue"], 15)
        s.text(x + 62, 285, a, 18, P["navy"], "bold", "middle"); s.text(x + 62, 308, b, 13, P["grey"], anchor="middle")
        if i < 3: s.arrow(x + 126, 270, x + 142, 270, P["blue"], 3)
    s.rect(322, 360, 556, 80, "#FFFFFF", P["lgrey"], 1.5, 10)
    s.lines(600, 390, ["Reliable  ·  Scalable  ·  Automated  ·  Monitored", "Pipelines that run every day without anyone babysitting them"], 15, P["navy"], anchor="middle", lh=24)
    s.text(1000, 150, "CONSUMERS", 14, P["grey"], "bold")
    for i, t in enumerate(["Data analysts", "Data scientists", "Dashboards", "ML models"]):
        s.chip(970, 166 + i * 62, 190, 44, t, P["lgrey"], P["navy"], 16, P["mid"])
        s.arrow(900, 300, 966, 188 + i * 62, P["grey"], 2)
    s.rect(40, 500, 1120, 110, P["navy"], None, 0, 14)
    s.text(70, 540, "Without data engineering:", 18, "#FF9E8E", "bold")
    s.text(70, 566, "data is scattered, late, duplicated and untrusted.", 17, "#FFFFFF")
    s.text(640, 540, "With data engineering:", 18, "#7CD6A5", "bold")
    s.text(640, 566, "data is reliable, available and fast, so others can do their jobs.", 17, "#FFFFFF")
    s.save(out)


def roles(out):
    s = S(1200, 600, "Data Engineer vs Analyst vs Scientist vs ML Engineer", "Overlapping skills, different questions.")
    data = [("Data Engineer", P["orange"], "Can everyone get reliable data?", "Pipelines, storage, quality, scale", "SQL, Python, Spark, Airflow, Kafka", "Trusted, ready-to-use data"),
            ("Data Analyst", P["blue"], "What happened, and why?", "Reporting, dashboards, SQL analysis", "SQL, BI tools, Excel", "Reports and insights"),
            ("Data Scientist", P["purple"], "What will happen? What should we do?", "Statistics, modelling, experiments", "Python, notebooks, ML libraries", "Models and predictions"),
            ("ML Engineer", P["green"], "How do we run models in production?", "Deploy, monitor and scale models", "ML frameworks, MLOps, APIs", "Production ML systems")]
    labels = ["Core question", "Focus", "Typical tools", "Delivers"]
    for i, (n, c, *vals) in enumerate(data):
        x = 40 + i * 283
        s.card(x, 120, 270, 440, n, "#FFFFFF", c)
        for r, v in enumerate(vals):
            y = 188 + r * 94
            s.text(x + 18, y, labels[r].upper(), 12, c, "bold")
            for k, l in enumerate(wrap(v, 27)): s.text(x + 18, y + 26 + k * 22, l, 17, P["navy"], "bold" if r == 0 else "normal")
    s.save(out)


def lifecycle(out):
    s = S(1200, 640, "The Data Pipeline Lifecycle", "Every pipeline, from a tiny script to a huge platform, follows the same five stages.")
    st = [("Ingest", "Collect data from sources", "Kafka, CDC, file drops", P["blue"]), ("Store", "Keep it safe and cheap", "Object storage, Delta", P["green"]),
          ("Process", "Clean, join, aggregate", "Spark, SQL, dbt", P["orange"]), ("Serve", "Make it fast to query", "SQL warehouse, gold tables", P["purple"]),
          ("Consume", "Put it to use", "Dashboards, ML, apps", P["red"])]
    for i, (n, d, ex, c) in enumerate(st):
        x = 40 + i * 228
        s.rect(x, 130, 208, 250, "#FFFFFF", c, 3, 14)
        s.rect(x, 130, 208, 56, c, None, 0, 14); s.rect(x, 160, 208, 26, c, None, 0, 0)
        s.badge(x + 32, 158, str(i + 1), "#FFFFFF", 15); s.text(x + 32, 164, str(i + 1), 16, c, "bold", "middle")
        s.text(x + 118, 166, n, 24, "#FFFFFF", "bold", "middle")
        for k, l in enumerate(wrap(d, 20)): s.text(x + 104, 226 + k * 22, l, 17, P["navy"], "bold", "middle")
        s.text(x + 104, 306, "EXAMPLES", 11, c, "bold", "middle")
        for k, l in enumerate(wrap(ex, 22)): s.text(x + 104, 328 + k * 20, l, 15, P["grey"], anchor="middle")
        if i < 4: s.arrow(x + 210, 255, x + 226, 255, P["navy"], 3)
    bars = [("Orchestration: runs the steps in the right order, on schedule, with retries", P["navy"]),
            ("Data quality & monitoring: catches bad data and broken jobs early", P["grey"]),
            ("Security & governance: who can see what, and where data came from", P["mid"])]
    for i, (t, c) in enumerate(bars):
        s.rect(40, 410 + i * 60, 1120, 46, c, None, 0, 12)
        s.text(600, 440 + i * 60, t, 17, "#FFFFFF", "bold", "middle")
    s.save(out)


def etl_elt(out):
    s = S(1200, 700, "ETL vs ELT", "The same three steps, in a different order.")
    lanes = [("ETL: Extract → Transform → Load", P["blue"], ["Sources", "Extract", "Transform\n(separate server)", "Load", "Data warehouse"], 2, 170),
             ("ELT: Extract → Load → Transform", P["orange"], ["Sources", "Extract", "Load\n(raw, as-is)", "Raw data in\nlake / warehouse", "Transform\n(inside, at scale)"], 4, 390)]
    for t, c, boxes, hi, y in lanes:
        s.text(40, y - 12, t, 21, c, "bold")
        for i, b in enumerate(boxes):
            x = 40 + i * 235
            on = i == hi
            s.rect(x, y, 190, 100, c if on else "#FFFFFF", c, 3, 14)
            for k, l in enumerate(b.split("\n")):
                s.text(x + 95, y + (54 if "\n" not in b else 44) + k * 22, l, 17, "#FFFFFF" if on else P["navy"], "bold", "middle")
            if i < 4: s.arrow(x + 192, y + 50, x + 233, y + 50, c, 3)
    s.text(40, 310, "Data is reshaped BEFORE it is stored.", 17, P["blue"], "bold")
    s.text(40, 530, "Data is stored first, reshaped AFTER, using the platform's own compute.", 17, P["orange"], "bold")
    s.rect(40, 566, 1120, 112, P["lgold"], None, 0, 14)
    s.text(70, 602, "Why ELT became popular in the cloud", 18, P["navy"], "bold")
    s.text(70, 630, "Cheap storage + scalable compute + the raw data is kept, so you can re-run or change the logic later.", 16, P["navy"])
    s.text(70, 654, "ETL is still common where data must be cleaned or masked before it lands, or for small, stable systems.", 16, P["grey"])
    s.save(out)


def batch_stream(out):
    s = S(1200, 640, "Batch vs Streaming", "When do you process the data: in chunks on a schedule, or continuously as it arrives?")
    s.card(40, 120, 1120, 215, "Batch: collect first, process later", "#FFFFFF", P["blue"], size=17)
    for i in range(3):
        x = 70 + i * 300
        s.rect(x, 180, 200, 80, P["lblue"], P["blue"], 2, 10)
        for k in range(14): s.circle(x + 18 + (k % 7) * 27, 202 + (k // 7) * 30, 6, P["blue"])
        s.text(x + 100, 282, f"{i}:00 – {i+1}:00", 14, P["grey"], "bold", "middle")
        s.arrow(x + 204, 220, x + 236, 220, P["navy"], 3)
        s.chip(x + 240, 206, 56, 28, "job", P["blue"], size=14)
    s.text(700, 312, "Latency: minutes to hours.  Example: the nightly sales report.", 16, P["navy"], "bold", "middle")
    s.card(40, 355, 1120, 215, "Streaming: process each event as it arrives", "#FFFFFF", P["orange"], size=17)
    s.rect(70, 435, 1060, 60, P["lorange"], P["orange"], 2, 30)
    for k in range(18): s.circle(90 + k * 28, 465, 7, P["orange"])
    s.rect(700, 425, 150, 80, P["orange"], None, 0, 12); s.text(775, 470, "process", 17, "#FFFFFF", "bold", "middle")
    for k in range(5): s.arrow(860 + k * 54, 465, 905 + k * 54, 465, P["navy"], 2.5)
    s.text(600, 548, "Latency: milliseconds to seconds.  Example: card-fraud detection.", 16, P["navy"], "bold", "middle")
    s.rect(40, 585, 1120, 40, P["navy"], None, 0, 12)
    s.text(600, 612, "Many platforms use both: streaming for what is urgent, batch for what is big.", 17, "#FFFFFF", "bold", "middle")
    s.save(out)


ALL = [("00-module-banner", banner), ("00-learning-roadmap", roadmap), ("01-oltp-vs-olap", oltp_olap),
       ("02-five-vs-of-big-data", five_vs), ("02-data-types", data_types), ("02-data-scale-ladder", scale_ladder),
       ("02-real-world-scenarios", industry), ("03-data-engineer-role", de_role), ("03-role-comparison", roles),
       ("03-pipeline-lifecycle", lifecycle), ("03-etl-vs-elt", etl_elt), ("03-batch-vs-streaming", batch_stream)]
