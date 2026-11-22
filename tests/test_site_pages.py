import csv
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
BASE = "https://evemcgivern.github.io/app-governance-kit/"
SUFFIX = " | App Governance Kit"

TOP_PAGES = sorted(p.name for p in SITE.glob("*.html"))
INNER_PAGES = [n for n in TOP_PAGES if n != "index.html"]
NAV_RE = re.compile(r'<nav class="site-nav".*?</nav>', re.S)
CURRENT_RE = re.compile(r' aria-current="page"')

# Group label, then (link text, target page) in the order the nav shows them.
GROUPS = [
    ("Start", [("SAM toolkit", "sam-toolkit.html")]),
    ("Do", [("AI skills", "tools.html")]),
    ("Learn", [("Practicum", "practicum.html"), ("Case studies", "case-studies.html"),
               ("Field guide", "field-guide.html")]),
    ("Explore", [("Application lifecycle", "lifecycle.html"), ("Crosswalk explorer", "crosswalk.html"),
                 ("Themes by stage", "impact-map.html")]),
]


def read(name: str) -> str:
    return (SITE / name).read_text(encoding="utf-8")


def nav_of(html: str) -> str:
    return NAV_RE.search(html).group(0)


def footer_of(html: str) -> str:
    return re.search(r'<footer class="site-footer">.*?</footer>', html, re.S).group(0)


def meta(html: str, attr: str, key: str) -> str:
    m = re.search(rf'<meta {attr}="{re.escape(key)}" content="([^"]*)"', html)
    return m.group(1) if m else ""


def title_of(html: str) -> str:
    return re.search(r"<title>(.*?)</title>", html, re.S).group(1)


def jsonld_of(html: str) -> dict:
    return json.loads(re.search(r'<script type="application/ld\+json">\s*(.*?)</script>', html, re.S).group(1))


class TitleTests(unittest.TestCase):
    def test_titles_end_with_the_site_name_everywhere(self):
        pages = [SITE / n for n in TOP_PAGES] + sorted((SITE / "docs").rglob("*.html"))
        for p in pages:
            html = p.read_text(encoding="utf-8")
            t = title_of(html)
            self.assertTrue(t.endswith(SUFFIX), f"{p}: {t}")
            self.assertNotIn("Eve McGivern", t, p)
            self.assertEqual(meta(html, "property", "og:title"), t, p)
            self.assertEqual(meta(html, "name", "twitter:title"), t, p)
            self.assertEqual(meta(html, "property", "og:site_name"), "App Governance Kit", p)

    def test_json_ld_names_use_the_site_name_not_the_person(self):
        for n in TOP_PAGES:
            graph = jsonld_of(read(n))["@graph"]
            for node in graph:
                if node["@type"] in ("WebSite", "ProfilePage"):
                    self.assertTrue(node["name"].endswith("App Governance Kit"), (n, node["name"]))
                    self.assertNotIn("Eve McGivern |", node["name"])

    def test_descriptions_say_more_than_a_fragment(self):
        for n in TOP_PAGES:
            html = read(n)
            d = meta(html, "name", "description")
            self.assertTrue(110 <= len(d) <= 200, f"{n}: {len(d)} characters: {d}")
            self.assertEqual(meta(html, "property", "og:description"), d, n)
            self.assertEqual(meta(html, "name", "twitter:description"), d, n)
            self.assertNotIn("—", d)


if __name__ == "__main__":
    unittest.main()
