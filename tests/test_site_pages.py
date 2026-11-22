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


class NavTests(unittest.TestCase):
    def test_every_top_level_page_has_the_same_nav(self):
        navs = {n: CURRENT_RE.sub("", nav_of(read(n))) for n in TOP_PAGES}
        first = navs["index.html"]
        for name, nav in navs.items():
            self.assertEqual(nav, first, f"{name} has a different nav from index.html")

    def test_every_top_level_page_has_the_same_footer_apart_from_current_page(self):
        first = CURRENT_RE.sub("", footer_of(read("index.html")))
        for name in TOP_PAGES:
            self.assertEqual(CURRENT_RE.sub("", footer_of(read(name))), first, name)

    def test_nav_is_grouped_start_do_learn_explore(self):
        nav = nav_of(read("index.html"))
        labels = re.findall(r'<p class="nav-group__label"[^>]*>([^<]+)</p>', nav)
        self.assertEqual(labels, [g for g, _ in GROUPS])
        groups = re.findall(r'<div class="nav-group".*?</ul>\s*</div>', nav, re.S)
        self.assertEqual(len(groups), 4)
        for (label, links), html in zip(GROUPS, groups):
            found = re.findall(r'<li><a href="([^"#]+)(?:#[^"]*)?"[^>]*>([^<]+?)(?:\s*<span class="nav-badge">[^<]*</span>)?</a>', html)
            self.assertEqual([(t, h) for h, t in found], links, label)

    def test_sam_toolkit_is_first_and_opens_the_playbook_path(self):
        nav = nav_of(read("index.html"))
        first = re.search(r'<li><a href="([^"]+)"[^>]*>(.*?)</a>', nav, re.S)
        self.assertEqual(first.group(1), "sam-toolkit.html#start")
        self.assertIn('<span class="nav-badge">Start here</span>', first.group(2))
        self.assertIn('id="start"', read("sam-toolkit.html"))

    def test_about_is_in_the_footer_not_the_nav(self):
        self.assertNotIn("about.html", nav_of(read("index.html")))
        for name in TOP_PAGES:
            self.assertIn('href="about.html"', footer_of(read(name)), name)

    def test_renamed_labels_and_practicum_caption(self):
        nav = nav_of(read("index.html"))
        self.assertNotIn(">Lifecycle<", nav)
        self.assertNotIn(">Impact map<", nav)
        tip = re.search(r'id="tip-practicum">([^<]*)<', nav).group(1)
        self.assertTrue(tip.startswith("Exercises"), tip)

    def test_nav_collapses_behind_a_menu_disclosure(self):
        nav = nav_of(read("index.html"))
        self.assertRegex(nav, r'<details class="nav-menu">\s*<summary[^>]*>Menu</summary>')
        self.assertEqual(nav.count("<details"), 1)

    def test_aria_current_marks_the_page_you_are_on(self):
        for name in INNER_PAGES:
            nav, foot = nav_of(read(name)), footer_of(read(name))
            marked = re.findall(r'<a href="([^"#]+)[^>]*aria-current="page"', nav + foot)
            self.assertEqual(marked, [name], name)
        self.assertEqual(len(CURRENT_RE.findall(nav_of(read("index.html")))), 0)

    def test_every_nav_link_has_a_tip(self):
        nav = nav_of(read("index.html"))
        ids = re.findall(r'aria-describedby="([^"]+)"', nav)
        self.assertEqual(len(ids), 8)
        for i in ids:
            self.assertIn(f'id="{i}"', nav)


if __name__ == "__main__":
    unittest.main()
