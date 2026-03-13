#!/usr/bin/env bash
set -euo pipefail

if rg -n "^(<<<<<<<|=======|>>>>>>>)" --glob '!node_modules/**' >/tmp/conflicts.txt; then
  echo "Merge conflict markers found:"
  cat /tmp/conflicts.txt
  exit 1
fi

echo "No merge conflict markers found."
