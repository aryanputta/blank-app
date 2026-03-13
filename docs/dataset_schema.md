# Dataset schema

I store telemetry as row-wise time series records with these columns:

- `satellite_id`: satellite run identifier such as `SAT_01`
- `timestamp`: sample index at 10 Hz
- `power_w`: power draw in watts
- `temp_c`: bus temperature in Celsius
- `voltage_v`: bus voltage in volts
- `wheel_rpm`: reaction wheel speed in RPM
- `fault_class`: one of `NOMINAL`, `POWER_SPIKE`, `THERMAL_DRIFT`, `VOLTAGE_DROP`, `WHEEL_OSCILLATION`, `SENSOR_DROPOUT`

I generate ten satellites and keep SAT_09 and SAT_10 for held-out testing.
