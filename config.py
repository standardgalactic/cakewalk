from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(os.environ.get("CAKEWALK_BASE_DIR", Path(__file__).resolve().parent))
REPOS_DIR = Path(os.environ.get("CAKEWALK_REPOS_DIR", BASE_DIR / "repos"))
STATE_DIR = BASE_DIR / "state"
CANDIDATES_DIR = BASE_DIR / "candidates"
CONFIGS_DIR = BASE_DIR / "configs"
BUILD_DIR = BASE_DIR / "build"
SCHEDULE_DIR = BASE_DIR / "schedule"
LOGS_DIR = BASE_DIR / "logs"
VISUALIZER_DIR = BASE_DIR / "visualizer"
DASHBOARD_DIR = BASE_DIR / "dashboard"

LEDGER_PATH = STATE_DIR / "ledger.json"
SETTINGS_PATH = STATE_DIR / "settings.json"

ORG = os.environ.get("CAKEWALK_ORG", "standardgalactic")
RECENT_REPOS = int(os.environ.get("CAKEWALK_RECENT_REPOS", "10"))
DAILY_HOUR_UTC = int(os.environ.get("CAKEWALK_DAILY_HOUR_UTC", "15"))
DEFAULT_DESCRIPTION = os.environ.get(
    "CAKEWALK_DEFAULT_DESCRIPTION",
    "Generated with Cakewalk from archived source material.",
)
PRIVACY_STATUS = os.environ.get("CAKEWALK_PRIVACY_STATUS", "private")
YOUTUBE_SECRETS = os.environ.get("CAKEWALK_YOUTUBE_SECRETS", str(STATE_DIR / "client_secrets.json"))
YOUTUBE_TOKEN = os.environ.get("CAKEWALK_YOUTUBE_TOKEN", str(STATE_DIR / "oauth_token.json"))

for path in [REPOS_DIR, STATE_DIR, CANDIDATES_DIR, CONFIGS_DIR, BUILD_DIR, SCHEDULE_DIR, LOGS_DIR]:
    path.mkdir(parents=True, exist_ok=True)
