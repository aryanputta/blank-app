# satellite-anomaly-detection

## Project Overview
I built this repository to support my paper, **Hybrid Satellite Telemetry Anomaly Detection: A Dataset, Fault Taxonomy, Recurrence Plot Computer Vision Method, and Comparative Machine Learning Study**. My goal is to make every experiment reproducible while keeping sensitive local environment details out of version control.

I study satellite telemetry anomaly detection across multiple simulated spacecraft so I can identify both known and subtle failure signatures. Fault type labels matter because operators need to know what failed, not only whether a sample is anomalous.

I include a dedicated `WHEEL_OSCILLATION` class because reaction wheel instability can cascade into attitude control failure. I use the Kepler reaction wheel failure as a motivating historical example that shows why early detection of oscillation behavior is critical.

## Dataset Description
My dataset contains approximately 100,000 timestamped telemetry readings sampled across ten simulated satellites and four telemetry channels:

- `power_w`
- `temp_c`
- `voltage_v`
- `wheel_rpm`

My fault taxonomy has five classes:

- `POWER_SPIKE`
- `THERMAL_DRIFT`
- `VOLTAGE_DROP`
- `WHEEL_OSCILLATION`
- `SENSOR_DROPOUT`

## Models Implemented
I evaluate the four architectures from my paper:

- LSTM Autoencoder
- CNN on Recurrence Plots
- Standard Autoencoder
- Isolation Forest

## Key Results
These are the headline numbers I report in the paper:

- CNN recurrence plot model achieves **0.91 F1** on `WHEEL_OSCILLATION`
- LSTM autoencoder achieves **0.84 overall F1**
- Hybrid hardware noise improves generalization by approximately **6.5 percent F1**

## Live Embedded Demo
My embedded demonstration pipeline is:

**Arduino sensor array → Raspberry Pi 4 → recurrence plot encoding → model classification**

I measured end to end inference latency under **150 milliseconds** in the demo setup.

## Reproducibility
I provide scripts that regenerate dataset processing, model training, and evaluation. If Kaggle data is not downloaded yet, my replication script creates a local simulation fallback so the full workflow still runs end to end. I skip figure generation by default in the one-command script so setup is faster.

### 1) Download dataset from Kaggle
```bash
kaggle datasets download aryantputta/hybrid-satellite-telemetry -p data --unzip
```

### 2) Set up environment
```bash
bash replication/bootstrap_environment.sh
source .venv/bin/activate
```

Manual option:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Or with Conda:
```bash
conda env create -f environment.yml
conda activate satellite-anomaly-detection
```

### 3) Train models
```bash
python training/train_cnn.py
python training/train_lstm.py
python training/train_autoencoder.py
python training/train_isolation_forest.py
```

### 4) Evaluate models
```bash
python evaluation/evaluate_models.py
python evaluation/compute_metrics.py
```

### 5) Regenerate figures (optional)
```bash
python figures/generate_fig5_architecture.py
python figures/generate_fig8_results.py
python figures/generate_fig9_fault_type.py
python figures/generate_fig10_noise_effect.py
```

### One command reproduction (figures skipped by default)
```bash
bash replication/reproduce_paper_results.sh
```

To include figures in the one-command run:
```bash
SKIP_FIGURES=0 bash replication/reproduce_paper_results.sh
```

## Figure Reproduction
I fixed layout issues in my figure scripts:

- Figure 5 output labels are not cropped.
- Figure 7 Arduino Uno label fits correctly inside its diagram box.

## Evaluation Protocol
I use a per satellite split to prevent memorization of a single simulated satellite.

- Training satellites: `SAT_01` to `SAT_08`
- Testing satellites: `SAT_09` to `SAT_10`

## Environment and API Security
I keep local secrets in `.env` and I do not commit secrets, keys, or private config files.

I provide `.env.example` as a safe template.
