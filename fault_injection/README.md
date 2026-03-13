# Fault injection module

I keep the fault implementation in `fault_library.py` so I can reuse one consistent taxonomy everywhere.

For each fault, I document:
- affected channel
- duration
- signal pattern
- label assignment

Durations in samples: POWER_SPIKE 30, THERMAL_DRIFT 100, VOLTAGE_DROP 50, WHEEL_OSCILLATION 80, SENSOR_DROPOUT 20.
