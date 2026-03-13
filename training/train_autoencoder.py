"""Train dense autoencoder baseline."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from models.standard_autoencoder import build_autoencoder


def main() -> None:
    rng = np.random.default_rng(42)
    x = rng.normal(size=(2_000, 200)).astype("float32")
    model = build_autoencoder(input_dim=200)
    history = model.fit(x, x, epochs=1, batch_size=64, verbose=1, validation_split=0.1)
    output = Path("artifacts/models/standard_autoencoder.keras")
    output.parent.mkdir(parents=True, exist_ok=True)
    model.save(output)
    Path("results").mkdir(exist_ok=True)
    Path("results/ae_training_log.json").write_text(str(history.history))
    print(f"Saved {output}")


if __name__ == "__main__":
    main()
