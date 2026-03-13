"""Normalize telemetry channels with z-score statistics from training data."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

FEATURES = ["power_w", "temp_c", "voltage_v", "wheel_rpm"]


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in FEATURES:
        mu = out[col].mean()
        sigma = out[col].std() or 1.0
        out[col] = (out[col] - mu) / sigma
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/hybrid_telemetry.csv"))
    parser.add_argument("--output", type=Path, default=Path("data/hybrid_telemetry_normalized.csv"))
    args = parser.parse_args()

    df = pd.read_csv(args.input).fillna(method="ffill").fillna(0)
    out = normalize(df)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output, index=False)
    print(f"Saved normalized telemetry to {args.output}")


if __name__ == "__main__":
    main()
