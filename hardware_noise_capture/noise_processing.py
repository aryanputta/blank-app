"""Process Arduino noise traces and merge them with telemetry channels."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def normalize_noise(noise_df: pd.DataFrame) -> pd.DataFrame:
    channels = [c for c in noise_df.columns if c.startswith("ch")]
    noise_df = noise_df.copy()
    for c in channels:
        series = noise_df[c].astype(float)
        baseline = series.iloc[: min(100, len(series))].mean()
        centered = series - baseline
        noise_df[c] = centered / (centered.std() + 1e-8)
    return noise_df


def blend_noise(telemetry_df: pd.DataFrame, noise_df: pd.DataFrame, scale: float = 0.03) -> pd.DataFrame:
    out = telemetry_df.copy()
    feature_map = {
        "power_w": "ch0",
        "temp_c": "ch1",
        "voltage_v": "ch2",
        "wheel_rpm": "ch3",
    }
    noise_df = normalize_noise(noise_df)
    for feature, channel in feature_map.items():
        repeated = np.resize(noise_df[channel].to_numpy(), len(out))
        out[feature] = out[feature].astype(float) + scale * repeated
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--telemetry", type=Path, default=Path("data/simulated_telemetry_faults.csv"))
    parser.add_argument("--noise", type=Path, default=Path("data/arduino_noise.csv"))
    parser.add_argument("--output", type=Path, default=Path("data/hybrid_telemetry.csv"))
    args = parser.parse_args()

    telemetry_df = pd.read_csv(args.telemetry)
    noise_df = pd.read_csv(args.noise)
    blended = blend_noise(telemetry_df, noise_df)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    blended.to_csv(args.output, index=False)
    print(f"Saved hybrid telemetry to {args.output}")


if __name__ == "__main__":
    main()
