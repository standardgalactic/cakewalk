#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$BASE_DIR"

mkdir -p repos state candidates configs build schedule logs

cat <<MSG
Cakewalk bootstrap complete.

Suggested next steps:
  1. Put GitHub credentials in gh if you want automatic cloning.
  2. Start the dashboard: python3 dashboard/server.py
  3. Run one cycle: ./walk.sh
MSG
