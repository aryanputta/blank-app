# Repository Rename Steps

I cannot rename the GitHub repository from this environment because I do not have your authenticated GitHub session.

Please rename it in less than one minute:

1. Open your repository on GitHub.
2. Go to **Settings**.
3. In **Repository name**, change it to:
   - `satellite-anomaly-detection`
4. Click **Rename**.

After rename, update your local remote with:

```bash
git remote set-url origin https://github.com/aryanputta/satellite-anomaly-detection.git
```

Verify:

```bash
git remote -v
```
