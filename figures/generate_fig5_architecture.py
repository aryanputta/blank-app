"""Generate architecture and hardware pipeline diagrams with safe label spacing."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


def add_box(ax, x, y, text, width=2.2, height=0.9):
    box = FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.04", linewidth=1.5, facecolor="#eaf2ff")
    ax.add_patch(box)
    ax.text(x + width / 2, y + height / 2, text, ha="center", va="center", fontsize=9, wrap=True)


def main() -> None:
    fig, ax = plt.subplots(figsize=(12, 4.4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis("off")

    add_box(ax, 0.3, 2.5, "Arduino Uno\nSensor Array", width=2.3)
    add_box(ax, 3.0, 2.5, "Raspberry Pi 4\nData Ingest", width=2.2)
    add_box(ax, 5.6, 2.5, "Recurrence Plot\nEncoder", width=2.2)
    add_box(ax, 8.2, 2.5, "CNN Classifier", width=1.8)
    add_box(ax, 10.3, 2.5, "Fault Label\nOutput", width=1.5)

    for x in [2.7, 5.3, 7.9, 10.1]:
        ax.annotate("", xy=(x + 0.2, 2.95), xytext=(x - 0.2, 2.95), arrowprops=dict(arrowstyle="->", lw=1.5))

    ax.text(0.3, 1.0, "Figure 5 and Figure 7 layout-safe labels", fontsize=10)

    out = Path("artifacts/figures/fig5_architecture.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout(pad=1.2)
    fig.savefig(out, dpi=300, bbox_inches="tight")
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
