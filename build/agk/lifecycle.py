import csv
from collections.abc import Collection
from pathlib import Path

STAGES = (("plan", "Plan and request"), ("acquire", "Acquire"), ("deploy", "Deploy"),
          ("operate", "Operate"), ("optimize", "Review and optimize"), ("retire", "Retire"))
COLUMNS = ("stage", "question", "tool", "xw")


class LifecycleError(Exception):
    pass


def load_questions(path: Path, tools: Collection[str], known_xw: Collection[str]) -> list[dict[str, str]]:
    stage_ids = {s for s, _ in STAGES}
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != COLUMNS:
            raise LifecycleError(f"columns must be {','.join(COLUMNS)}; got {reader.fieldnames}")
        rows = []
        for n, row in enumerate(reader, start=2):
            row = {k: (v or "").strip() for k, v in row.items()}
            if row["stage"] not in stage_ids:
                raise LifecycleError(f"line {n}: unknown stage {row['stage']!r}")
            if not row["question"]:
                raise LifecycleError(f"line {n}: empty question")
            if row["tool"] not in tools:
                raise LifecycleError(f"line {n}: unknown tool {row['tool']!r}")
            if row["xw"] not in known_xw:
                raise LifecycleError(f"line {n}: unknown crosswalk row {row['xw']}")
            rows.append(row)
    empty = [s for s, _ in STAGES if not any(r["stage"] == s for r in rows)]
    if empty:
        raise LifecycleError(f"no questions for stage(s): {', '.join(empty)}")
    return rows


def render_checklist(rows: list[dict[str, str]]) -> str:
    out = ["# Application lifecycle questions", "",
           "Questions to ask at each stage. Each names the crosswalk row it satisfies and the kit tool that handles it.", ""]
    for slug, label in STAGES:
        out += [f"## {label}", ""]
        out += [f"- [ ] {r['question']} [[{r['xw']}]] (tool: `{r['tool']}`)" for r in rows if r["stage"] == slug]
        out.append("")
    return "\n".join(out)
