import csv
import json
from pathlib import Path

from agk.grade import MAX_EXTRA

ORDER = ("program-setup", "itam-maturity", "crosswalk", "rationalization", "access-review",
         "ai-intake", "hardware-lifecycle")
TABLES = ("apps", "licenses", "employees", "accounts", "ai-systems", "maturity-answers", "devices")
TEXTS = ("controls", "council-draft")


class PracticumError(Exception):
    pass


def _section(text: str, heading: str) -> str:
    parts = text.split(f"## {heading}\n", 1)
    if len(parts) < 2:
        return ""
    return parts[1].split("\n## ", 1)[0].strip()


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
        exercises.append({"tool": tool, "title": title, "scenario": scenario, "file": matches[0].name})
    return {"exercises": exercises, "tables": tables, "texts": texts, "key": key,
            "crosswalk": [{"id": r["id"], "theme": r["theme"]} for r in crosswalk.values()],
            "max_extra": MAX_EXTRA}
