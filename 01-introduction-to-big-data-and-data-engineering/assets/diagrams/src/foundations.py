from lib import S, P


def d01_problem(out):
    s = S(1200, 560, "The Scenario: 100 GB of Data Every Day", "You are a Data Analyst at XYZ Company.")
    s.building(90, 190, 110, 140)
    s.text(145, 372, "XYZ Company", 20, P["navy"], "bold", "middle")
    s.arrow(250, 270, 520, 270, P["orange"], 4)
    s.text(385, 255, "generates", 20, P["orange"], "bold", "middle")
    for i in range(3):
        s.db(560 + i * 14, 190 + i * 14, 90, 110, P["lblue"])
    s.text(640, 372, "100 GB per day", 24, P["navy"], "bold", "middle")
    # stat cards
    stats = [("≈ 3 TB", "per month"), ("≈ 36 TB", "per year"), ("≈ 1 billion", "rows per day*")]
    for i, (a, b) in enumerate(stats):
        x = 790 + 0
        y = 150 + i * 92
        s.rect(x, y, 370, 78, "#FFFFFF", P["lgrey"], 2, 12)
        s.text(x + 24, y + 38, a, 28, P["orange"], "bold")
        s.text(x + 24, y + 63, b, 17, P["grey"])
    s.text(790, 438, "*assuming about 100 bytes per row", 14, P["grey"], italic=True)
    s.rect(40, 440, 720, 90, P["navy"], None, 0, 14)
    s.text(70, 478, "Where can we store and analyse it?", 24, "#FFFFFF", "bold")
    for i, (t, c) in enumerate([("Excel", P["green"]), ("MySQL", P["blue"]), ("Databricks", P["orange"])]):
        s.chip(70 + i * 160, 492, 145, 32, t, c, size=17)
    s.save(out)


def d02_excel_mysql(out):
    s = S(1200, 760, "Why Excel and MySQL Are Not Enough", "Test each option against 100 GB per day.")
    s.card(40, 120, 540, 380, "1 · Excel", "#FFFFFF", P["green"])
    s.notebook(70, 180, 80, 100)
    s.text(170, 205, "Like a NOTEBOOK", 22, P["green"], "bold")
    s.text(170, 232, "good for small data", 18, P["grey"])
    for i, t in enumerate(["Stores only ~1 million rows per sheet",
                           "Crashes on large data (all in one PC's memory)",
                           "Manual handling: copy, paste, drag formulas"]):
        s.cross(80, 322 + i * 40, 9)
        s.text(104, 328 + i * 40, t, 17)
    s.chip(70, 452, 230, 32, "Not for 100 GB/day", P["red"], size=15)
    s.card(620, 120, 540, 380, "2 · MySQL", "#FFFFFF", P["blue"])
    s.warehouse(650, 178, 110, 90)
    s.text(782, 205, "Like a WAREHOUSE", 22, P["blue"], "bold")
    s.text(782, 232, "good storage, limited capacity & speed", 16, P["grey"])
    s.tick(660, 322, 9); s.text(684, 328, "Structured tables + SQL, better than Excel", 17)
    s.cross(660, 362, 9); s.text(684, 368, "Scaling is difficult (manual setup)", 17)
    s.cross(660, 402, 9); s.text(684, 408, "Performance drops with massive data", 17)
    s.chip(650, 452, 230, 32, "Not for 100 GB/day", P["red"], size=15)
    s.text(40, 545, "How big is the gap? One day of data vs Excel's row limit", 19, P["navy"], "bold")
    s.rect(40, 565, 1120, 36, P["orange"], None, 0, 8)
    s.text(1140, 590, "One day of data ≈ 1,000,000,000 rows", 17, "#FFFFFF", "bold", "end")
    s.rect(40, 620, 14, 36, P["green"], None, 0, 4)
    s.text(66, 645, "Excel limit: 1,048,576 rows (about 1/1000 of one day)", 17, P["green"], "bold")
    s.rect(40, 685, 1120, 52, P["navy"], None, 0, 12)
    s.text(600, 719, "Excel is too small. MySQL is too limited. We need something built for big data.", 20, "#FFFFFF", "bold", "middle")
    s.save(out)


def d03_scaling(out):
    s = S(1200, 620, "Scale Up vs Scale Out", "What if we increase the processor / computing power?")
    s.card(40, 120, 540, 400, "Vertical scaling: scale UP", "#FFFFFF", P["red"])
    s.text(310, 196, "ONE machine, made bigger and bigger", 18, P["red"], "bold", "middle")
    for i, (w, h, price) in enumerate([(70, 50, "$"), (90, 80, "$$$"), (110, 120, "$$$$$$")]):
        x = 90 + i * 140
        s.server(x, 430 - h, w, h)
        s.text(x + w / 2, 430 - h - 12, price, 22, P["red"], "bold", "middle")
    s.arrow(90, 280, 500, 215, P["red"], 3)
    s.rect(70, 455, 480, 50, P["lorange"], None, 0, 10)
    s.text(310, 486, "Expensive · has a ceiling · if it fails, everything stops", 16, P["red"], "bold", "middle")
    s.card(620, 120, 540, 400, "Horizontal scaling: scale OUT", "#FFFFFF", P["green"])
    s.text(890, 196, "MANY ordinary machines, working together", 18, P["green"], "bold", "middle")
    for r in range(2):
        for c in range(4):
            s.server(650 + c * 125, 200 + r * 110, 100, 70)
    s.text(890, 425, "$ each, and you only add what you need", 17, P["green"], "bold", "middle")
    s.rect(650, 455, 480, 50, P["lgreen"], None, 0, 10)
    s.text(890, 486, "Cost grows steadily · no real limit · one failure is OK", 16, P["green"], "bold", "middle")
    s.rect(40, 540, 1120, 56, P["navy"], None, 0, 14)
    s.text(600, 576, "Big data isn't about a bigger machine. It's about MANY machines acting like ONE.", 21, "#FFFFFF", "bold", "middle")
    s.save(out)


def d04_single_machine(out):
    s = S(1200, 440, "Single Machine Setup", "Works well for small data: a few queries on one machine.")
    s.db(90, 170, 90, 110); s.text(135, 316, "Database", 20, P["navy"], "bold", "middle")
    s.server(500, 170, 190, 110); s.text(595, 316, "One machine", 20, P["navy"], "bold", "middle")
    s.text(595, 340, "processor + computing power", 16, P["grey"], anchor="middle")
    s.person(990, 175, 90); s.text(1035, 316, "User", 20, P["navy"], "bold", "middle")
    s.arrow(950, 215, 700, 215, P["purple"], 3); s.text(825, 200, "1 · sends a query", 16, P["purple"], "bold", "middle")
    s.arrow(500, 235, 190, 235, P["purple"], 3); s.text(345, 224, "2 · asks for data", 16, P["purple"], "bold", "middle")
    s.arrow(190, 262, 500, 262, P["blue"], 3); s.text(345, 290, "3 · data comes back", 16, P["blue"], "bold", "middle")
    s.arrow(700, 262, 950, 262, P["blue"], 3); s.text(825, 290, "4 · result returned", 16, P["blue"], "bold", "middle")
    s.rect(40, 375, 1120, 44, P["lgold"], None, 0, 10)
    s.text(600, 404, "Small data: fine.   Big data: this one machine becomes the bottleneck.", 19, P["navy"], "bold", "middle")
    s.save(out)


def cluster(out, kind):
    hd = kind == "hdd"
    acc = P["blue"] if hd else P["orange"]
    title = "Hadoop: Distributed Storage + Parallel Processing" if hd else "Spark: The Same Idea, But In Memory"
    sub = ("Each machine has its own HDD (storage) and processor." if hd
           else "Each machine now keeps its data in Memory (RAM) next to its processor.")
    s = S(1200, 660, title, sub)
    s.db(60, 270, 80, 100); s.text(100, 404, "Database", 19, P["navy"], "bold", "middle")
    ys = [130, 252, 374, 496]
    for i, y in enumerate(ys):
        s.rect(380, y - 8, 230, 108, "#FFFFFF", P["lgrey"], 2, 12)
        s.text(395, y + 10, f"Machine {i+1}", 14, P["grey"], "bold")
        if hd:
            s.hdd(398, y + 22, 50)
        else:
            s.ram(394, y + 34, 62, 30)
        s.server(480, y + 20, 110, 68)
        s.arrow(150, 320, 376, y + 46, P["navy"], 2.5)
        s.arrow(612, y + 46, 794, 300 + i * 30, acc, 2.5)
    s.grid(800, 290, 150, 110, 3, 4, P["blue"])
    s.text(875, 428, "Combined result", 19, P["navy"], "bold", "middle")
    s.arrow(960, 345, 1040, 345, acc, 3)
    s.person(1050, 308, 70); s.text(1085, 408, "User", 19, P["navy"], "bold", "middle")
    s.badge(260, 128, "1"); s.text(260, 160, "Split the data", 15, P["navy"], "bold", "middle")
    s.badge(700, 128, "2"); s.text(700, 160, "Process in parallel", 15, P["navy"], "bold", "middle")
    s.badge(875, 128, "3"); s.text(875, 160, "Combine", 15, P["navy"], "bold", "middle")
    if hd:
        s.rect(40, 610, 1120, 36, P["lblue"], None, 0, 10)
        s.text(600, 634, "HDFS stores the data  ·  MapReduce processes it  ·  YARN manages the machines", 17, P["navy"], "bold", "middle")
    else:
        s.rect(40, 610, 1120, 36, P["lorange"], None, 0, 10)
        s.text(600, 634, "Only one thing changed: HDD → RAM.  RAM is far faster than a disk, so Spark is far faster.", 17, P["navy"], "bold", "middle")
    s.save(out)


def d05_hadoop(out): cluster(out, "hdd")
def d07_spark(out): cluster(out, "ram")


def d06_fault(out):
    s = S(1200, 620, "Hadoop Fault Tolerance: Copies Save the Day", "Each block is stored on 3 different machines (default replication = 3).")
    # file
    s.rect(40, 150, 150, 170, "#FFFFFF", P["navy"], 2.5, 8)
    s.text(115, 185, "Big file", 18, P["navy"], "bold", "middle")
    for i, (b, c) in enumerate([("A", P["blue"]), ("B", P["green"]), ("C", P["gold"])]):
        s.rect(62, 205 + i * 36, 106, 28, c, None, 0, 6); s.text(115, 226 + i * 36, f"Block {b}", 15, "#FFFFFF", "bold", "middle")
    s.arrow(195, 235, 270, 235, P["navy"], 3); s.text(232, 215, "split", 14, P["grey"], "bold", "middle")
    cols = {"A": P["blue"], "B": P["green"], "C": P["gold"]}
    nodes = [("Node 1", "ABC", False), ("Node 2", "AC", True), ("Node 3", "BC", False), ("Node 4", "AB", False)]
    for i, (n, bl, dead) in enumerate(nodes):
        x = 290 + i * 225
        s.rect(x, 130, 200, 260, "#EEF0F2" if dead else "#FFFFFF", P["red"] if dead else P["lgrey"], 3 if dead else 2, 14)
        s.text(x + 100, 162, n, 19, P["grey"] if dead else P["navy"], "bold", "middle")
        s.server(x + 45, 175, 110, 64, dead)
        for j, b in enumerate(bl):
            s.rect(x + 20 + j * 56, 262, 48, 40, cols[b], None, 0, 8, op=0.35 if dead else None)
            s.text(x + 44 + j * 56, 289, b, 20, "#FFFFFF", "bold", "middle")
        if dead:
            s.cross(x + 100, 345, 22)
    s.text(290 + 225 + 100, 418, "FAILED", 18, P["red"], "bold", "middle")
    s.rect(40, 450, 1120, 140, P["lgreen"], P["green"], 2, 14)
    s.text(70, 490, "Is the data lost?  No.", 24, P["green"], "bold")
    s.lines(70, 525, ["Block A is still on Node 1 and Node 4.   Block B is on Nodes 1, 3 and 4.   Block C is on Nodes 1 and 3.",
                      "Hadoop notices the failure and automatically makes new copies on healthy machines."], 17, P["navy"], lh=28)
    s.save(out)


def d08_hadoop_vs_spark(out):
    s = S(1200, 620, "Why Spark Is Faster Than Hadoop MapReduce", "Hadoop writes to disk after every step. Spark keeps data in memory between steps.")
    s.text(40, 150, "Hadoop MapReduce  (disk-based)", 21, P["blue"], "bold")
    for i, t in enumerate(["Read", "Map", "Reduce", "Next job"]):
        x = 40 + i * 290
        s.rect(x, 170, 130, 56, P["lblue"], P["blue"], 2, 10); s.text(x + 65, 205, t, 18, P["navy"], "bold", "middle")
        if i < 3:
            s.arrow(x + 134, 198, x + 286, 198, P["blue"], 3)
            s.hdd(x + 182, 232, 40)
            s.text(x + 202, 292, "write to disk", 13, P["blue"], "bold", "middle")
    s.text(1160, 205, "SLOW", 28, P["red"], "bold", "end")
    s.text(40, 350, "Spark  (in-memory)", 21, P["orange"], "bold")
    for i, t in enumerate(["Read", "Step 1", "Step 2", "Result"]):
        x = 40 + i * 290
        s.rect(x, 370, 130, 56, P["lorange"], P["orange"], 2, 10); s.text(x + 65, 405, t, 18, P["navy"], "bold", "middle")
        if i < 3:
            s.arrow(x + 134, 398, x + 286, 398, P["orange"], 3)
            s.ram(x + 176, 436, 56, 26)
            s.text(x + 204, 484, "stays in RAM", 13, P["orange"], "bold", "middle")
    s.text(1160, 405, "FAST", 28, P["green"], "bold", "end")
    s.rect(40, 520, 1120, 70, P["navy"], None, 0, 14)
    s.text(70, 550, "Disk is slow.  Memory is fast.", 22, "#FFFFFF", "bold")
    s.text(70, 576, "Multi-step jobs: Spark can be up to ~100x faster for in-memory workloads. Streaming is near real-time (micro-batches).", 15, "#C8D6E0")
    s.save(out)


def d09_spark_arch(out):
    s = S(1200, 660, "Spark Architecture: Driver and Executors", "The driver is the manager. The executors are the workers.")
    s.rect(40, 140, 260, 190, P["lorange"], P["orange"], 3, 14)
    s.text(170, 172, "DRIVER", 22, P["orange"], "bold", "middle")
    s.notebook(135, 184, 70, 90)
    s.lines(170, 297, ["runs your code, plans the work"], 14, P["navy"], anchor="middle")
    s.rect(400, 175, 230, 100, P["lgrey"], P["grey"], 2.5, 14)
    s.text(515, 215, "CLUSTER MANAGER", 18, P["navy"], "bold", "middle")
    s.text(515, 242, "hands out machines", 15, P["grey"], anchor="middle")
    s.arrow(300, 225, 396, 225, P["navy"], 3)
    for i in range(3):
        x, y = 720, 120 + i * 150
        s.rect(x, y, 440, 130, "#FFFFFF", P["blue"], 2.5, 14)
        s.text(x + 18, y + 28, f"EXECUTOR {i+1}", 17, P["blue"], "bold")
        s.server(x + 18, y + 40, 90, 60)
        s.ram(x + 130, y + 40, 62, 28)
        s.text(x + 130, y + 90, "memory", 13, P["grey"])
        for j in range(3):
            s.rect(x + 215 + j * 72, y + 40, 62, 36, P["blue"], None, 0, 6)
            s.text(x + 246 + j * 72, y + 63, f"P{i*3+j+1}", 15, "#FFFFFF", "bold", "middle")
        s.text(x + 215, y + 100, "partitions → tasks", 14, P["grey"])
        s.arrow(634, 225, x - 4, y + 65, P["navy"], 2.5)
    s.line(940, 550, 940, 600, P["green"], 3, "7 5")
    s.line(940, 600, 170, 600, P["green"], 3, "7 5")
    s.arrow(170, 600, 170, 336, P["green"], 3, "7 5")
    s.text(560, 590, "results flow back to the driver", 16, P["green"], "bold", "middle")
    s.rect(250, 380, 420, 170, "#FFFFFF", P["lgrey"], 2, 14)
    s.text(270, 415, "Remember", 18, P["navy"], "bold")
    s.lines(270, 446, ["Partition = one chunk of the data.", "Task = work on one partition,", "run by an executor.",
                       "Spark runs many tasks at once."], 16, lh=26)
    s.save(out)


def d10_how_spark_works(out):
    s = S(1200, 500, "How Spark Works in 4 Steps", "Load → split → process in parallel → combine.")
    xs = [40, 330, 620, 910]
    titles = ["Load big data", "Split into chunks", "Process on many machines", "Combine results"]
    terms = ["a DataFrame", "partitions", "executors run tasks", "back to the driver"]
    for i, x in enumerate(xs):
        s.rect(x, 130, 250, 290, "#FFFFFF", P["lgrey"], 2, 14)
        s.badge(x + 36, 168, str(i + 1))
        s.text(x + 64, 175, titles[i], 17 if i != 2 else 15, P["navy"], "bold")
        if i < 3: s.arrow(x + 254, 275, x + 286, 275, P["orange"], 4)
    s.rect(75, 235, 180, 90, P["blue"], P["navy"], 2.5, 8); s.text(165, 288, "BIG DATA", 20, "#FFFFFF", "bold", "middle")
    for j in range(4):
        s.rect(358 + j * 52, 245, 44, 70, [P["blue"], P["green"], P["gold"], P["purple"]][j], None, 0, 6)
        s.text(380 + j * 52, 288, f"P{j+1}", 15, "#FFFFFF", "bold", "middle")
    for j in range(2):
        for k in range(2):
            s.server(650 + k * 100, 225 + j * 62, 80, 50)
    s.grid(955, 250, 150, 90, 3, 4, P["blue"])
    for i, t in enumerate(terms):
        s.chip(xs[i] + 35, 372, 180, 30, t, P["lorange"], P["orange"], 14, P["orange"])
    s.text(600, 462, "Technical terms in orange.   Spark does all of this for you automatically.", 17, P["grey"], anchor="middle")
    s.save(out)


def d11_evolution(out):
    s = S(1200, 700, "The Big Picture: Each Tool Fixes the Last One's Limit", "Excel → MySQL → Hadoop → Spark → Databricks")
    items = [("Excel", P["green"], "notebook", "~1M rows, one PC, manual", "Needs a real database"),
             ("MySQL", P["blue"], "warehouse", "Hard to scale, slows down", "Needs many machines"),
             ("Hadoop", P["gold"], "hdd", "Distributed, but disk-based = slow", "Needs speed"),
             ("Spark", P["orange"], "ram", "Fast, in-memory, but hard to run", "Needs it managed"),
             ("Databricks", P["red"], "cloud", "Managed, unified, governed", "You are here")]
    for i, (n, c, ic, wall, nxt) in enumerate(items):
        x = 40 + i * 226
        s.card(x, 150, 206, 400, n, "#FFFFFF", c)
        cx = x + 103
        if ic == "notebook": s.notebook(cx - 35, 215, 70, 90)
        elif ic == "warehouse": s.warehouse(cx - 50, 225, 100, 80)
        elif ic == "hdd": s.hdd(cx - 28, 235, 56)
        elif ic == "ram": s.ram(cx - 36, 248, 72, 34)
        else: s.cloud(cx - 60, 230, 120, 70, P["lorange"])
        s.text(cx, 345, "Limit" if i < 4 else "Solves it with", 14, P["grey"], "bold", "middle")
        ls = {0: ["About 1 million rows,", "crashes, manual"], 1: ["Hard to scale,", "slow at 100 GB/day"],
              2: ["Disk-based:", "slow multi-step jobs"], 3: ["Hard to set up", "and manage"], 4: ["Managed Spark +", "governance + notebooks"]}[i]
        s.lines(cx, 372, ls, 16, P["navy"], "bold", "middle", lh=22)
        s.rect(x + 14, 440, 178, 90, c if i == 4 else P["lgrey"], None, 0, 10)
        s.text(cx, 468, "Fix:" if i < 4 else "Today:", 13, "#FFFFFF" if i == 4 else P["grey"], "bold", "middle")
        fl = {0: ["Tables + SQL"], 1: ["Many machines", "(Hadoop)"], 2: ["In-memory", "(Spark)"], 3: ["Managed platform", "(Databricks)"],
              4: ["Spark made easy,", "unified & governed"]}[i]
        s.lines(cx, 492, fl, 16, "#FFFFFF" if i == 4 else P["navy"], "bold", "middle", lh=20)
        if i < 4: s.arrow(x + 208, 350, x + 224, 350, P["navy"], 3)
    s.rect(40, 585, 1120, 80, P["navy"], None, 0, 14)
    s.text(600, 632, "Databricks is not magic. It is Spark, made easy, unified and governed.", 24, "#FFFFFF", "bold", "middle")
    s.save(out)


def d12_pyspark(out):
    s = S(1000, 300, "Apache Spark + Python = PySpark")
    s.rect(60, 110, 250, 120, P["lorange"], P["orange"], 3, 16)
    s.text(185, 160, "Apache Spark", 26, P["orange"], "bold", "middle"); s.text(185, 192, "the fast engine", 17, P["grey"], anchor="middle")
    s.text(350, 187, "+", 48, P["navy"], "bold", "middle")
    s.rect(390, 110, 220, 120, P["lblue"], P["blue"], 3, 16)
    s.text(500, 160, "Python", 26, P["blue"], "bold", "middle"); s.text(500, 192, "the friendly language", 17, P["grey"], anchor="middle")
    s.text(650, 187, "=", 48, P["navy"], "bold", "middle")
    s.rect(690, 110, 250, 120, P["navy"], None, 0, 16)
    s.text(815, 160, "PySpark", 28, "#FFFFFF", "bold", "middle"); s.text(815, 192, "Spark, driven by Python", 16, "#C8D6E0", anchor="middle")
    s.text(500, 270, "Spark itself is written in Scala. PySpark lets analysts and engineers use Python.", 17, P["grey"], anchor="middle")
    s.save(out)


ALL = [("01-problem", d01_problem), ("02-excel-vs-mysql", d02_excel_mysql), ("03-scale-up-vs-out", d03_scaling),
       ("04-single-machine", d04_single_machine), ("05-hadoop", d05_hadoop), ("06-hdfs-fault-tolerance", d06_fault),
       ("07-spark", d07_spark), ("08-hadoop-vs-spark", d08_hadoop_vs_spark), ("09-spark-architecture", d09_spark_arch),
       ("10-how-spark-works", d10_how_spark_works), ("11-evolution", d11_evolution), ("12-pyspark", d12_pyspark)]

