#!/usr/bin/env bash
set -euo pipefail
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
line="0 2 * * * cd '$BASE_DIR' && ./walk.sh >> '$BASE_DIR/logs/cakewalk.log' 2>&1"
( crontab -l 2>/dev/null | grep -v 'cakewalk/walk.sh' ; echo "$line" ) | crontab -
echo "Installed cron entry: $line"
