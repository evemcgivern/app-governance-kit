import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = (ROOT / "site" / "tools.html").read_text(encoding="utf-8")
METHODS = ROOT / "methods"
FIELDS = ["What it does", "You give it", "You get", "Use it when", "Decision stays with"]


def method_keys() -> list[str]:
    return sorted(p.name for p in METHODS.iterdir() if (p / "method.md").exists())


def method_title(key: str) -> str:
    text = (METHODS / key / "method.md").read_text(encoding="utf-8")
    return re.search(r"(?m)^title: (.+)$", text).group(1).strip()


def overview() -> str:
    m = re.search(r'<section[^>]*id="overview"[^>]*>(.*?)</section>', PAGE, re.S)
    assert m, "overview section not found"
    return m.group(1)


def entries() -> list[str]:
    return re.findall(r'<li class="card tool-card">(.*?)</li>', overview(), re.S)


def text_of(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).strip()


class ToolsOverviewTests(unittest.TestCase):
    def test_one_entry_per_method(self):
        keys = [re.search(r'<h3><a href="#([a-z-]+)">', e).group(1) for e in entries()]
        self.assertEqual(sorted(keys), method_keys())
        self.assertEqual(len(keys), len(set(keys)))

    def test_each_entry_links_to_an_existing_card(self):
        for e in entries():
            key = re.search(r'<h3><a href="#([a-z-]+)">', e).group(1)
            self.assertRegex(PAGE, rf'<article class="card" id="{key}">')

    def test_entry_name_matches_the_method_title(self):
        for e in entries():
            m = re.search(r'<h3><a href="#([a-z-]+)">([^<]+)</a></h3>', e)
            self.assertEqual(m.group(2), method_title(m.group(1)))

    def test_five_fields_in_order_and_not_empty(self):
        for e in entries():
            labels = re.findall(r"<dt>([^<]+)</dt>", e)
            self.assertEqual(labels, FIELDS, e[:80])
            for dd in re.findall(r"<dd>(.*?)</dd>", e, re.S):
                self.assertGreaterEqual(len(text_of(dd)), 8, e[:80])

    def test_overview_comes_before_install(self):
        self.assertLess(PAGE.index('id="overview"'), PAGE.index('id="install"'))
        self.assertLess(PAGE.index('id="overview"'), PAGE.index('<article class="card"'))

    def test_list_is_labelled_and_headings_nest(self):
        self.assertRegex(PAGE, r'<section aria-labelledby="overview-heading" id="overview">\s*<h2 id="overview-heading">What each tool does</h2>')
        self.assertEqual(PAGE.count("<h1"), 1)
        body = PAGE[PAGE.index('id="overview"'):PAGE.index('id="install"')]
        self.assertNotIn("<h4", body)
        self.assertEqual(len(re.findall(r"<h3>", body)), len(method_keys()))

    def test_no_em_dashes_in_overview(self):
        self.assertNotIn("—", overview())

    def test_title_and_description_rules_still_hold(self):
        title = re.search(r"<title>(.*?)</title>", PAGE).group(1)
        self.assertTrue(title.endswith(" | App Governance Kit"))
        desc = re.search(r'<meta name="description" content="([^"]+)"', PAGE).group(1)
        self.assertGreater(len(desc), 60)
        self.assertIn("nine governance tools, plus a router and a study coach", PAGE)

    def test_decision_cells_name_a_role_or_say_not_found(self):
        for e in entries():
            dd = re.findall(r"<dd>(.*?)</dd>", e, re.S)[4]
            self.assertTrue(re.search(r"owner|counsel|sponsor|approver|learner|Legal|you|lead|Not found", text_of(dd), re.I), text_of(dd))


if __name__ == "__main__":
    unittest.main()
