import re
from collections.abc import Collection
from pathlib import Path

PARTS = ("What it means", "Key work", "Evidence it produces", "Usually owned by")
HEAD_RE = re.compile(r"^## (XW-\d{3}) .+$", re.M)


class ThemesError(Exception):
    pass


def load_themes(path: Path, known: Collection[str]) -> dict[str, dict[str, str]]:
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    heads = list(HEAD_RE.finditer(text))
    out: dict[str, dict[str, str]] = {}
    for i, m in enumerate(heads):
        rid = m.group(1)
        if rid not in known:
            raise ThemesError(f"{rid}: not in the crosswalk")
        if rid in out:
            raise ThemesError(f"{rid}: described twice")
        body = text[m.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        parts = {}
        for label in PARTS:
            pm = re.search(rf"^- \*\*{re.escape(label)}:\*\* (.+)$", body, re.M)
            if not pm or not pm.group(1).strip():
                raise ThemesError(f"{rid}: missing '{label}'")
            parts[label] = pm.group(1).strip()
        out[rid] = parts
    missing = sorted(set(known) - out.keys())
    if missing:
        raise ThemesError(f"no description for {', '.join(missing)}")
    return out
