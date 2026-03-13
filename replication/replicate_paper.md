# Paper replication guide

I use this guide to reproduce the benchmark in a clean environment.

## Commands

```bash
bash replication/bootstrap_environment.sh
source .venv/bin/activate
kaggle datasets download aryantputta/hybrid-satellite-telemetry -p data --unzip
bash replication/run_full_pipeline.sh
python plots/generate_plots.py
```

If I want the heavy figure scripts too, I run:

```bash
SKIP_FIGURES=0 bash replication/run_full_pipeline.sh
```
