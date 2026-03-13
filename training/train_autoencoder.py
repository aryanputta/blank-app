"""Train dense autoencoder baseline."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from models.standard_autoencoder import build_autoencoder


def main() -> None:
    x = np.random.randn(2_000, 256).astype("float32")
    model = build_autoencoder(input_dim=256)
    model.fit(x, x, epochs=1, batch_size=64, verbose=1)
    output = Path("artifacts/models/standard_autoencoder.keras")
    output.parent.mkdir(parents=True, exist_ok=True)
    model.save(output)
    print(f"Saved {output}")


if __name__ == "__main__":
    main()
