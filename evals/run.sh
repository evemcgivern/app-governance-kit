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
real_codex_home=""

cleanup() {
  # If codex rotated its token during the run, write-temp-then-rename
  # replaces the auth.json symlink inside $iso_home with a regular file
  # holding the refreshed credential. Recover it onto the real auth file
  # before $iso_home is removed, or the refreshed login is lost and the
  # real auth.json is left holding a rotated (now-invalid) token. Never
  # print, log, or cat the credential.
  if [ -n "$real_codex_home" ] && [ -f "$iso_home/.codex/auth.json" ] && [ ! -L "$iso_home/.codex/auth.json" ]; then
    chmod 600 "$iso_home/.codex/auth.json"
    mv -f "$iso_home/.codex/auth.json" "$real_codex_home/auth.json"
  fi
  rm -rf "$work" "$iso_home"
}
trap cleanup EXIT

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
  # available there via symlink (never copied, never logged). See cleanup()
  # above for recovering a token codex refreshes during the run.
  codex)
    real_codex_home="${CODEX_HOME:-$HOME/.codex}"
    [ -f "$real_codex_home/auth.json" ] || {
      echo "codex is not logged in (no auth.json in $real_codex_home)" >&2
      exit 2
    }
    mkdir -p "$iso_home/.codex"
    ln -s "$real_codex_home/auth.json" "$iso_home/.codex/auth.json"
    # Pass through locale/proxy settings a real network call may need;
    # everything else inherited from the caller's environment is dropped.
    pass_through=()
    if [ -n "${LANG:-}" ]; then pass_through+=("LANG=$LANG"); fi
    if [ -n "${LC_ALL:-}" ]; then pass_through+=("LC_ALL=$LC_ALL"); fi
    if [ -n "${HTTPS_PROXY:-}" ]; then pass_through+=("HTTPS_PROXY=$HTTPS_PROXY"); fi
    if [ -n "${HTTP_PROXY:-}" ]; then pass_through+=("HTTP_PROXY=$HTTP_PROXY"); fi
    if [ -n "${NO_PROXY:-}" ]; then pass_through+=("NO_PROXY=$NO_PROXY"); fi
    if [ -n "${SSL_CERT_FILE:-}" ]; then pass_through+=("SSL_CERT_FILE=$SSL_CERT_FILE"); fi
    if [ -n "${https_proxy:-}" ]; then pass_through+=("https_proxy=$https_proxy"); fi
    if [ -n "${http_proxy:-}" ]; then pass_through+=("http_proxy=$http_proxy"); fi
    if [ -n "${no_proxy:-}" ]; then pass_through+=("no_proxy=$no_proxy"); fi
    if [ "${#pass_through[@]}" -gt 0 ]; then
      env -i HOME="$iso_home" CODEX_HOME="$iso_home/.codex" PATH="$PATH" TERM="${TERM:-xterm}" "${pass_through[@]}" \
        codex exec --sandbox read-only --skip-git-repo-check -- "$prompt" > "$out"
    else
      env -i HOME="$iso_home" CODEX_HOME="$iso_home/.codex" PATH="$PATH" TERM="${TERM:-xterm}" \
        codex exec --sandbox read-only --skip-git-repo-check -- "$prompt" > "$out"
    fi
    ;;
  *) echo "runner must be claude or codex" >&2; exit 2 ;;
esac
cd "$root"
PYTHONPATH=build python3 -m agk.grade --tool "$tool" --output "$out"
