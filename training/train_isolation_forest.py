"""Train Isolation Forest baseline."""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np

from models.isolation_forest import build_isolation_forest


def main() -> None:
    x = np.random.randn(10_000, 4)
    model = build_isolation_forest()
    model.fit(x)
    output = Path("artifacts/models/isolation_forest.joblib")
    output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output)
    print(f"Saved {output}")


if __name__ == "__main__":
    main()
