import re
from collections.abc import Collection

STEP_RE = re.compile(r"^\s*(?:\d+\.|- \[[ xX]\])\s+\S")
TAG_RE = re.compile(r"\[\[(XW-\d{3})\]\]")


def check_tags(text: str, known: Collection[str], label: str) -> list[str]:
    errors: list[str] = []
    in_fence = False
    for n, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not STEP_RE.match(line):
            continue
        tags = TAG_RE.findall(line)
        if not tags:
            errors.append(f"{label}:{n}: step has no clause tag")
        errors.extend(f"{label}:{n}: unknown clause tag {t}" for t in tags if t not in known)
    return errors
