"""Analyze captured hardware noise: autocorrelation, PSD, and Gaussian comparison."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import welch


def lag1_autocorr(x: np.ndarray) -> float:
    x0 = x[:-1] - np.mean(x[:-1])
    x1 = x[1:] - np.mean(x[1:])
    denom = (np.linalg.norm(x0) * np.linalg.norm(x1)) or 1.0
    return float(np.dot(x0, x1) / denom)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/arduino_noise.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("plots"))
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    signal = df["ch0"].to_numpy(dtype=float)
    fs = 10.0

    args.output_dir.mkdir(parents=True, exist_ok=True)

    rho1 = lag1_autocorr(signal)
    Path(args.output_dir / "noise_summary.txt").write_text(
        f"lag1_autocorrelation={rho1:.3f}\nexpected_paper_reference~0.72\n"
    )

    f, pxx = welch(signal, fs=fs, nperseg=min(256, len(signal)))
    plt.figure(figsize=(7, 4))
    plt.semilogy(f, pxx)
    plt.axvline(5.0, color="r", linestyle="--", label="5 Hz reference")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("PSD")
    plt.title("Hardware noise PSD")
    plt.legend()
    plt.tight_layout()
    plt.savefig(args.output_dir / "noise_psd.png", dpi=160)
    plt.close()

    gaussian = np.random.default_rng(42).normal(np.mean(signal), np.std(signal), size=len(signal))
    plt.figure(figsize=(7, 4))
    plt.hist(signal, bins=30, alpha=0.6, label="captured")
    plt.hist(gaussian, bins=30, alpha=0.6, label="gaussian")
    plt.legend()
    plt.tight_layout()
    plt.savefig(args.output_dir / "noise_gaussian_comparison.png", dpi=160)
    plt.close()

    print(f"lag-1 autocorrelation: {rho1:.3f}")


if __name__ == "__main__":
    main()
