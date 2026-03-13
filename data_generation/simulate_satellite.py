"""Simulate multi-satellite telemetry streams for reproducible anomaly experiments."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def simulate_dataset(samples_per_satellite: int = 10_000, random_seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(random_seed)
    satellites = [f"SAT_{i:02d}" for i in range(1, 11)]
    records: list[dict] = []

    for sat in satellites:
        time_index = np.arange(samples_per_satellite)
        phase = rng.uniform(0, 2 * np.pi)
        power = 125 + 8 * np.sin(time_index / 150 + phase) + rng.normal(0, 1.2, samples_per_satellite)
        temp = 24 + 2.5 * np.sin(time_index / 210 + phase / 2) + rng.normal(0, 0.5, samples_per_satellite)
        voltage = 28 + 0.8 * np.sin(time_index / 180) + rng.normal(0, 0.12, samples_per_satellite)
        wheel = 3600 + 180 * np.sin(time_index / 65 + phase) + rng.normal(0, 25, samples_per_satellite)

        for i in range(samples_per_satellite):
            records.append(
                {
                    "satellite_id": sat,
                    "timestamp": int(i),
                    "power_w": float(power[i]),
                    "temp_c": float(temp[i]),
                    "voltage_v": float(voltage[i]),
                    "wheel_rpm": float(wheel[i]),
                    "fault_class": "NOMINAL",
                }
            )

    return pd.DataFrame.from_records(records)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples-per-satellite", type=int, default=10_000)
    parser.add_argument("--output", type=Path, default=Path("data/simulated_telemetry.csv"))
    args = parser.parse_args()

    df = simulate_dataset(samples_per_satellite=args.samples_per_satellite)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)
    print(f"Saved simulated dataset to {args.output} with {len(df)} rows")


if __name__ == "__main__":
    main()
