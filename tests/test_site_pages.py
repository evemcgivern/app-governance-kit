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


class BreadcrumbTests(unittest.TestCase):
    def test_top_level_pages_have_a_home_and_page_breadcrumb(self):
        for name in INNER_PAGES:
            html = read(name)
            m = re.search(r'<nav class="breadcrumb" aria-label="Breadcrumb">(.*?)</nav>', html, re.S)
            self.assertTrue(m, name)
            items = re.findall(r"<li>(.*?)</li>", m.group(1), re.S)
            self.assertEqual(len(items), 2, name)
            self.assertIn('<a href="index.html">Home</a>', items[0])
            self.assertRegex(items[1], r'^<span aria-current="page">[^<]+</span>$')

    def test_home_page_has_no_breadcrumb(self):
        self.assertNotIn("Breadcrumb", read("index.html"))

    def test_back_link_is_kept_on_docs_pages(self):
        html = (SITE / "docs" / "sam-toolkit" / "guide.html").read_text(encoding="utf-8")
        self.assertIn('class="doc-back"', html)

    def test_docs_pages_have_home_group_and_file_breadcrumb(self):
        html = (SITE / "docs" / "sam-toolkit" / "guide.html").read_text(encoding="utf-8")
        m = re.search(r'<nav class="breadcrumb" aria-label="Breadcrumb">(.*?)</nav>', html, re.S)
        items = re.findall(r"<li>(.*?)</li>", m.group(1), re.S)
        self.assertEqual(len(items), 3)
        self.assertIn('<a href="../../index.html">Home</a>', items[0])
        self.assertIn('<a href="../../sam-toolkit.html">SAM toolkit</a>', items[1])
        self.assertRegex(items[2], r'^<span aria-current="page">[^<]+</span>$')


class LlmsAndSitemapTests(unittest.TestCase):
    llms = (SITE / "llms.txt").read_text(encoding="utf-8")

    def test_crosswalk_row_count_matches_the_csv(self):
        rows = list(csv.DictReader((ROOT / "methods" / "crosswalk" / "crosswalk.csv").open(encoding="utf-8")))
        self.assertIn(f"a {len(rows)}-row crosswalk", self.llms)
        self.assertNotRegex(self.llms, r"\b(?!%d\b)\d+-row crosswalk" % len(rows))

    def test_toolkit_count_in_the_summary_is_the_repo_count(self):
        n = len([f for f in (ROOT / "sam-toolkit").iterdir() if f.suffix in (".md", ".csv")])
        self.assertEqual(n, 40)
        self.assertIn("forty-file SAM toolkit", self.llms)
        self.assertNotIn("thirteen-file", self.llms)

    def test_playbook_is_listed_first_then_the_ten_steps(self):
        md = (ROOT / "sam-toolkit" / "itam-program-playbook.md").read_text(encoding="utf-8")
        steps = re.findall(r"^### (Step (\d+): .+)$", md, re.M)
        self.assertEqual(len(steps), 10)
        section = self.llms.split("## Start here: the playbook", 1)[1].split("\n## ", 1)[0]
        self.assertIn("itam-program-playbook.html)", section.splitlines()[2])
        step_lines = [l for l in section.splitlines() if re.match(r"- \[Step \d+", l)]
        self.assertEqual(len(step_lines), 10)
        for (heading, n), line in zip(steps, step_lines):
            self.assertIn(heading, line)
            self.assertIn("itam-program-playbook.html#step-", line)
            self.assertGreater(len(line.split("): ", 1)[1]), 30, line)
        self.assertLess(self.llms.index("## Start here: the playbook"), self.llms.index("## The nine tools"))

    def test_the_two_lifecycle_checks_are_tagged(self):
        self.assertIn("software-lifecycle (software end of life)", self.llms)
        self.assertIn("hardware-lifecycle (devices, from purchase to wipe)", self.llms)

    def test_sitemap_lists_every_page(self):
        sitemap = (SITE / "sitemap.xml").read_text(encoding="utf-8")
        locs = set(re.findall(r"<loc>([^<]+)</loc>", sitemap))
        want = {BASE if p.name == "index.html" else BASE + p.name for p in SITE.glob("*.html")}
        want |= {BASE + p.relative_to(SITE).as_posix() for p in (SITE / "docs").rglob("*.html")}
        self.assertEqual(locs, want)
        self.assertEqual(len(re.findall(r"<loc>", sitemap)), len(locs))

    def test_sitemap_has_no_dates(self):
        self.assertNotIn("lastmod", (SITE / "sitemap.xml").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
