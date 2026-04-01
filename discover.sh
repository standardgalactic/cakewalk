#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
REPOS_DIR="${CAKEWALK_REPOS_DIR:-$BASE_DIR/repos}"
OUT_FILE="$BASE_DIR/state/discovered_paths.txt"
ORG="${CAKEWALK_ORG:-standardgalactic}"
RECENT_REPOS="${CAKEWALK_RECENT_REPOS:-10}"

mkdir -p "$REPOS_DIR" "$BASE_DIR/state"
: > "$OUT_FILE"

if command -v gh >/dev/null 2>&1; then
  mapfile -t repos < <(gh repo list "$ORG" --limit "$RECENT_REPOS" --json nameWithOwner,updatedAt --jq 'sort_by(.updatedAt) | reverse | .[].nameWithOwner')
else
  echo "[warn] gh not found; scanning existing repos directory only"
  repos=()
fi

for repo in "${repos[@]:-}"; do
  [[ -z "$repo" ]] && continue
  name="$(basename "$repo")"
  target="$REPOS_DIR/$name"
  if [[ -d "$target/.git" ]]; then
    echo "[refresh] $repo"
    git -C "$target" fetch --depth=1 origin || true
    branch="$(git -C "$target" rev-parse --abbrev-ref HEAD || echo main)"
    git -C "$target" pull --ff-only origin "$branch" || true
  else
    echo "[clone] $repo"
    git clone --depth=1 "https://github.com/$repo.git" "$target" || true
  fi
done

find "$REPOS_DIR" -type f -name '*.mp3' | sort | while read -r mp3; do
  vtt="${mp3%.mp3}.vtt"
  pdf="${mp3%.mp3}.pdf"
  if [[ -f "$vtt" ]]; then
    printf '%s|%s|%s\n' "$mp3" "$vtt" "$([[ -f "$pdf" ]] && printf '%s' "$pdf")" >> "$OUT_FILE"
  fi
done

echo "[discover] wrote $OUT_FILE"
