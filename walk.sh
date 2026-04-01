#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$BASE_DIR"

echo "[cakewalk] discover"
./discover.sh

echo "[cakewalk] build manifest"
python3 build_manifest.py

echo "[cakewalk] select defaults"
python3 select.py

echo "[cakewalk] render"
python3 render.py

echo "[cakewalk] schedule"
python3 schedule.py

echo "[cakewalk] publish"
python3 publish.py

echo "[cakewalk] done"
