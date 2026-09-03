#!/bin/bash
# Server-local scheduled updater. Never merges to main.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

git switch main
git pull --ff-only origin main

if [ "${PUSH_UPDATES:-0}" = "1" ]; then
  python3 scripts/prepare_updates.py --apply --push
else
  python3 scripts/prepare_updates.py --apply
fi
