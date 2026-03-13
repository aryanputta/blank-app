"""Train Isolation Forest baseline."""

from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np

from models.isolation_forest import build_isolation_forest


def main() -> None:
    rng = np.random.default_rng(42)
    x = rng.normal(size=(10_000, 4))
    model = build_isolation_forest(random_state=42)
    model.fit(x)
    output = Path("artifacts/models/isolation_forest.joblib")
    output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output)
    Path("results").mkdir(exist_ok=True)
    Path("results/iforest_training_log.json").write_text('{"status":"fit_complete"}')
    print(f"Saved {output}")


if __name__ == "__main__":
    main()
