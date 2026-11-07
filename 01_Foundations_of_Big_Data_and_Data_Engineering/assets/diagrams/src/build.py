"""Builds every diagram (SVG + PNG). Usage: python build.py   (needs: pip install cairosvg)"""
import pathlib
import cairosvg
import foundations as F
import platform_diagrams as PL
import diagrams_a as A
import diagrams_b as B
from lib import S

here = pathlib.Path(__file__).resolve().parent
svg_dir, png_dir = here.parent / "svg", here.parent / "png"
svg_dir.mkdir(exist_ok=True); png_dir.mkdir(exist_ok=True)

# (output name, drawing function)
jobs = list(A.ALL) + list(B.ALL) + [
    ("01-business-problem", F.d01_problem), ("01-excel-vs-mysql", F.d02_excel_mysql),
    ("04-single-machine", F.d04_single_machine), ("04-scale-up-vs-out", F.d03_scaling),
    ("05-hadoop-cluster", F.d05_hadoop), ("05-hdfs-fault-tolerance", F.d06_fault),
    ("06-spark-cluster", F.d07_spark), ("06-disk-vs-memory", F.d08_hadoop_vs_spark),
    ("06-spark-architecture", F.d09_spark_arch), ("06-how-spark-works", F.d10_how_spark_works),
    ("07-pyspark-equation", F.d12_pyspark), ("08-evolution-poster", F.d11_evolution),
    ("09-platform-layers", PL.d13_platform_layers), ("09-lakehouse", PL.d14_lakehouse),
    ("09-control-and-compute-plane", PL.d15_planes), ("09-delta-lake", PL.d17_delta), ("09-medallion", PL.d18_medallion),
]
for name, fn in sorted(jobs, key=lambda j: j[0]):
    p = svg_dir / f"{name}.svg"
    fn(str(p))
    cairosvg.svg2png(url=str(p), write_to=str(png_dir / f"{name}.png"), scale=1.5)

# repository-level banner
root_assets = here.parents[3] / "assets"
root_assets.mkdir(exist_ok=True)
A.repo_banner(str(root_assets / "banner.svg"))
cairosvg.svg2png(url=str(root_assets / "banner.svg"), write_to=str(root_assets / "banner.png"), scale=1.5)
print("built", len(jobs), "module diagrams + repo banner")
