"""Generate the hybrid satellite telemetry dataset used in my paper."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

FAULT_ORDER = [
    "POWER_SPIKE",
    "THERMAL_DRIFT",
    "VOLTAGE_DROP",
    "WHEEL_OSCILLATION",
    "SENSOR_DROPOUT",
]


def simulate_satellite(
    satellite_id: str,
    n_steps: int = 10_000,
    sample_hz: int = 10,
    amplitude_scale: float = 1.0,
    phase_jitter_rad: float = 0.0,
) -> pd.DataFrame:
    """Simulate one satellite telemetry run with a 90-minute orbital period."""
    t = np.arange(n_steps)
    orbital_period_steps = 90 * 60 * sample_hz

    power_phase = phase_jitter_rad
    temp_phase = np.pi / 4 + phase_jitter_rad
    voltage_phase = -np.pi / 3 + phase_jitter_rad
    wheel_phase = phase_jitter_rad

    power_w = 120 + amplitude_scale * 10 * np.sin(2 * np.pi * t / orbital_period_steps + power_phase)
    temp_c = 24 + amplitude_scale * 3 * np.sin(2 * np.pi * t / orbital_period_steps + temp_phase)
    voltage_v = 28 + amplitude_scale * 0.8 * np.sin(2 * np.pi * t / orbital_period_steps + voltage_phase)
    wheel_rpm = 3600 + amplitude_scale * 180 * np.sin(2 * np.pi * t / (2 * orbital_period_steps) + wheel_phase)

    df = pd.DataFrame(
        {
            "timestamp": t,
            "satellite_id": satellite_id,
            "power_w": power_w,
            "temp_c": temp_c,
            "voltage_v": voltage_v,
            "wheel_rpm": wheel_rpm,
            "anomaly": 0,
            "fault_type": "NOMINAL",
        }
    )
    return df


def inject_faults(df: pd.DataFrame, seed: int) -> pd.DataFrame:
    """Inject one instance of each fault class into a satellite run with a per-satellite seed."""
    out = df.copy()
    rng = np.random.default_rng(seed)

    specs = {
        "POWER_SPIKE": {"duration": 30, "channel": "power_w"},
        "THERMAL_DRIFT": {"duration": 100, "channel": "temp_c"},
        "VOLTAGE_DROP": {"duration": 50, "channel": "voltage_v"},
        "WHEEL_OSCILLATION": {"duration": 80, "channel": "wheel_rpm"},
        "SENSOR_DROPOUT": {"duration": 20, "channel": "all"},
    }

    margin = 400
    starts = rng.choice(np.arange(margin, len(out) - margin), size=len(specs), replace=False)

    for start, fault in zip(starts, FAULT_ORDER):
        dur = specs[fault]["duration"]
        end = min(len(out), start + dur)
        sl = slice(start, end)

        if fault == "POWER_SPIKE":
            out.loc[sl, "power_w"] += 20 * np.exp(-np.arange(end - start) / 8)
        elif fault == "THERMAL_DRIFT":
            out.loc[sl, "temp_c"] += np.linspace(0, 9, end - start)
        elif fault == "VOLTAGE_DROP":
            out.loc[sl, "voltage_v"] -= 2.2
        elif fault == "WHEEL_OSCILLATION":
            out.loc[sl, "wheel_rpm"] += 240 * np.sin(2 * np.pi * np.arange(end - start) / 8)
        elif fault == "SENSOR_DROPOUT":
            out.loc[sl, ["power_w", "temp_c", "voltage_v", "wheel_rpm"]] = np.nan

        out.loc[sl, "anomaly"] = 1
        out.loc[sl, "fault_type"] = fault

    return out


def _load_noise_csv(path: Path, n_steps: int) -> pd.DataFrame:
    if path.exists():
        noise = pd.read_csv(path)
    else:
        rng = np.random.default_rng(42)
        noise = pd.DataFrame(
            {
                "ch0": rng.normal(0, 1, n_steps),
                "ch1": rng.normal(0, 1, n_steps),
                "ch2": rng.normal(0, 1, n_steps),
                "ch3": rng.normal(0, 1, n_steps),
            }
        )

    cols = [c for c in noise.columns if c.startswith("ch")]
    noise = noise[cols].copy()
    for c in cols:
        noise[c] = (noise[c] - noise[c].mean()) / (noise[c].std() + 1e-8)
    if len(noise) < n_steps:
        reps = int(np.ceil(n_steps / len(noise)))
        noise = pd.concat([noise] * reps, ignore_index=True)
    return noise.iloc[:n_steps].reset_index(drop=True)


def generate(global_seed: int = 42) -> pd.DataFrame:
    """Generate SAT_01 to SAT_10 with orbital variability, fault injection, and hardware noise blending."""
    rng = np.random.default_rng(global_seed)
    frames: list[pd.DataFrame] = []

    noise_path = Path("noise/arduino_noise_capture/noise_log.csv")

    for i in range(1, 11):
        satellite_id = f"SAT_{i:02d}"
        amp = 1.0 + rng.uniform(-0.10, 0.10)
        phase = rng.uniform(-0.1, 0.1)
        sat_seed = int(global_seed + i)

        base = simulate_satellite(
            satellite_id=satellite_id,
            amplitude_scale=amp,
            phase_jitter_rad=phase,
        )
        faulted = inject_faults(base, seed=sat_seed)

        noise = _load_noise_csv(noise_path, len(faulted))
        faulted["power_w"] = faulted["power_w"].fillna(method="ffill").fillna(0) + 0.35 * noise["ch0"]
        faulted["temp_c"] = faulted["temp_c"].fillna(method="ffill").fillna(0) + 0.08 * noise["ch1"]
        faulted["voltage_v"] = faulted["voltage_v"].fillna(method="ffill").fillna(0) + 0.03 * noise["ch2"]
        faulted["wheel_rpm"] = faulted["wheel_rpm"].fillna(method="ffill").fillna(0) + 4.0 * noise["ch3"]

        frames.append(faulted)

    dataset = pd.concat(frames, ignore_index=True)
    out_path = Path("data/hybrid_satellite_telemetry.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    dataset.to_csv(out_path, index=False)

    anomaly_rate = float(dataset["anomaly"].mean() * 100)
    counts = dataset["fault_type"].value_counts().to_dict()
    print(f"Saved {out_path}")
    print(f"Total rows: {len(dataset):,}")
    print(f"Anomaly rate: {anomaly_rate:.2f}%")
    print(f"Fault class distribution: {counts}")
    return dataset


if __name__ == "__main__":
    np.random.seed(42)
    generate(global_seed=42)
