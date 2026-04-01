#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from common_io import load_json, save_json
from config import LEDGER_PATH, PRIVACY_STATUS, SCHEDULE_DIR, YOUTUBE_SECRETS, YOUTUBE_TOKEN


def upload_to_youtube(video_path: str, title: str, description: str, publish_at: str, privacy_status: str) -> dict:
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except Exception as exc:
        raise RuntimeError(f"YouTube dependencies unavailable: {exc}") from exc

    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    creds = None
    token_path = Path(YOUTUBE_TOKEN)
    secrets_path = Path(YOUTUBE_SECRETS)

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(secrets_path), scopes)
            creds = flow.run_local_server(port=0)
        token_path.write_text(creds.to_json(), encoding="utf-8")

    youtube = build("youtube", "v3", credentials=creds)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {"title": title, "description": description},
            "status": {
                "privacyStatus": privacy_status,
                "publishAt": publish_at,
                "selfDeclaredMadeForKids": False,
            },
        },
        media_body=MediaFileUpload(video_path),
    )
    return request.execute()


ledger = load_json(LEDGER_PATH, default={"items": {}, "events": []})
items = ledger.setdefault("items", {})
now = datetime.now(timezone.utc)
published = 0

for path in sorted(Path(SCHEDULE_DIR).glob("*.json")):
    entry = load_json(path)
    publish_at = datetime.fromisoformat(entry["publish_at"]) if entry.get("publish_at") else None
    if entry.get("published"):
        continue
    if publish_at and publish_at > now:
        continue

    item_id = entry["id"]
    video_path = entry.get("video_path")
    if not video_path or not Path(video_path).exists():
        items[item_id]["status"] = "publish_error"
        items[item_id]["publish_error"] = "Missing rendered video"
        continue

    if Path(YOUTUBE_SECRETS).exists():
        try:
            response = upload_to_youtube(
                video_path=video_path,
                title=entry["title"],
                description=entry["description"],
                publish_at=entry["publish_at"],
                privacy_status=entry.get("privacy_status", PRIVACY_STATUS),
            )
            entry["youtube_response"] = response
            entry["published"] = True
            entry["published_at_runtime"] = now.isoformat()
            items[item_id]["status"] = "published"
            items[item_id]["published_at"] = now.isoformat()
            published += 1
        except Exception as exc:
            items[item_id]["status"] = "publish_error"
            items[item_id]["publish_error"] = str(exc)
    else:
        entry["published"] = True
        entry["published_at_runtime"] = now.isoformat()
        entry["mock"] = True
        items[item_id]["status"] = "published_mock"
        items[item_id]["published_at"] = now.isoformat()
        published += 1

    save_json(path, entry)

ledger["events"].append({"event": "publish", "count": published})
save_json(LEDGER_PATH, ledger)
print(f"[publish] processed {published} entries")
