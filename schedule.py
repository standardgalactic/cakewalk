#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

from common_io import load_json, save_json
from config import CONFIGS_DIR, LEDGER_PATH, SCHEDULE_DIR, SETTINGS_PATH

ledger = load_json(LEDGER_PATH, default={"items": {}, "events": []})
settings = load_json(SETTINGS_PATH, default={})
items = ledger.setdefault("items", {})

existing = []
for path in Path(SCHEDULE_DIR).glob("*.json"):
    payload = load_json(path)
    if payload.get("publish_at"):
        existing.append(payload["publish_at"])

slot_hour = int(settings.get("default_publish_hour_utc", 15))
step_days = int(settings.get("default_publish_days_apart", 1))
base = datetime.now(timezone.utc).replace(hour=slot_hour, minute=0, second=0, microsecond=0)
if base <= datetime.now(timezone.utc):
    base += timedelta(days=1)
base += timedelta(days=len(existing) * step_days)

scheduled = 0
for config_path in sorted(Path(CONFIGS_DIR).glob("*.json")):
    config = load_json(config_path)
    item_id = config["id"]
    item = items.get(item_id, {})
    if item.get("status") != "rendered":
        continue
    schedule_path = SCHEDULE_DIR / f"{item_id}.json"
    if schedule_path.exists():
        continue

    entry = {
        "id": item_id,
        "title": config["title"],
        "description": config["description"],
        "video_path": item.get("rendered_video"),
        "privacy_status": settings.get("default_privacy_status", "private"),
        "publish_at": base.isoformat(),
        "published": False,
    }
    save_json(schedule_path, entry)
    items[item_id]["scheduled_for"] = entry["publish_at"]
    items[item_id]["status"] = "scheduled"
    base += timedelta(days=step_days)
    scheduled += 1

ledger["events"].append({"event": "schedule", "count": scheduled})
save_json(LEDGER_PATH, ledger)
print(f"[schedule] created {scheduled} schedule entries")
