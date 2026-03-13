"""Inject paper-aligned fault segments into simulated telemetry."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from fault_injection.fault_library import FAULT_SPECS, apply_fault_segment


def inject_faults(df: pd.DataFrame, seed: int = 7) -> pd.DataFrame:
    out = df.copy()
    rng = np.random.default_rng(seed)
    per_satellite = []

    for sat, sat_df in out.groupby("satellite_id", sort=False):
        sat_idx = sat_df.index.to_numpy()
        sat_len = len(sat_idx)
        starts = rng.integers(0, max(1, sat_len - 120), size=len(FAULT_SPECS))
        for i, fault_name in enumerate(FAULT_SPECS):
            apply_fault_segment(out, int(sat_idx[starts[i]]), fault_name, seed=seed)
        per_satellite.append(sat)

    print(f"Injected all five fault classes across satellites: {', '.join(per_satellite)}")
    return out


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
