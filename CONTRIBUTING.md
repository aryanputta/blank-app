# Contributing

## Adding sensor channels

1. Update `simulate_satellite()` in `data/generate_dataset.py` to emit the new channel.
2. Update recurrence input assembly so `window_to_rp_image()` is called per new channel.
3. Update model input shapes and retrain, or fine-tune with the protocol below.

## Adding fault types

1. Add the fault definition in `inject_faults()` in `data/generate_dataset.py`.
2. Update fault tables in `evaluation/fault_type_eval.py`.
3. Retrain models and regenerate benchmark outputs.

## Using real mission telemetry

Follow the fine-tune protocol in the README using a frozen encoder and low learning rate (`1e-5`).
I freeze encoder layers because hybrid training already captures non-Gaussian noise patterns.

## Opening issues

Please label issues as:
- `[bug]`
- `[extension]`
- `[data]`
