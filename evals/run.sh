#!/usr/bin/env bash
# Usage: evals/run.sh <tool> <claude|codex>
# Feeds the built SKILL.md plus the demo data to the CLI; grades the answer.
set -euo pipefail
tool="$1"; runner="$2"
root="$(cd "$(dirname "$0")/.." && pwd)"
skill="$root/dist/$runner/skills/$tool/SKILL.md"
[ -f "$skill" ] || { echo "missing $skill — run make build" >&2; exit 2; }
out="$root/evals/results/$tool-$runner-$(date +%Y%m%d-%H%M%S).md"
prompt="$(cat "$skill")

$(cat "$root/evals/prompts/$tool.txt")"
work="$(mktemp -d)"
trap "rm -rf '$work'" EXIT
find "$root/demo-estate" -maxdepth 1 -type f ! -name answer-key.json ! -name generate.py -exec cp {} "$work" \;
cd "$work"
case "$runner" in
  claude) claude -p "$prompt" --allowedTools Read > "$out" ;;
  codex)  codex exec --sandbox read-only "$prompt" > "$out" ;;
  *) echo "runner must be claude or codex" >&2; exit 2 ;;
esac
cd "$root"
PYTHONPATH=build python3 -m agk.grade --tool "$tool" --output "$out"
