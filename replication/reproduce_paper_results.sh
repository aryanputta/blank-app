#!/usr/bin/env bash
set -euo pipefail

SKIP_FIGURES="${SKIP_FIGURES:-1}"

mkdir -p data artifacts results plots

if [ ! -f data/hybrid_satellite_telemetry.csv ] && [ ! -f data/simulated_telemetry.csv ]; then
  echo "No local telemetry CSV found. Generating simulation baseline..."
  python data_generation/simulate_satellite.py
fi

if [ ! -f data/simulated_telemetry_faults.csv ]; then
  python data_generation/inject_faults.py
fi

if [ ! -f data/arduino_noise.csv ]; then
  echo "timestamp_ms,ch0,ch1,ch2,ch3" > data/arduino_noise.csv
  for i in $(seq 0 1999); do
    echo "$((i*100)),$((500 + (i%17))),$((510 + (i%13))),$((495 + (i%11))),$((505 + (i%19)))" >> data/arduino_noise.csv
  done
fi

python hardware_noise_capture/noise_processing.py --telemetry data/simulated_telemetry_faults.csv --noise data/arduino_noise.csv --output data/hybrid_telemetry.csv
python hardware_noise_capture/noise_analysis.py --input data/arduino_noise.csv --output-dir plots
python preprocessing/normalize_telemetry.py --input data/hybrid_telemetry.csv --output data/hybrid_telemetry_normalized.csv
python windowing/window_telemetry.py --input data/hybrid_telemetry_normalized.csv --output artifacts/windows.npy --window 50 --stride 10
python recurrence_plot_encoder/rp_encoder.py --input data/hybrid_telemetry_normalized.csv --window-size 50 --eps 0.1
python training/train_cnn.py
python training/train_lstm.py
python training/train_autoencoder.py
python training/train_isolation_forest.py
python evaluation/evaluate_models.py
python evaluation/compute_metrics.py
python plots/generate_plots.py

if [ "$SKIP_FIGURES" = "0" ]; then
  python figures/generate_fig5_architecture.py
  python figures/generate_fig8_results.py
  python figures/generate_fig9_fault_type.py
  python figures/generate_fig10_noise_effect.py
else
  echo "Skipping figure generation (set SKIP_FIGURES=0 to enable)."
fi

echo "Replication workflow complete."
