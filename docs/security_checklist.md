# Security checklist

- [x] `.env` and `.env.local` are gitignored
- [x] private key and certificate patterns are gitignored (`*.pem`, `*.key`, `*.crt`)
- [x] Kaggle credential files are gitignored (`kaggle.json`, `.kaggle/`)
- [x] no API keys are hardcoded in Python scripts
- [x] no absolute local machine paths are used in training/evaluation scripts
- [x] repository does not commit raw Kaggle telemetry dumps by default
