import json
import re
from pathlib import Path

LINK_RE = re.compile(r'(?:href|src)="([^"]+)"')


def inject_data(html: str, name: str, data: list) -> str:
    pattern = re.compile(rf"<!--{name}-DATA-->.*?<!--/{name}-DATA-->", re.S)
    if not pattern.search(html):
        raise ValueError(f"page has no <!--{name}-DATA--> markers")
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    block = (f'<!--{name}-DATA--><script type="application/json" id="{name.lower()}-data">'
             f'{payload}</script><!--/{name}-DATA-->')
    return pattern.sub(lambda _: block, html)


def broken_links(site_dir: Path) -> list[str]:
    """Links that point at nothing, in the top-level pages and in site/journal/. A link is resolved
    against the folder of the page that holds it. A link that leaves site/ is broken even when the file
    exists in the repo, because it will not exist on the published site."""
    out = []
    root = site_dir.resolve()
    pages = sorted(site_dir.glob("*.html")) + sorted((site_dir / "journal").glob("*.html"))
    for page in pages:
        for target in LINK_RE.findall(page.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            resolved = (page.parent / target.split("#")[0]).resolve()
            if root not in resolved.parents and resolved != root or not resolved.exists():
                out.append(f"{page.relative_to(site_dir).as_posix()}: {target}")
    return out
