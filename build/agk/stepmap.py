"""The step map: which playbook step each toolkit file, practicum exercise, case study and glossary term serves.
`steps/step-map.csv` is the one source; pages and tests read it here."""
import csv
from pathlib import Path

KINDS = ("file", "practicum", "case", "term")
COLUMNS = ["kind", "key", "main_step", "also_steps", "frequency", "note"]
VALID_STEPS = {str(n) for n in range(1, 11)} | {"beyond"}


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
