#!/usr/bin/env python3
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import sys
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from common_io import load_json, save_json
from config import BUILD_DIR, CANDIDATES_DIR, CONFIGS_DIR, LEDGER_PATH, SETTINGS_PATH


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, content_type: str, payload: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def _json(self, status: int, data) -> None:
        self._send(status, "application/json; charset=utf-8", json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/candidates":
            candidates = [load_json(path) for path in sorted(CANDIDATES_DIR.glob("*.json"))]
            configs = {path.stem: load_json(path) for path in sorted(CONFIGS_DIR.glob("*.json"))}
            for entry in candidates:
                entry["config"] = configs.get(entry["id"])
            self._json(200, candidates)
            return
        if parsed.path == "/api/config":
            params = parse_qs(parsed.query)
            item_id = params.get("id", [""])[0]
            path = CONFIGS_DIR / f"{item_id}.json"
            if not path.exists():
                self._json(404, {"error": "not found"})
                return
            self._json(200, load_json(path))
            return
        if parsed.path == "/api/settings":
            self._json(200, load_json(SETTINGS_PATH, default={}))
            return
        if parsed.path == "/api/ledger":
            self._json(200, load_json(LEDGER_PATH, default={}))
            return
        if parsed.path.startswith("/media/"):
            rel = parsed.path.removeprefix("/media/")
            target = BASE_DIR / rel
            if target.exists() and target.is_file():
                data = target.read_bytes()
                ctype = "application/octet-stream"
                if target.suffix.lower() == ".mp3":
                    ctype = "audio/mpeg"
                elif target.suffix.lower() == ".mp4":
                    ctype = "video/mp4"
                elif target.suffix.lower() == ".vtt":
                    ctype = "text/vtt; charset=utf-8"
                elif target.suffix.lower() == ".json":
                    ctype = "application/json; charset=utf-8"
                self._send(200, ctype, data)
                return
            self._json(404, {"error": "missing media"})
            return
        if parsed.path in ["/", "/index.html"]:
            data = (BASE_DIR / "dashboard/index.html").read_bytes()
            self._send(200, "text/html; charset=utf-8", data)
            return
        static_path = BASE_DIR / "dashboard" / parsed.path.lstrip("/")
        if static_path.exists() and static_path.is_file():
            content_type = "text/plain; charset=utf-8"
            if static_path.suffix == ".css":
                content_type = "text/css; charset=utf-8"
            elif static_path.suffix == ".js":
                content_type = "application/javascript; charset=utf-8"
            self._send(200, content_type, static_path.read_bytes())
            return
        self._json(404, {"error": "not found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        payload = self.rfile.read(length) if length else b"{}"
        data = json.loads(payload.decode("utf-8"))

        if parsed.path == "/api/config":
            item_id = data["id"]
            save_json(CONFIGS_DIR / f"{item_id}.json", data)
            self._json(200, {"ok": True})
            return
        if parsed.path == "/api/settings":
            save_json(SETTINGS_PATH, data)
            self._json(200, {"ok": True})
            return
        self._json(404, {"error": "not found"})


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8787), Handler)
    print("Cakewalk dashboard at http://127.0.0.1:8787")
    server.serve_forever()


if __name__ == "__main__":
    main()
