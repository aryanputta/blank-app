# Conflict resolution decisions for PR #3

I resolve the conflicted files listed in the PR by keeping the feature-branch implementation for the satellite anomaly benchmark.

## Decision rule

- Keep current branch content for the 21 conflicted files listed in GitHub merge UI.
- Do not reintroduce removed Next.js scaffold files.
- Preserve Kaggle publishing and reproducibility scripts already added on this branch.

## How to apply

```bash
bash scripts/resolve_pr3_conflicts.sh
```

Then commit and push:

```bash
git commit -m "Resolve PR #3 merge conflicts"
git push
```
