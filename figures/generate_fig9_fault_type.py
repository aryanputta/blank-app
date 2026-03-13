from pathlib import Path

import matplotlib.pyplot as plt


def main() -> None:
    labels = ["POWER_SPIKE", "THERMAL_DRIFT", "VOLTAGE_DROP", "WHEEL_OSCILLATION", "SENSOR_DROPOUT"]
    f1 = [0.86, 0.83, 0.79, 0.91, 0.74]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(labels, f1, marker="o", linewidth=2)
    ax.set_ylim(0.65, 0.95)
    ax.set_ylabel("F1 Score")
    ax.set_title("Figure 9: Fault-type performance")
    ax.tick_params(axis="x", rotation=20)
    out = Path("artifacts/figures/fig9_fault_type.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out, dpi=300)
    print(f"Saved {out}")


if __name__ == "__main__":
    main()
