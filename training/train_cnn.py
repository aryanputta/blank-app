"""Train CNN classifier on recurrence plot tensors."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from models.cnn_autoencoder import build_cnn


def main() -> None:
    x = np.load("artifacts/recurrence_plots.npy")
    x = x[..., None]
    y = np.random.randint(0, 5, size=len(x))
    model = build_cnn(input_shape=x.shape[1:])
    model.fit(x, y, epochs=1, batch_size=64, verbose=1)
    output = Path("artifacts/models/cnn_rp.keras")
    output.parent.mkdir(parents=True, exist_ok=True)
    model.save(output)
    print(f"Saved {output}")


if __name__ == "__main__":
    main()
