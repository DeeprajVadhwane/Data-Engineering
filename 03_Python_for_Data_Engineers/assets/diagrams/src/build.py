"""Builds every Module 03 diagram (SVG + PNG). Usage: python build.py   (needs: pip install cairosvg)"""
import pathlib

import cairosvg

import diagrams as D

here = pathlib.Path(__file__).resolve().parent
svg_dir, png_dir = here.parent / "svg", here.parent / "png"
svg_dir.mkdir(exist_ok=True)
png_dir.mkdir(exist_ok=True)
for name, fn in D.ALL:
    p = svg_dir / f"{name}.svg"
    fn(str(p))
    cairosvg.svg2png(url=str(p), write_to=str(png_dir / f"{name}.png"), scale=1.5)
print("built", len(D.ALL), "diagrams")
