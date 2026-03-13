"""Train CNN recurrence-plot autoencoder on normal windows."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from models.cnn_autoencoder import build_cnn_autoencoder


def main() -> None:
    x = np.load("artifacts/recurrence_plots.npy")
    model = build_cnn_autoencoder(input_shape=x.shape[1:])
    history = model.fit(x, x, epochs=1, batch_size=32, verbose=1, validation_split=0.1)
    output = Path("artifacts/models/cnn_rp.keras")
    output.parent.mkdir(parents=True, exist_ok=True)
    model.save(output)
    Path("results").mkdir(exist_ok=True)
    Path("results/cnn_training_log.json").write_text(str(history.history))
    print(f"Saved {output}")


if __name__ == "__main__":
    main()
