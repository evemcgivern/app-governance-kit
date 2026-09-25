import csv
import json
import re
from pathlib import Path

from agk.grade import MAX_EXTRA

ORDER = ("program-setup", "itam-maturity", "crosswalk", "rationalization", "access-review",
         "ai-intake", "hardware-lifecycle")
TABLES = ("apps", "licenses", "employees", "accounts", "ai-systems", "maturity-answers", "devices")
TEXTS = ("controls", "council-draft")
GITHUB_BLOB_BASE = "https://github.com/evemcgivern/app-governance-kit/blob/main/"

_FILE_LINE_RE = re.compile(r"^-\s*\[`([^`]+)`\]\(([^)]+)\)\s*—\s*(.+)$")
_NUMBERED_RE = re.compile(r"^\d+\.\s*(.+)$")


class PracticumError(Exception):
    pass


def _section(text: str, heading: str) -> str:
    parts = text.split(f"## {heading}\n", 1)
    if len(parts) < 2:
        return ""
    return parts[1].split("\n## ", 1)[0].strip()


def _parse_files(section_text: str) -> list[dict]:
    files = []
    for line in section_text.splitlines():
        m = _FILE_LINE_RE.match(line.strip())
        if not m:
            continue
        label, href, description = m.groups()
        if href.startswith("../"):
            href = GITHUB_BLOB_BASE + href[3:]
        files.append({"label": label, "href": href, "description": description})
    return files


def _parse_work_through(section_text: str) -> tuple[str, list[str]]:
    lines = section_text.splitlines()
    intro_lines, hints = [], []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- "):
            hints.append(stripped[2:].strip())
        elif stripped and not hints:
            intro_lines.append(stripped)
    return " ".join(intro_lines).strip(), hints


def _parse_reflect(section_text: str) -> list[str]:
    questions = []
    for line in section_text.splitlines():
        m = _NUMBERED_RE.match(line.strip())
        if m:
            questions.append(m.group(1).strip())
    return questions


def practicum_payload(demo_dir: Path, exercises_dir: Path, crosswalk: dict) -> dict:
    tables = {}
    for name in TABLES:
        with open(demo_dir / f"{name}.csv", newline="", encoding="utf-8") as f:
            tables[name] = list(csv.DictReader(f))
    texts = {name: (demo_dir / f"{name}.md").read_text(encoding="utf-8") for name in TEXTS}
    key = json.loads((demo_dir / "answer-key.json").read_text(encoding="utf-8"))
    exercises = []
    for tool in ORDER:
        matches = sorted(exercises_dir.glob(f"[0-9][0-9]-{tool}.md"))
        if len(matches) != 1:
            raise PracticumError(f"expected one exercise for {tool}, found {len(matches)}")
        text = matches[0].read_text(encoding="utf-8")
        scenario = _section(text, "Scenario")
        if not scenario:
            raise PracticumError(f"{matches[0].name}: missing ## Scenario")
        title = text.splitlines()[0].lstrip("#").strip()
        work_through_intro, work_through_hints = _parse_work_through(_section(text, "Work through"))
        exercises.append({
            "tool": tool, "title": title, "scenario": scenario, "file": matches[0].name,
            "files": _parse_files(_section(text, "Files")),
            "work_through_intro": work_through_intro,
            "work_through_hints": work_through_hints,
            "reflect": _parse_reflect(_section(text, "Reflect")),
            "cert_link": _section(text, "Certification link"),
        })
    return {"exercises": exercises, "tables": tables, "texts": texts, "key": key,
            "crosswalk": [{"id": r["id"], "theme": r["theme"]} for r in crosswalk.values()],
            "max_extra": MAX_EXTRA}
