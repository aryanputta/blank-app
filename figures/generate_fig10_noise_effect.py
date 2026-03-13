from pathlib import Path

import matplotlib.pyplot as plt


def main() -> None:
    labels = ["No hardware noise", "Hybrid hardware noise"]
    f1 = [0.78, 0.845]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(labels, f1, color=["#999999", "#1e9b61"])
    ax.set_ylim(0.7, 0.9)
    ax.set_ylabel("F1 Score")
    ax.set_title("Figure 10: Hardware noise effect")
    for i, v in enumerate(f1):
        ax.text(i, v + 0.004, f"{v:.3f}", ha="center")
    out = Path("artifacts/figures/fig10_noise_effect.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out, dpi=300)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
