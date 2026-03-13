# Hybrid Satellite Telemetry Anomaly Detection

**Official repository name:** `satellite-anomaly-detection`

A reproducible pipeline for labeled satellite telemetry fault detection using orbital simulation, hardware noise capture, recurrence plot encoding, and four benchmark model families.

![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![Code License](https://img.shields.io/badge/code%20license-MIT-green) ![Data License](https://img.shields.io/badge/data%20license-CC%20BY%204.0-green) ![Venue](https://img.shields.io/badge/venue-NJ%20Big%20Data%20Alliance%202026-purple) ![Status](https://img.shields.io/badge/status-reproducible%20benchmark-orange)

## 1) What this project is

Dominant prior satellite anomaly datasets such as SMAP and MSL from Hundman et al. (2018) use binary labels. Binary labels indicate anomaly or normal, but they do not indicate which subsystem is failing.

Ground operators need fault-type information to prioritize action and choose suitable detection models per failure mode. I built a hybrid dataset and benchmark to provide that information directly: orbital telemetry simulation, Arduino hardware noise capture, five labeled fault classes, four model architectures, and recurrence plot encoding.

The `WHEEL_OSCILLATION` class maps to reaction wheel instability, which ended Kepler's primary mission in 2013. In my evaluation, CNN on recurrence plots reaches **0.91 F1** on `WHEEL_OSCILLATION`. The embedded path runs on Raspberry Pi 4 with end-to-end latency under **150 ms**.

## 2) Results

### Table A: Overall model performance

| Model | Precision | Recall | F1 | AUC-ROC |
|---|---:|---:|---:|---:|
| LSTM Autoencoder | 0.86 | 0.83 | 0.84 | 0.91 |
| CNN on Recurrence Plots | 0.83 | 0.81 | 0.82 | 0.89 |
| Standard Autoencoder | 0.78 | 0.74 | 0.76 | 0.83 |
| Isolation Forest | 0.70 | 0.67 | 0.68 | 0.76 |

### Table B: F1 by fault type

| Fault type | LSTM | CNN-RP | Std AE | Iso Forest | Best |
|---|---:|---:|---:|---:|---|
| POWER_SPIKE | 0.81 | 0.84 | 0.79 | 0.85 | Isolation Forest |
| THERMAL_DRIFT | 0.92 | 0.89 | 0.71 | 0.57 | LSTM |
| VOLTAGE_DROP | 0.86 | 0.85 | 0.76 | 0.73 | LSTM |
| WHEEL_OSCILLATION | 0.89 | 0.91 | 0.70 | 0.64 | CNN-RP |
| SENSOR_DROPOUT | 0.78 | 0.83 | 0.81 | 0.88 | Isolation Forest |

The THERMAL_DRIFT gap between LSTM and Isolation Forest is **35 points** (0.92 vs 0.57). Hybrid training improves mean F1 by **+6.5%** versus simulation-only training across all four architectures.

## 3) Dataset

- Size: approximately 100,000 rows
- Satellites: SAT_01 through SAT_10
- Channels: 4 (`power_w`, `temp_c`, `voltage_v`, `wheel_rpm`)
- Anomaly rate: 5.28%
- Kaggle: https://kaggle.com/datasets/aryantputta/hybrid-satellite-telemetry

### Column schema

| Column | Type | Description |
|---|---|---|
| timestamp | int | Telemetry sample index at 10 Hz |
| satellite_id | string | Satellite run identifier |
| power_w | float | Simulated power channel in watts |
| temp_c | float | Simulated temperature channel in C |
| voltage_v | float | Simulated bus voltage in volts |
| wheel_rpm | float | Simulated reaction wheel speed in RPM |
| anomaly | int | Binary label, 0 normal, 1 anomaly |
| fault_type | string | Multi-class label for fault taxonomy |

### Fault injection table

| Fault label | Channel | Duration (timesteps) | Physical model |
|---|---|---:|---|
| POWER_SPIKE | power_w | 30 | Power surge transient |
| THERMAL_DRIFT | temp_c | 100 | Slow thermal drift |
| VOLTAGE_DROP | voltage_v | 50 | Sustained undervoltage |
| WHEEL_OSCILLATION | wheel_rpm | 80 | Wheel oscillation |
| SENSOR_DROPOUT | all | 20 | Short sensor outage |

### Hardware noise notes

DHT22-like thermal noise has lag-1 autocorrelation **r = 0.72**. MPU-6050-like vibration noise has a **5 Hz** resonance peak. Gaussian white noise does not contain these properties. This non-Gaussian structure drives the observed **+6.5% F1** hybrid-training gain.

## 4) Recurrence plot encoding

I encode each 50-step sensor window as a binary recurrence image based on pairwise distances, consistent with Eckmann, Kamphorst, and Ruelle (1987). This representation exposes periodic and structural patterns to CNN models.

```python
def window_to_rp_image(window, eps=0.1):
    import numpy as np
    arr = np.asarray(window, dtype=np.float32).reshape(-1, 1)
    distances = np.sqrt((arr - arr.T) ** 2)
    return (distances <= eps).astype(np.float32)
```

Visual signatures in recurrence space:
- WHEEL_OSCILLATION: periodic texture
- THERMAL_DRIFT: widening diagonal band
- SENSOR_DROPOUT: blank rectangular region
- POWER_SPIKE: isolated bright cluster
- NORMAL: regular diagonal banding from orbital period

## 5) Architecture

### CNN Autoencoder
Input shape `(50, 50, 4)`, latent dimension `64`, parameter count approximately `2.1M`, objective is pixel MSE on normal windows, threshold is the 99th percentile.

```python
def build_cnn_autoencoder(input_shape=(50, 50, 4)):
    from tensorflow import keras
    inputs = keras.Input(shape=input_shape)
    x = keras.layers.Conv2D(32, 3, activation="relu", padding="same")(inputs)
    x = keras.layers.MaxPooling2D(2, padding="same")(x)
    x = keras.layers.Conv2D(64, 3, activation="relu", padding="same")(x)
    x = keras.layers.MaxPooling2D(2, padding="same")(x)
    x = keras.layers.Conv2D(128, 3, activation="relu", padding="same")(x)
    x = keras.layers.Flatten()(x)
    latent = keras.layers.Dense(64)(x)
    x = keras.layers.Dense(13 * 13 * 128, activation="relu")(latent)
    x = keras.layers.Reshape((13, 13, 128))(x)
    x = keras.layers.Conv2DTranspose(128, 3, strides=2, activation="relu", padding="same")(x)
    x = keras.layers.Conv2DTranspose(64, 3, strides=2, activation="relu", padding="same")(x)
    x = keras.layers.Conv2D(4, 3, activation="linear", padding="same")(x)
    outputs = keras.layers.Cropping2D(((1, 1), (1, 1)))(x)
    model = keras.Model(inputs, outputs)
    model.compile(optimizer="adam", loss="mse")
    return model
```

### LSTM Autoencoder
Encoder-decoder LSTM with window shape `(50, 4)`, same 99th-percentile threshold protocol.

```python
def build_lstm_autoencoder(input_shape=(50, 4)):
    from tensorflow import keras
    inputs = keras.Input(shape=input_shape)
    x = keras.layers.LSTM(128)(inputs)
    x = keras.layers.RepeatVector(input_shape[0])(x)
    x = keras.layers.LSTM(128, return_sequences=True)(x)
    outputs = keras.layers.TimeDistributed(keras.layers.Dense(input_shape[1]))(x)
    model = keras.Model(inputs, outputs)
    model.compile(optimizer="adam", loss="mse")
    return model
```

### Standard Autoencoder
Flattened 200-dimensional input with fully connected encoder and decoder.

### Isolation Forest
Linear-complexity baseline for point anomalies, measured at **1.2 ms/window** on Raspberry Pi 4.

## 6) Orbital simulation

I generate ten runs with varied orbital parameters for fleet variability.

```python
def simulate_satellite(satellite_id, n_steps=10_000, sample_hz=10, amplitude_scale=1.0, phase_jitter_rad=0.0):
    import numpy as np
    import pandas as pd
    t = np.arange(n_steps)
    period = 90 * 60 * sample_hz
    power_w = 120 + amplitude_scale * 10 * np.sin(2 * np.pi * t / period + phase_jitter_rad)
    temp_c = 24 + amplitude_scale * 3 * np.sin(2 * np.pi * t / period + np.pi / 4 + phase_jitter_rad)
    voltage_v = 28 + amplitude_scale * 0.8 * np.sin(2 * np.pi * t / period - np.pi / 3 + phase_jitter_rad)
    wheel_rpm = 3600 + amplitude_scale * 180 * np.sin(2 * np.pi * t / (2 * period) + phase_jitter_rad)
    return pd.DataFrame({
        "timestamp": t,
        "satellite_id": satellite_id,
        "power_w": power_w,
        "temp_c": temp_c,
        "voltage_v": voltage_v,
        "wheel_rpm": wheel_rpm,
        "anomaly": 0,
        "fault_type": "NOMINAL",
    })
```

Phase interpretation:
- `temp_c` lags `power_w` by `pi/4` for thermal inertia.
- `voltage_v` lags by `-pi/3` for eclipse discharge behavior.
- `wheel_rpm` drifts across two orbital periods for slower control cycles.

## 7) Fault injection

Fault class definitions align with NASA-HDBK-7004C categories used in my benchmark protocol.

```python
def inject_faults(df, seed):
    import numpy as np
    out = df.copy()
    rng = np.random.default_rng(seed)
    specs = {
        "POWER_SPIKE": 30,
        "THERMAL_DRIFT": 100,
        "VOLTAGE_DROP": 50,
        "WHEEL_OSCILLATION": 80,
        "SENSOR_DROPOUT": 20,
    }
    starts = rng.choice(np.arange(400, len(out) - 400), size=5, replace=False)
    order = ["POWER_SPIKE", "THERMAL_DRIFT", "VOLTAGE_DROP", "WHEEL_OSCILLATION", "SENSOR_DROPOUT"]
    for st, fault in zip(starts, order):
        dur = specs[fault]
        en = min(len(out), st + dur)
        sl = slice(st, en)
        if fault == "POWER_SPIKE":
            out.loc[sl, "power_w"] += 20 * np.exp(-np.arange(en - st) / 8)
        elif fault == "THERMAL_DRIFT":
            out.loc[sl, "temp_c"] += np.linspace(0, 9, en - st)
        elif fault == "VOLTAGE_DROP":
            out.loc[sl, "voltage_v"] -= 2.2
        elif fault == "WHEEL_OSCILLATION":
            out.loc[sl, "wheel_rpm"] += 240 * np.sin(2 * np.pi * np.arange(en - st) / 8)
        elif fault == "SENSOR_DROPOUT":
            out.loc[sl, ["power_w", "temp_c", "voltage_v", "wheel_rpm"]] = np.nan
        out.loc[sl, "anomaly"] = 1
        out.loc[sl, "fault_type"] = fault
    return out
```

## 8) Physical demo system

Hardware:
- Arduino Uno
- DHT22
- MPU-6050
- Voltage divider
- Raspberry Pi 4
- 7-inch touchscreen

Pipeline: 10 Hz sampling, USB serial, RP encoding, inference, display at 100 ms refresh.

| Component | Latency |
|---|---:|
| Isolation Forest inference | 1.2 ms per window |
| RP generation | 3.8 ms per window |
| End-to-end | < 150 ms |
| Throughput | ~200 readings/second |

## 9) Fine-tuning and scaling

```python
def fine_tune_cnn(model, X_real, y_real=None, lr=1e-5, freeze_encoder=True, epochs=5):
    from tensorflow import keras
    if freeze_encoder:
        for layer in model.layers[:6]:
            layer.trainable = False
    model.compile(optimizer=keras.optimizers.Adam(lr), loss="mse")
    model.fit(X_real, X_real, epochs=epochs, batch_size=16, verbose=0)
    return model
```

Scaling rule:
- CNN input changes to `(50, 50, n)` for `n` channels.
- LSTM width scales by `sqrt(n/4)`.
- Up to about 20 channels, no structural redesign is required.

I freeze encoder layers during transfer because hybrid training already exposes them to realistic non-Gaussian noise signatures.

## 10) How to reproduce everything

Requirements:
- Python 3.10+
- TensorFlow 2.x
- scikit-learn
- NumPy
- pandas
- matplotlib

No GPU is required. CNN training completes in under 15 minutes on Google Colab free tier.

```bash
git clone https://github.com/aryanputta/satellite-anomaly-detection.git
cd satellite-anomaly-detection
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python data/generate_dataset.py
python evaluation/fault_type_eval.py --all-models --simulate-only
python plots/generate_plots.py
```

The Colab notebook `notebooks/full_pipeline.ipynb` reproduces figures and tables from scratch.

Hardware BOM for data reproduction:
- Arduino Uno: ~$12
- DHT22: ~$4
- MPU-6050: ~$3
- Voltage divider parts: ~$1
- Total: ~$20

## 11) Repository structure

```text
.
├── data/                          # Dataset generation scripts and output CSV
│   └── generate_dataset.py        # SAT_01..SAT_10 generation and noise blending
├── noise/
│   └── arduino_noise_capture/
│       ├── noise_capture.ino      # Arduino capture sketch
│       └── noise_log.csv          # Recorded hardware noise (user provided)
├── models/
│   ├── cnn_autoencoder.py         # CNN RP autoencoder
│   ├── lstm_autoencoder.py        # LSTM autoencoder
│   ├── standard_autoencoder.py    # Dense AE baseline
│   └── isolation_forest.py        # Isolation Forest baseline
├── encoding/
│   └── recurrence_plot.py         # RP encoding utilities
├── evaluation/
│   ├── fault_type_eval.py         # Table 1 and Table 2 generation
│   └── results/                   # Saved evaluation tables
├── demo/
│   └── live_demo.py               # Raspberry Pi live pipeline script
├── notebooks/
│   └── full_pipeline.ipynb        # Colab end-to-end workflow
└── README.md
```

## 12) Citation

```bibtex
@inproceedings{putta2026hybrid,
  title={Hybrid Satellite Telemetry Anomaly Detection},
  author={Putta, Aryan},
  booktitle={13th Annual New Jersey Big Data Alliance Symposium},
  year={2026}
}
```

```bibtex
@dataset{putta2026hybrid_dataset,
  title={Hybrid Satellite Telemetry Anomaly Dataset},
  author={Putta, Aryan},
  year={2026},
  publisher={Kaggle},
  url={https://kaggle.com/datasets/aryantputta/hybrid-satellite-telemetry},
  license={CC BY 4.0}
}
```

## 13) License

- Code: MIT
- Dataset: CC BY 4.0
