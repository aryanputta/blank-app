"""Generate benchmark plots from results files."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    out = Path("plots")
    out.mkdir(exist_ok=True)

    metrics_csv = Path("results/model_comparison_metrics.csv")
    if metrics_csv.exists():
        df = pd.read_csv(metrics_csv)
        plt.figure(figsize=(8, 4))
        plt.bar(df["model"], df["f1"])
        plt.xticks(rotation=20, ha="right")
        plt.ylabel("F1")
        plt.tight_layout()
        plt.savefig(out / "model_f1_comparison.png", dpi=160)
        plt.close()

    overall_json = Path("results/overall_metrics.json")
    if overall_json.exists():
        payload = json.loads(overall_json.read_text())
        fault_f1 = payload.get("fault_f1", {})
        if fault_f1:
            plt.figure(figsize=(8, 4))
            plt.bar(list(fault_f1.keys()), list(fault_f1.values()))
            plt.ylabel("F1")
            plt.xticks(rotation=20, ha="right")
            plt.tight_layout()
            plt.savefig(out / "fault_type_f1.png", dpi=160)
            plt.close()

    print("Generated plots from results/")


if __name__ == "__main__":
    main()
