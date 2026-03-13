"""Fault injection utilities for the five paper fault classes."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class FaultSpec:
    name: str
    channel: str
    duration: int
    description: str


FAULT_SPECS: dict[str, FaultSpec] = {
    "POWER_SPIKE": FaultSpec("POWER_SPIKE", "power_w", 30, "Transient power surge"),
    "THERMAL_DRIFT": FaultSpec("THERMAL_DRIFT", "temp_c", 100, "Slow thermal increase"),
    "VOLTAGE_DROP": FaultSpec("VOLTAGE_DROP", "voltage_v", 50, "Sustained undervoltage"),
    "WHEEL_OSCILLATION": FaultSpec("WHEEL_OSCILLATION", "wheel_rpm", 80, "Wheel speed oscillation"),
    "SENSOR_DROPOUT": FaultSpec("SENSOR_DROPOUT", "all", 20, "Temporary sensor outage"),
}


def apply_fault_segment(df: pd.DataFrame, start_idx: int, fault_name: str, seed: int = 42) -> None:
    spec = FAULT_SPECS[fault_name]
    end_idx = min(start_idx + spec.duration, len(df))
    sl = slice(start_idx, end_idx)
    t = np.arange(end_idx - start_idx)
    rng = np.random.default_rng(seed + start_idx)

    if fault_name == "POWER_SPIKE":
        pulse = 18.0 * np.exp(-t / 10.0)
        df.loc[sl, "power_w"] = df.loc[sl, "power_w"].to_numpy() + pulse
    elif fault_name == "THERMAL_DRIFT":
        df.loc[sl, "temp_c"] = df.loc[sl, "temp_c"].to_numpy() + np.linspace(0.0, 9.0, len(t))
    elif fault_name == "VOLTAGE_DROP":
        df.loc[sl, "voltage_v"] = df.loc[sl, "voltage_v"].to_numpy() - 2.2
    elif fault_name == "WHEEL_OSCILLATION":
        osc = 240.0 * np.sin(2.0 * np.pi * t / 8.0)
        df.loc[sl, "wheel_rpm"] = df.loc[sl, "wheel_rpm"].to_numpy() + osc
    elif fault_name == "SENSOR_DROPOUT":
        for col in ["power_w", "temp_c", "voltage_v", "wheel_rpm"]:
            df.loc[sl, col] = np.nan

    if len(t) > 0:
        jitter = rng.normal(0, 0.03, len(t))
        if fault_name != "SENSOR_DROPOUT":
            df.loc[sl, spec.channel] = df.loc[sl, spec.channel].to_numpy() * (1 + jitter)
    df.loc[sl, "fault_class"] = fault_name
