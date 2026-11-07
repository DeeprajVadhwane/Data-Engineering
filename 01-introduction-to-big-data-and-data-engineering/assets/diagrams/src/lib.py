"""Tiny SVG drawing toolkit used to produce the course diagrams."""
from html import escape

P = dict(bg="#FAF8F5", navy="#0B2026", ink="#1B3139", orange="#FF5F46", lorange="#FFE6E0",
         blue="#2272B4", lblue="#DCEBF7", green="#1B8A5A", lgreen="#DDF1E7", grey="#5F7281",
         lgrey="#E8ECEF", gold="#E8A317", lgold="#FFF3D6", white="#FFFFFF", red="#D93A25",
         purple="#6C4FBF", lpurple="#ECE6FA", mid="#9AA8B4")
FONT = "Helvetica, Arial, 'DejaVu Sans', sans-serif"


class S:
    def __init__(self, w, h, title=None, sub=None):
        self.w, self.h, self.e, self.colors = w, h, [], set()
        self.add(f'<rect width="{w}" height="{h}" rx="16" fill="{P["bg"]}"/>')
        if title:
            self.text(40, 54, title, 30, P["navy"], "bold")
            self.add(f'<rect x="40" y="64" width="64" height="5" rx="2.5" fill="{P["orange"]}"/>')
        if sub:
            self.text(40, 98, sub, 17, P["grey"])

    def add(self, s): self.e.append(s)

    def rect(self, x, y, w, h, fill="#FFFFFF", stroke=None, sw=2, rx=12, dash=None, op=None):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        da = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' opacity="{op}"' if op else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{st}{da}{o}/>')

    def text(self, x, y, t, size=18, fill=None, weight="normal", anchor="start", italic=False, op=None):
        fill = fill or P["ink"]
        it = ' font-style="italic"' if italic else ""
        o = f' opacity="{op}"' if op else ""
        self.add(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
                 f'fill="{fill}" text-anchor="{anchor}"{it}{o}>{escape(str(t))}</text>')

    def lines(self, x, y, ls, size=17, fill=None, weight="normal", anchor="start", lh=None):
        lh = lh or size * 1.35
        for i, l in enumerate(ls):
            self.text(x, y + i * lh, l, size, fill, weight, anchor)

    def line(self, x1, y1, x2, y2, color="#5F7281", sw=2, dash=None):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{da} stroke-linecap="round"/>')

    def arrow(self, x1, y1, x2, y2, color=None, sw=3, dash=None):
        color = color or P["navy"]
        self.colors.add(color)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{da} '
                 f'stroke-linecap="round" marker-end="url(#ah{color[1:]})"/>')

    def path(self, d, fill="none", stroke=None, sw=2):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.add(f'<path d="{d}" fill="{fill}"{st} stroke-linejoin="round"/>')

    def circle(self, cx, cy, r, fill="#FFFFFF", stroke=None, sw=2):
        st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"{st}/>')

    def badge(self, cx, cy, n, fill=None, r=17):
        self.circle(cx, cy, r, fill or P["orange"])
        self.text(cx, cy + 6, n, 18, "#FFFFFF", "bold", "middle")

    def chip(self, x, y, w, h, t, fill, fg="#FFFFFF", size=16, stroke=None):
        self.rect(x, y, w, h, fill, stroke, 1.5, h / 2)
        self.text(x + w / 2, y + h / 2 + size * 0.35, t, size, fg, "bold", "middle")

    def card(self, x, y, w, h, head, fill, headfill, headfg="#FFFFFF", stroke=None, hh=40, size=18):
        self.rect(x, y, w, h, fill, stroke or headfill, 2, 14)
        self.add(f'<path d="M{x},{y+hh} L{x},{y+14} Q{x},{y} {x+14},{y} L{x+w-14},{y} Q{x+w},{y} {x+w},{y+14} L{x+w},{y+hh} Z" fill="{headfill}"/>')
        self.text(x + w / 2, y + hh / 2 + size * 0.35, head, size, headfg, "bold", "middle")

    # ---------- icons ----------
    def db(self, x, y, w=60, h=72, fill=None, stroke=None):
        fill, stroke = fill or P["lblue"], stroke or P["navy"]
        ry = h * 0.14; rx = w / 2
        self.add(f'<ellipse cx="{x+rx}" cy="{y+h-ry}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        self.add(f'<rect x="{x}" y="{y+ry}" width="{w}" height="{h-2*ry}" fill="{fill}"/>')
        self.line(x, y + ry, x, y + h - ry, stroke, 2); self.line(x + w, y + ry, x + w, y + h - ry, stroke, 2)
        self.add(f'<ellipse cx="{x+rx}" cy="{y+ry}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        self.path(f"M{x},{y+h*0.45} A{rx},{ry} 0 0 0 {x+w},{y+h*0.45}", stroke=stroke, sw=1.5)

    def server(self, x, y, w=100, h=70, dead=False):
        base = "#9AA8B4" if dead else "#4F7CA8"
        self.rect(x, y, w, h, base, P["navy"], 2, 8)
        uh = h / 3
        for i in range(3):
            yy = y + i * uh
            if i: self.line(x + 4, yy, x + w - 4, yy, P["navy"], 1)
            self.rect(x + 10, yy + uh / 2 - 4, w * 0.45, 8, "#DCEBF7", None, 0, 3)
            self.circle(x + w - 22, yy + uh / 2, 4, "#7CD6A5" if not dead else "#C8D0D7")
            self.circle(x + w - 36, yy + uh / 2, 4, "#FF8C7A" if not dead else "#C8D0D7")

    def hdd(self, x, y, s=46):
        self.rect(x, y, s, s, "#FFFFFF", P["navy"], 2, 8)
        self.circle(x + s / 2, y + s / 2, s * 0.30, "#E8ECEF", P["navy"], 1.5)
        self.circle(x + s / 2, y + s / 2, s * 0.07, P["navy"])
        self.line(x + s / 2, y + s / 2, x + s * 0.80, y + s * 0.22, P["navy"], 2)

    def ram(self, x, y, w=58, h=28):
        self.rect(x, y, w, h, "#8ED16F", P["navy"], 1.5, 3)
        for i in range(4):
            self.rect(x + 6 + i * 13, y + 5, 9, 11, P["navy"], None, 0, 2)
        for i in range(10):
            self.rect(x + 4 + i * 5.2, y + h - 5, 3, 5, P["gold"], None, 0, 0)

    def person(self, x, y, s=44, color=None):
        color = color or P["red"]
        self.circle(x + s / 2, y + s * 0.28, s * 0.2, "#FFFFFF", color, 3)
        self.path(f"M{x+s*0.12},{y+s} Q{x+s*0.12},{y+s*0.55} {x+s/2},{y+s*0.55} Q{x+s*0.88},{y+s*0.55} {x+s*0.88},{y+s}",
                  "#FFFFFF", color, 3)

    def building(self, x, y, w=80, h=100):
        self.rect(x, y, w, h, "#FFFFFF", P["navy"], 2.5, 4)
        self.rect(x + w * 0.1, y - 18, w * 0.8, 18, P["blue"], P["navy"], 2, 3)
        for r in range(4):
            for c in range(3):
                col = P["gold"] if (r + c) % 2 == 0 else P["blue"]
                self.rect(x + 10 + c * (w - 20) / 3, y + 12 + r * 20, (w - 20) / 3 - 6, 12, col, None, 0, 2)

    def grid(self, x, y, w, h, rows=3, cols=4, fill=None):
        fill = fill or P["blue"]
        self.rect(x, y, w, h, fill, P["navy"], 2, 4)
        for i in range(1, rows): self.line(x, y + i * h / rows, x + w, y + i * h / rows, P["navy"], 2)
        for j in range(1, cols): self.line(x + j * w / cols, y, x + j * w / cols, y + h, P["navy"], 2)

    def notebook(self, x, y, w=70, h=90):
        self.rect(x, y, w, h, "#FFFFFF", P["navy"], 2.5, 6)
        for i in range(5):
            self.circle(x + 8, y + 14 + i * 16, 4, P["mid"], P["navy"], 1.5)
        for i in range(5):
            self.line(x + 24, y + 20 + i * 14, x + w - 10, y + 20 + i * 14, P["mid"], 2)

    def warehouse(self, x, y, w=100, h=80):
        self.path(f"M{x},{y+h*0.3} L{x+w/2},{y} L{x+w},{y+h*0.3} Z", P["blue"], P["navy"], 2.5)
        self.rect(x + 4, y + h * 0.3, w - 8, h * 0.7, "#FFFFFF", P["navy"], 2.5, 2)
        self.rect(x + w * 0.25, y + h * 0.5, w * 0.5, h * 0.5, P["lblue"], P["navy"], 2, 2)
        for i in range(1, 4): self.line(x + w * 0.25, y + h * 0.5 + i * h * 0.125, x + w * 0.75, y + h * 0.5 + i * h * 0.125, P["navy"], 1.5)

    def cloud(self, x, y, w=120, h=70, fill=None):
        fill = fill or P["lblue"]
        self.add(f'<g fill="{fill}" stroke="{P["navy"]}" stroke-width="2">'
                 f'<ellipse cx="{x+w*0.3}" cy="{y+h*0.62}" rx="{w*0.25}" ry="{h*0.32}"/>'
                 f'<ellipse cx="{x+w*0.52}" cy="{y+h*0.4}" rx="{w*0.26}" ry="{h*0.38}"/>'
                 f'<ellipse cx="{x+w*0.72}" cy="{y+h*0.62}" rx="{w*0.26}" ry="{h*0.32}"/></g>')
        self.add(f'<rect x="{x+w*0.3}" y="{y+h*0.55}" width="{w*0.42}" height="{h*0.4}" fill="{fill}"/>')
        self.add(f'<ellipse cx="{x+w*0.5}" cy="{y+h*0.55}" rx="{w*0.3}" ry="{h*0.15}" fill="{fill}"/>')

    def cross(self, cx, cy, r=14, color=None):
        color = color or P["red"]
        self.line(cx - r, cy - r, cx + r, cy + r, color, 5); self.line(cx - r, cy + r, cx + r, cy - r, color, 5)

    def tick(self, cx, cy, r=12, color=None):
        color = color or P["green"]
        self.path(f"M{cx-r},{cy} L{cx-r*0.3},{cy+r*0.8} L{cx+r},{cy-r*0.8}", stroke=color, sw=5)

    def save(self, path):
        defs = "".join(f'<marker id="ah{c[1:]}" markerWidth="12" markerHeight="12" refX="11" refY="6" orient="auto" '
                       f'markerUnits="userSpaceOnUse"><path d="M0,0 L12,6 L0,12 z" fill="{c}"/></marker>' for c in self.colors)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}">'
               f'<defs>{defs}</defs>{"".join(self.e)}</svg>')
        open(path, "w").write(svg)
