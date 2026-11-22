"""The step map: which playbook step each toolkit file, practicum exercise, case study and glossary term serves.
`steps/step-map.csv` is the one source; pages and tests read it here."""
import csv
from pathlib import Path

KINDS = ("file", "practicum", "case", "term")
COLUMNS = ["kind", "key", "main_step", "also_steps", "frequency", "note"]
VALID_STEPS = {str(n) for n in range(1, 11)} | {"beyond"}

CSV_NOTE = "Not found means no source record was located; never put an estimate there."
# Required columns come only from the playbook's "Done when" lists. Only the renewal calendar names columns.
REQUIRED_COLUMNS = {"renewal-calendar": ("contract_end", "notice_days", "notice_deadline", "decision_owner",
                                         "decided_on")}
WORDS_PER_MINUTE = 200
READING_MIN_WORDS = 1000


class StepMapError(Exception):
    pass


def load_map(root: Path) -> list[dict]:
    path = root / "steps" / "step-map.csv"
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != COLUMNS:
            raise StepMapError(f"{path.name}: columns must be {', '.join(COLUMNS)}")
        rows = []
        for r in reader:
            r = dict(r)
            r["also_steps"] = [s for s in r["also_steps"].split(";") if s]
            if r["kind"] not in KINDS:
                raise StepMapError(f"{r['key']}: unknown kind {r['kind']!r}")
            for s in [r["main_step"]] + r["also_steps"]:
                if s not in VALID_STEPS:
                    raise StepMapError(f"{r['key']}: step {s!r} is not 1 to 10 or beyond")
            rows.append(r)
    return rows


def find(rows: list[dict], kind: str, key: str) -> dict | None:
    return next((r for r in rows if r["kind"] == kind and r["key"] == key), None)


def _join(items: list[str]) -> str:
    if len(items) <= 2:
        return " and ".join(items)
    return ", ".join(items[:-1]) + ", and " + items[-1]


def step_words(steps: list[str]) -> str:
    return ("step " if len(steps) == 1 else "steps ") + _join(steps)


def feeds_line(row: dict) -> str:
    if row["main_step"] == "beyond":
        lead = "Not part of a step."
    else:
        lead = f"Feeds step {row['main_step']}."
        if row["also_steps"]:
            lead += f" Also {step_words(row['also_steps'])}."
    return (f"{lead} Review: {row['frequency']}. Keep it in the versioned place your records policy names, "
            "with access limited.")


def required_line(stem: str) -> str:
    cols = REQUIRED_COLUMNS.get(stem)
    if not cols:
        return ""
    return f"Required columns, from the playbook's checklist for this step: {_join(list(cols))}."


def practice_line(row: dict) -> str:
    if row["main_step"] == "beyond":
        return "Practice for work beyond the ten steps."
    return f"Practice for playbook {step_words([row['main_step']] + row['also_steps'])}."


def case_line(row: dict) -> str:
    if row["main_step"] == "beyond":
        return "This case is beyond the ten steps."
    steps = " and ".join(f"step {s}" for s in [row["main_step"]] + row["also_steps"])
    return f"This is what {steps} output looks like."


def related_line(rows: list[dict], n: int) -> str:
    """The playbook's Related row for step n: its exercises, cases and glossary terms, from the map."""
    def hits(kind):
        return [r for r in rows if r["kind"] == kind and str(n) in [r["main_step"]] + r["also_steps"]]
    parts = []
    ex = [f"[exercise {r['key'][:2]}: {r['note']}](../practicum/{r['key']}.md)" for r in hits("practicum")]
    if ex:
        parts.append(", ".join(ex))
    cases = [f"[{r['note']}](../site/case-studies.html#case-{r['key']})" for r in hits("case")]
    if cases:
        parts.append("case study " + ", ".join(cases))
    terms = [r["key"] for r in hits("term")]
    if terms:
        parts.append("[glossary](../field-guide/glossary.md): " + ", ".join(terms))
    return f"- Related: {'; '.join(parts)}." if parts else ""


def text_words(blocks: list[dict]) -> int:
    def items(its):
        return sum(len(i["text"].split()) + items(i.get("children", [])) for i in its)
    total = 0
    for b in blocks:
        if b["type"] in ("heading", "p"):
            total += len(b["text"].split())
        elif b["type"] == "list":
            total += items(b["items"])
        elif b["type"] == "table":
            total += sum(len(c.split()) for r in b["rows"] for c in r)
    return total


def reading_minutes(words: int) -> int:
    return max(1, int(words / WORDS_PER_MINUTE + 0.5))


def reading_line(words: int) -> str:
    if words < READING_MIN_WORDS:
        return ""
    return f"About {reading_minutes(words)} minutes to read (an estimate at {WORDS_PER_MINUTE} words per minute)."
