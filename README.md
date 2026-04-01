# Cakewalk

UNTESTED

**Protocol Suite**

[Agent Skill Pipeline](https://github.com/standardgalactic/cakewalk/tree/main/protocol/README.md)

[Essay](https://standardgalactic.github.io/cakewalk/Protocol%20Suite.pdf)

**Content engine**

Cakewalk is an autonomous system that discovers source material, transforms it into video, and schedules it for publication over time.

It is designed to run continuously, converting a living corpus into a stream of videos with minimal intervention.

---

## What it does

Cakewalk operates as a pipeline:

* Scans repositories for audio files with matching subtitles
* Builds a candidate set of publishable media
* Generates video outputs using ffmpeg and visualizers
* Attaches metadata and descriptions
* Schedules videos across future timestamps
* Publishes automatically (or simulates publishing)

It can run once, or indefinitely via cron.

---

## Core idea

Cakewalk treats content as a continuous process rather than a one-time task.

Each run advances the system forward:

source material → candidates → rendered videos → scheduled outputs

Over time, this produces a structured, time-ordered channel from an evolving corpus.

---

## Project structure

```
cakewalk/
  walk.sh              # main pipeline entrypoint
  discover.sh          # finds MP3 + VTT pairs
  build_manifest.py    # creates candidate objects
  select.py            # chooses items to process
  render.py            # builds videos with ffmpeg
  schedule.py          # assigns publish times
  publish.py           # uploads or simulates upload

  candidates/          # discovered media
  configs/             # per-video configuration
  build/               # rendered videos
  schedule/            # scheduled publish entries
  state/               # persistent system state

  dashboard/           # browser-based control surface
  visualizer/          # rendering components
```

---

## Quick start

```
chmod +x walk.sh discover.sh
./walk.sh
```

This will:

* discover content
* generate configs
* render videos
* schedule them
* simulate publishing

---

## Running continuously

Set up a cron job:

```
crontab -e
```

```
0 2 * * * /path/to/cakewalk/walk.sh >> log.txt 2>&1
```

Cakewalk will now run daily and extend the schedule over time.

---

## Dashboard

Start the local dashboard:

```
python3 dashboard/server.py
```

Open:

```
http://localhost:8000
```

The dashboard allows:

* previewing candidate videos
* editing titles, descriptions, and parameters
* selecting visualizers
* preparing items before scheduling

---

## Rendering

Videos are generated using ffmpeg.

Current features include:

* subtitle burn-in
* audio playback control (speed, tone-ready)
* pluggable visualizers (Lissajous, waveform, etc.)

The visualizer system can be extended independently.

---

## Publishing

`publish.py` currently simulates uploads.

To enable real uploads:

* configure YouTube Data API credentials
* replace the mock uploader with API calls

---

## Description generation

Cakewalk can attach structured descriptions using:

* extracted text (PDF / EPUB / MHTML)
* chunked summaries
* repository metadata

This allows descriptions to be generated automatically from source material.

---

## Philosophy

Cakewalk is not just an uploader.

It is a system that:

* treats content as a continuous process
* separates discovery, transformation, and publication
* allows both autonomous operation and manual intervention

Over time, it becomes a persistent engine that converts structure into media.
