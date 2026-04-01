#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from common_io import load_json, save_json
from config import CANDIDATES_DIR, CONFIGS_DIR, LEDGER_PATH, SETTINGS_PATH

ledger = load_json(LEDGER_PATH, default={"items": {}, "events": []})
settings = load_json(SETTINGS_PATH, default={})
items = ledger.setdefault("items", {})

created = 0
for path in sorted(Path(CANDIDATES_DIR).glob("*.json")):
    candidate = load_json(path)
    item_id = candidate["id"]
    if (CONFIGS_DIR / f"{item_id}.json").exists():
        continue

    title = f"{settings.get('title_prefix', '')}{candidate['title']}{settings.get('title_suffix', '')}".strip()
    description = (
        f"Source repository: {candidate['repo']}\n\n"
        f"This video pairs archived audio with aligned captions.\n\n"
        f"{settings.get('default_description_footer', 'Generated with Cakewalk.')}"
    )
    config = {
        "id": item_id,
        "repo": candidate["repo"],
        "title": title,
        "description": description,
        "mp3": candidate["mp3"],
        "vtt": candidate["vtt"],
        "pdf": candidate.get("pdf"),
        "visualizer": settings.get("default_visualizer", "static"),
        "speed": float(settings.get("default_speed", 1.0)),
        "tone": float(settings.get("default_tone", 1.0)),
        "ready": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    save_json(CONFIGS_DIR / f"{item_id}.json", config)
    items[item_id]["selected"] = True
    items[item_id]["status"] = "configured"
    created += 1

ledger["events"].append({"event": "select_defaults", "count": created})
save_json(LEDGER_PATH, ledger)
print(f"[select] created {created} config files")
