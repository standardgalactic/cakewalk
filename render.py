#!/usr/bin/env python3
from __future__ import annotations

import shlex
import subprocess
from pathlib import Path

from common_io import load_json, save_json
from config import BUILD_DIR, CONFIGS_DIR, LEDGER_PATH


def ffmpeg_quote(path: str) -> str:
    return path.replace('\\', '\\\\').replace(':', '\\:').replace("'", "\\'")


ledger = load_json(LEDGER_PATH, default={"items": {}, "events": []})
items = ledger.setdefault("items", {})
rendered = 0

for config_path in sorted(Path(CONFIGS_DIR).glob("*.json")):
    config = load_json(config_path)
    item_id = config["id"]
    output_path = BUILD_DIR / f"{item_id}.mp4"

    if output_path.exists():
        items[item_id]["rendered_video"] = str(output_path)
        items[item_id]["status"] = "rendered"
        continue

    mp3 = config["mp3"]
    vtt = config["vtt"]
    visualizer = config.get("visualizer", "static")
    speed = float(config.get("speed", 1.0))

    subtitle_filter = f"subtitles='{ffmpeg_quote(vtt)}'"

    if visualizer == "waveform":
        video_input = [
            "-f", "lavfi",
            "-i", f"showwaves=s=1280x720:mode=line:rate=30:colors=white",
        ]
        video_map = ["-map", "0:v:0", "-map", "1:a:0"]
        inputs = video_input + ["-i", mp3]
    else:
        inputs = [
            "-f", "lavfi",
            "-i", "color=c=black:s=1280x720:r=30",
            "-i", mp3,
        ]
        video_map = ["-map", "0:v:0", "-map", "1:a:0"]

    audio_filters = []
    if abs(speed - 1.0) > 1e-6:
        audio_filters.append(f"atempo={speed}")

    cmd = ["ffmpeg", "-y", *inputs, *video_map, "-vf", subtitle_filter]
    if audio_filters:
        cmd += ["-af", ",".join(audio_filters)]
    cmd += [
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-shortest",
        str(output_path),
    ]

    print("[render]", " ".join(shlex.quote(part) for part in cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr)
        items[item_id]["status"] = "render_error"
        items[item_id]["render_error"] = result.stderr[-4000:]
        continue

    items[item_id]["rendered_video"] = str(output_path)
    items[item_id]["status"] = "rendered"
    rendered += 1

ledger["events"].append({"event": "render", "count": rendered})
save_json(LEDGER_PATH, ledger)
print(f"[render] completed {rendered} renders")
