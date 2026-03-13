"""Encode telemetry windows into recurrence plot tensors."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist


FEATURES = ["power_w", "temp_c", "voltage_v", "wheel_rpm"]


def recurrence_plot(window: np.ndarray, eps: float = 0.8) -> np.ndarray:
    distances = cdist(window, window, metric="euclidean")
    rp = (distances <= eps).astype(np.float32)
    return rp


def encode_file(input_csv: Path, output_npy: Path, window_size: int = 64) -> None:
    df = pd.read_csv(input_csv).fillna(method="ffill").fillna(0)
    values = df[FEATURES].to_numpy(dtype=np.float32)
    images = []
    for start in range(0, len(values) - window_size, window_size):
        window = values[start : start + window_size]
        images.append(recurrence_plot(window))
    arr = np.stack(images)
    output_npy.parent.mkdir(parents=True, exist_ok=True)
    np.save(output_npy, arr)
    print(f"Saved recurrence plot tensor {arr.shape} to {output_npy}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/hybrid_telemetry.csv"))
    parser.add_argument("--output", type=Path, default=Path("artifacts/recurrence_plots.npy"))
    parser.add_argument("--window-size", type=int, default=64)
    args = parser.parse_args()
    encode_file(args.input, args.output, args.window_size)


if __name__ == "__main__":
    main()
