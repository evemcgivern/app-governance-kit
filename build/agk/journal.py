"""The Journal: Markdown posts built into pages with a generated index.

Posts live in posts/YYYY-MM-DD-slug.md. Drafts live in docs/journal-drafts/ (ignored by git) and
are only built by the preview command. Standard library only; output is deterministic.
"""
from __future__ import annotations

import datetime as dt
import json
import re
from dataclasses import dataclass
from html import escape
from pathlib import Path

from agk.docs import BASE, PAGE, PRINT_BUTTON, body_html, chrome, parse_markdown

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


# ---------- pages ----------

INTRO = "Field notes on setting up asset management, as I learn it."
LICENSE_URL = "https://opensource.org/licenses/MIT"
LICENSE_LINE = "MIT licensed, like the kit."
AUTHOR = {"@type": "Person", "name": "Eve McGivern", "url": "https://evemcgivern.github.io/"}
DRAFT_BANNER = '<p class="meta journal-draft"><strong>Draft, not published.</strong> Only you can see this preview.</p>'
NOINDEX = '<meta name="robots" content="noindex">'


def _json_ld(graph: list[dict]) -> str:
    text = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=1)
    return text.replace("</", "<\\/")


def _crumbs(*items: tuple[str, str]) -> dict:
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": name, "item": url} for i, (name, url) in enumerate(items, 1)]}


def _page(*, title: str, description: str, up: str, canonical: str, jsonld: str, index_html: str, back_href: str,
          back_label: str, extra: str, body: str, print_button: str, preview: bool) -> str:
    header, footer = chrome(index_html, up)
    html = PAGE.format(title=escape(title), description=escape(description, quote=True), up=up, canonical=canonical,
                       base=BASE, jsonld=jsonld, header=header, footer=footer, back_href=back_href,
                       back_label=escape(back_label), actions="", extra=extra, body=body, print_button=print_button)
    if preview:
        html = html.replace("<head>", "<head>\n" + NOINDEX, 1)
    return html


def render_post(post: Post, index_html: str, *, preview: bool = False) -> str:
    """The full page for one post, as it is written to site/journal/<slug>.html."""
    canonical = f"{BASE}journal/{post.slug}.html"
    graph = [
        _crumbs(("Home", BASE), ("Journal", f"{BASE}journal.html"), (post.title, canonical)),
        {"@type": "BlogPosting", "headline": post.title, "description": post.summary, "url": canonical,
         "datePublished": post.date, "dateModified": post.updated or post.date, "author": AUTHOR,
         "license": LICENSE_URL, "isAccessibleForFree": True, "isPartOf": {"@type": "WebSite", "url": BASE}}]
    label = STATUS_LABELS[post.status]
    meta = f"{escape(label)} \u00b7 {escape(post.date)}"
    if post.updated:
        meta += f" \u00b7 Updated {escape(post.updated)}"
    extra = f'  <p class="meta journal-meta">{meta}</p>\n'
    if preview:
        extra = f"  {DRAFT_BANNER}\n" + extra
    body = body_html(parse_markdown(post.body), lambda href: href)
    body += f'\n<p class="meta journal-license">{LICENSE_LINE}</p>'
    return _page(title=post.title, description=post.summary, up="../", canonical=canonical, jsonld=_json_ld(graph),
                 index_html=index_html, back_href="../journal.html", back_label="Journal", extra=extra, body=body,
                 print_button=PRINT_BUTTON, preview=preview)


def _entry(post: Post) -> str:
    return (f'<li><a href="journal/{post.slug}.html">{escape(post.title)}</a> '
            f'<span class="meta">{escape(post.date)} \u00b7 {escape(STATUS_LABELS[post.status])}</span><br>'
            f'{escape(post.summary)}</li>')


def render_index(posts: list[Post], index_html: str, *, preview: bool = False) -> str:
    """The full page for site/journal.html: the spine post first, then the rest newest first."""
    canonical = f"{BASE}journal.html"
    graph = [_crumbs(("Home", BASE), ("Journal", canonical)),
             {"@type": "CollectionPage", "name": "Journal", "description": INTRO, "url": canonical,
              "author": AUTHOR, "license": LICENSE_URL, "isPartOf": {"@type": "WebSite", "url": BASE}}]
    spine = [p for p in posts if p.spine]
    rest = [p for p in posts if not p.spine]
    parts = [f"<p>{escape(INTRO)}</p>"]
    if spine:
        parts.append('<h2 id="start-here">Start here</h2>\n<ul class="link-list">' + "".join(_entry(p) for p in spine)
                     + "</ul>")
    parts.append('<h2 id="newest-first">Newest first</h2>\n<ul class="link-list">' + "".join(_entry(p) for p in rest)
                 + "</ul>")
    extra = f"  {DRAFT_BANNER}\n" if preview else ""
    return _page(title="Journal", description=INTRO, up="", canonical=canonical, jsonld=_json_ld(graph),
                 index_html=index_html, back_href="index.html", back_label="Home", extra=extra,
                 body="\n".join(parts), print_button="", preview=preview)
