"""Encode telemetry windows into 50x50x4 recurrence plot tensors."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist

FEATURES = ["power_w", "temp_c", "voltage_v", "wheel_rpm"]


def recurrence_plot_1d(signal: np.ndarray, eps: float) -> np.ndarray:
    d = cdist(signal[:, None], signal[:, None], metric="euclidean")
    return (d <= eps).astype(np.float32)


def telemetry_to_rp(values: np.ndarray, eps: float = 0.1) -> np.ndarray:
    # values shape: (window=50, channels=4)
    channels = [recurrence_plot_1d(values[:, i], eps=eps) for i in range(values.shape[1])]
    return np.stack(channels, axis=-1)


def encode_file(input_csv: Path, output_npy: Path, window_size: int = 50, eps: float = 0.1) -> np.ndarray:
    df = pd.read_csv(input_csv).fillna(method="ffill").fillna(0)
    values = df[FEATURES].to_numpy(dtype=np.float32)
    tensors = []
    for start in range(0, len(values) - window_size + 1, window_size):
        window = values[start : start + window_size]
        tensors.append(telemetry_to_rp(window, eps=eps))
    arr = np.stack(tensors) if tensors else np.empty((0, 50, 50, 4), dtype=np.float32)
    output_npy.parent.mkdir(parents=True, exist_ok=True)
    np.save(output_npy, arr)
    print(f"Saved recurrence plot tensor {arr.shape} to {output_npy}")
    return arr


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/hybrid_telemetry.csv"))
    parser.add_argument("--output", type=Path, default=Path("artifacts/recurrence_plots.npy"))
    parser.add_argument("--window-size", type=int, default=50)
    parser.add_argument("--eps", type=float, default=0.1)
    args = parser.parse_args()
    encode_file(args.input, args.output, args.window_size, args.eps)


if __name__ == "__main__":
    main()
