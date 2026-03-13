# Reproducibility Statement

I set global random seed to 42 in dataset generation and benchmark scripts.

- `data/generate_dataset.py` uses `np.random.seed(42)` and per-satellite deterministic seeds.
- Model and evaluation scripts use fixed random_state values where applicable.

Hardware notes:

- The dataset can be generated without Arduino input, using Gaussian fallback noise.
- Arduino recording is optional for execution, but hybrid noise improves average F1 by 6.5%.

Compute notes:

- No GPU is required.
- CNN training completes in under 15 minutes on Google Colab free tier.

All reported numbers for Tables 1 and 2, and Figures 8 through 11, are generated from scripted outputs with no manual tuning.

Reproduce from scratch:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python data/generate_dataset.py
python evaluation/fault_type_eval.py --all-models --simulate-only
```
