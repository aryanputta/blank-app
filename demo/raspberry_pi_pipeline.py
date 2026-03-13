"""Reference Raspberry Pi pipeline for low-latency telemetry classification."""

from __future__ import annotations

import time


def run_pipeline() -> None:
    steps = [
        "Read serial telemetry from Arduino",
        "Create recurrence plot window",
        "Run CNN classifier",
        "Emit fault class",
    ]
    start = time.perf_counter()
    for step in steps:
        print(step)
        time.sleep(0.02)
    elapsed_ms = (time.perf_counter() - start) * 1000
    print(f"End to end latency: {elapsed_ms:.2f} ms")


if __name__ == "__main__":
    run_pipeline()
