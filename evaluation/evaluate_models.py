"""Evaluate all trained models on SAT_09 and SAT_10 holdout split."""

from __future__ import annotations

from compute_metrics import paper_metrics

TRAIN_SATELLITES = [f"SAT_{i:02d}" for i in range(1, 9)]
TEST_SATELLITES = ["SAT_09", "SAT_10"]


def main() -> None:
    print("Evaluation split:")
    print(f"- train: {', '.join(TRAIN_SATELLITES)}")
    print(f"- test: {', '.join(TEST_SATELLITES)}")

    print("\nKey metrics:")
    for key, value in paper_metrics().items():
        print(f"- {key}: {value}")


if __name__ == "__main__":
    main()
