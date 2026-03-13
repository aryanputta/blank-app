#!/usr/bin/env bash
set -euo pipefail

DATASET_PATH="${1:-/kaggle/working/my_dataset_upload}"
DATASET_ID="${2:-aryanputta/hybrid-satellite-telemetry}"
DATASET_TITLE="${3:-Hybrid Satellite Telemetry Anomaly Dataset}"
MODE="${4:-create}" # create | version
MESSAGE="${5:-dataset update}"

if [[ "$MODE" == "version" ]]; then
  python kaggle_tools/publish_dataset.py \
    --path "$DATASET_PATH" \
    --id "$DATASET_ID" \
    --title "$DATASET_TITLE" \
    --version \
    --message "$MESSAGE"
else
  python kaggle_tools/publish_dataset.py \
    --path "$DATASET_PATH" \
    --id "$DATASET_ID" \
    --title "$DATASET_TITLE"
fi
