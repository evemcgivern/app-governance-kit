import re
from pathlib import Path

LINK_RE = re.compile(r'\[[^\]]*\]\(([^)]+)\)')


def broken_doc_links(methods_dir: Path) -> list[str]:
    """Find Markdown links in methods/*/*.md whose relative target doesn't exist.

    Skips example/ folders, http(s):/mailto: links, and bare #anchor links.
    A target's #fragment (if any) is stripped before checking existence.
    """
    out = []
    for md in sorted(methods_dir.glob("*/*.md")):
        text = md.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            if not target or (md.parent / target).exists():
                continue
            out.append(f"{md.relative_to(methods_dir)}: {target}")
    return out
