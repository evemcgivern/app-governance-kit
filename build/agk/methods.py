from dataclasses import dataclass
from pathlib import Path

REQUIRED_FILES = ("method.md", "checklist.md", "sop.md", "platform-guide.md", "copilot-test.md")
REQUIRED_META = ("name", "title", "description")


class MethodError(Exception):
    pass


@dataclass(frozen=True)
class Method:
    name: str
    title: str
    description: str
    dir: Path
    body: str
    template: Path


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    text = text.lstrip("﻿").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        raise MethodError("missing frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise MethodError("unterminated frontmatter")
    meta = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        if not sep:
            raise MethodError(f"bad frontmatter line: {line!r}")
        meta[key.strip()] = value.strip()
    return meta, text[end + 5:]


def load_method(d: Path) -> Method:
    missing = [f for f in REQUIRED_FILES if not (d / f).is_file()]
    templates = sorted(p for p in d.glob("template.*") if p.suffix in (".md", ".csv"))
    if not templates:
        missing.append("template.md or template.csv")
    example = d / "example"
    if not example.is_dir() or not any(example.iterdir()):
        missing.append("example/ (with at least one file)")
    if missing:
        raise MethodError(f"{d.name}: missing {', '.join(missing)}")
    if len(templates) > 1:
        raise MethodError(f"{d.name}: expected one template, found {[p.name for p in templates]}")
    meta, body = parse_frontmatter((d / "method.md").read_text(encoding="utf-8"))
    absent = [k for k in REQUIRED_META if not meta.get(k)]
    if absent:
        raise MethodError(f"{d.name}: method.md frontmatter missing {', '.join(absent)}")
    if meta["name"] != d.name:
        raise MethodError(f"{d.name}: frontmatter name {meta['name']!r} must match folder name")
    return Method(meta["name"], meta["title"], meta["description"], d, body, templates[0])


def method_dirs(methods_dir: Path) -> list[Path]:
    return sorted(p for p in methods_dir.iterdir()
                  if p.is_dir() and not p.name.startswith(("_", ".")))
