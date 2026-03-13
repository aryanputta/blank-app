#!/usr/bin/env bash
set -euo pipefail

# Run this after a merge/rebase reports conflicts, from your feature branch.
# It resolves all conflicted files by keeping current-branch content.

conflicted_files=$(git diff --name-only --diff-filter=U || true)

if [[ -z "$conflicted_files" ]]; then
  echo "No conflicted files found."
  exit 0
fi

echo "Resolving conflicts by keeping current-branch changes:"
printf '%s
' "$conflicted_files"

while IFS= read -r file; do
  [[ -z "$file" ]] && continue
  git checkout --ours -- "$file"
  git add "$file"
done <<< "$conflicted_files"

echo "All conflicted files staged with current-branch versions."
echo "Now run: git commit -m 'Resolve merge conflicts keeping feature branch content'"
