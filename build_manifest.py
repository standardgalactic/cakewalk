#!/usr/bin/env python3
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Dict, List

from common_io import load_json, save_json
from config import CANDIDATES_DIR, LEDGER_PATH, REPOS_DIR


def stable_id(mp3: str, vtt: str) -> str:
    digest = hashlib.sha256(f"{mp3}|{vtt}".encode("utf-8")).hexdigest()
    return digest[:12]


def infer_repo_name(path: Path) -> str:
    try:
        rel = path.relative_to(REPOS_DIR)
        return rel.parts[0]
    except Exception:
        return path.parent.name


def infer_title(path: Path) -> str:
    return path.stem.replace("_", " ").replace("-", " ").strip() or path.stem


ledger = load_json(LEDGER_PATH, default={"items": {}, "events": []})
items: Dict[str, dict] = ledger.setdefault("items", {})
manifest: List[dict] = []

source_file = Path("state/discovered_paths.txt")
if source_file.exists():
    for raw in source_file.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        mp3, vtt, pdf = (raw.split("|", 2) + [""])[:3]
        mp3_path = Path(mp3)
        vtt_path = Path(vtt)
        pdf_path = Path(pdf) if pdf else None
        item_id = stable_id(mp3, vtt)
        repo_name = infer_repo_name(mp3_path)
        title = infer_title(mp3_path)
        candidate = {
            "id": item_id,
            "repo": repo_name,
            "title": title,
            "mp3": str(mp3_path),
            "vtt": str(vtt_path),
            "pdf": str(pdf_path) if pdf_path and pdf_path.exists() else None,
            "status": items.get(item_id, {}).get("status", "discovered"),
            "selected": items.get(item_id, {}).get("selected", False),
            "rendered_video": items.get(item_id, {}).get("rendered_video"),
            "scheduled_for": items.get(item_id, {}).get("scheduled_for"),
            "published_at": items.get(item_id, {}).get("published_at"),
        }
        items[item_id] = {**items.get(item_id, {}), **candidate}
        manifest.append(candidate)
        save_json(CANDIDATES_DIR / f"{item_id}.json", candidate)

ledger["events"].append({"event": "build_manifest", "count": len(manifest)})
save_json(LEDGER_PATH, ledger)
print(f"[manifest] wrote {len(manifest)} candidates")
