"""Render four comparable QLoRA runs from the collected statistics CSV."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parents[1] / "assets"
with (root / "benchmark-statistics.csv").open() as source:
    rows = [row for row in csv.DictReader(source) if row["experiment"].startswith("E2B text-QLoRA")]
labels = [row["experiment"].replace("E2B text-QLoRA ", "") for row in rows]
means = [float(row["mean"]) for row in rows]
errors = [[float(row["mean"]) - float(row["ci95_low"]) for row in rows],
          [float(row["ci95_high"]) - float(row["mean"]) for row in rows]]
fig, ax = plt.subplots(figsize=(10, 4.6), layout="constrained")
ax.barh(labels, means, xerr=errors, capsize=5, color=["#187760", "#187760", "#365f9c", "#365f9c"])
for i, row in enumerate(rows):
    ax.text(float(row["ci95_high"]) + 12, i, f"{means[i]:.1f}s | n={row['n']}", va="center", fontsize=11)
ax.set_xlim(0, 770)
ax.invert_yaxis()
ax.set_xlabel("External wall time (seconds) | mean and 95% confidence interval")
ax.set_title("E2B text-QLoRA | symmetric 2+2 GPUs", loc="left", pad=18)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="x", alpha=.15)
fig.savefig(root / "qlora-wall-time.png", dpi=180)
plt.close(fig)
