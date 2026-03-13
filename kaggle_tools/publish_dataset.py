"""Publish or version a Kaggle dataset from a local folder.

I added this helper to avoid the common Kaggle error:
Permission 'datasets.create' was denied.

Usage examples:
  python kaggle_tools/publish_dataset.py --path /kaggle/working/my_dataset --id aryanputta/hybrid-satellite-telemetry --title "Hybrid Satellite Telemetry Anomaly Dataset"
  python kaggle_tools/publish_dataset.py --path /kaggle/working/my_dataset --id aryanputta/hybrid-satellite-telemetry --title "Hybrid Satellite Telemetry Anomaly Dataset" --version
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path


def ensure_kaggle_token() -> None:
    """Ensure ~/.kaggle/kaggle.json exists, build it from env vars if provided."""
    target = Path.home() / ".kaggle" / "kaggle.json"
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists():
        os.chmod(target, 0o600)
        return

    username = os.getenv("KAGGLE_USERNAME")
    key = os.getenv("KAGGLE_KEY")
    if not username or not key:
        raise RuntimeError(
            "Missing Kaggle credentials. Set KAGGLE_USERNAME and KAGGLE_KEY or place ~/.kaggle/kaggle.json."
        )

    target.write_text(json.dumps({"username": username, "key": key}, indent=2))
    os.chmod(target, 0o600)


def write_metadata(path: Path, dataset_id: str, title: str) -> None:
    """Create dataset-metadata.json required by Kaggle CLI."""
    metadata = {
        "title": title,
        "id": dataset_id,
        "licenses": [{"name": "CC-BY-4.0"}],
    }
    (path / "dataset-metadata.json").write_text(json.dumps(metadata, indent=2))


def run(cmd: list[str]) -> None:
    completed = subprocess.run(cmd, capture_output=True, text=True)
    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        stdout = completed.stdout.strip()
        detail = stderr or stdout or "unknown error"
        if "datasets.create" in detail and "denied" in detail:
            raise RuntimeError(
                "Kaggle denied datasets.create. Verify account permissions, token freshness, and owner slug in --id."
            )
        raise RuntimeError(detail)
    print(completed.stdout.strip() or "ok")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", required=True, help="Folder containing files to publish")
    parser.add_argument("--id", required=True, help="Kaggle dataset id, example aryanputta/hybrid-satellite-telemetry")
    parser.add_argument("--title", required=True, help="Dataset title")
    parser.add_argument("--version", action="store_true", help="Create new dataset version instead of first create")
    parser.add_argument("--message", default="dataset update", help="Version message when --version is used")
    args = parser.parse_args()

    dataset_path = Path(args.path)
    if not dataset_path.exists() or not dataset_path.is_dir():
        raise RuntimeError(f"Dataset path does not exist: {dataset_path}")

    ensure_kaggle_token()
    write_metadata(dataset_path, args.id, args.title)

    if args.version:
        run(["kaggle", "datasets", "version", "-p", str(dataset_path), "-m", args.message])
    else:
        run(["kaggle", "datasets", "create", "-p", str(dataset_path)])


if __name__ == "__main__":
    main()
