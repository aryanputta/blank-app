# Reproduce paper results

I reproduce the project in this order:

1. Bootstrap environment
2. Download Kaggle dataset
3. Run full pipeline
4. Verify results and plots files

```bash
bash replication/bootstrap_environment.sh
source .venv/bin/activate
kaggle datasets download aryantputta/hybrid-satellite-telemetry -p data --unzip
bash replication/run_full_pipeline.sh
python plots/generate_plots.py
```

Expected outputs:
- `results/model_comparison_metrics.csv`
- `results/overall_metrics.json`
- `results/hardware_noise_ablation.json`
- `results/reconstruction_error_stats.json`
