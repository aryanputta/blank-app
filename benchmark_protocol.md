# Benchmark protocol

I designed this benchmark so another researcher can reproduce my comparison study exactly.

## Dataset structure
I use telemetry records with these columns:

- `satellite_id`
- `timestamp`
- `power_w`
- `temp_c`
- `voltage_v`
- `wheel_rpm`
- `fault_class`

I organize the data by simulated satellite identity and keep timestamps ordered inside each satellite stream.

## Fault taxonomy
I evaluate five anomaly types:

- `POWER_SPIKE`
- `THERMAL_DRIFT`
- `VOLTAGE_DROP`
- `WHEEL_OSCILLATION`
- `SENSOR_DROPOUT`

## Evaluation metrics
I report:

- Per class precision, recall, and F1
- Macro F1 across all fault classes
- Overall F1 for global comparison

I also report targeted F1 for `WHEEL_OSCILLATION` because reaction wheel instability is operationally critical.

## Model comparison procedure
I train and evaluate all models on the same split.

- Training satellites: `SAT_01` to `SAT_08`
- Testing satellites: `SAT_09` to `SAT_10`

I run:

1. LSTM Autoencoder
2. CNN on recurrence plots
3. Standard Autoencoder
4. Isolation Forest

I compare model performance under two settings:

- simulation only input
- hybrid input that adds Arduino hardware noise traces
