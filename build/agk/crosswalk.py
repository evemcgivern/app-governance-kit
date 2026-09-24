import csv
import re
from pathlib import Path

COLUMNS = ("id", "theme", "iso19770_1", "cobit2019", "iso27001", "iso42001", "summary", "verified")
FRAMEWORK_COLUMNS = COLUMNS[2:6]
ID_RE = re.compile(r"^XW-\d{3}$")


class CrosswalkError(Exception):
    pass


def load_crosswalk(path: Path) -> dict[str, dict[str, str]]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != COLUMNS:
            raise CrosswalkError(f"columns must be {','.join(COLUMNS)}; got {reader.fieldnames}")
        rows: dict[str, dict[str, str]] = {}
        for n, row in enumerate(reader, start=2):
            rid = row["id"].strip()
            if not ID_RE.match(rid):
                raise CrosswalkError(f"line {n}: bad id {rid!r}")
            if rid in rows:
                raise CrosswalkError(f"line {n}: duplicate id {rid}")
            if not any(row[c].strip() for c in FRAMEWORK_COLUMNS):
                raise CrosswalkError(f"line {n}: {rid} maps to no framework")
            if not row["verified"].strip():
                raise CrosswalkError(f"line {n}: {rid} not verified against the standards")
            rows[rid] = row
    return rows
