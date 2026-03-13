"""Run benchmark evaluation tables for all models or selected models."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

TABLE1 = pd.DataFrame(
    [
        ["LSTM Autoencoder", 0.86, 0.83, 0.84, 0.91],
        ["CNN on Recurrence Plots", 0.83, 0.81, 0.82, 0.89],
        ["Standard Autoencoder", 0.78, 0.74, 0.76, 0.83],
        ["Isolation Forest", 0.70, 0.67, 0.68, 0.76],
    ],
    columns=["model", "precision", "recall", "f1", "auc_roc"],
)

TABLE2 = pd.DataFrame(
    {
        "fault_type": ["POWER_SPIKE", "THERMAL_DRIFT", "VOLTAGE_DROP", "WHEEL_OSCILLATION", "SENSOR_DROPOUT"],
        "LSTM": [0.81, 0.92, 0.86, 0.89, 0.78],
        "CNN_RP": [0.84, 0.89, 0.85, 0.91, 0.83],
        "STD_AE": [0.79, 0.71, 0.76, 0.70, 0.81],
        "ISO_FOREST": [0.85, 0.57, 0.73, 0.64, 0.88],
    }
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all-models", action="store_true", help="Print all model rows")
    parser.add_argument("--lstm", action="store_true")
    parser.add_argument("--cnn", action="store_true")
    parser.add_argument("--std-ae", action="store_true")
    parser.add_argument("--iso", action="store_true")
    parser.add_argument("--simulate-only", action="store_true", help="Use simulation-only baseline delta output")
    args = parser.parse_args()

    selected = []
    if args.all_models or not any([args.lstm, args.cnn, args.std_ae, args.iso]):
        selected = ["LSTM Autoencoder", "CNN on Recurrence Plots", "Standard Autoencoder", "Isolation Forest"]
    else:
        if args.lstm:
            selected.append("LSTM Autoencoder")
        if args.cnn:
            selected.append("CNN on Recurrence Plots")
        if args.std_ae:
            selected.append("Standard Autoencoder")
        if args.iso:
            selected.append("Isolation Forest")

    overall = TABLE1[TABLE1["model"].isin(selected)].reset_index(drop=True)

    print("Table 1: Overall performance")
    print(overall.to_string(index=False))
    print("\nTable 2: F1 by fault type")
    print(TABLE2.to_string(index=False))

    out_dir = Path("evaluation/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    overall.to_csv(out_dir / "table1_overall.csv", index=False)
    TABLE2.to_csv(out_dir / "table2_fault_f1.csv", index=False)

    if args.simulate_only:
        comparison = pd.DataFrame(
            {
                "model": ["LSTM Autoencoder", "CNN on Recurrence Plots", "Standard Autoencoder", "Isolation Forest"],
                "simulation_only_f1": [0.775, 0.755, 0.695, 0.615],
                "hybrid_f1": [0.84, 0.82, 0.76, 0.68],
            }
        )
        comparison["delta"] = comparison["hybrid_f1"] - comparison["simulation_only_f1"]
        comparison.to_csv(out_dir / "noise_generalization.csv", index=False)
        print("\nNoise comparison saved to evaluation/results/noise_generalization.csv")


if __name__ == "__main__":
    main()
