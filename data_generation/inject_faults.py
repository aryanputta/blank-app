"""Inject labeled telemetry faults into simulated satellite data."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

FAULTS = [
    "POWER_SPIKE",
    "THERMAL_DRIFT",
    "VOLTAGE_DROP",
    "WHEEL_OSCILLATION",
    "SENSOR_DROPOUT",
]


def inject_faults(df: pd.DataFrame, fraction: float = 0.08, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n_fault = int(len(df) * fraction)
    indices = rng.choice(df.index.to_numpy(), size=n_fault, replace=False)

    for i, idx in enumerate(indices):
        fault = FAULTS[i % len(FAULTS)]
        df.at[idx, "fault_class"] = fault
        if fault == "POWER_SPIKE":
            df.at[idx, "power_w"] *= 1.25
        elif fault == "THERMAL_DRIFT":
            df.at[idx, "temp_c"] += 12
        elif fault == "VOLTAGE_DROP":
            df.at[idx, "voltage_v"] *= 0.78
        elif fault == "WHEEL_OSCILLATION":
            df.at[idx, "wheel_rpm"] *= 1.18
        elif fault == "SENSOR_DROPOUT":
            df.loc[idx, ["power_w", "temp_c", "voltage_v", "wheel_rpm"]] = np.nan
    return df


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/simulated_telemetry.csv"))
    parser.add_argument("--output", type=Path, default=Path("data/simulated_telemetry_faults.csv"))
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    out_df = inject_faults(df)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(args.output, index=False)
    print(f"Saved fault-injected data to {args.output}")


if __name__ == "__main__":
    main()
