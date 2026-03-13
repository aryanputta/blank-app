# Hybrid Satellite Telemetry Anomaly Dataset

I generated this dataset to provide labeled satellite telemetry fault classes with reproducible simulation, hardware noise capture, and benchmark-ready evaluation artifacts in one package.

Paper: https://arxiv.org/abs/2501.00001  
GitHub: https://github.com/aryanputta/satellite-anomaly-detection

## The Problem with Existing Benchmarks

Dominant satellite anomaly datasets such as SMAP and MSL from Hundman et al. (2018), and many KDD-style anomaly datasets, use binary labels. Binary labels answer one question, anomaly or not anomaly.

For operations, that is incomplete. Ground teams need subsystem-specific fault identity, progression behavior, and model-specific performance tradeoffs. A binary alert does not specify whether the issue is thermal drift, power surge, wheel instability, or sensor dropout.

I provide open fault-type labels with fixed durations and documented injection logic. I also include WHEEL_OSCILLATION because reaction wheel bearing failures ended Kepler's primary mission in 2013. In my benchmark, CNN recurrence-plot encoding reaches 0.91 F1 on WHEEL_OSCILLATION.

## What Is in the Dataset

- Rows: approximately 100,000
- Satellite runs: 10 (`SAT_01` to `SAT_10`)
- Sensor channels: 4
- Anomaly rate: 5.28%

| Column name | Type | Units | Description |
|---|---|---|---|
| timestamp | int | timestep | Sample index at 10 Hz |
| satellite_id | string | n/a | Satellite run identifier |
| power_w | float | watts | Electrical power channel |
| temp_c | float | celsius | Thermal channel |
| voltage_v | float | volts | Bus voltage channel |
| wheel_rpm | float | rpm | Reaction wheel speed channel |
| anomaly | int | binary | 0 for normal, 1 for anomaly |
| fault_type | string | class label | Fault taxonomy label |

## Fault Types

| fault_type | affected column | injection duration (timesteps) | physical phenomenon modeled | source |
|---|---|---:|---|---|
| POWER_SPIKE | power_w | 30 | transient load surge | NASA-HDBK-7004C |
| THERMAL_DRIFT | temp_c | 100 | persistent thermal drift | NASA-HDBK-7004C |
| VOLTAGE_DROP | voltage_v | 50 | sustained bus undervoltage | NASA-HDBK-7004C |
| WHEEL_OSCILLATION | wheel_rpm | 80 | reaction wheel oscillation | NASA-HDBK-7004C |
| SENSOR_DROPOUT | all channels | 20 | telemetry outage | NASA-HDBK-7004C |

## How the Dataset Was Built

### 5a) Orbital physics simulation

I model four channels with sinusoidal orbital dynamics over a 90-minute LEO period. Temperature lags power by `pi/4` for thermal inertia. Voltage lags by `-pi/3` for eclipse discharge effects. Wheel RPM evolves across two orbital periods. I generate 10 runs with amplitude variation of +/-10% and phase jitter of +/-0.1 radians.

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

### 5b) Arduino hardware noise capture

I captured physical noise on Arduino Uno with DHT22, MPU-6050, and a voltage divider at 10 Hz for 30 minutes.

- DHT22-like thermal noise lag-1 autocorrelation: `r = 0.72`
- MPU-6050-like resonance peak: `5 Hz`
- These properties are absent in Gaussian white noise models

This non-Gaussian noise structure aligns with the +6.5% average F1 improvement for hybrid training.

```cpp
void loop() {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_ADDR, 6, true);

  int16_t ax = Wire.read() << 8 | Wire.read();
  Wire.read(); Wire.read();
  Wire.read(); Wire.read();

  int dhtProxy = digitalRead(DHT_PIN) * 100;
  int voltRaw = analogRead(VOLTAGE_PIN);

  float tempNoise = dhtProxy - baselineTemp;
  float accelNoise = (float)ax - baselineAccel;
  float voltNoise = (float)voltRaw - baselineVolt;

  Serial.print(millis());
  Serial.print(",");
  Serial.print(tempNoise);
  Serial.print(",");
  Serial.print(accelNoise);
  Serial.print(",");
  Serial.println(voltNoise);

  delay(100);
}
```

### 5c) Fault injection

I inject each fault once per satellite run with a per-satellite seed.

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

## Benchmark Results

### 6a) Overall model performance

| Model | Precision | Recall | F1 | AUC-ROC |
|---|---:|---:|---:|---:|
| LSTM Autoencoder | 0.86 | 0.83 | 0.84 | 0.91 |
| CNN on Recurrence Plots | 0.83 | 0.81 | 0.82 | 0.89 |
| Standard Autoencoder | 0.78 | 0.74 | 0.76 | 0.83 |
| Isolation Forest | 0.70 | 0.67 | 0.68 | 0.76 |

### 6b) F1 by fault type

| Fault type | LSTM | CNN-RP | Std AE | Iso Forest |
|---|---:|---:|---:|---:|
| POWER_SPIKE | 0.81 | 0.84 | 0.79 | **0.85** |
| THERMAL_DRIFT | **0.92** | 0.89 | 0.71 | 0.57 |
| VOLTAGE_DROP | **0.86** | 0.85 | 0.76 | 0.73 |
| WHEEL_OSCILLATION | 0.89 | **0.91** | 0.70 | 0.64 |
| SENSOR_DROPOUT | 0.78 | 0.83 | 0.81 | **0.88** |

### 6c to 6e) Key findings

Model ranking reverses by fault type. A model that leads on POWER_SPIKE does not lead on THERMAL_DRIFT. The THERMAL_DRIFT gap is 35 points between LSTM (0.92) and Isolation Forest (0.57). Hybrid training yields +6.5% average F1 across four architectures. This matters for environmental missions because missed thermal drift can bias calibration for greenhouse gas, sea-surface temperature, and polar ice products.

## Recurrence Plot Encoding

I encode 50-step windows as binary recurrence matrices from pairwise distances. This maps telemetry structure into image space and lets me apply standard CNN architectures directly.

The method follows recurrence analysis from Eckmann et al. (1987). In this dataset, WHEEL_OSCILLATION forms periodic textures, THERMAL_DRIFT forms widening diagonal structures, SENSOR_DROPOUT forms blank rectangles, and POWER_SPIKE forms localized bright clusters.

```python
def window_to_rp_image(window, eps=0.1):
    import numpy as np
    arr = np.asarray(window, dtype=np.float32).reshape(-1, 1)
    distances = np.sqrt((arr - arr.T) ** 2)
    return (distances <= eps).astype(np.float32)
```

## Quickstart

```python
import pandas as pd

df = pd.read_csv("hybrid_satellite_telemetry.csv")

train = df[df["satellite_id"].isin([f"SAT_{i:02d}" for i in range(1, 9)])]
test = df[df["satellite_id"].isin(["SAT_09", "SAT_10"])]

print("train rows", len(train))
print("test rows", len(test))
print(df["fault_type"].value_counts(normalize=True).mul(100).round(3))
```

Recommended split is SAT_01 through SAT_08 for train and SAT_09 through SAT_10 for test. The `fault_type` column supports multi-class classification directly.

Full pipeline notebook: https://github.com/aryanputta/satellite-anomaly-detection/blob/main/notebooks/full_pipeline.ipynb

## Files in This Dataset

| filename | description | format | size |
|---|---|---|---|
| hybrid_satellite_telemetry.csv | main benchmark telemetry table | CSV | ~8-12 MB |
| generate_dataset.py | dataset generation script | Python | ~10 KB |
| noise_capture.ino | Arduino capture sketch | Arduino C++ | ~2 KB |
| recurrence_plot.py | recurrence encoding utility | Python | ~3 KB |
| full_pipeline.ipynb | end-to-end benchmark tutorial | Jupyter notebook | ~100-300 KB |

## Citation

APA:

Putta, A. (2026). *Hybrid Satellite Telemetry Anomaly Detection: A Dataset, Fault Taxonomy, Recurrence Plot Computer Vision Method, and Comparative Machine Learning Study*. 13th Annual New Jersey Big Data Alliance Symposium.

```bibtex
@inproceedings{putta2026hybrid,
  title={Hybrid Satellite Telemetry Anomaly Detection: A Dataset, Fault Taxonomy, Recurrence Plot Computer Vision Method, and Comparative Machine Learning Study},
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

## Intended Uses and Known Limitations

Intended uses:
- Satellite health monitoring ML research
- Anomaly detection benchmarking
- Time-series computer vision studies
- Embedded ML deployment tests
- Reproducibility studies

Known limitations:
- Four channels only, operational spacecraft usually have hundreds
- Room-temperature hardware noise, not thermal-vacuum conditions
- Fault magnitudes from literature priors, not mission archive validation
- A fixed threshold parameter still requires tuning per deployment

## Acknowledgments

Faculty Advisor: Prof. Santosh Nagarakatte, Rutgers University.  
Venue: 13th Annual New Jersey Big Data Alliance Symposium, May 20, 2026.
