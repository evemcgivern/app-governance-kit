"""The Journal: Markdown posts built into pages with a generated index.

Posts live in posts/YYYY-MM-DD-slug.md. Drafts live in docs/journal-drafts/ (ignored by git) and
are only built by the preview command. Standard library only; output is deterministic.
"""
from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path

STATUS_LABELS = {"field-note": "Field note", "essay": "Essay", "study-path": "Study path"}
REQUIRED_KEYS = ("title", "date", "status", "summary")
MAX_SUMMARY = 200
FILE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-([a-z0-9-]+)\.md$")


class JournalError(Exception):
    """A post or the journal as a whole is not valid; the message says which file and why."""


@dataclass(frozen=True)
class Post:
    slug: str
    title: str
    date: str
    updated: str | None
    status: str
    summary: str
    spine: bool
    body: str
    path: Path


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    """Return the key: value pairs between the first two --- lines, and the Markdown after them."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise JournalError("no front matter: the file must start with a --- line")
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        raise JournalError("front matter is not closed with a --- line")
    keys: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        if ":" not in line:
            raise JournalError(f"front matter line has no colon: {line!r}")
        key, value = line.split(":", 1)
        keys[key.strip()] = value.strip()
    return keys, "\n".join(lines[end + 1:]).lstrip("\n")


def _check_date(name: str, key: str, value: str) -> None:
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        raise JournalError(f"{name}: {key} must be a real date written YYYY-MM-DD, not {value!r}") from None


def parse_post(path: Path) -> Post:
    name = path.name
    match = FILE_RE.match(name)
    if not match:
        raise JournalError(f"{name}: the file name must be YYYY-MM-DD-slug.md, with a slug of a-z, 0-9 and hyphens")
    try:
        keys, body = parse_front_matter(path.read_text(encoding="utf-8"))
    except JournalError as e:
        raise JournalError(f"{name}: {e}") from None
    for key in REQUIRED_KEYS:
        if not keys.get(key):
            raise JournalError(f"{name}: missing {key}")
    _check_date(name, "date", keys["date"])
    updated = keys.get("updated") or None
    if updated:
        _check_date(name, "updated", updated)
    if keys["status"] not in STATUS_LABELS:
        raise JournalError(f"{name}: status must be one of {', '.join(STATUS_LABELS)}, not {keys['status']!r}")
    if len(keys["summary"]) > MAX_SUMMARY:
        raise JournalError(f"{name}: summary is {len(keys['summary'])} characters; the limit is {MAX_SUMMARY}")
    spine = keys.get("spine", "false")
    if spine not in ("true", "false"):
        raise JournalError(f"{name}: spine must be true or false, not {spine!r}")
    return Post(slug=match.group(2), title=keys["title"], date=keys["date"], updated=updated,
                status=keys["status"], summary=keys["summary"], spine=spine == "true", body=body, path=path)


def load_posts(directory: Path) -> list[Post]:
    """All posts in a folder, newest date first and then by slug. A missing folder holds no posts."""
    if not directory.is_dir():
        return []
    posts = [parse_post(p) for p in sorted(directory.glob("*.md"))]
    seen: dict[str, Path] = {}
    for post in posts:
        if post.slug in seen:
            raise JournalError(f"{post.path.name}: the slug {post.slug!r} is already used by {seen[post.slug].name}")
        seen[post.slug] = post.path
    if sum(1 for p in posts if p.spine) > 1:
        names = ", ".join(p.path.name for p in posts if p.spine)
        raise JournalError(f"only one post may have spine: true, found {names}")
    posts.sort(key=lambda p: p.slug)
    posts.sort(key=lambda p: p.date, reverse=True)
    return posts
