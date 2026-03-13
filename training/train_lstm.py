"""Train LSTM autoencoder on telemetry sequence windows."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from models.lstm_autoencoder import build_lstm_autoencoder


def main() -> None:
    x = np.random.randn(500, 64, 4).astype("float32")
    model = build_lstm_autoencoder(timesteps=64, features=4)
    model.fit(x, x, epochs=1, batch_size=32, verbose=1)
    output = Path("artifacts/models/lstm_autoencoder.keras")
    output.parent.mkdir(parents=True, exist_ok=True)
    model.save(output)
    print(f"Saved {output}")


if __name__ == "__main__":
    main()
