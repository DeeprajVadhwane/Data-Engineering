"""Module 03 diagrams (SVG). Palette: blue foundations, orange engines/logic, green results, red problems."""
from lib import S, P

NAVY, INK, GREY = P["navy"], P["ink"], P["grey"]
NB = "\u00a0"


def nb(t):
    return t.replace("  ", NB * 2)



def box(s, x, y, w, h, lines, fill, stroke, size=17, fg=None, bold_first=True):
    s.rect(x, y, w, h, fill, stroke, 2, 12)
    n = len(lines)
    top = y + h / 2 - (n - 1) * size * 0.68 + size * 0.33
    for i, l in enumerate(lines):
        s.text(x + w / 2, top + i * size * 1.35, l, size, fg or INK, "bold" if (i == 0 and bold_first) else "normal", "middle")


def flow(s, y, items, x0=40, w=190, h=100, gap=40, size=17):
    """Horizontal row of boxes joined by arrows. items = (title, [sub lines], fill, stroke)."""
    for i, (t, sub, f, c) in enumerate(items):
        x = x0 + i * (w + gap)
        box(s, x, y, w, h, [t] + sub, f, c, size)
        if i < len(items) - 1:
            s.arrow(x + w + 2, y + h / 2, x + w + gap - 2, y + h / 2, NAVY, 3)


def cells(s, x, y, items, cw=70, ch=56, hl=(), fill="#FFFFFF", stroke=None, size=22, neg=True):
    n = len(items)
    for i, it in enumerate(items):
        f = P["lgold"] if i in hl else fill
        s.rect(x + i * cw, y, cw, ch, f, stroke or P["blue"], 2, 0)
        s.text(x + i * cw + cw / 2, y + ch * 0.66, str(it), size, NAVY, "bold", "middle")
        s.text(x + i * cw + cw / 2, y - 10, str(i), 15, P["blue"], "bold", "middle")
        if neg:
            s.text(x + i * cw + cw / 2, y + ch + 22, str(i - n), 15, P["orange"], "bold", "middle")


def table(s, x, y, cols, rows, cw, rh=30, head=None, size=15):
    head = head or P["blue"]
    w = cw * len(cols)
    s.rect(x, y, w, rh, head, NAVY, 1.5, 4)
    for j, c in enumerate(cols):
        s.text(x + j * cw + cw / 2, y + rh * 0.68, c, size, "#FFFFFF", "bold", "middle")
    for i, r in enumerate(rows):
        s.rect(x, y + rh * (i + 1), w, rh, "#FFFFFF", NAVY, 1, 0)
        for j, c in enumerate(r):
            s.text(x + j * cw + cw / 2, y + rh * (i + 1) + rh * 0.68, c, size, INK, "normal", "middle")


def d00_banner(path):
    s = S(1200, 320)
    s.text(60, 120, "Python for Data Engineers", 54, NAVY, "bold")
    s.add(f'<rect x="60" y="140" width="110" height="7" rx="3.5" fill="{P["orange"]}"/>')
    s.text(60, 192, "From the first print() to a working data application", 24, GREY)
    s.text(60, 240, "Module 03  |  19 topics  |  Python 3", 20, P["blue"], "bold")
    s.grid(800, 70, 300, 180, 4, 4, P["lblue"])
    s.chip(830, 270, 100, 30, "def", P["blue"], size=14)
    s.chip(940, 270, 100, 30, "class", P["orange"], size=14)
    s.chip(1050, 270, 90, 30, "with", P["green"], size=14)
    s.save(path)


def d00_roadmap(path):
    s = S(1200, 640, "Learning roadmap", "19 topics in six stages. Each builds on the one before")
    names = ["Intro", "Types", "Operators", "Lists", "Tuples, sets", "Dictionary", "Strings I", "Conditions", "While loops",
             "Strings II", "Comprehensions", "Functions I", "Functions II", "Classes", "Inheritance", "Polymorphism",
             "Files, errors", "Streamlit", "Review"]
    cols = [P["blue"]] * 3 + [P["orange"]] * 3 + [P["green"]] * 5 + [P["purple"]] * 2 + [P["gold"]] * 3 + [P["grey"]] * 3
    for i, n in enumerate(names):
        r, c = divmod(i, 5)
        x, y = 40 + c * 228, 140 + r * 115
        s.rect(x, y, 200, 85, "#FFFFFF", cols[i], 3, 14)
        s.badge(x + 28, y + 28, f"{i+1:02d}", cols[i], 18)
        s.text(x + 100, y + 68, n, 19, NAVY, "bold", "middle")
    x = 40
    for lab, c in [("Foundations 01-03", P["blue"]), ("Collections 04-06", P["orange"]), ("Text and control 07-11", P["green"]),
                   ("Functions 12-13", P["purple"]), ("OOP 14-16", P["gold"]), ("Files, apps 17-19", P["grey"])]:
        w = 14 + len(lab) * 8
        s.chip(x, 600, w, 28, lab, c, size=13)
        x += w + 14
    s.save(path)


def d01_pipeline(path):
    s = S(1200, 440, "Where Python sits in a data platform", "Python connects, controls and checks. SQL engines do the heavy transformation")
    s.rect(40, 130, 1120, 250, P["lblue"], P["blue"], 2, 18)
    s.text(60, 158, "Python: fetch, validate, orchestrate, retry, log, alert", 18, P["blue"], "bold")
    flow(s, 190, [("Sources", ["files, APIs,", "databases"], P["lgrey"], GREY), ("Ingest", ["Python reads", "and checks"], "#FFFFFF", P["blue"]),
                  ("Transform", ["SQL / Spark", "engine"], P["lorange"], P["orange"]), ("Gold tables", ["clean, modelled"], P["lgreen"], P["green"]),
                  ("Consumers", ["dashboards,", "Streamlit"], P["lgold"], P["gold"])], x0=60, w=175, h=110, gap=40)
    s.text(60, 345, "Same job, two tools: SQL for set-based work inside the engine, Python for everything around it.", 16, INK)
    s.save(path)


def d01_runs(path):
    s = S(1200, 330, "How Python runs your code", "Compile to bytecode once, then the virtual machine executes it")
    flow(s, 140, [("Source code", [".py file or", "notebook cell"], P["lblue"], P["blue"]), ("Compiler", ["checks syntax,", "makes bytecode"], P["lorange"], P["orange"]),
                  ("Bytecode", ["compact internal", "instructions"], P["lgrey"], GREY), ("Python VM", ["runs one", "instruction at a time"], P["lorange"], P["orange"]),
                  ("Output", ["results, files,", "side effects"], P["lgreen"], P["green"])], x0=40, w=185, h=110, gap=48)
    s.text(40, 296, "CPython is the standard implementation. Heavy numeric work is left to engines such as SQL, Spark and pandas.", 16, GREY)
    s.save(path)


def d02_names(path):
    s = S(1200, 440, "A name is a label attached to a value", "Assignment binds a name to an object. It does not put the value inside the name")
    rows = [("quantity", "int", "10"), ("price", "float", "499.99"), ("region", "str", "'West'"), ("city", "str", "'West'")]
    for i, (n, t, v) in enumerate(rows):
        y = 140 + i * 62
        s.chip(60, y, 150, 38, n, P["blue"], size=17)
    s.arrow(212, 159, 480, 159, NAVY, 2.5)
    s.arrow(212, 221, 480, 221, NAVY, 2.5)
    s.arrow(212, 283, 480, 283, NAVY, 2.5)
    s.arrow(212, 345, 480, 296, NAVY, 2.5)
    box(s, 485, 134, 200, 50, ["int", "10"], P["lgreen"], P["green"], 15)
    box(s, 485, 196, 200, 50, ["float", "499.99"], P["lgreen"], P["green"], 15)
    box(s, 485, 258, 200, 56, ["str", "'West'"], P["lgreen"], P["green"], 15)
    s.card(740, 140, 400, 230, "Remember", P["lgold"], P["gold"], NAVY)
    s.lines(760, 205, ["The type belongs to the value, not the name", "A name can be rebound: x = 10, then x = 'ten'",
                       "Two names can point at the same object", "Names are case sensitive: Total is not total"], 16)
    s.save(path)


def d03_operators(path):
    s = S(1200, 460, "Operator families", "Combine them to build a condition that is True or False")
    fam = [("Arithmetic", nb("+  -  *  /  //  %  **"), P["blue"]), ("Assignment", nb("=  +=  -=  *=  /="), P["blue"]),
           ("Comparison", nb("==  !=  >  <  >=  <="), P["orange"]), ("Logical", nb("and  or  not"), P["orange"]),
           ("Identity", nb("is  is not"), P["purple"])]
    for i, (t, ex, c) in enumerate(fam):
        x = 40 + i * 226
        s.card(x, 130, 206, 110, t, "#FFFFFF", c, hh=38, size=17)
        s.text(x + 103, 205, ex, 14, INK, "bold", "middle")
    s.arrow(600, 250, 600, 300, NAVY, 3)
    box(s, 330, 305, 540, 90, ["amount >= 1000 and status == 'completed'", "-> True or False"], P["lgreen"], P["green"], 18)
    s.text(40, 430, "Precedence: arithmetic first, then comparison, then not, and, or. Use brackets when unsure.", 16, GREY)
    s.save(path)


def d03_is(path):
    s = S(1200, 440, "== compares values, is compares identity", "Two names can share one object, or hold equal but separate objects")
    s.card(40, 130, 540, 270, "One object, two names", P["lblue"], P["blue"])
    s.chip(80, 200, 70, 34, "a", P["blue"]); s.chip(80, 260, 70, 34, "b", P["blue"])
    s.arrow(152, 217, 330, 240, NAVY, 2.5); s.arrow(152, 277, 330, 255, NAVY, 2.5)
    box(s, 335, 215, 200, 60, ["list", "[1, 2, 3]"], "#FFFFFF", P["blue"], 16)
    s.text(80, 345, nb("a == b: True    a is b: True"), 18, P["green"], "bold")
    s.card(620, 130, 540, 270, "Two objects, equal content", P["lorange"], P["orange"])
    s.chip(660, 200, 70, 34, "c", P["orange"]); s.chip(660, 260, 70, 34, "d", P["orange"])
    s.arrow(732, 217, 900, 200, NAVY, 2.5); s.arrow(732, 277, 900, 280, NAVY, 2.5)
    box(s, 905, 175, 200, 55, ["list", "[1, 2, 3]"], "#FFFFFF", P["orange"], 16)
    box(s, 905, 255, 200, 55, ["list", "[1, 2, 3]"], "#FFFFFF", P["orange"], 16)
    s.text(660, 345, nb("c == d: True    c is d: False"), 18, P["red"], "bold")
    s.save(path)


def d04_list(path):
    s = S(1200, 420, "A list: positive and negative indexes", "orders = [120, 80, 300, 150, 90]")
    cells(s, 160, 170, [120, 80, 300, 150, 90], cw=110, ch=64, hl=(1, 2, 3))
    s.text(60, 207, "value", 15, GREY, "bold"); s.text(60, 170 - 12, "index", 15, P["blue"], "bold"); s.text(60, 270, "negative", 15, P["orange"], "bold")
    box(s, 160, 310, 660, 70, ["orders[1:4]  ->  [80, 300, 150]", "start included, stop excluded"], P["lgold"], P["gold"], 17)
    box(s, 850, 170, 300, 64, ["orders[-1]  ->  90", "last item"], P["lblue"], P["blue"], 16)
    s.save(path)


def d05_sets(path):
    s = S(1200, 460, "Set operations", "A = customers who ordered in November, B = customers who ordered in December")
    s.circle(330, 250, 120, P["lblue"], P["blue"], 3)
    s.circle(470, 250, 120, P["lorange"], P["orange"], 3)
    s.add(f'<clipPath id="cs"><circle cx="330" cy="250" r="120"/></clipPath><circle clip-path="url(#cs)" cx="470" cy="250" r="120" fill="{P["green"]}" opacity="0.8"/>')
    s.text(270, 255, "A only", 18, NAVY, "bold", "middle"); s.text(530, 255, "B only", 18, NAVY, "bold", "middle"); s.text(400, 255, "both", 18, "#FFFFFF", "bold", "middle")
    ops = [("A | B", "union: in either", P["blue"]), ("A & B", "intersection: in both", P["green"]),
           ("A - B", "difference: in A, not in B", P["orange"]), ("A ^ B", "symmetric difference: in one only", P["purple"])]
    for i, (o, d, c) in enumerate(ops):
        y = 140 + i * 72
        s.chip(700, y, 110, 40, o, c, size=19)
        s.text(830, y + 27, d, 17, INK)
    s.text(700, 440, "Sets also remove duplicates: set([1, 1, 2]) is {1, 2}", 15, GREY)
    s.save(path)


def d06_dict(path):
    s = S(1200, 440, "A dictionary maps keys to values", "Lookup by key, not by position")
    pairs = [("'order_id'", "1001"), ("'customer'", "'Meera Iyer'"), ("'region'", "'West'"), ("'amount'", "1200.5")]
    s.text(100, 140, "keys (unique, immutable)", 16, P["blue"], "bold"); s.text(520, 140, "values (any type)", 16, P["green"], "bold")
    for i, (k, v) in enumerate(pairs):
        y = 158 + i * 66
        box(s, 60, y, 250, 48, [k], P["lblue"], P["blue"], 17)
        box(s, 480, y, 270, 48, [v], P["lgreen"], P["green"], 17)
        s.arrow(312, y + 24, 478, y + 24, NAVY, 2.5)
    s.card(800, 158, 340, 240, "Use it for", P["lgold"], P["gold"], NAVY)
    s.lines(820, 222, ["JSON objects and API responses", "database rows", "configuration", "lookups and counters", "order['amount']  ->  1200.5"], 16)
    s.save(path)


def d06_copy(path):
    s = S(1200, 520, "Shallow versus deep copy", "A shallow copy shares nested objects. A deep copy duplicates everything")
    s.card(40, 130, 540, 340, "copy.copy(a): shared inner list", P["lorange"], P["orange"])
    box(s, 70, 200, 180, 56, ["a", "{'items': *}"], "#FFFFFF", P["orange"], 15)
    box(s, 70, 330, 180, 56, ["b", "{'items': *}"], "#FFFFFF", P["orange"], 15)
    box(s, 380, 262, 170, 56, ["list", "['x', 'y']"], P["lgold"], P["gold"], 16)
    s.arrow(252, 232, 378, 285, NAVY, 2.5); s.arrow(252, 358, 378, 298, NAVY, 2.5)
    s.text(70, 440, "b['items'].append('z') changes a as well", 16, P["red"], "bold")
    s.card(620, 130, 540, 340, "copy.deepcopy(a): independent", P["lgreen"], P["green"])
    box(s, 650, 200, 180, 56, ["a", "{'items': *}"], "#FFFFFF", P["green"], 15)
    box(s, 650, 330, 180, 56, ["b", "{'items': *}"], "#FFFFFF", P["green"], 15)
    box(s, 960, 200, 170, 56, ["list", "['x', 'y']"], P["lgold"], P["gold"], 16)
    box(s, 960, 330, 170, 56, ["list", "['x', 'y']"], P["lgold"], P["gold"], 16)
    s.arrow(832, 228, 958, 228, NAVY, 2.5); s.arrow(832, 358, 958, 358, NAVY, 2.5)
    s.text(650, 440, "b['items'].append('z') leaves a unchanged", 16, P["green"], "bold")
    s.save(path)


def d07_string(path):
    s = S(1200, 440, "A string is a sequence of characters", "code = 'ORD-1001'")
    cells(s, 170, 170, list("ORD-1001"), cw=90, ch=64, hl=(0, 1, 2))
    box(s, 170, 310, 360, 64, ["code[0:3]  ->  'ORD'", "slice stops before position 3"], P["lgold"], P["gold"], 16)
    box(s, 560, 310, 330, 64, ["code[-4:]  ->  '1001'", "last four characters"], P["lblue"], P["blue"], 16)
    box(s, 920, 310, 230, 64, ["code[::-1]", "reversed"], P["lgreen"], P["green"], 16)
    s.text(40, 415, "Strings are immutable: methods return a new string, they never change the original.", 16, GREY)
    s.save(path)


def d08_flow(path):
    s = S(1200, 500, "A condition sends each record down one branch", "order amount classified as High, Medium or Low")
    box(s, 470, 130, 260, 56, ["amount"], P["lblue"], P["blue"], 18)
    s.arrow(600, 188, 600, 220, NAVY, 3)
    s.add(f'<polygon points="600,222 760,282 600,342 440,282" fill="{P["lorange"]}" stroke="{P["orange"]}" stroke-width="3"/>')
    s.text(600, 288, "amount >= 1000 ?", 18, NAVY, "bold", "middle")
    s.arrow(760, 282, 900, 282, NAVY, 3); s.text(810, 270, "yes", 15, P["green"], "bold", "middle")
    box(s, 905, 255, 220, 56, ["High"], P["lgreen"], P["green"], 18)
    s.arrow(600, 344, 600, 380, NAVY, 3); s.text(618, 366, "no", 15, P["red"], "bold")
    s.add(f'<polygon points="600,382 740,425 600,468 460,425" fill="{P["lorange"]}" stroke="{P["orange"]}" stroke-width="3"/>')
    s.text(600, 431, "amount >= 500 ?", 17, NAVY, "bold", "middle")
    s.arrow(740, 425, 900, 425, NAVY, 3); s.text(820, 413, "yes", 15, P["green"], "bold", "middle")
    box(s, 905, 398, 220, 56, ["Medium"], P["lgreen"], P["green"], 18)
    s.arrow(460, 425, 330, 425, NAVY, 3); s.text(395, 413, "no", 15, P["red"], "bold", "middle")
    box(s, 110, 398, 220, 56, ["Low"], P["lgrey"], GREY, 18)
    s.save(path)


def d08_ifelse(path):
    s = S(1200, 420, "if, elif, else", "Python checks the conditions in order and runs only the first block that is True")
    rows = [("if", "status == 'completed'", "count revenue", P["green"]), ("elif", "status == 'cancelled'", "log and skip", P["orange"]),
            ("elif", "status == 'pending'", "hold for later", P["gold"]), ("else", "anything else", "reject, reason: unknown status", P["red"])]
    for i, (k, c, a, col) in enumerate(rows):
        y = 140 + i * 66
        s.chip(60, y, 90, 44, k, col, size=19)
        box(s, 170, y, 380, 44, [c], "#FFFFFF", col, 17, bold_first=False)
        s.arrow(552, y + 22, 640, y + 22, NAVY, 2.5)
        box(s, 645, y, 420, 44, [a], "#FFFFFF", col, 17, bold_first=False)
        if i < 3:
            s.text(110, y + 62, "False", 13, GREY, "bold", "middle")
    s.text(60, 405, "Order matters: a later branch is only reached if every earlier condition was False.", 16, GREY)
    s.save(path)


def d09_while(path):
    s = S(1200, 520, "A while loop", "Test the condition. If True run the body and test again. If False leave")
    box(s, 80, 250, 170, 70, ["Start"], P["lblue"], P["blue"], 18)
    s.arrow(252, 285, 340, 285, NAVY, 3)
    s.add(f'<polygon points="480,210 620,285 480,360 340,285" fill="{P["lorange"]}" stroke="{P["orange"]}" stroke-width="3"/>')
    s.text(480, 291, "condition ?", 18, NAVY, "bold", "middle")
    s.arrow(620, 285, 740, 285, NAVY, 3); s.text(680, 272, "True", 15, P["green"], "bold", "middle")
    box(s, 745, 250, 220, 70, ["Run the body", "change something"], P["lgreen"], P["green"], 16)
    s.line(855, 322, 855, 420, NAVY, 3); s.line(855, 420, 480, 420, NAVY, 3); s.arrow(480, 420, 480, 362, NAVY, 3)
    s.text(670, 445, "back to the test", 15, GREY, "middle")
    s.arrow(480, 210, 480, 182, NAVY, 3); s.text(498, 188, "False", 15, P["red"], "bold")
    box(s, 380, 130, 200, 50, ["Exit the loop"], P["lgrey"], GREY, 17)
    s.chip(1000, 250, 150, 36, "break: leave now", P["red"], size=14); s.chip(1000, 300, 190, 36, "continue: next test", P["gold"], size=14)
    s.save(path)


def d10_ordchr(path):
    s = S(1200, 400, "ord() and chr()", "Every character has a numeric code. ord gives the code, chr gives the character back")
    for i, (c, n) in enumerate([("A", 65), ("B", 66), ("Z", 90), ("a", 97), ("0", 48)]):
        x = 60 + i * 150
        box(s, x, 150, 110, 56, [f"'{c}'"], P["lblue"], P["blue"], 22)
        s.arrow(x + 40, 208, x + 40, 262, P["orange"], 2.5); s.text(x + 14, 240, "ord", 13, P["orange"], "bold")
        s.arrow(x + 70, 262, x + 70, 208, P["green"], 2.5); s.text(x + 76, 240, "chr", 13, P["green"], "bold")
        box(s, x, 264, 110, 56, [str(n)], P["lgold"], P["gold"], 22)
    s.text(60, 365, "Shift a letter by 3:  chr(ord('A') + 3)  ->  'D'", 18, NAVY, "bold")
    s.save(path)


def d11_loopcomp(path):
    s = S(1200, 440, "A comprehension is a loop that builds a collection", "Same result, one line")
    s.card(40, 130, 520, 270, "for loop", P["lgrey"], GREY)
    s.lines(70, 205, [nb(l) for l in ["totals = []", "for amount in amounts:", "    if amount > 0:", "        totals.append(amount * 1.18)"]], 17, INK)
    s.arrow(570, 265, 640, 265, NAVY, 3)
    s.card(650, 130, 510, 270, "comprehension", P["lgreen"], P["green"])
    s.text(680, 245, "totals = [amount * 1.18", 18, NAVY, "bold"); s.text(680, 280, nb("          for amount in amounts"), 18, NAVY, "bold")
    s.text(680, 315, nb("          if amount > 0]"), 18, NAVY, "bold")
    s.text(680, 372, "Use it while it stays easy to read", 15, GREY)
    s.save(path)


def d11_anatomy(path):
    s = S(1200, 400, "Anatomy of a comprehension", "[ expression  for item in iterable  if condition ]")
    parts = [("expression", "what to keep", "amount * 1.18", P["green"], 60, 240), ("for item in iterable", "where from", "for amount in amounts", P["blue"], 340, 330),
             ("if condition", "optional filter", "if amount > 0", P["orange"], 700, 250)]
    for t, d, ex, c, x, w in parts:
        s.card(x, 150, w, 140, t, "#FFFFFF", c, hh=40, size=17)
        s.text(x + w / 2, 225, d, 16, INK, "normal", "middle"); s.text(x + w / 2, 260, ex, 15, c, "bold", "middle")
    s.text(60, 345, "A dict comprehension has the same shape:  { key: value  for item in iterable  if condition }", 16, GREY)
    s.save(path)


def d12_anatomy(path):
    s = S(1200, 380, "A function: inputs, steps, result", "Write the steps once, use them many times")
    box(s, 50, 140, 220, 100, ["Inputs", "arguments"], P["lblue"], P["blue"], 18)
    s.arrow(272, 190, 360, 190, NAVY, 3)
    box(s, 365, 120, 380, 140, ["clean_amount(text)", "strip, remove commas,", "convert to float"], P["lorange"], P["orange"], 18)
    s.arrow(747, 190, 835, 190, NAVY, 3)
    box(s, 840, 140, 220, 100, ["Result", "return value"], P["lgreen"], P["green"], 18)
    s.text(50, 320, "No return statement means the function returns None.", 16, GREY)
    s.save(path)


def d12_terms(path):
    s = S(1200, 420, "Parts of a function", "Definition on top, call below")
    s.rect(60, 130, 1080, 100, "#FFFFFF", P["blue"], 2, 12)
    s.text(90, 190, nb("def  apply_tax ( amount ,  rate = 0.18 ) :   return amount * (1 + rate)"), 22, NAVY, "bold")
    for x, t, c in [(80, "keyword", P["blue"]), (215, "name", P["orange"]), (400, "parameters", P["green"]), (720, "body / return", P["purple"])]:
        s.chip(x, 245, 130 if len(t) < 9 else 150, 30, t, c, size=14)
    s.rect(60, 300, 1080, 80, "#FFFFFF", P["green"], 2, 12)
    s.text(90, 350, nb("apply_tax ( 1200 ,  rate = 0.05 )"), 22, NAVY, "bold")
    s.chip(500, 322, 300, 32, "arguments: positional and keyword", P["green"], size=13)
    s.save(path)


def d13_legb(path):
    s = S(1200, 520, "LEGB: how Python finds a name", "Search from the inside out and stop at the first match")
    layers = [("Built-in", "len, print, sum", P["lgrey"], GREY, 80, 130, 1040, 360), ("Global", "module level", P["lblue"], P["blue"], 130, 170, 940, 300),
              ("Enclosing", "outer function", P["lgold"], P["gold"], 180, 210, 840, 240), ("Local", "current function", P["lgreen"], P["green"], 230, 250, 740, 180)]
    for t, d, f, c, x, y, w, h in layers:
        s.rect(x, y, w, h, f, c, 3, 18)
        s.text(x + 16, y + 28, f"{t}: {d}", 17, NAVY, "bold")
    s.text(260, 340, "Lookup order:  Local  ->  Enclosing  ->  Global  ->  Built-in", 18, NAVY, "bold")
    s.text(260, 375, "global and nonlocal let a function rebind an outer name", 16, GREY)
    s.save(path)


def d13_mfr(path):
    s = S(1200, 460, "map, filter, reduce", "Transform every item, keep some items, or fold all items into one value")
    rows = [("map(f, items)", "transform each", [("10", "12"), ("20", "24"), ("30", "36")], P["blue"], "x * 1.2"),
            ("filter(f, items)", "keep matching", [("10", "x"), ("20", "20"), ("30", "30")], P["orange"], "x > 15"),
            ("reduce(f, items)", "fold to one", [("10", ""), ("20", ""), ("30", "60")], P["green"], "a + b")]
    for i, (t, d, vals, c, fn) in enumerate(rows):
        y = 140 + i * 105
        s.chip(40, y + 10, 190, 38, t, c, size=16)
        s.text(40, y + 72, d, 15, GREY)
        for j, (a, b) in enumerate(vals):
            box(s, 290 + j * 80, y + 8, 64, 42, [a], "#FFFFFF", c, 17)
        s.arrow(540, y + 29, 640, y + 29, NAVY, 2.5); s.text(590, y + 20, fn, 13, c, "bold", "middle")
        res = {"map": ["12", "24", "36"], "filter": ["20", "30"], "reduce": ["60"]}[t.split("(")[0]]
        for j, r in enumerate(res):
            box(s, 650 + j * 80, y + 8, 64, 42, [r], c, c, 17, "#FFFFFF")
    s.save(path)


def d14_class(path):
    s = S(1200, 480, "A class is a blueprint. Objects are built from it", "class Order: attributes hold data, methods hold behaviour")
    s.card(40, 130, 400, 300, "class Order", P["lblue"], P["blue"])
    s.lines(64, 200, ["Attributes", "  order_id, customer, amount", "", "Methods", "  total_with_tax()", "  mark_completed()", "", "__init__ sets the attributes"], 16)
    for i, (o, c, a) in enumerate([("order_a", "Meera Iyer", "1200.0"), ("order_b", "Rohan Shah", "800.0"), ("order_c", "Anika Gupta", "500.0")]):
        y = 130 + i * 100
        s.arrow(442, 280, 560, y + 40, NAVY, 2)
        s.card(565, y, 360, 85, f"{o} = Order(...)", "#FFFFFF", P["green"], hh=34, size=16)
        s.text(580, y + 68, f"customer={c}   amount={a}", 15, INK)
    s.text(960, 200, "One class,", 17, NAVY, "bold"); s.text(960, 226, "many objects.", 17, NAVY, "bold"); s.text(960, 262, "Each object has", 15, GREY); s.text(960, 284, "its own data.", 15, GREY)
    s.save(path)


def d15_hier(path):
    s = S(1200, 460, "Inheritance with abstraction", "The pipeline depends on the base class. Each source supplies its own read()")
    box(s, 400, 120, 400, 110, ["DataSource (abstract)", "read()  <- must be overridden", "describe()  <- shared"], P["lpurple"], P["purple"], 17)
    for i, (n, d) in enumerate([("CsvSource", "read from a CSV file"), ("JsonSource", "read from a JSON file"), ("DbSource", "read from a database")]):
        x = 100 + i * 340
        box(s, x, 320, 300, 90, [n, d, "overrides read()"], P["lgreen"], P["green"], 16)
        s.arrow(600, 232, x + 150, 318, NAVY, 2.5)
    s.text(400, 275, "is-a", 15, GREY, "bold")
    s.save(path)


def d15_types(path):
    s = S(1200, 520, "The five inheritance patterns", "Arrows point from child to parent")

    def node(x, y, t, c=P["blue"]):
        box(s, x, y, 80, 36, [t], "#FFFFFF", c, 16)

    def link(x1, y1, x2, y2):
        s.arrow(x1, y1, x2, y2, NAVY, 2)
    # single
    s.text(100, 150, "Single", 18, NAVY, "bold"); node(60, 180, "A"); node(60, 270, "B"); link(100, 270, 100, 218)
    s.text(300, 150, "Multilevel", 18, NAVY, "bold"); node(260, 175, "A"); node(260, 240, "B"); node(260, 305, "C"); link(300, 240, 300, 213); link(300, 305, 300, 278)
    s.text(520, 150, "Multiple", 18, NAVY, "bold"); node(470, 185, "A"); node(570, 185, "B"); node(520, 290, "C"); link(540, 290, 510, 223); link(560, 290, 600, 223)
    s.text(780, 150, "Hierarchical", 18, NAVY, "bold"); node(780, 185, "A"); node(700, 290, "B"); node(780, 290, "C"); node(860, 290, "D")
    link(740, 290, 800, 223); link(820, 290, 820, 223); link(900, 290, 840, 223)
    s.text(1030, 150, "Hybrid", 18, NAVY, "bold"); node(1030, 185, "A"); node(960, 250, "B"); node(1100, 250, "C"); node(1030, 330, "D")
    link(990, 250, 1050, 223); link(1140, 250, 1090, 223); link(1050, 330, 990, 288); link(1050, 330, 1110, 288)
    s.card(60, 400, 1080, 90, "Method Resolution Order (MRO)", P["lgold"], P["gold"], NAVY, hh=34, size=16)
    s.text(80, 475, "With several parents, Python searches classes in a fixed order. See it with ClassName.__mro__", 15, INK)
    s.save(path)


def d16_poly(path):
    s = S(1200, 480, "Polymorphism and encapsulation", "One call, many behaviours. Data guarded by methods")
    s.card(40, 130, 540, 320, "Polymorphism", P["lblue"], P["blue"])
    box(s, 70, 200, 200, 56, ["pipeline"], "#FFFFFF", P["blue"], 17)
    s.text(70, 285, "source.read()", 18, P["blue"], "bold")
    for i, n in enumerate(["CsvSource.read()", "JsonSource.read()", "DbSource.read()"]):
        y = 190 + i * 75
        box(s, 360, y, 190, 50, [n], P["lgreen"], P["green"], 15)
        s.arrow(272, 228, 358, y + 25, NAVY, 2)
    s.card(620, 130, 540, 320, "Encapsulation", P["lorange"], P["orange"])
    box(s, 650, 200, 200, 200, ["Order object", "_amount  (internal)", "", "@property amount", "getter and setter", "validate before storing"], "#FFFFFF", P["orange"], 15)
    s.lines(880, 250, ["Outside code", "uses order.amount", "never touches", "the internal value", "directly"], 16)
    s.save(path)


def d17_pipeline(path):
    s = S(1200, 520, "A robust file pipeline", "Read, validate, write. Every failure is handled, counted and logged")
    flow(s, 130, [("Read file", ["with open(...)", "utf-8"], P["lblue"], P["blue"]), ("Parse rows", ["csv / json", "module"], P["lblue"], P["blue"]),
                  ("Validate", ["try / except", "per row"], P["lorange"], P["orange"]), ("Write", ["clean file", "with open(...)"], P["lgreen"], P["green"])],
         x0=50, w=230, h=100, gap=60)
    s.arrow(555, 232, 555, 300, P["red"], 2.5)
    box(s, 430, 303, 250, 70, ["rejected rows", "with a reason"], P["lorange"], P["red"], 16)
    s.card(740, 300, 400, 150, "Around the flow", P["lgold"], P["gold"], NAVY, hh=34, size=16)
    s.lines(760, 365, ["logging: counts and errors", "retry for transient failures", "gate: stop if too many rejects"], 15)
    s.text(50, 440, "Files are closed automatically by with, even when an error occurs.", 16, GREY)
    s.save(path)


def d18_rerun(path):
    s = S(1200, 460, "The Streamlit rerun model", "Every interaction runs the whole script again, top to bottom")
    flow(s, 130, [("User", ["changes a widget"], P["lblue"], P["blue"]), ("Script reruns", ["top to bottom"], P["lorange"], P["orange"]),
                  ("Widgets return", ["their new values"], "#FFFFFF", P["blue"]), ("Page redraws", ["table, chart,", "metrics"], P["lgreen"], P["green"])],
         x0=50, w=230, h=100, gap=60)
    s.line(1000, 232, 1000, 290, NAVY, 2.5); s.line(1000, 290, 165, 290, NAVY, 2.5); s.arrow(165, 290, 165, 234, NAVY, 2.5)
    s.text(450, 318, "next interaction starts another run", 15, GREY)
    s.card(50, 350, 520, 90, "@st.cache_data", P["lgreen"], P["green"], hh=32, size=16)
    s.text(70, 420, "expensive loading runs once, answers come from the cache", 15, INK)
    s.card(620, 350, 520, 90, "st.session_state", P["lgold"], P["gold"], NAVY, hh=32, size=16)
    s.text(640, 420, "values that must survive between reruns", 15, INK)
    s.save(path)


def d19_path(path):
    s = S(1200, 520, "The learning path", "Each stage uses the one before")
    stages = [("Foundations", "01-03", P["blue"]), ("Collections", "04-06", P["orange"]), ("Text and control", "07-11", P["green"]),
              ("Functions", "12-13", P["purple"]), ("OOP", "14-16", P["gold"]), ("Files and apps", "17-18", P["grey"])]
    for i, (t, r, c) in enumerate(stages):
        x, h = 40 + i * 190, 90 + i * 40
        y = 440 - h
        s.rect(x, y, 175, h, c, c, 2, 10)
        s.text(x + 87, y + 30, t, 16, "#FFFFFF", "bold", "middle")
        s.text(x + 87, y + 56, f"topics {r}", 14, "#FFFFFF", "normal", "middle")
    s.text(40, 478, "End point: a small, tested data application that reads, cleans, handles failure and shows the result.", 16, INK)
    s.save(path)


ALL = [("00-module-banner", d00_banner), ("00-learning-roadmap", d00_roadmap), ("01-python-in-the-pipeline", d01_pipeline),
       ("01-how-python-runs", d01_runs), ("02-names-and-values", d02_names), ("03-operators-overview", d03_operators),
       ("03-is-vs-equals", d03_is), ("04-list-indexing", d04_list), ("05-set-operations", d05_sets), ("06-dictionary-structure", d06_dict),
       ("06-shallow-vs-deep-copy", d06_copy), ("07-string-indexing", d07_string), ("08-conditional-flow", d08_flow),
       ("08-if-elif-else", d08_ifelse), ("09-while-loop-flow", d09_while), ("10-ord-chr", d10_ordchr),
       ("11-loop-vs-comprehension", d11_loopcomp), ("11-comprehension-anatomy", d11_anatomy), ("12-function-anatomy", d12_anatomy),
       ("12-function-terms", d12_terms), ("13-legb-scopes", d13_legb), ("13-map-filter-reduce", d13_mfr),
       ("14-class-and-objects", d14_class), ("15-connector-hierarchy", d15_hier), ("15-inheritance-types", d15_types),
       ("16-polymorphism-and-encapsulation", d16_poly), ("17-robust-file-pipeline", d17_pipeline),
       ("18-streamlit-rerun-model", d18_rerun), ("19-python-learning-path", d19_path)]
