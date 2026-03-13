# Paper replication guide

I use this guide to reproduce every result in my paper.

1. I download the Kaggle dataset.
2. I generate baseline simulation and inject labeled faults.
3. I blend hardware noise collected from Arduino traces.
4. I encode recurrence plots.
5. I train all four model families.
6. I evaluate the held out satellites SAT_09 and SAT_10.
7. I optionally regenerate figures used in the manuscript when needed.

## Commands

```bash
bash replication/bootstrap_environment.sh
source .venv/bin/activate
kaggle datasets download aryantputta/hybrid-satellite-telemetry -p data --unzip
python data_generation/simulate_satellite.py
python data_generation/inject_faults.py
python hardware_noise_capture/noise_processing.py --noise data/arduino_noise.csv
python recurrence_plot_encoder/rp_encoder.py
python training/train_cnn.py
python training/train_lstm.py
python training/train_autoencoder.py
python training/train_isolation_forest.py
python evaluation/evaluate_models.py
python evaluation/compute_metrics.py
# Optional figure regeneration
python figures/generate_fig5_architecture.py
python figures/generate_fig8_results.py
python figures/generate_fig9_fault_type.py
python figures/generate_fig10_noise_effect.py
```

I run the one-command pipeline without figures by default:

```bash
bash replication/reproduce_paper_results.sh
```

I include figures in that pipeline only when needed:

```bash
SKIP_FIGURES=0 bash replication/reproduce_paper_results.sh
```
