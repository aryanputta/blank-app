"""Live Raspberry Pi telemetry demo with serial ingestion, RP encoding, and anomaly output."""

from __future__ import annotations

import collections
import time
from pathlib import Path

import joblib
import numpy as np
import serial

from encoding.recurrence_plot import window_to_rp_image


def _infer_fault_label(score: float) -> str:
    if score > 0.95:
        return "SENSOR_DROPOUT"
    if score > 0.75:
        return "WHEEL_OSCILLATION"
    if score > 0.55:
        return "THERMAL_DRIFT"
    return "NOMINAL"


def main() -> None:
    ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
    model_path = Path("artifacts/models/isolation_forest.joblib")
    model = joblib.load(model_path) if model_path.exists() else None

    buffer = collections.deque(maxlen=50)
    refresh_s = 0.1

    try:
        while True:
            cycle_start = time.perf_counter()
            line = ser.readline().decode("utf-8", errors="ignore").strip()
            parts = line.split(",")
            if len(parts) < 4:
                continue

            try:
                t_n, a_n, v_n = float(parts[1]), float(parts[2]), float(parts[3])
            except ValueError:
                continue

            # expanded to 4 channels for compatibility with trained models
            sample = np.array([t_n, a_n, v_n, a_n], dtype=np.float32)
            buffer.append(sample)

            if len(buffer) == 50:
                seq = np.stack(buffer)
                rp_channels = [window_to_rp_image(seq[:, i], eps=0.1) for i in range(4)]
                rp = np.stack(rp_channels, axis=-1)

                features = seq.reshape(1, -1)
                score = float(-model.score_samples(features)[0]) if model is not None else float(np.mean(rp))
                label = _infer_fault_label(score)

                latency_ms = (time.perf_counter() - cycle_start) * 1000
                print(f"score={score:.4f} label={label} latency_ms={latency_ms:.2f}")

            elapsed = time.perf_counter() - cycle_start
            sleep_t = max(0.0, refresh_s - elapsed)
            time.sleep(sleep_t)

    finally:
        ser.close()


if __name__ == "__main__":
    main()
