import re
import unittest
from pathlib import Path

from agk.site import broken_links

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
PAGE = (SITE / "case-studies.html").read_text(encoding="utf-8")

CASES = ["case-audit-response", "case-ai-intake", "case-rationalization", "case-renewals",
         "case-retirement", "case-gap-plan"]
LIST_RE = re.compile(r'<ul class="case-list[^"]*">(.*?)</ul>', re.S)


def cards() -> list[str]:
    m = LIST_RE.search(PAGE)
    assert m, "case list not found"
    return re.findall(r'<li class="card case-card">(.*?)</li>', m.group(1), re.S)


class CaseStudiesPageTests(unittest.TestCase):
    def test_every_case_has_a_card_linking_to_its_section(self):
        found = [re.search(r'<h3><a href="#(case-[a-z-]+)">', c).group(1) for c in cards()]
        self.assertEqual(found, CASES)
        for case in CASES:
            self.assertIn(f'id="{case}"', PAGE)

    def test_each_card_has_title_summary_and_tool(self):
        for card in cards():
            self.assertRegex(card, r'<h3><a href="#case-[a-z-]+">[^<]{10,}</a></h3>')
            summary = re.search(r'<p class="case-card__summary">([^<]+)</p>', card)
            self.assertTrue(summary and len(summary.group(1)) > 40, card)
            tool = re.search(r'<p class="meta case-card__tool">[^<]*<a [^>]*>([^<]+)</a>', card)
            self.assertTrue(tool and tool.group(1).strip(), card)

    def test_list_comes_before_the_explanation(self):
        self.assertLess(PAGE.index('class="case-list '), PAGE.index("How to read these"))
        self.assertLess(PAGE.index("How to read these"), PAGE.index('id="case-audit-response"'))

    def test_list_is_labelled_and_explanation_is_collapsible(self):
        self.assertRegex(PAGE, r'<section aria-labelledby="cases-heading">\s*<h2 id="cases-heading">')
        self.assertRegex(PAGE, r"<details[^>]*>\s*<summary>How to read these</summary>")
        self.assertEqual(PAGE.count("<h1"), 1)

    def test_explanation_sentences_are_kept(self):
        for phrase in ["These are worked examples, not client case studies.",
                       "Every point where a person decides is marked",
                       "Nothing here is legal advice",
                       "Write Not found where the files hold no figure."]:
            self.assertIn(phrase, PAGE)

    def test_playbook_step_links_point_at_real_headings(self):
        playbook = (SITE / "docs/sam-toolkit/itam-program-playbook.html").read_text(encoding="utf-8")
        steps = re.findall(r'href="docs/sam-toolkit/itam-program-playbook\.html#([^"]+)"', PAGE)
        self.assertTrue(steps)
        for step in steps:
            self.assertIn(f'id="{step}"', playbook)

    def test_title_and_description_rules(self):
        self.assertRegex(PAGE, r"<title>Case studies \| App Governance Kit</title>")
        for pattern in (r'name="description" content="([^"]*)"', r'property="og:description" content="([^"]*)"',
                        r'name="twitter:description" content="([^"]*)"'):
            text = re.search(pattern, PAGE).group(1)
            self.assertLessEqual(len(text), 160)
            self.assertTrue(text.startswith("Six worked examples"), text)

    def test_no_broken_links_on_site(self):
        self.assertEqual([b for b in broken_links(SITE) if b.startswith("case-studies.html")], [])

    def test_no_em_dashes_added(self):
        self.assertNotIn("—", PAGE)


if __name__ == "__main__":
    unittest.main()
