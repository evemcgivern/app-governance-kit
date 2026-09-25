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
    out = []
    for page in sorted(site_dir.glob("*.html")):
        for target in LINK_RE.findall(page.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if not (site_dir / target.split("#")[0]).exists():
                out.append(f"{page.name}: {target}")
    return out
