#!/usr/bin/env bash
set -euo pipefail

base_directory="${PWD}"

directories=(
  "abraxas" "agora" "arcanum" "alphabet" "antivenom" "backward-compatibility"
  "brain" "bubble-city" "capstone" "Centerfuge" "circle-of-fifths" "cogniscium"
  "eclectric-oil" "example" "experiments" "ensign" "Haplopraxis/IFM" "hepastitium"
  "human" "hyperspace" "keen-unicoder" "keyboard" "library" "logical-connectives"
  "lorax" "mindgame" "mirror" "negentropy" "phonograph" "pacer" "prototypes"
  "psychohistory" "quadrivium" "quantum-soup" "umbilicus" "secret-message"
  "sitemap" "spherepop" "standardgalactic.github.io" "substrate" "supercube"
  "systada" "technobabble" "teleosemantics" "terminal-simulator" "theory"
  "transcript" "unscannable-interfaces" "vectorspace" "xanadu" "zetetics"
  "zygomindfulness" "xylomancy"
)

for dir in "${directories[@]}"; do
  target="$base_directory/$dir"
  if [[ -d "$target/.git" ]]; then
    echo "[push] $dir"
    git -C "$target" push
  else
    echo "[skip] missing git repo: $target"
  fi
done
