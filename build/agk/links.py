import csv
from pathlib import Path

from agk.lifecycle import STAGES

TYPES = {
    "refers_to": ("Refers to", "Referenced by"),
    "may_impact": ("May impact", "May be impacted by"),
    "blocks": ("Blocks", "Blocked by"),
    "leads_to": ("Leads to", "Led from"),
}
COLUMNS = ("from_id", "type", "to_id", "note")


class LinkError(Exception):
    pass


def link_items(questions: list[dict], stages: dict) -> dict[str, dict]:
    items: dict[str, dict] = {slug: {"stage": slug, "kind": "stage", "text": label} for slug, label in STAGES}

    def add(item_id: str, entry: dict) -> None:
        if item_id in items:
            raise LinkError(f"id {item_id} used twice")
        items[item_id] = entry

    for q in questions:
        add(q["id"], {"stage": q["stage"], "kind": "question", "text": q["question"]})
    for slug, info in stages.items():
        for r in info["rules"]:
            add(r["id"], {"stage": slug, "kind": "rule", "text": r["text"]})
    return items


def load_links(path: Path, items: dict[str, dict]) -> dict[str, list[dict]]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != COLUMNS:
            raise LinkError(f"columns must be {','.join(COLUMNS)}; got {reader.fieldnames}")
        out: dict[str, list[dict]] = {}
        seen = set()
        for n, row in enumerate(reader, start=2):
            a, kind, b, note = ((row.get(c) or "").strip() for c in COLUMNS)
            if kind not in TYPES:
                raise LinkError(f"line {n}: unknown link type {kind!r}")
            for step in (a, b):
                if step not in items:
                    raise LinkError(f"line {n}: unknown step {step!r}")
            if a == b:
                raise LinkError(f"line {n}: {a} links to itself")
            if kind == "leads_to" and not (items[a]["kind"] == items[b]["kind"] == "stage"):
                raise LinkError(f"line {n}: leads_to links stages only")
            if (a, kind, b) in seen:
                raise LinkError(f"line {n}: duplicate link")
            seen.add((a, kind, b))
            forward, reverse = TYPES[kind]
            out.setdefault(a, []).append({"label": forward, "type": kind, "target": b, "note": note, "inverse": False})
            out.setdefault(b, []).append({"label": reverse, "type": kind, "target": a, "note": note, "inverse": True})
    return out
