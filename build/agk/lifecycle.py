import csv
import re
from collections.abc import Collection
from pathlib import Path

STAGES = (("plan", "Plan and request"), ("acquire", "Acquire"), ("deploy", "Deploy"),
          ("operate", "Operate"), ("optimize", "Review and optimize"), ("retire", "Retire"))
COLUMNS = ("stage", "question", "tool", "xw")
STAGE_PARTS = ("What happens", "Gate to move on", "Hands off to", "Who decides")
_TAG_RE = re.compile(r"\[\[(XW-\d{3})\]\]")


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


def load_stages(path: Path, known_xw: Collection[str]) -> dict:
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    together = re.search(r"^## How it works together\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not together or not together.group(1).strip():
        raise LifecycleError("stages.md: missing 'How it works together' text")
    slugs = [s for s, _ in STAGES]
    heads = {m.group(1): m for m in re.finditer(rf"^## ({'|'.join(slugs)})\b.*$", text, re.M)}
    missing = [s for s in slugs if s not in heads]
    if missing:
        raise LifecycleError(f"no section for stage: {', '.join(missing)}")
    order = sorted(heads.values(), key=lambda m: m.start())
    stages = {}
    for i, m in enumerate(order):
        slug = m.group(1)
        body = text[m.end(): order[i + 1].start() if i + 1 < len(order) else len(text)]
        info: dict = {}
        for label in STAGE_PARTS:
            pm = re.search(rf"^- \*\*{re.escape(label)}:\*\* (.+)$", body, re.M)
            if not pm or not pm.group(1).strip():
                raise LifecycleError(f"{slug}: missing '{label}'")
            info[label] = pm.group(1).strip()
        targets, _, note = info["Hands off to"].partition(" — ")
        info["Hands off to"] = [t.strip() for t in targets.split(",") if t.strip()]
        info["Hand-off note"] = note.strip()
        for t in info["Hands off to"]:
            if t not in slugs:
                raise LifecycleError(f"{slug}: hands off to unknown stage {t!r}")
        rules_part = body.split("### Rules that apply", 1)
        rules = []
        for line in (rules_part[1] if len(rules_part) > 1 else "").splitlines():
            if not line.startswith("- "):
                continue
            tags = _TAG_RE.findall(line)
            if not tags:
                raise LifecycleError(f"{slug}: rule has no clause tag: {line[2:60]}")
            for t in tags:
                if t not in known_xw:
                    raise LifecycleError(f"{slug}: unknown crosswalk row {t}")
            rules.append({"text": _TAG_RE.sub("", line[2:]).strip(), "xw": tags})
        if not rules:
            raise LifecycleError(f"{slug}: no rules")
        info["rules"] = rules
        stages[slug] = info
    return {"together": together.group(1).strip(), "stages": stages}


def render_checklist(rows: list[dict[str, str]], stages: dict | None = None) -> str:
    out = ["# Application lifecycle questions", "",
           "Questions to ask at each stage. Each names the crosswalk row it satisfies and the kit tool that handles it.", ""]
    for slug, label in STAGES:
        out += [f"## {label}", ""]
        if stages:
            s = stages[slug]
            out += [f"{s['What happens']}", "", "Rules that apply:", ""]
            out += [f"- {r['text']} " + " ".join(f"[[{x}]]" for x in r["xw"]) for r in s["rules"]]
            out += ["", f"Gate to move on: {s['Gate to move on']}",
                    f"Hands off to: {', '.join(s['Hands off to'])}. {s['Hand-off note']}".rstrip(),
                    f"Who decides: {s['Who decides']}", "", "Questions to ask:", ""]
        out += [f"- [ ] {r['question']} [[{r['xw']}]] (tool: `{r['tool']}`)" for r in rows if r["stage"] == slug]
        out.append("")
    return "\n".join(out)
