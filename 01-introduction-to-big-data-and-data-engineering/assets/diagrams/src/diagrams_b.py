"""Diagrams for topics 04-09: distributed computing, Hadoop, Spark, PySpark, evolution, platforms."""
import extras
from lib import S, P
from extras import wrap


def building_blocks(out):
    s = S(1200, 640, "Five Building Blocks of Distributed Systems", "Every big-data tool is built from the same few ideas.")
    cards = [("Partitioning", "Split data into pieces", P["blue"]), ("Parallelism", "Work on pieces at the same time", P["orange"]),
             ("Replication", "Keep copies on several machines", P["green"]), ("Fault tolerance", "Keep going when a machine fails", P["red"]),
             ("Data locality", "Move the code to the data, not the data to the code", P["purple"])]
    for i, (n, d, c) in enumerate(cards):
        x = 40 + i * 227
        s.card(x, 130, 212, 400, n, "#FFFFFF", c, size=18)
        cx = x + 106
        if i == 0:
            s.rect(cx - 70, 190, 140, 40, P["blue"], None, 0, 6)
            s.arrow(cx, 236, cx, 262, P["navy"], 3)
            for k in range(4): s.rect(cx - 72 + k * 38, 270, 32, 40, [P["blue"], P["green"], P["gold"], P["purple"]][k], None, 0, 5)
        elif i == 1:
            for k in range(3):
                s.server(cx - 85 + k * 60, 200, 50, 40); s.arrow(cx - 60 + k * 60, 246, cx - 60 + k * 60, 286, P["orange"], 3)
            s.text(cx, 312, "all at once", 14, P["orange"], "bold", "middle")
        elif i == 2:
            for k in range(3):
                s.server(cx - 80 + k * 58, 208, 48, 38)
                s.rect(cx - 72 + k * 58, 256, 32, 24, P["green"], None, 0, 5); s.text(cx - 56 + k * 58, 273, "A", 14, "#FFFFFF", "bold", "middle")
            s.text(cx, 312, "same block, 3 places", 14, P["green"], "bold", "middle")
        elif i == 3:
            s.server(cx - 80, 205, 50, 40); s.server(cx - 25, 205, 50, 40, True); s.server(cx + 30, 205, 50, 40)
            s.cross(cx, 270, 14); s.text(cx, 312, "one fails, job continues", 14, P["red"], "bold", "middle")
        else:
            s.db(cx - 80, 196, 44, 56, P["lblue"]); s.rect(cx - 12, 214, 56, 26, P["purple"], None, 0, 6)
            s.text(cx + 16, 232, "code", 13, "#FFFFFF", "bold", "middle"); s.arrow(cx + 48, 227, cx + 78, 227, P["purple"], 3)
            s.text(cx, 312, "small code travels,", 14, P["purple"], "bold", "middle"); s.text(cx, 330, "big data stays put", 14, P["purple"], "bold", "middle")
        for k, l in enumerate(wrap(d, 22)): s.text(x + 106, 395 + k * 24, l, 17, P["navy"], "bold", "middle")
    s.text(600, 580, "Hadoop and Spark both combine all five.", 20, P["navy"], "bold", "middle")
    s.save(out)


def parallel_speedup(out):
    s = S(1200, 520, "The Power of Reading in Parallel", "How long does it take just to READ 100 GB once?")
    s.text(40, 160, "1 machine", 20, P["red"], "bold")
    s.rect(40, 176, 1120, 60, P["red"], None, 0, 12)
    s.text(1140, 214, "≈ 683 seconds  (about 11 minutes)", 21, "#FFFFFF", "bold", "end")
    s.text(40, 290, "100 machines, each reading 1 GB", 20, P["green"], "bold")
    s.rect(40, 306, 1120 * 6.83 / 683, 60, P["green"], None, 0, 4)
    s.text(76, 344, "≈ 7 seconds", 21, P["green"], "bold")
    s.rect(40, 395, 1120, 90, P["lgold"], None, 0, 12)
    s.text(60, 425, "Assumptions: 150 MB/s sequential read per disk, 1 GB = 1,024 MB, perfectly even split, no overhead.", 15, P["navy"])
    s.text(60, 449, "Real clusters add coordination costs and are slower than this ideal, but the lesson holds:", 15, P["navy"])
    s.text(60, 473, "dividing the data divides the time. That is why we scale OUT.", 15, P["navy"], "bold")
    s.save(out)


def hdfs_arch(out):
    s = S(1200, 700, "HDFS Architecture: NameNode and DataNodes", "One manager that knows where everything is, many workers that hold the data.")
    s.person(50, 330, 56); s.text(78, 410, "Client", 18, P["navy"], "bold", "middle")
    s.rect(430, 120, 360, 190, P["lorange"], P["orange"], 3, 16)
    s.text(610, 152, "NameNode (the manager)", 19, P["orange"], "bold", "middle")
    s.text(610, 174, "stores metadata only, never the data", 14, P["grey"], anchor="middle")
    s.rect(450, 190, 320, 100, "#FFFFFF", P["orange"], 1.5, 8)
    for k, l in enumerate(["/sales/jan.csv → B1, B2, B3", "B1 → DataNode 1, 2, 4", "B2 → DataNode 1, 3, 4", "B3 → DataNode 2, 3, 1"]):
        s.text(464, 214 + k * 22, l, 14, P["navy"])
    for i in range(4):
        x = 190 + i * 235
        s.rect(x, 480, 205, 150, "#FFFFFF", P["blue"], 2.5, 14)
        s.text(x + 102, 506, f"DataNode {i+1}", 16, P["blue"], "bold", "middle")
        s.server(x + 47, 518, 110, 52)
        for k, b in enumerate([["B1", "B2", "B3"], ["B1", "B3"], ["B2", "B3"], ["B1", "B2"]][i]):
            s.rect(x + 22 + k * 56, 584, 48, 30, [P["blue"], P["green"], P["gold"]][int(b[1]) - 1], None, 0, 6)
            s.text(x + 46 + k * 56, 605, b, 14, "#FFFFFF", "bold", "middle")
        s.line(x + 102, 480, 610 + (i - 1.5) * 50, 312, P["mid"], 2, "6 5")
    s.arrow(112, 345, 426, 225, P["navy"], 3); s.badge(250, 262, "1", P["navy"], 14)
    s.text(112, 300, "Where is jan.csv?", 14, P["navy"], "bold")
    s.arrow(426, 270, 112, 372, P["orange"], 3); s.badge(290, 340, "2", P["orange"], 14)
    s.arrow(80, 392, 186, 540, P["blue"], 3); s.badge(120, 480, "3", P["blue"], 14)
    s.text(204, 668, "Read and write blocks directly from DataNodes", 15, P["blue"], "bold")
    s.text(840, 330, "dashed = heartbeat + block report", 14, P["grey"], italic=True)
    s.text(840, 352, "every few seconds", 14, P["grey"], italic=True)
    s.text(840, 150, "Blocks: 128 MB by default", 15, P["navy"], "bold"); s.text(840, 174, "Replication: 3 copies by default", 15, P["navy"], "bold")
    s.save(out)


def mapreduce(out):
    s = S(1200, 700, "MapReduce Step by Step: Counting Words", "Goal: count how many times each word appears across a huge set of files.")
    heads = [(40, 150, "1 · Input splits"), (240, 220, "2 · Map"), (520, 190, "3 · Shuffle & sort"), (770, 160, "4 · Reduce"), (990, 170, "5 · Output")]
    for x, w, t in heads:
        s.rect(x, 120, w, 40, P["navy"], None, 0, 10); s.text(x + w / 2, 146, t, 16, "#FFFFFF", "bold", "middle")
    splits = ["big data", "big ideas", "data matters"]
    maps = [["(big, 1)", "(data, 1)"], ["(big, 1)", "(ideas, 1)"], ["(data, 1)", "(matters, 1)"]]
    for i in range(3):
        y = 190 + i * 130
        s.rect(40, y, 150, 100, "#FFFFFF", P["blue"], 2.5, 12); s.text(115, y + 28, f"Split {i+1}", 13, P["grey"], "bold", "middle")
        s.text(115, y + 62, splits[i], 18, P["navy"], "bold", "middle")
        s.arrow(194, y + 50, 238, y + 50, P["navy"], 3)
        s.rect(240, y, 220, 100, P["lorange"], P["orange"], 2.5, 12)
        s.text(350, y + 26, f"Map task {i+1}", 13, P["grey"], "bold", "middle")
        for k, p in enumerate(maps[i]): s.text(350, y + 56 + k * 24, p, 17, P["navy"], "bold", "middle")
    groups = [("big", "[1, 1]"), ("data", "[1, 1]"), ("ideas", "[1]"), ("matters", "[1]")]
    gy = [175, 265, 355, 445]
    for (w, v), y in zip(groups, gy):
        s.rect(520, y, 190, 66, P["lgold"], P["gold"], 2.5, 12)
        s.text(615, y + 40, f"{w}  →  {v}", 19, P["navy"], "bold", "middle")
    feeds = {0: [0, 1], 1: [0, 2], 2: [1], 3: [2]}
    for g, srcs in feeds.items():
        for sidx in srcs:
            s.arrow(462, 240 + sidx * 130 + (g % 2) * 10 - 10, 518, gy[g] + 33, P["mid"], 2)
    for k, (y, h, t, rows) in enumerate([(165, 190, "Reducer 1", ["big → 2", "data → 2"]), (370, 140, "Reducer 2", ["ideas → 1", "matters → 1"])]):
        s.rect(770, y, 160, h - 20 if k == 0 else h - 20, P["lgreen"], P["green"], 2.5, 12)
        s.text(850, y + 28, t, 13, P["grey"], "bold", "middle")
        s.text(850, y + 66, "sum the 1s", 16, P["green"], "bold", "middle")
    for g in (0, 1): s.arrow(712, gy[g] + 33, 768, 260, P["green"], 2.5)
    for g in (2, 3): s.arrow(712, gy[g] + 33, 768, 440, P["green"], 2.5)
    for k, (y, rows) in enumerate([(185, ["big → 2", "data → 2"]), (385, ["ideas → 1", "matters → 1"])]):
        s.arrow(932, y + 40, 988, y + 40, P["navy"], 3)
        s.rect(990, y - 5, 170, 100, "#FFFFFF", P["green"], 2.5, 12)
        for j, r in enumerate(rows): s.text(1075, y + 38 + j * 28, r, 18, P["navy"], "bold", "middle")
    s.hdd(300, 590, 40); s.text(352, 616, "map output is written to local disk", 14, P["grey"], "bold")
    s.hdd(780, 590, 40); s.text(832, 616, "final output is written to HDFS", 14, P["grey"], "bold")
    s.rect(40, 645, 1120, 40, P["lgold"], None, 0, 10)
    s.text(600, 672, "Map: emit (word, 1)  ·  Shuffle: bring identical words together over the network  ·  Reduce: add them up", 15, P["navy"], "bold", "middle")
    s.save(out)


def hadoop_ecosystem(out):
    s = S(1200, 700, "The Hadoop Ecosystem", "Three core components, plus a family of tools built on top.")
    s.rect(40, 540, 760, 90, P["blue"], None, 0, 14); s.text(420, 578, "HDFS", 28, "#FFFFFF", "bold", "middle")
    s.text(420, 608, "storage: distributed, replicated file system", 16, "#DCEBF7", anchor="middle")
    s.rect(40, 440, 760, 84, P["green"], None, 0, 14); s.text(420, 476, "YARN", 28, "#FFFFFF", "bold", "middle")
    s.text(420, 504, "resource management: decides which machine runs which task", 16, "#DDF1E7", anchor="middle")
    for i, (n, d) in enumerate([("MapReduce", "batch processing"), ("Spark", "fast in-memory processing"), ("Tez", "optimised batch DAGs")]):
        x = 40 + i * 258
        s.rect(x, 340, 244, 84, P["orange"] if i != 1 else P["red"], None, 0, 14)
        s.text(x + 122, 376, n, 22, "#FFFFFF", "bold", "middle"); s.text(x + 122, 402, d, 14, "#FFF1EE", anchor="middle")
    for i, (n, d) in enumerate([("Hive", "SQL on Hadoop"), ("Pig", "dataflow scripts"), ("HBase", "NoSQL on HDFS")]):
        x = 40 + i * 258
        s.rect(x, 230, 244, 90, P["purple"], None, 0, 14)
        s.text(x + 122, 268, n, 22, "#FFFFFF", "bold", "middle"); s.text(x + 122, 296, d, 14, "#E8E0FA", anchor="middle")
    s.text(40, 214, "TOOLS FOR USERS", 13, P["purple"], "bold"); s.text(40, 328 - 0, "", 1)
    s.rect(850, 130, 310, 500, "#FFFFFF", P["grey"], 2.5, 16)
    s.text(1005, 164, "Around the stack", 19, P["navy"], "bold", "middle")
    for i, (n, d) in enumerate([("Sqoop", "import from SQL databases"), ("Flume / Kafka", "ingest logs and streams"), ("Oozie", "schedule workflows"), ("ZooKeeper", "coordinate the cluster"), ("Ranger / Kerberos", "security")]):
        y = 190 + i * 86
        s.rect(870, y, 270, 70, P["lgrey"], None, 0, 12)
        s.text(1005, y + 30, n, 18, P["navy"], "bold", "middle"); s.text(1005, y + 54, d, 14, P["grey"], anchor="middle")
    s.text(40, 150, "Spark can run on YARN and read from HDFS:", 16, P["navy"], "bold")
    s.text(40, 174, "the ecosystem is a toolbox, not a single product.", 16, P["navy"])
    s.save(out)


def lazy_dag(out):
    s = S(1200, 700, "Lazy Evaluation and the DAG", "Spark records your steps as a plan. Only an action makes it run.")
    s.rect(40, 120, 560, 330, P["navy"], None, 0, 14)
    lines = [([('df ', "#FFFFFF"), ('= spark.read.parquet(', "#FFFFFF"), ('"sales"', "#7CD6A5"), (')', "#FFFFFF")], "transformation", P["blue"]),
             ([('big ', "#FFFFFF"), ('= df.filter(df.amount > 100)', "#FFFFFF")], "transformation", P["blue"]),
             ([('out ', "#FFFFFF"), ('= big.groupBy(', "#FFFFFF"), ('"region"', "#7CD6A5"), (').sum(', "#FFFFFF"), ('"amount"', "#7CD6A5"), (')', "#FFFFFF")], "transformation", P["blue"]),
             ([('out.show()', "#FFB4A6")], "ACTION", P["orange"])]
    for i, (parts, tag, c) in enumerate(lines):
        y = 166 + i * 66
        s.mono(60, y, parts, 15)
        s.chip(60, y + 10, 140 if tag == "ACTION" else 150, 24, tag, c, size=13)
    s.text(60, 434, "Lines 1-3: nothing runs. Line 4: everything runs.", 14, "#9FB4C2")
    s.rect(650, 120, 510, 330, "#FFFFFF", P["lgrey"], 2, 14)
    s.text(905, 150, "The plan Spark builds (a DAG)", 17, P["navy"], "bold", "middle")
    s.rect(670, 168, 190, 220, P["lblue"], P["blue"], 2, 12, "8 5"); s.text(765, 188, "Stage 1", 14, P["blue"], "bold", "middle")
    s.rect(950, 168, 190, 220, P["lorange"], P["orange"], 2, 12, "8 5"); s.text(1045, 188, "Stage 2", 14, P["orange"], "bold", "middle")
    for i, (t, c) in enumerate([("Read", P["blue"]), ("Filter", P["blue"])]):
        s.rect(700, 210 + i * 80, 130, 52, c, None, 0, 10); s.text(765, 243 + i * 80, t, 17, "#FFFFFF", "bold", "middle")
    s.arrow(765, 264, 765, 288, P["navy"], 3)
    s.rect(980, 210, 130, 52, P["blue"], None, 0, 10); s.text(1045, 243, "GroupBy+Sum", 14, "#FFFFFF", "bold", "middle")
    s.rect(980, 290, 130, 52, P["orange"], None, 0, 10); s.text(1045, 323, "Show", 17, "#FFFFFF", "bold", "middle")
    s.arrow(1045, 264, 1045, 288, P["navy"], 3)
    s.arrow(832, 340, 976, 238, P["red"], 3)
    s.text(906, 300, "SHUFFLE", 13, P["red"], "bold", "middle")
    s.text(906, 318, "(data moves)", 12, P["red"], anchor="middle")
    s.rect(40, 480, 1120, 190, P["lgold"], None, 0, 14)
    s.text(70, 520, "Why lazy is smart", 19, P["navy"], "bold")
    for i, t in enumerate(["Spark sees the WHOLE plan before running, so it can optimise it (reorder, skip, combine steps).",
                           "A shuffle splits the plan into stages. Stages are made of tasks, one task per partition.",
                           "If a machine fails, Spark replays the recorded steps (the lineage) to rebuild lost data."]):
        s.tick(80, 556 + i * 36, 8); s.text(100, 562 + i * 36, t, 16, P["navy"])
    s.save(out)


def narrow_wide(out):
    s = S(1200, 600, "Narrow vs Wide Transformations", "Does a step need data from other partitions? If yes, Spark must shuffle.")
    for pi, (x0, title, c, wide, ex, note) in enumerate([(40, "Narrow: no data movement", P["green"], False, "filter · select · withColumn · map", "Each output partition depends on ONE input partition. Fast."),
                                                     (620, "Wide: shuffle across the network", P["red"], True, "groupBy · join · distinct · orderBy", "Each output partition depends on MANY input partitions. Costly.")]):
        s.card(x0, 120, 540, 400, title, "#FFFFFF", c)
        s.text(x0 + 90, 190, "Input", 14, P["grey"], "bold", "middle"); s.text(x0 + 450, 190, "Output", 14, P["grey"], "bold", "middle")
        for k in range(3):
            y = 210 + k * 80
            s.rect(x0 + 40, y, 100, 52, P["lblue"], P["blue"], 2, 10); s.text(x0 + 90, y + 32, f"P{k+1}", 17, P["navy"], "bold", "middle")
            s.rect(x0 + 400, y, 100, 52, P["lorange"], P["orange"], 2, 10); s.text(x0 + 450, y + 32, f"P{k+1}'", 17, P["navy"], "bold", "middle")
            if wide:
                for j in range(3): s.arrow(x0 + 142, y + 26, x0 + 398, 210 + j * 80 + 26, c, 2)
            else:
                s.arrow(x0 + 142, y + 26, x0 + 398, y + 26, c, 3)
        s.text(x0 + 270, 480, ex, 16, c, "bold", "middle")
        s.text(x0 + 270, 504, "", 1)
    s.rect(40, 535, 1120, 44, P["navy"], None, 0, 12)
    s.text(600, 564, "Good Spark code keeps shuffles to a minimum.", 19, "#FFFFFF", "bold", "middle")
    s.save(out)


def spark_ecosystem(out):
    s = S(1200, 700, "The Spark Ecosystem", "One engine, many workloads.")
    s.text(40, 140, "WRITE IN", 13, P["grey"], "bold")
    for i, t in enumerate(["Python", "SQL", "Scala", "Java", "R"]): s.chip(40 + i * 150, 152, 136, 34, t, P["lgrey"], P["navy"], 16, P["mid"])
    libs = [("Spark SQL &\nDataFrames", P["orange"]), ("Structured\nStreaming", P["blue"]), ("MLlib\nmachine learning", P["green"]), ("GraphX\ngraph processing", P["purple"])]
    for i, (t, c) in enumerate(libs):
        x = 40 + i * 282
        s.rect(x, 220, 266, 100, c, None, 0, 14)
        for k, l in enumerate(t.split("\n")): s.text(x + 133, 262 + k * 26, l, 21 if k == 0 else 15, "#FFFFFF", "bold" if k == 0 else "normal", "middle")
    s.rect(40, 340, 1120, 110, P["navy"], None, 0, 14)
    s.text(600, 382, "Spark Core", 28, "#FFFFFF", "bold", "middle")
    s.text(600, 414, "task scheduling · memory management · fault recovery · RDDs", 16, "#9FB4C2", anchor="middle")
    s.text(40, 484, "RUNS ON", 13, P["grey"], "bold")
    for i, t in enumerate(["Standalone", "YARN", "Kubernetes", "Local (your laptop)"]): s.chip(40 + i * 280, 496, 262, 36, t, P["lblue"], P["blue"], 16, P["blue"])
    s.text(40, 568, "READS FROM", 13, P["grey"], "bold")
    for i, t in enumerate(["HDFS", "S3 / ADLS / GCS", "Kafka", "JDBC databases", "Delta / Parquet"]):
        s.chip(40 + i * 226, 580, 210, 36, t, P["lgreen"], P["green"], 15, P["green"])
    s.text(600, 666, "Batch, SQL, streaming and ML share the same engine, the same API ideas and the same cluster.", 17, P["navy"], "bold", "middle")
    s.save(out)


def pyspark_arch(out):
    s = S(1200, 640, "How PySpark Works", "Your Python code is a remote control. The real work runs in the JVM on the cluster.")
    st = [("Your Python code", "df.filter(...) then .groupBy(...)", P["blue"]), ("PySpark API + Py4J", "translates calls into JVM calls", P["purple"]),
          ("Spark driver (JVM)", "optimises plan, builds DAG", P["orange"]), ("Executors (JVM)", "run tasks on partitions", P["green"])]
    for i, (a, b, c) in enumerate(st):
        x = 40 + i * 285
        s.rect(x, 150, 255, 190, "#FFFFFF", c, 3, 16)
        s.rect(x, 150, 255, 52, c, None, 0, 16); s.rect(x, 180, 255, 22, c, None, 0, 0)
        s.badge(x + 30, 176, str(i + 1), "#FFFFFF", 14); s.text(x + 30, 182, str(i + 1), 15, c, "bold", "middle")
        s.text(x + 150, 183, a, 17 if len(a) < 20 else 15, "#FFFFFF", "bold", "middle")
        for k, l in enumerate(wrap(b, 24)): s.text(x + 127, 250 + k * 22, l, 16, P["navy"], anchor="middle")
        if i < 3: s.arrow(x + 257, 245, x + 283, 245, P["navy"], 3)
    s.text(167, 310, "runs in Python", 13, P["blue"], "bold", "middle"); s.text(452, 310, "the bridge", 13, P["purple"], "bold", "middle")
    s.text(737, 310, "runs in the JVM", 13, P["orange"], "bold", "middle"); s.text(1022, 310, "runs in the JVM", 13, P["green"], "bold", "middle")
    s.rect(780, 370, 380, 90, P["lgrey"], P["mid"], 2, 12, "8 5")
    s.text(970, 402, "Python workers (only when needed)", 15, P["navy"], "bold", "middle")
    s.text(970, 428, "used by Python UDFs; data is copied", 14, P["grey"], anchor="middle"); s.text(970, 448, "between the JVM and Python", 14, P["grey"], anchor="middle")
    s.arrow(1022, 342, 1000, 366, P["mid"], 2.5, "6 4")
    s.rect(40, 370, 700, 90, P["lgreen"], P["green"], 2, 12)
    s.text(60, 404, "Built-in DataFrame operations run entirely in the JVM:", 16, P["navy"], "bold")
    s.text(60, 430, "PySpark speed is close to Scala for these. Python only describes the work.", 16, P["navy"])
    s.rect(40, 495, 1120, 110, P["navy"], None, 0, 14)
    s.text(70, 535, "Practical rules", 19, "#FFFFFF", "bold")
    s.text(70, 565, "Prefer built-in functions over Python UDFs  ·  Avoid collect() on big data  ·  Use pandas UDFs when you need Python logic", 15, "#C8D6E0")
    s.text(70, 590, "Install locally with  pip install pyspark  (needs Java).", 15, "#C8D6E0")
    s.save(out)


def timeline(out):
    s = S(1200, 740, "A Timeline of Big Data Processing", "Each milestone solved a problem the previous one could not.")
    ev = [("1970", "Relational model", "Codd proposes tables and SQL-style relations", P["blue"]),
          ("1985", "Excel", "Spreadsheets reach every desk", P["green"]),
          ("1995", "MySQL", "Open-source SQL database released", P["blue"]),
          ("2003-04", "Google papers", "GFS and MapReduce describe distributed storage and processing", P["gold"]),
          ("2006", "Hadoop", "Open-source HDFS + MapReduce", P["gold"]),
          ("2010", "Spark open-sourced", "Born at UC Berkeley's AMPLab in 2009", P["orange"]),
          ("2013", "YARN & Databricks", "Hadoop 2 adds YARN; Databricks is founded", P["orange"]),
          ("2014", "Spark 1.0", "Becomes a top-level Apache project", P["orange"]),
          ("2019", "Delta Lake", "Open-sourced: reliable tables on data lakes", P["red"]),
          ("2021", "Lakehouse paper", "The lakehouse architecture is formalised", P["red"])]
    s.line(60, 380, 1140, 380, P["navy"], 6)
    for i, (y, t, d, c) in enumerate(ev):
        x = 122 + i * 108
        up = i % 2 == 0
        s.circle(x, 380, 13, c, P["navy"], 3)
        cy = 150 if up else 440
        s.line(x, 380 - (0 if not up else 0), x, cy + (150 if up else 0), c, 3)
        s.rect(x - 92, cy, 184, 150, "#FFFFFF", c, 3, 12)
        s.text(x, cy + 30, y, 20, c, "bold", "middle")
        s.text(x, cy + 54, t, 15, P["navy"], "bold", "middle")
        for k, l in enumerate(wrap(d, 22)[:4]): s.text(x, cy + 78 + k * 17, l, 12, P["grey"], anchor="middle")
    for i, (c, t) in enumerate([(P["blue"], "Single machine & databases"), (P["gold"], "Hadoop era"), (P["orange"], "Spark era"), (P["red"], "Lakehouse era")]):
        s.rect(60 + i * 290, 690, 16, 16, c, None, 0, 4); s.text(84 + i * 290, 704, t, 15, P["navy"], "bold")
    s.save(out)


def modern_stack(out):
    s = S(1200, 720, "A Modern Data Platform at a Glance", "The five lifecycle stages, with example tools for each.")
    cols = [("Sources", ["Apps", "Databases", "IoT sensors", "SaaS & logs"], P["grey"]),
            ("Ingest", ["Kafka", "CDC (Debezium)", "Auto Loader", "Airbyte"], P["blue"]),
            ("Store", ["S3 / ADLS / GCS", "Delta Lake", "Parquet"], P["green"]),
            ("Process", ["Apache Spark", "SQL / dbt", "Apache Flink"], P["orange"]),
            ("Serve", ["SQL warehouse", "Gold tables", "APIs"], P["purple"]),
            ("Consume", ["BI dashboards", "ML models", "Applications"], P["red"])]
    for i, (n, tools, c) in enumerate(cols):
        x = 40 + i * 190
        s.rect(x, 130, 170, 330, "#FFFFFF", c, 3, 14)
        s.rect(x, 130, 170, 50, c, None, 0, 14); s.rect(x, 160, 170, 20, c, None, 0, 0)
        s.text(x + 85, 163, n, 20, "#FFFFFF", "bold", "middle")
        for k, t in enumerate(tools): s.chip(x + 12, 200 + k * 56, 146, 40, t, P["lgrey"], P["navy"], 14, P["mid"])
        if i < 5: s.arrow(x + 172, 295, x + 188, 295, P["navy"], 3)
    bars = [("Orchestration: Airflow, Databricks Jobs", P["navy"]), ("Governance & security: Unity Catalog, IAM, encryption", P["grey"]),
            ("Monitoring & data quality: alerts, tests, lineage", P["mid"])]
    for i, (t, c) in enumerate(bars):
        s.rect(40, 485 + i * 58, 1120, 46, c, None, 0, 12); s.text(600, 515 + i * 58, t, 17, "#FFFFFF", "bold", "middle")
    s.text(600, 690, "Tool names are examples. The stages stay the same when the tools change.", 16, P["grey"], anchor="middle", italic=True)
    s.save(out)


ALL = [("04-distributed-building-blocks", building_blocks), ("04-parallel-speedup", parallel_speedup),
       ("05-hdfs-architecture", hdfs_arch), ("05-mapreduce-word-count", mapreduce), ("05-hadoop-ecosystem", hadoop_ecosystem),
       ("06-lazy-evaluation-dag", lazy_dag), ("06-narrow-vs-wide", narrow_wide), ("06-spark-ecosystem", spark_ecosystem),
       ("07-pyspark-architecture", pyspark_arch), ("08-timeline", timeline), ("09-modern-data-platform", modern_stack)]
