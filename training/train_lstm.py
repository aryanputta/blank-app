"""Train LSTM autoencoder on normal telemetry windows."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from models.lstm_autoencoder import build_lstm_autoencoder


def main() -> None:
    rng = np.random.default_rng(42)
    x = rng.normal(size=(500, 50, 4)).astype("float32")
    model = build_lstm_autoencoder(timesteps=50, features=4)
    history = model.fit(x, x, epochs=1, batch_size=32, verbose=1, validation_split=0.1)
    output = Path("artifacts/models/lstm_autoencoder.keras")
    output.parent.mkdir(parents=True, exist_ok=True)
    model.save(output)
    Path("results").mkdir(exist_ok=True)
    Path("results/lstm_training_log.json").write_text(str(history.history))
    print(f"Saved {output}")


if __name__ == "__main__":
    main()
