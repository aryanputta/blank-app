#!/usr/bin/env bash
set -euo pipefail

# Resolve the specific PR #3 conflict set shown in GitHub UI by keeping this branch's content.
# Run from the feature branch after merging/rebasing main and hitting conflicts.

FILES=(
  .gitignore
  README.md
  data_generation/inject_faults.py
  data_generation/simulate_satellite.py
  demo/raspberry_pi_pipeline.py
  evaluation/compute_metrics.py
  evaluation/evaluate_models.py
  hardware_noise_capture/arduino_capture.ino
  hardware_noise_capture/noise_processing.py
  models/cnn_autoencoder.py
  models/isolation_forest.py
  models/lstm_autoencoder.py
  models/standard_autoencoder.py
  recurrence_plot_encoder/rp_encoder.py
  replication/replicate_paper.md
  replication/reproduce_paper_results.sh
  requirements.txt
  training/train_autoencoder.py
  training/train_cnn.py
  training/train_isolation_forest.py
  training/train_lstm.py
)

missing=0
for f in "${FILES[@]}"; do
  if [[ ! -e "$f" ]]; then
    echo "Missing expected file: $f"
    missing=1
  fi
done

if [[ "$missing" -ne 0 ]]; then
  echo "Aborting because one or more expected files are missing."
  exit 1
fi

for f in "${FILES[@]}"; do
  if git diff --name-only --diff-filter=U | grep -qx "$f"; then
    git checkout --ours -- "$f"
    git add "$f"
    echo "Resolved with ours: $f"
  fi
done

remaining=$(git diff --name-only --diff-filter=U || true)
if [[ -n "$remaining" ]]; then
  echo "Other conflicts remain:"
  echo "$remaining"
  exit 2
fi

echo "Target conflict set resolved."
echo "Next: git commit -m 'Resolve PR #3 merge conflicts' && git push"
