"""Window telemetry into 50-step segments for sequence and RP models."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

FEATURES = ["power_w", "temp_c", "voltage_v", "wheel_rpm"]


def build_windows(df: pd.DataFrame, window: int = 50, stride: int = 10) -> np.ndarray:
    values = df[FEATURES].to_numpy(dtype=np.float32)
    windows = []
    for start in range(0, len(values) - window + 1, stride):
        windows.append(values[start : start + window])
    return np.stack(windows) if windows else np.empty((0, window, len(FEATURES)), dtype=np.float32)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/hybrid_telemetry_normalized.csv"))
    parser.add_argument("--output", type=Path, default=Path("artifacts/windows.npy"))
    parser.add_argument("--window", type=int, default=50)
    parser.add_argument("--stride", type=int, default=10)
    args = parser.parse_args()

    df = pd.read_csv(args.input).fillna(0)
    arr = build_windows(df, window=args.window, stride=args.stride)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.save(args.output, arr)
    print(f"Saved windows {arr.shape} to {args.output}")


if __name__ == "__main__":
    main()
