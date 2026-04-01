#!/usr/bin/env bash
set -euo pipefail
trap 'echo "Script interrupted"; exit 130' INT

current_directory="$(basename "$PWD")"
if [[ "$current_directory" != "GitHub" ]]; then
  echo "This script must be run from the 'GitHub' directory. Aborting."
  exit 1
fi

base_directory="$PWD"

directories=(
  "abraxas" "agora" "arcanum" "alphabet" "antivenom" "backward-compatibility"
  "brain" "bubble-city" "capstone" "Centerfuge" "circle-of-fifths" "codex"
  "cogniscium" "eclectric-oil" "example" "experiments" "ensign" "Haplopraxis/IFM"
  "hepastitium" "human" "hyperspace" "keen-unicoder" "keyboard" "kitbash"
  "library" "logical-connectives" "lorax" "mindgame" "mirror" "negentropy"
  "phonograph" "pacer" "prototypes" "psychohistory" "quadrivium" "quantum-soup"
  "umbilicus" "secret-message" "sitemap" "spherepop" "standardgalactic.github.io"
  "substrate" "supercube" "systada" "technobabble" "teleosemantics"
  "terminal-simulator" "theory" "transcript" "unscannable-interfaces" "vectorspace"
  "xanadu" "zetetics" "zygomindfulness" "xylomancy"
)

for dir in "${directories[@]}"; do
  echo "-----------------------------------------"
  echo "Starting processing for directory: $dir"
  full_path="$base_directory/$dir"

  if [[ ! -d "$full_path/.git" ]]; then
    echo "Directory $full_path does not exist or is not a Git repository"
    continue
  fi

  primary_branch="$(git -C "$full_path" symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || true)"
  if [[ -z "$primary_branch" ]]; then
    primary_branch="$(git -C "$full_path" rev-parse --abbrev-ref HEAD)"
  fi

  echo "Primary branch for $dir is $primary_branch"
  git -C "$full_path" pull origin "$primary_branch"
  echo "Git pull completed on $primary_branch"
  echo "Finished processing for directory: $dir"
done

echo "Script completed."
