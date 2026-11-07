"""Generates the SVG diagrams used in the repository (consistent style)."""
from xml.sax.saxutils import escape
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "diagrams")
NAVY, BLUE, LIGHT, ORANGE, GREEN, GRAY, RED, PURPLE = (
    "#0B3C5D", "#1D70B8", "#E8F1FA", "#F28C28", "#2E8B57", "#5B6770", "#C0392B", "#6C4AB6")
BRONZE, SILVER, GOLD = "#CD7F32", "#9AA5B1", "#D4A017"
FONT = "Helvetica, Arial, sans-serif"


class Svg:
    def __init__(self, w, h, title):
        self.w, self.h, self.parts = w, h, []
        self.title = title
        self.defs = (
            '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{GRAY}"/></marker></defs>')

    def rect(self, x, y, w, h, fill=LIGHT, stroke=BLUE, rx=10, sw=1.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def text(self, x, y, s, size=14, fill=NAVY, weight="normal", anchor="middle"):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>')

    def box(self, x, y, w, h, lines, fill=LIGHT, stroke=BLUE, tfill=NAVY, size=14, bold_first=True, dash=None):
        self.rect(x, y, w, h, fill, stroke, dash=dash)
        n = len(lines)
        lh = size + 5
        y0 = y + h / 2 - (n - 1) * lh / 2 + size * 0.35
        for i, l in enumerate(lines):
            self.text(x + w / 2, y0 + i * lh, l, size if i else size, tfill,
                      "bold" if (i == 0 and bold_first) else "normal")

    def arrow(self, x1, y1, x2, y2, label=None, color=GRAY, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2"{d} marker-end="url(#arr)"/>')
        if label:
            self.text((x1 + x2) / 2, (y1 + y2) / 2 - 6, label, 12, GRAY)

    def title_bar(self, s):
        self.text(self.w / 2, 34, s, 20, NAVY, "bold")

    def save(self, name):
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" role="img" aria-label="{escape(self.title)}">'
               f'<title>{escape(self.title)}</title>{self.defs}<rect width="{self.w}" height="{self.h}" fill="#FFFFFF"/>' + "".join(self.parts) + "</svg>")
        with open(os.path.join(OUT, name), "w") as f:
            f.write(svg)


# 1 ─ Scaling --------------------------------------------------------------
s = Svg(900, 420, "Vertical versus horizontal scaling")
s.title_bar("Scaling up vs scaling out")
s.rect(30, 60, 410, 330, "#FFF8F0", ORANGE, dash="6 4")
s.rect(460, 60, 410, 330, "#F0FAF4", GREEN, dash="6 4")
s.text(235, 90, "Vertical scaling (scale up)", 16, ORANGE, "bold")
s.text(665, 90, "Horizontal scaling (scale out)", 16, GREEN, "bold")
s.box(60, 190, 100, 70, ["1 server", "8 cores", "32 GB"], "#FFFFFF", ORANGE, size=13)
s.arrow(170, 225, 235, 225, color=ORANGE)
s.box(245, 130, 170, 190, ["1 BIGGER server", "64 cores", "512 GB RAM", "20 TB disk"], "#FFFFFF", ORANGE, size=14)
s.text(235, 345, "Costly, has a hard ceiling, single point of failure", 12, GRAY)
s.box(480, 190, 90, 70, ["1 server", "8 cores", "32 GB"], "#FFFFFF", GREEN, size=13)
s.arrow(578, 225, 625, 225, color=GREEN)
for i, (x, y) in enumerate([(640, 125), (755, 125), (640, 235), (755, 235)]):
    s.box(x, y, 100, 90, [f"Server {i+1}", "8 cores", "32 GB"], "#FFFFFF", GREEN, size=13)
s.text(665, 345, "Cheaper hardware, scales further, survives failures", 12, GRAY)
s.save("01-scaling.svg")

# 2 ─ HDFS ---------------------------------------------------------------
s = Svg(900, 440, "HDFS architecture")
s.title_bar("HDFS: one NameNode, many DataNodes")
s.box(320, 60, 260, 80, ["NameNode (the librarian)", "file names, folders,", "which block lives where"], "#FDF1E2", ORANGE, size=13)
s.text(595, 105, "metadata only, no file data", 12, GRAY, anchor="start")
xs = [40, 250, 460, 670]
blocks = [("Block 1", "Block 4'"), ("Block 2", "Block 1'"), ("Block 3", "Block 2'"), ("Block 4", "Block 3'")]
for i, x in enumerate(xs):
    s.arrow(450, 140, x + 95, 215, color=GRAY, dash="4 3")
    s.rect(x, 215, 190, 165, "#FFFFFF", BLUE)
    s.text(x + 95, 240, f"DataNode {i+1}", 14, NAVY, "bold")
    s.box(x + 20, 258, 150, 46, [blocks[i][0] + " (128 MB)"], LIGHT, BLUE, size=13, bold_first=False)
    s.box(x + 20, 316, 150, 46, [blocks[i][1] + " (replica)"], "#F2F2F2", GRAY, size=13, bold_first=False, dash="4 3")
s.text(450, 410, "A 512 MB file is split into four 128 MB blocks; each block is copied to other DataNodes (replication)", 12, GRAY)
s.save("02-hdfs-architecture.svg")

# 3 ─ MapReduce ----------------------------------------------------------
s = Svg(980, 440, "MapReduce word flow for revenue by city")
s.title_bar("MapReduce: revenue per city")
cols = [(30, "INPUT", ["101 Hyderabad 500", "102 Mumbai 700", "103 Hyderabad 300", "104 Bangalore 800", "105 Mumbai 200", "106 Hyderabad 400"]),
        (270, "MAP", ["(Hyderabad, 500)", "(Mumbai, 700)", "(Hyderabad, 300)", "(Bangalore, 800)", "(Mumbai, 200)", "(Hyderabad, 400)"]),
        (510, "SHUFFLE & SORT", ["Hyderabad → [500, 300, 400]", "Mumbai → [700, 200]", "Bangalore → [800]"]),
        (750, "REDUCE", ["Hyderabad = 1200", "Mumbai = 900", "Bangalore = 800"])]
fills = [LIGHT, "#FFF3E0", "#EFE9FB", "#E6F5EC"]
strokes = [BLUE, ORANGE, PURPLE, GREEN]
for (x, head, rows), f, st in zip(cols, fills, strokes):
    w = 200 if head != "SHUFFLE & SORT" else 220
    s.rect(x, 70, w, 300, f, st)
    s.text(x + w / 2, 100, head, 15, st, "bold")
    step = 40 if len(rows) == 6 else 70
    start = 140 if len(rows) == 6 else 160
    for i, r in enumerate(rows):
        s.text(x + w / 2, start + i * step, r, 13 if head != "SHUFFLE & SORT" else 12, NAVY)
for x1, x2 in [(232, 266), (472, 506), (734, 746)]:
    s.arrow(x1, 220, x2, 220)
s.text(490, 405, "Each machine maps its own slice; the framework groups equal keys; reducers produce the final totals", 12, GRAY)
s.save("03-mapreduce-flow.svg")

# 4 ─ Spark architecture ------------------------------------------------
s = Svg(900, 470, "Spark architecture")
s.title_bar("Spark architecture: driver, cluster manager, executors")
s.box(60, 70, 230, 90, ["Your code", "PySpark / SQL notebook"], LIGHT, BLUE)
s.box(335, 70, 230, 90, ["Driver", "plans the job, schedules tasks"], "#FDF1E2", ORANGE)
s.box(610, 70, 230, 90, ["Cluster manager", "allocates machines & resources"], "#EFE9FB", PURPLE)
s.arrow(290, 115, 332, 115)
s.arrow(565, 115, 607, 115)
for i, x in enumerate([60, 335, 610]):
    s.arrow(450, 160, x + 115, 225, dash="4 3")
    s.rect(x, 225, 230, 175, "#FFFFFF", GREEN)
    s.text(x + 115, 250, f"Worker node {i+1}", 14, GREEN, "bold")
    s.box(x + 20, 265, 190, 60, [f"Executor {i+1}", "runs tasks, caches data"], "#E6F5EC", GREEN, size=13)
    s.box(x + 20, 338, 55, 40, ["Task"], LIGHT, BLUE, size=12, bold_first=False)
    s.box(x + 87, 338, 55, 40, ["Task"], LIGHT, BLUE, size=12, bold_first=False)
    s.box(x + 154, 338, 55, 40, ["Task"], LIGHT, BLUE, size=12, bold_first=False)
s.text(450, 435, "Each task processes one partition of the data. Results flow back to the driver or are written to storage.", 12, GRAY)
s.save("04-spark-architecture.svg")

# 5 ─ Lazy evaluation ---------------------------------------------------
s = Svg(980, 330, "Lazy evaluation flow")
s.title_bar("Lazy evaluation: nothing runs until an action")
steps = [("read()", "transformation", LIGHT, BLUE), ("filter()", "transformation", LIGHT, BLUE), ("select()", "transformation", LIGHT, BLUE),
         ("Logical plan", "recorded, not run", "#EFE9FB", PURPLE), ("count() / display()", "ACTION", "#FDE8E6", RED),
         ("Optimise + run", "tasks on executors", "#E6F5EC", GREEN)]
x = 20
for i, (a, b, f, st) in enumerate(steps):
    s.box(x, 110, 140, 80, [a, b], f, st, size=13)
    if i < len(steps) - 1:
        s.arrow(x + 142, 150, x + 158, 150)
    x += 160
s.text(250, 235, "Build the plan (instant)", 13, BLUE, "bold")
s.text(810, 235, "Execute the plan (real work)", 13, GREEN, "bold")
s.text(490, 285, "Because Spark sees the whole plan first, it can reorder and combine steps efficiently.", 12, GRAY)
s.save("05-lazy-evaluation.svg")

# 6 ─ Medallion ---------------------------------------------------------
s = Svg(980, 360, "Medallion architecture")
s.title_bar("Medallion architecture: Bronze → Silver → Gold")
s.box(20, 120, 150, 110, ["Sources", "CSV, JSON, APIs,", "databases"], "#F2F2F2", GRAY, size=13)
layers = [(215, "BRONZE", "Raw data as ingested", BRONZE, "#FBEFE3"), (415, "SILVER", "Cleaned & validated", "#6D7885", "#EEF1F4"), (615, "GOLD", "Business-ready tables", GOLD, "#FCF5DC")]
for x, n, d, st, f in layers:
    s.box(x, 105, 170, 140, [n, d], f, st, size=14)
s.box(815, 70, 150, 55, ["Dashboards"], LIGHT, BLUE, size=13)
s.box(815, 140, 150, 55, ["SQL analytics"], LIGHT, BLUE, size=13)
s.box(815, 210, 150, 55, ["ML / AI"], LIGHT, BLUE, size=13)
s.arrow(172, 175, 212, 175); s.arrow(387, 175, 412, 175); s.arrow(587, 175, 612, 175)
for y in (97, 167, 237):
    s.arrow(787, 175, 812, y)
s.text(300, 275, "append-only", 12, GRAY); s.text(500, 275, "dedupe, fix nulls,", 12, GRAY); s.text(500, 292, "cast types", 12, GRAY); s.text(700, 275, "aggregate, join", 12, GRAY)
s.text(490, 335, "Each layer is a set of Delta tables governed by Unity Catalog.", 12, GRAY)
s.save("06-medallion-architecture.svg")

# 7 ─ Journey ------------------------------------------------------------
s = Svg(1000, 330, "From single machine to Databricks")
s.title_bar("The journey: one machine → Databricks")
items = [("1", "Single\nmachine"), ("2", "Vertical\nscaling"), ("3", "Horizontal\nscaling"), ("4", "Distributed\ncomputing"), ("5", "HDFS"),
         ("6", "MapReduce"), ("7", "Spark"), ("8", "PySpark"), ("9", "Databricks")]
colors = [GRAY, ORANGE, GREEN, GREEN, BLUE, BLUE, PURPLE, PURPLE, RED]
x = 20
for (n, t), c in zip(items, colors):
    s.rect(x, 110, 100, 100, "#FFFFFF", c, sw=2.5)
    s.text(x + 50, 140, n, 20, c, "bold")
    for j, line in enumerate(t.split("\n")):
        s.text(x + 50, 170 + j * 18, line, 13, NAVY)
    if n != "9":
        s.arrow(x + 102, 160, x + 108, 160)
    x += 108
s.text(500, 260, "Each step fixes a limitation of the previous one.", 14, GRAY)
s.save("07-journey.svg")

# 8 ─ Banner ---------------------------------------------------------------
s = Svg(1000, 220, "Repository banner")
s.parts.append(f'<rect width="1000" height="220" fill="{NAVY}"/>')
s.parts.append(f'<rect y="205" width="1000" height="15" fill="{ORANGE}"/>')
s.text(500, 90, "From Big Data to Spark, PySpark & Databricks", 34, "#FFFFFF", "bold")
s.text(500, 130, "A beginner-friendly learning path for data engineers", 18, "#BFD7EA")
for i, (t, c) in enumerate([("Hadoop", BLUE), ("Spark", ORANGE), ("PySpark", GREEN), ("Databricks", RED), ("Delta Lake", PURPLE)]):
    x = 140 + i * 142
    s.rect(x, 155, 125, 32, c, c, rx=16)
    s.text(x + 62, 176, t, 14, "#FFFFFF", "bold")
s.save("banner.svg")

# 9 ─ Five Vs ---------------------------------------------------------------
s = Svg(980, 300, "The five Vs of Big Data")
s.title_bar("The 5 Vs of Big Data")
vs = [("Volume", "How much data", "billions of records", BLUE), ("Velocity", "How fast it arrives", "millisecond decisions", ORANGE),
      ("Variety", "Different formats", "tables, JSON, images", GREEN), ("Veracity", "How trustworthy", "duplicates, gaps, errors", RED),
      ("Value", "Business benefit", "insight, revenue, retention", PURPLE)]
for i, (a, b, c, col) in enumerate(vs):
    x = 20 + i * 190
    s.rect(x, 70, 175, 180, "#FFFFFF", col, sw=2.5)
    s.rect(x, 70, 175, 50, col, col)
    s.text(x + 87, 103, a, 18, "#FFFFFF", "bold")
    s.text(x + 87, 160, b, 14, NAVY, "bold")
    s.text(x + 87, 195, c, 12, GRAY)
s.save("08-five-vs.svg")

# 10 ─ Traditional vs modern -------------------------------------------------
s = Svg(980, 470, "Traditional versus modern data architecture")
s.title_bar("Traditional approach vs modern approach")
s.rect(20, 60, 450, 380, "#FFF8F0", ORANGE, dash="6 4")
s.rect(510, 60, 450, 380, "#F0FAF4", GREEN, dash="6 4")
s.text(245, 90, "TRADITIONAL", 16, ORANGE, "bold")
s.text(735, 90, "MODERN", 16, GREEN, "bold")
trad = [("Data sources", "files, databases, applications"), ("Nightly ETL jobs", "fixed schema, scheduled batches"),
        ("One server / warehouse", "storage and compute tied together"), ("Reports", "mostly structured, historical")]
mod = [("Data sources", "apps, events, logs, IoT, files"), ("Cloud object storage + Delta Lake", "cheap, elastic, reliable tables"),
       ("Distributed compute (Spark)", "scaled up or down on demand"), ("Bronze → Silver → Gold", "SQL, BI, ML and AI on one platform")]
for i, ((a, b), (c, d)) in enumerate(zip(trad, mod)):
    y = 115 + i * 80
    s.box(50, y, 390, 58, [a, b], "#FFFFFF", ORANGE, size=13)
    s.box(540, y, 390, 58, [c, d], "#FFFFFF", GREEN, size=13)
    if i < 3:
        s.arrow(245, y + 60, 245, y + 77, color=ORANGE)
        s.arrow(735, y + 60, 735, y + 77, color=GREEN)
s.text(245, 425, "Scale up, plan capacity, manage hardware", 12, GRAY)
s.text(735, 425, "Scale out, pay for use, managed platform", 12, GRAY)
s.save("08-traditional-vs-modern.svg")

# 11 ─ Lakehouse -------------------------------------------------------------
s = Svg(980, 400, "Lakehouse architecture")
s.title_bar("Data lake + data warehouse = lakehouse")
s.box(30, 90, 230, 130, ["Data lake", "any format, cheap storage,", "weak reliability"], "#FFF8F0", ORANGE, size=13)
s.box(30, 240, 230, 100, ["Data warehouse", "structured, fast SQL,", "rigid and costly"], "#EFE9FB", PURPLE, size=13)
s.arrow(262, 155, 332, 190); s.arrow(262, 290, 332, 230)
s.rect(335, 75, 615, 280, "#F0FAF4", GREEN, dash="6 4")
s.text(642, 102, "LAKEHOUSE", 15, GREEN, "bold")
s.box(360, 120, 565, 52, ["Consumers", "Databricks SQL · dashboards · machine learning · AI"], "#FFFFFF", BLUE, size=13)
s.box(360, 182, 565, 44, ["Governance (Unity Catalog)", "access control · lineage · discovery"], "#FFFFFF", BLUE, size=13)
s.box(360, 236, 565, 44, ["Delta Lake", "ACID transactions · schema control · time travel"], "#FFFFFF", BLUE, size=13)
s.box(360, 290, 565, 44, ["Cloud object storage", "Amazon S3 · Azure Data Lake Storage · Google Cloud Storage"], "#FFFFFF", BLUE, size=13)
s.save("09-lakehouse.svg")

print("diagrams written:", sorted(os.listdir(OUT)))
