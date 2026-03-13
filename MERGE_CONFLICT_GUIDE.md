# Merge conflict fix guide

I could not fetch your GitHub base branch from this environment because outbound GitHub access is blocked by proxy restrictions (`CONNECT tunnel failed, response 403`).

I added a one-command conflict resolver script so you can resolve your existing PR conflicts locally and push immediately.

## Quick steps

1. Open your local branch for this PR.
2. Merge or rebase the target branch into it (for example `main`).
3. Run:

```bash
bash scripts/resolve_conflicts_keep_current_branch.sh
```

4. Commit and push:

```bash
git commit -m "Resolve merge conflicts keeping feature branch content"
git push
```

This script keeps the feature-branch version for every conflicted file and stages the result.
