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
iso_home="$(mktemp -d)"
trap "rm -rf '$work' '$iso_home'" EXIT
find "$root/demo-estate" -maxdepth 1 -type f ! -name answer-key.json ! -name generate.py -exec cp {} "$work" \;
find "$(dirname "$skill")" -maxdepth 1 -type f ! -name SKILL.md -exec cp {} "$work" \;
cd "$work"
case "$runner" in
  # --safe-mode disables CLAUDE.md, personal skills, installed plugins, hooks,
  # MCP servers, custom commands/agents (auth still works normally).
  claude) claude -p --safe-mode --allowedTools Read -- "$prompt" > "$out" ;;
  # Codex has no equivalent single flag: --ignore-user-config only skips
  # $CODEX_HOME/config.toml, not the personal skill directories under $HOME.
  # Isolate with a throwaway HOME, and make ONLY the login credential
  # available there via symlink (never copied, never logged).
  codex)
    mkdir -p "$iso_home/.codex"
    ln -s "$HOME/.codex/auth.json" "$iso_home/.codex/auth.json"
    env -i HOME="$iso_home" CODEX_HOME="$iso_home/.codex" PATH="$PATH" TERM="${TERM:-xterm}" \
      codex exec --sandbox read-only --skip-git-repo-check -- "$prompt" > "$out"
    ;;
  *) echo "runner must be claude or codex" >&2; exit 2 ;;
esac
cd "$root"
PYTHONPATH=build python3 -m agk.grade --tool "$tool" --output "$out"
