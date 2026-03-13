"""Reference Raspberry Pi pipeline for live anomaly scoring."""

from __future__ import annotations

import collections
import time

import numpy as np

from recurrence_plot_encoder.rp_encoder import telemetry_to_rp


def fake_arduino_stream():
    rng = np.random.default_rng(42)
    while True:
        yield rng.normal(loc=[120, 24, 28, 3600], scale=[1.0, 0.3, 0.1, 10.0]).astype(float)


def run_pipeline() -> None:
    buffer = collections.deque(maxlen=50)
    stream = fake_arduino_stream()

    for _ in range(50):
        buffer.append(next(stream))

    start = time.perf_counter()
    window = np.array(buffer, dtype=np.float32)
    rp_tensor = telemetry_to_rp(window, eps=0.1)
    anomaly_score = float(np.mean(rp_tensor))
    fault_label = "WHEEL_OSCILLATION" if anomaly_score > 0.55 else "NOMINAL"
    latency_ms = (time.perf_counter() - start) * 1000

    print(f"Telemetry buffer shape: {window.shape}")
    print(f"RP tensor shape: {rp_tensor.shape}")
    print(f"Anomaly score: {anomaly_score:.4f}")
    print(f"Predicted fault label: {fault_label}")
    print(f"Refresh latency: {latency_ms:.2f} ms")


if __name__ == "__main__":
    run_pipeline()
