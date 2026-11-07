from lib import S, P


def d13_platform_layers(out):
    s = S(1200, 780, "The Databricks Platform: One Platform, Every Workload", "Read it from the bottom up: data first, then governance, then the engine, then what you do with it.")
    tiles = [("Business\nIntelligence", P["purple"]), ("Data\nWarehousing", P["blue"]), ("AI &\nData Science", P["orange"]),
             ("ETL & Real-Time\nAnalytics", P["green"]), ("Orchestration", P["gold"])]
    s.text(40, 150, "WHAT YOU DO", 14, P["grey"], "bold")
    for i, (t, c) in enumerate(tiles):
        x = 40 + i * 226
        s.rect(x, 162, 206, 100, c, None, 0, 14)
        a = t.split("\n")
        s.lines(x + 103, 208 if len(a) > 1 else 218, a, 19, "#FFFFFF", "bold", "middle", lh=25)
    s.rect(40, 282, 1120, 92, P["navy"], None, 0, 14)
    s.text(600, 322, "Data Intelligence Engine", 24, "#FFFFFF", "bold", "middle")
    s.text(600, 352, "the compute that runs your code: Spark + Photon, serverless or clusters", 16, "#C8D6E0", anchor="middle")
    s.rect(40, 394, 1120, 84, P["red"], None, 0, 14)
    s.text(600, 432, "Unified Governance  ·  Unity Catalog", 24, "#FFFFFF", "bold", "middle")
    s.text(600, 460, "who can see what · where data came from · auditing · discovery", 16, "#FFE0DA", anchor="middle")
    s.rect(40, 498, 1120, 84, P["orange"], None, 0, 14)
    s.text(600, 536, "Unified Data  ·  Delta Lake", 24, "#FFFFFF", "bold", "middle")
    s.text(600, 564, "structured + semi-structured + unstructured data, all in one place", 16, "#FFF1EE", anchor="middle")
    s.rect(40, 602, 1120, 84, P["lblue"], P["blue"], 2.5, 14, "10 6")
    s.text(600, 640, "Open Data Lake", 24, P["navy"], "bold", "middle")
    s.text(600, 668, "cheap cloud storage (S3, ADLS, GCS) in open formats (Parquet, Delta)", 16, P["grey"], anchor="middle")
    s.rect(40, 706, 1120, 50, P["lgold"], None, 0, 12)
    s.text(600, 738, "Unified = one platform for every role.   Open = open formats, no lock-in.   At scale = GBs to PBs.", 17, P["navy"], "bold", "middle")
    s.save(out)


def d14_lakehouse(out):
    s = S(1200, 600, "Lakehouse = Data Warehouse + Data Lake", "The best of both worlds on one platform.")
    s.card(40, 130, 330, 340, "Data Warehouse", "#FFFFFF", P["blue"])
    s.warehouse(165, 180, 80, 64)
    for i, (ok, t) in enumerate([(1, "Reliable, fast SQL"), (0, "Expensive"), (0, "Structured data only"), (0, "Weak for ML")]):
        (s.tick if ok else s.cross)(70, 292 + i * 44, 9)
        s.text(94, 298 + i * 44, t, 17)
    s.text(405, 305, "+", 56, P["navy"], "bold", "middle")
    s.card(440, 130, 330, 340, "Data Lake", "#FFFFFF", P["green"])
    s.cloud(565, 180, 80, 60, P["lgreen"])
    for i, (ok, t) in enumerate([(1, "Cheap storage"), (1, "Any kind of data"), (1, "Good for ML"), (0, "No reliability (ACID)")]):
        (s.tick if ok else s.cross)(470, 292 + i * 44, 9)
        s.text(494, 298 + i * 44, t, 17)
    s.text(805, 305, "=", 56, P["navy"], "bold", "middle")
    s.card(840, 130, 320, 340, "LAKEHOUSE", "#FFFFFF", P["orange"])
    s.cloud(960, 180, 80, 60, P["lorange"])
    for i, t in enumerate(["Cheap, open storage", "Any kind of data", "Reliable (ACID) + fast SQL", "Great for ML and AI"]):
        s.tick(870, 292 + i * 44, 9)
        s.text(894, 298 + i * 44, t, 17, P["navy"], "bold")
    s.rect(40, 495, 1120, 70, P["navy"], None, 0, 14)
    s.text(600, 538, "Databricks is a lakehouse platform: Delta Lake adds the warehouse-style reliability on top of the lake.", 19, "#FFFFFF", "bold", "middle")
    s.save(out)


def d15_planes(out):
    s = S(1200, 720, "How Databricks Is Built: Control Plane and Compute Plane", "Where things run, in plain language.")
    s.person(60, 330, 60); s.text(90, 420, "You", 19, P["navy"], "bold", "middle")
    s.text(90, 442, "(browser)", 15, P["grey"], anchor="middle")
    s.rect(220, 120, 360, 520, P["lorange"], P["orange"], 3, 16)
    s.text(400, 156, "CONTROL PLANE", 22, P["orange"], "bold", "middle")
    s.text(400, 180, "managed by Databricks", 15, P["grey"], anchor="middle")
    for i, t in enumerate(["Web app / workspace UI", "Notebooks and Jobs scheduler", "Cluster manager", "Unity Catalog (metadata)"]):
        s.rect(250, 205 + i * 90, 300, 66, "#FFFFFF", P["orange"], 2, 10)
        s.text(400, 245 + i * 90, t, 17, P["navy"], "bold", "middle")
    s.arrow(130, 360, 214, 360, P["navy"], 3)
    s.rect(680, 120, 480, 340, P["lblue"], P["blue"], 3, 16)
    s.text(920, 156, "COMPUTE PLANE", 22, P["blue"], "bold", "middle")
    s.text(920, 180, "where your code actually runs", 15, P["grey"], anchor="middle")
    s.server(715, 210, 90, 60); s.text(760, 292, "Driver", 15, P["navy"], "bold", "middle")
    for i in range(3):
        s.server(830 + i * 105, 210, 90, 60); s.text(875 + i * 105, 292, f"Worker {i+1}", 15, P["navy"], "bold", "middle")
    s.text(920, 345, "Clusters / serverless compute", 17, P["navy"], "bold", "middle")
    s.rect(700, 375, 440, 62, "#FFFFFF", P["blue"], 1.5, 10)
    s.lines(920, 400, ["Classic: runs in YOUR cloud account", "Serverless: runs in Databricks' account (managed for you)"], 14, P["navy"], anchor="middle", lh=22)
    s.arrow(584, 330, 676, 330, P["orange"], 3)
    s.text(630, 318, "launch &", 13, P["orange"], "bold", "middle"); s.text(630, 352, "manage", 13, P["orange"], "bold", "middle")
    s.rect(680, 500, 480, 140, P["lgreen"], P["green"], 3, 16)
    s.text(920, 536, "YOUR CLOUD STORAGE", 20, P["green"], "bold", "middle")
    s.db(715, 560, 46, 56, P["lgreen"], P["navy"]); s.db(775, 560, 46, 56, P["lgreen"], P["navy"])
    s.lines(960, 578, ["S3 / ADLS / GCS", "your data stays here", "in open formats"], 15, P["navy"], anchor="middle", lh=22)
    s.arrow(920, 462, 920, 496, P["green"], 3); s.arrow(900, 496, 900, 466, P["green"], 3)
    s.text(1000, 484, "read / write", 14, P["green"], "bold")
    s.rect(40, 660, 1120, 44, P["navy"], None, 0, 12)
    s.text(600, 689, "Databricks runs the platform. Your data stays in your cloud storage.", 19, "#FFFFFF", "bold", "middle")
    s.save(out)


def d16_unity_catalog(out):
    s = S(1200, 640, "Unity Catalog: The Three-Level Namespace", "Everything has a full name:  catalog . schema . object")
    s.rect(40, 130, 250, 80, P["navy"], None, 0, 12)
    s.text(165, 165, "Metastore", 21, "#FFFFFF", "bold", "middle"); s.text(165, 190, "one per region", 14, "#C8D6E0", anchor="middle")
    s.rect(350, 130, 250, 80, P["red"], None, 0, 12)
    s.text(475, 165, "Catalog", 21, "#FFFFFF", "bold", "middle"); s.text(475, 190, "e.g. prod, dev, workspace", 14, "#FFE0DA", anchor="middle")
    s.rect(660, 130, 250, 80, P["orange"], None, 0, 12)
    s.text(785, 165, "Schema", 21, "#FFFFFF", "bold", "middle"); s.text(785, 190, "e.g. sales, finance", 14, "#FFF1EE", anchor="middle")
    s.arrow(294, 170, 346, 170, P["navy"], 3); s.arrow(604, 170, 656, 170, P["navy"], 3)
    objs = [("Table", P["blue"]), ("View", P["purple"]), ("Volume", P["green"]), ("Function", P["gold"]), ("ML Model", P["grey"])]
    s.text(960, 160, "level 3 · objects", 14, P["grey"], "bold")
    for i, (t, c) in enumerate(objs):
        s.chip(940, 172 + i * 44 - 0, 220, 34, t, c, size=16)
    s.arrow(914, 170, 936, 190, P["navy"], 3)
    s.rect(40, 260, 880, 150, "#FFFFFF", P["lgrey"], 2, 14)
    s.text(70, 296, "Example: a table called orders", 17, P["grey"], "bold")
    x0, cw, fs = 70, 16.8, 28
    mono = "'DejaVu Sans Mono', 'Courier New', monospace"
    s.add(f'<text x="{x0}" y="352" font-family="{mono}" font-size="{fs}" font-weight="bold" fill="{P["navy"]}" xml:space="preserve">'
          f'SELECT * FROM <tspan fill="{P["red"]}">prod</tspan>.<tspan fill="{P["orange"]}">sales</tspan>.<tspan fill="{P["blue"]}">orders</tspan>;</text>')
    base = x0 + 14 * cw
    s.text(base + 2 * cw, 386, "catalog", 15, P["red"], "bold", "middle")
    s.text(base + 5 * cw + 2.5 * cw, 386, "schema", 15, P["orange"], "bold", "middle")
    s.text(base + 11 * cw + 3 * cw, 386, "table", 15, P["blue"], "bold", "middle")
    s.rect(40, 440, 1120, 150, P["lgold"], None, 0, 14)
    s.text(70, 478, "What Unity Catalog gives you", 19, P["navy"], "bold")
    for i, t in enumerate(["Access control: who can read or write what", "Lineage: where did this data come from?",
                           "Auditing: who accessed it and when", "Discovery: search and document all your data"]):
        s.tick(80 + (i % 2) * 540, 515 + (i // 2) * 40, 8)
        s.text(100 + (i % 2) * 540, 521 + (i // 2) * 40, t, 17)
    s.save(out)


def d17_delta(out):
    s = S(1200, 600, "Delta Lake: Parquet Files + a Transaction Log", "A Delta table is just a folder. The _delta_log makes it reliable.")
    s.card(40, 130, 480, 250, "Plain Parquet files", "#FFFFFF", P["grey"])
    for i in range(4):
        s.rect(70 + (i % 2) * 210, 190 + (i // 2) * 80, 190, 56, P["lgrey"], P["grey"], 2, 8)
        s.text(165 + (i % 2) * 210, 224 + (i // 2) * 80, f"part-0000{i}.parquet", 15, P["navy"], anchor="middle")
    s.text(280, 365, "Just files. No guarantees.", 16, P["grey"], "bold", "middle")
    s.text(560, 262, "+", 50, P["navy"], "bold", "middle")
    s.card(600, 130, 560, 250, "Delta table (a folder)", "#FFFFFF", P["orange"])
    for i in range(2):
        s.rect(625, 190 + i * 66, 210, 52, P["lgrey"], P["grey"], 2, 8)
        s.text(730, 222 + i * 66, f"part-0000{i}.parquet", 15, P["navy"], anchor="middle")
    s.rect(860, 190, 275, 168, P["lorange"], P["orange"], 2.5, 10)
    s.text(997, 218, "_delta_log/", 18, P["orange"], "bold", "middle")
    for i, t in enumerate(["000.json  create table", "001.json  add files", "002.json  update rows"]):
        s.text(880, 252 + i * 30, t, 15, P["navy"])
    s.text(997, 345, "every change = a new version", 14, P["grey"], "bold", "middle")
    s.text(40, 430, "What the log gives you", 20, P["navy"], "bold")
    feats = [("ACID transactions", ["a failed write never leaves", "half-written data"], P["green"]),
             ("Time travel", ["query or restore an", "older version"], P["blue"]),
             ("Schema enforcement", ["bad data is rejected", "before it gets in"], P["purple"]),
             ("MERGE / UPDATE / DELETE", ["change rows in a", "data lake"], P["orange"])]
    for i, (h, ls, c) in enumerate(feats):
        x = 40 + i * 282
        s.rect(x, 450, 262, 120, "#FFFFFF", c, 2.5, 12)
        s.rect(x, 450, 262, 8, c, None, 0, 4)
        s.text(x + 131, 495, h, 17, c, "bold", "middle")
        s.lines(x + 131, 525, ls, 14, P["navy"], anchor="middle", lh=20)
    s.save(out)


def d18_medallion(out):
    s = S(1200, 560, "Medallion Architecture: Bronze → Silver → Gold", "The standard way to organise data in a lakehouse. Quality improves at every step.")
    s.rect(40, 200, 150, 170, "#FFFFFF", P["grey"], 2, 14)
    s.text(115, 236, "Sources", 19, P["navy"], "bold", "middle")
    s.lines(115, 270, ["files", "databases", "apps", "streams"], 15, P["grey"], anchor="middle", lh=24)
    layers = [("BRONZE", "#B9772F", "#F6E7D5", "Raw data, exactly as received", ["Never modify it", "Add load time and source"]),
              ("SILVER", "#7C8A96", "#E9EDF0", "Cleaned and validated", ["Remove duplicates", "Fix types, join, check quality"]),
              ("GOLD", P["gold"], P["lgold"], "Business-ready aggregates", ["Small, fast tables", "Built for dashboards and ML"])]
    for i, (n, c, lc, d, ls) in enumerate(layers):
        x = 250 + i * 290
        s.rect(x, 150, 250, 270, lc, c, 3, 16)
        s.rect(x, 150, 250, 50, c, None, 0, 16)
        s.rect(x, 180, 250, 20, c, None, 0, 0)
        s.text(x + 125, 184, n, 22, "#FFFFFF", "bold", "middle")
        s.text(x + 125, 240, d, 15, P["navy"], "bold", "middle")
        s.lines(x + 125, 285, ls, 15, P["navy"], anchor="middle", lh=24)
        s.db(x + 100, 330, 50, 66, "#FFFFFF", c)
        s.arrow(x - 56 if i == 0 else x - 38, 285, x - 4, 285, P["navy"], 3)
    s.text(600, 470, "Each layer is a set of Delta tables.   Re-running a job must not create duplicates (idempotent).", 17, P["navy"], "bold", "middle")
    s.rect(40, 495, 1120, 44, P["navy"], None, 0, 12)
    s.text(600, 524, "Bronze = trust nothing   ·   Silver = trust it   ·   Gold = use it", 19, "#FFFFFF", "bold", "middle")
    s.save(out)


def d19_compute(out):
    s = S(1200, 560, "Compute: Serverless vs Classic Clusters", "Compute = the machines that run your code.")
    s.card(40, 130, 540, 330, "Serverless compute", "#FFFFFF", P["orange"])
    s.cloud(70, 190, 110, 66, P["lorange"])
    s.text(200, 220, "Databricks manages it", 20, P["orange"], "bold")
    s.text(200, 246, "Nothing to configure.", 16, P["grey"])
    for i, t in enumerate(["Starts in seconds", "Scales automatically", "No cluster sizing or upgrades", "Default for Free Edition and most new work"]):
        s.tick(80, 305 + i * 38, 9); s.text(104, 311 + i * 38, t, 17)
    s.card(620, 130, 540, 330, "Classic cluster", "#FFFFFF", P["blue"])
    s.server(650, 195, 80, 54)
    for i in range(3): s.server(750 + i * 62, 205, 52, 36)
    s.text(940, 288, "1 driver + N workers", 15, P["grey"], "bold", "middle")
    for i, t in enumerate(["You choose machine size and runtime", "Full control: libraries, Spark settings", "Set auto-termination to save cost", "Use when you need custom control"]):
        s.tick(660, 330 + i * 32, 9); s.text(684, 336 + i * 32, t, 17)
    s.rect(40, 485, 1120, 50, P["navy"], None, 0, 12)
    s.text(600, 517, "Rule of thumb: start serverless. Choose a classic cluster only when you need control.", 19, "#FFFFFF", "bold", "middle")
    s.save(out)


def d20_who(out):
    s = S(1200, 600, "Who Can Use Databricks?", "One platform, many roles.")
    s.rect(480, 285, 240, 110, P["orange"], None, 0, 20)
    s.text(600, 336, "Databricks", 30, "#FFFFFF", "bold", "middle")
    s.text(600, 366, "one shared platform", 16, "#FFF1EE", anchor="middle")
    roles = [(40, 125, "Data Analyst", "Writes SQL, builds dashboards", P["blue"], (440, 185, 500, 285)),
             (760, 125, "Data Scientist", "Builds ML models in notebooks", P["purple"], (760, 185, 700, 285)),
             (40, 440, "Data Engineer", "Builds ETL pipelines, Delta tables, jobs", P["green"], (440, 500, 500, 395)),
             (760, 440, "Business Analyst", "Reads dashboards and reports", P["gold"], (760, 500, 700, 395))]
    for x, y, n, d, c, (x1, y1, x2, y2) in roles:
        s.line(x1, y1, x2, y2, c, 4)
        s.rect(x, y, 400, 120, "#FFFFFF", c, 3, 16)
        s.person(x + 24, y + 30, 56, c)
        s.text(x + 104, y + 62, n, 24, c, "bold")
        s.text(x + 104, y + 92, d, 15, P["navy"])
    s.save(out)


def d21_mock_notebook(out):
    s = S(1200, 760)
    s.rect(30, 20, 1140, 720, "#FFFFFF", P["lgrey"], 2, 14)
    s.rect(30, 20, 1140, 50, "#F1F3F5", P["lgrey"], 2, 14)
    s.text(60, 52, "workspace  /  Users  /  you  /  01_platform_tour", 16, P["grey"])
    s.chip(860, 30, 150, 30, "Serverless", P["green"], size=14)
    s.chip(1030, 30, 120, 30, "Run all", P["orange"], size=14)
    s.rect(30, 70, 190, 670, "#F7F8F9", P["lgrey"], 1, 0)
    for i, t in enumerate(["Workspace", "Catalog", "Compute", "Jobs & Pipelines", "SQL Editor", "Dashboards"]):
        s.rect(46, 92 + i * 52, 158, 38, P["lorange"] if i == 0 else "#F7F8F9", None, 0, 8)
        s.text(60, 117 + i * 52, t, 16, P["orange"] if i == 0 else P["navy"], "bold" if i == 0 else "normal")
    s.rect(250, 90, 890, 90, "#FFFFFF", P["lgrey"], 2, 8)
    s.text(270, 122, "Markdown cell", 12, P["grey"], "bold")
    s.text(270, 152, "Platform Tour", 26, P["navy"], "bold")
    s.rect(250, 200, 890, 120, "#FFFFFF", P["lgrey"], 2, 8)
    s.rect(250, 200, 36, 120, "#F1F3F5", None, 0, 8)
    s.path("M262,214 L262,232 L278,223 Z", P["green"])
    s.text(300, 230, "Python cell", 12, P["grey"], "bold")
    s.text(300, 266, "df = spark.range(10)", 20, P["navy"])
    s.text(300, 298, "display(df)", 20, P["navy"])
    s.rect(250, 340, 890, 230, "#FFFFFF", P["lgrey"], 2, 8)
    s.text(270, 366, "Output", 12, P["grey"], "bold")
    s.rect(270, 380, 300, 36, "#F1F3F5", P["lgrey"], 1, 0)
    s.text(285, 404, "id", 15, P["navy"], "bold")
    for i in range(5):
        s.rect(270, 416 + i * 28, 300, 28, "#FFFFFF", P["lgrey"], 1, 0)
        s.text(285, 436 + i * 28, str(i), 15, P["navy"])
    s.text(600, 404, "← result of display(df)", 15, P["orange"], "bold")
    s.text(600, 440, "Each cell runs on its own.", 15, P["grey"])
    s.text(600, 462, "Results appear right below.", 15, P["grey"])
    s.rect(250, 590, 890, 120, "#FFFFFF", P["lgrey"], 2, 8)
    s.text(270, 622, "SQL cell", 12, P["grey"], "bold")
    s.text(270, 660, "%sql", 20, P["purple"], "bold")
    s.text(270, 692, "SELECT current_catalog(), current_schema()", 20, P["navy"])
    s.text(600, 735, "Illustration: your workspace will look slightly different.", 14, P["grey"], anchor="middle", italic=True)
    s.save(out)


def d22_mock_catalog(out):
    s = S(1200, 700)
    s.rect(30, 20, 1140, 660, "#FFFFFF", P["lgrey"], 2, 14)
    s.rect(30, 20, 1140, 50, "#F1F3F5", P["lgrey"], 2, 14)
    s.text(60, 52, "Catalog Explorer", 18, P["navy"], "bold")
    s.rect(30, 70, 340, 610, "#F7F8F9", P["lgrey"], 1, 0)
    tree = [(0, "workspace", "catalog", P["red"]), (1, "default", "schema", P["orange"]), (2, "Tables", "", P["grey"]),
            (2, "course_data", "volume", P["green"]), (1, "course", "schema", P["orange"]), (2, "silver_sales", "table", P["blue"]),
            (2, "gold_daily_sales", "table", P["blue"]), (0, "samples", "catalog", P["red"]), (0, "system", "catalog", P["red"])]
    for i, (lv, n, k, c) in enumerate(tree):
        y = 110 + i * 46
        sel = n == "course_data"
        if sel: s.rect(40, y - 24, 320, 38, P["lgreen"], None, 0, 8)
        s.rect(60 + lv * 28, y - 12, 14, 14, c, None, 0, 3)
        s.text(84 + lv * 28, y + 2, n, 16, P["navy"], "bold" if sel else "normal")
        if k: s.text(350, y + 2, k, 12, P["grey"], anchor="end")
    s.text(400, 112, "workspace.default.course_data", 22, P["navy"], "bold")
    s.chip(400, 126, 80, 26, "Volume", P["green"], size=13)
    s.text(500, 145, "a governed folder for files", 15, P["grey"])
    s.rect(400, 175, 740, 40, "#F1F3F5", P["lgrey"], 1, 0)
    for x, t in [(420, "Name"), (800, "Size"), (960, "Last modified")]: s.text(x, 201, t, 15, P["navy"], "bold")
    rows = [("sales.csv", "102 KB"), ("customers.csv", "14 KB"), ("products.csv", "639 B"), ("events.json", "79 KB")]
    for i, (n, z) in enumerate(rows):
        y = 215 + i * 44
        s.rect(400, y, 740, 44, "#FFFFFF", P["lgrey"], 1, 0)
        s.text(420, y + 28, n, 16, P["navy"]); s.text(800, y + 28, z, 16, P["grey"]); s.text(960, y + 28, "today", 16, P["grey"])
    s.chip(960, 420, 180, 36, "Upload to this volume", P["orange"], size=14)
    s.rect(400, 490, 740, 150, P["lgold"], None, 0, 12)
    s.text(420, 524, "Files in a volume have a path:", 16, P["navy"], "bold")
    s.text(420, 560, "/Volumes/workspace/default/course_data/sales.csv", 17, P["blue"], "bold")
    s.text(420, 600, "catalog / schema / volume / file", 15, P["grey"])
    s.text(600, 668, "Illustration: your workspace will look slightly different.", 14, P["grey"], anchor="middle", italic=True)
    s.save(out)


ALL = [("13-platform-layers", d13_platform_layers), ("14-lakehouse", d14_lakehouse), ("15-control-compute-plane", d15_planes),
       ("16-unity-catalog", d16_unity_catalog), ("17-delta-lake", d17_delta), ("18-medallion", d18_medallion),
       ("19-compute-options", d19_compute), ("20-who-uses-databricks", d20_who),
       ("21-example-notebook", d21_mock_notebook), ("22-example-catalog-explorer", d22_mock_catalog)]
