#!/usr/bin/env bash
set -euo pipefail

progress_file="progress.log"
summary_file="source-control.txt"
main_dir="$(pwd)"
chunk_lines="${CAKEWALK_SUMMARY_CHUNK_LINES:-282}"
model="${CAKEWALK_OLLAMA_MODEL:-granite3.2:8b}"

is_processed() {
  grep -Fxq "$1" "$main_dir/$progress_file" 2>/dev/null
}

touch "$main_dir/$progress_file" "$main_dir/$summary_file"

echo "Script started at $(date)" >> "$main_dir/$progress_file"

auto_summarize() {
  local file="$1"
  if command -v ollama >/dev/null 2>&1; then
    ollama run "$model" "Summarize in detail and explain:" < "$file"
  else
    head -n 40 "$file"
  fi
}

process_files() {
  local dir="$1"
  for file in "$dir"/*.txt; do
    [[ -e "$file" ]] || continue
    [[ "$(basename "$file")" == "$summary_file" ]] && continue
    [[ -f "$file" ]] || continue

    local file_name
    file_name="$(basename "$file")"
    if is_processed "$file_name"; then
      continue
    fi

    sanitized_name="$(basename "$file" | tr -d '[:space:]')"
    temp_dir="$(mktemp -d "$dir/tmp_${sanitized_name}_XXXXXX")"
    split -l "$chunk_lines" "$file" "$temp_dir/chunk_"

    {
      echo "### $(basename "$file" .txt)"
      echo
      for chunk_file in "$temp_dir"/chunk_*; do
        [[ -f "$chunk_file" ]] || continue
        auto_summarize "$chunk_file"
        echo
      done
    } >> "$main_dir/$summary_file"

    rm -rf "$temp_dir"
    echo "$file_name" >> "$main_dir/$progress_file"
  done
}

process_subdirectories() {
  local parent_dir="$1"
  for dir in "$parent_dir"/*/; do
    [[ -d "$dir" ]] || continue
    process_files "$dir"
    process_subdirectories "$dir"
  done
}

process_files "$main_dir"
process_subdirectories "$main_dir"

echo "Script completed at $(date)" >> "$main_dir/$progress_file"
