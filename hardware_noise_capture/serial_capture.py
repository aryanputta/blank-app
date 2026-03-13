"""Capture Arduino serial stream into CSV at 10 Hz."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default="/dev/ttyACM0")
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--output", type=Path, default=Path("data/arduino_noise.csv"))
    args = parser.parse_args()

    # This script is a placeholder for pyserial runtime use on hardware.
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if not args.output.exists():
        args.output.write_text("timestamp_ms,ch0,ch1,ch2,ch3\n")
    print(f"Ready to capture from {args.port} at {args.baud} into {args.output}")


if __name__ == "__main__":
    main()
