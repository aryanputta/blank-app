# Fault taxonomy

I use five operationally meaningful fault classes:

1. `POWER_SPIKE`: transient power surge on the `power_w` channel for 30 samples.
2. `THERMAL_DRIFT`: upward drift in `temp_c` for 100 samples.
3. `VOLTAGE_DROP`: sustained bus undervoltage in `voltage_v` for 50 samples.
4. `WHEEL_OSCILLATION`: oscillatory disturbance in `wheel_rpm` for 80 samples.
5. `SENSOR_DROPOUT`: short missing-data outage across all channels for 20 samples.

I assign the corresponding class label to every affected sample.
