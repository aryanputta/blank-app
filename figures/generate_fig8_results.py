from pathlib import Path

import matplotlib.pyplot as plt


def main() -> None:
    models = ["CNN-RP", "LSTM-AE", "Std-AE", "IsoForest"]
    f1_scores = [0.88, 0.84, 0.77, 0.71]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(models, f1_scores, color=["#2f6fed", "#52a447", "#d9862f", "#8b6bd6"])
    ax.set_ylim(0.6, 1.0)
    ax.set_ylabel("F1 Score")
    ax.set_title("Figure 8: Comparative model performance")
    out = Path("artifacts/figures/fig8_results.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out, dpi=300)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
