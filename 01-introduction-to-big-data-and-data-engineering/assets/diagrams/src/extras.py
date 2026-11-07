"""Extra icons and helpers on top of lib.S."""
import textwrap
from lib import S, P


def wrap(t, n): return textwrap.wrap(t, n)


def gauge(self, cx, cy, r, color=None):
    color = color or P["orange"]
    self.path(f"M{cx-r},{cy} A{r},{r} 0 0 1 {cx+r},{cy}", "none", P["lgrey"], 9)
    self.path(f"M{cx-r},{cy} A{r},{r} 0 0 1 {cx+r*0.5},{cy-r*0.87}", "none", color, 9)
    self.line(cx, cy, cx + r * 0.5, cy - r * 0.62, P["navy"], 4)
    self.circle(cx, cy, 6, P["navy"])


def doc(self, x, y, w=50, h=64, color=None):
    color = color or P["blue"]
    self.path(f"M{x},{y} L{x+w-14},{y} L{x+w},{y+14} L{x+w},{y+h} L{x},{y+h} Z", "#FFFFFF", P["navy"], 2.5)
    self.path(f"M{x+w-14},{y} L{x+w-14},{y+14} L{x+w},{y+14}", "none", P["navy"], 2)
    for i in range(4):
        self.line(x + 9, y + 26 + i * 9, x + w - 9, y + 26 + i * 9, color, 3)


def photo(self, x, y, w=64, h=50):
    self.rect(x, y, w, h, P["lblue"], P["navy"], 2.5, 6)
    self.circle(x + w * 0.75, y + h * 0.3, h * 0.11, P["gold"])
    self.path(f"M{x+4},{y+h-4} L{x+w*0.35},{y+h*0.35} L{x+w*0.6},{y+h*0.7} L{x+w*0.75},{y+h*0.55} L{x+w-4},{y+h-4} Z", P["green"])


def table_icon(self, x, y, w, h, rows=4, cols=4, hl_row=None, hl_col=None):
    self.rect(x, y, w, h, "#FFFFFF", P["navy"], 2, 4)
    if hl_row is not None:
        self.rect(x, y + hl_row * h / rows, w, h / rows, P["orange"], None, 0, 0, op=0.45)
    if hl_col is not None:
        self.rect(x + hl_col * w / cols, y, w / cols, h, P["orange"], None, 0, 0, op=0.45)
    for i in range(1, rows): self.line(x, y + i * h / rows, x + w, y + i * h / rows, P["mid"], 1.5)
    for j in range(1, cols): self.line(x + j * w / cols, y, x + j * w / cols, y + h, P["mid"], 1.5)
    self.rect(x, y, w, h, "none", P["navy"], 2, 4)


def mono(self, x, y, parts, size=16, fill=None):
    f = "'DejaVu Sans Mono', 'Courier New', monospace"
    spans = "".join(f'<tspan fill="{c}">{t.replace("&","&amp;").replace("<","&lt;")}</tspan>' for t, c in parts)
    self.add(f'<text x="{x}" y="{y}" font-family="{f}" font-size="{size}" font-weight="bold" xml:space="preserve" fill="{fill or P["white"]}">{spans}</text>')


for fn in (gauge, doc, photo, table_icon, mono):
    setattr(S, fn.__name__, fn)
