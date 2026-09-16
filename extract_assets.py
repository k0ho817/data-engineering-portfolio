"""Extract original portfolio figures from the adjacent study workspace."""
from pathlib import Path
import base64
import json
import shutil
import unicodedata
import zipfile
import csv
from itertools import islice
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
STUDY = ROOT.parent
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)

def copy(source, name):
    shutil.copyfile(STUDY / source, OUT / name)

copy("DBLAB/test/final_report_20260521 2/avg_images_per_sec.png", "distributed-throughput.png")
copy("DBLAB/test/final_report_20260521 2/final_benchmark_summary.csv", "benchmark-summary.csv")
copy("DBLAB/study/prophet/season2.png", "prophet-components.png")

with zipfile.ZipFile(STUDY / "DBLAB/study/report/report2.pptx") as deck:
    (OUT / "trajectory-7.png").write_bytes(deck.read("ppt/media/image7.png"))

with (STUDY / "DBLAB/study/report/trajectory.csv").open() as source:
    sample = list(islice(csv.DictReader(source), 10000))
points = [row for row in sample if row["objectid"] == "790" and row["type"] == "bus"]
coordinates = [tuple(map(float, row["trajectory"].split(","))) for row in points]
latitude, longitude = zip(*coordinates)
with (OUT / "trajectory-sample.csv").open("w") as target:
    writer = csv.writer(target)
    writer.writerow(["objectid", "type", "latitude", "longitude", "timestamp"])
    writer.writerows((r["objectid"], r["type"], lat, lon, r["timeStamp"]) for r, (lat, lon) in zip(points, coordinates))
fig, ax = plt.subplots(figsize=(9, 6), layout="constrained")
ax.plot(longitude, latitude, color="#2158d0", linewidth=2, label="Recorded trajectory")
ax.scatter(longitude[0], latitude[0], color="#11795d", s=65, label="First observation", zorder=3)
ax.scatter(longitude[-1], latitude[-1], color="#b5414a", marker="s", s=55, label="Last observation", zorder=3)
ax.set(title=f"Bus 790 | {len(points):,} recorded positions", xlabel="Longitude (degrees)", ylabel="Latitude (degrees)")
ax.ticklabel_format(useOffset=False, style="plain")
ax.tick_params(axis="x", rotation=20)
ax.grid(alpha=.2)
ax.legend()
fig.savefig(OUT / "trajectory-recorded.png", dpi=180)
plt.close(fig)

notebook = json.loads((STUDY / "DBLAB/study/report2/code/1826015문경호.ipynb").read_text())
for number, output in enumerate(o for o in notebook["cells"][32]["outputs"] if "image/png" in o.get("data", {})):
    encoded = output["data"]["image/png"]
    (OUT / f"bike-result-{number}.png").write_bytes(base64.b64decode("".join(encoded)))

deck_path = next(p for p in STUDY.glob("KNUT25/*/*/*.pptx") if unicodedata.normalize("NFC", p.name) == "Aquila_최종발표_최종.pptx")
with zipfile.ZipFile(deck_path) as deck:
    for number in (29,):
        (OUT / f"aquila-{number}.png").write_bytes(deck.read(f"ppt/media/image{number}.png"))

print("Extracted original assets:", OUT)
