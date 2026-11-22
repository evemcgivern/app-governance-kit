import re
import unittest
from pathlib import Path

from agk.stepmap import load_map

ROOT = Path(__file__).resolve().parent.parent
PAGE = (ROOT / "site" / "sam-toolkit.html").read_text(encoding="utf-8")
PLAYBOOK = (ROOT / "sam-toolkit" / "itam-program-playbook.md").read_text(encoding="utf-8")
ROWS = [r for r in load_map(ROOT) if r["kind"] == "file"]
TYPES = {"Template", "Checklist", "Guide", "Prompts", "Worksheet", "SOP", "Procedure", "Playbook",
         "Self-assessment", "Plan", "Report", "Schedule", "Decision tree", "Spreadsheet", "Document"}


def steps_block() -> str:
    return PAGE.split("<!--STEPS-->", 1)[1].split("<!--/STEPS-->", 1)[0]


def sections() -> dict[str, str]:
    """Each step card keyed by its id suffix ("1" to "10", "beyond"), in page order."""
    found = re.findall(r'<section class="card step-card[^"]*" id="by-step-([\w]+)"[^>]*>(.*?)</section>',
                       steps_block(), re.S)
    return dict(found)


class StepSectionTests(unittest.TestCase):
    def test_ten_step_sections_in_order_then_the_loose_group(self):
        self.assertEqual(list(sections()), [str(n) for n in range(1, 11)] + ["beyond"])

    def test_each_step_heading_is_text_not_a_link(self):
        for n, sec in sections().items():
            h = re.search(r"<h3[^>]*>(.*?)</h3>", sec, re.S)
            self.assertIsNotNone(h, n)
            self.assertNotIn("<a ", h.group(1), n)

    def test_heading_ids_name_each_section(self):
        for n, sec in sections().items():
            self.assertRegex(sec, rf'<h3 id="by-step-{n}-heading"')
            self.assertRegex(steps_block(), rf'id="by-step-{n}"[^>]*aria-labelledby="by-step-{n}-heading"')

    def test_headings_stay_in_order(self):
        levels = [int(x) for x in re.findall(r"<h([1-6])", PAGE)]
        for a, b in zip(levels, levels[1:]):
            self.assertLessEqual(b, a + 1)

    def test_each_numbered_step_has_a_goal_from_the_playbook(self):
        for n, sec in sections().items():
            if n == "beyond":
                continue
            goal = re.search(r'<p class="step-card__goal">(.*?)</p>', sec, re.S)
            self.assertIsNotNone(goal, n)
            plain = re.sub(r"<[^>]+>", "", goal.group(1)).replace("&#x27;", "'").replace("&amp;", "&")
            self.assertIn(plain, re.sub(r" ?\[\[XW-\d+\]\]", "", PLAYBOOK), n)

    def test_each_numbered_step_links_to_its_playbook_section(self):
        for n, sec in sections().items():
            if n != "beyond":
                self.assertRegex(sec, rf'href="docs/sam-toolkit/itam-program-playbook\.html#step-{n}-[\w-]+"')


class StepperTests(unittest.TestCase):
    def stepper(self) -> str:
        m = re.search(r'<ol class="stepper">(.*?)</ol>', steps_block(), re.S)
        self.assertIsNotNone(m)
        return m.group(1)

    def test_ten_links_that_resolve_to_the_step_sections(self):
        hrefs = re.findall(r'<a href="#(by-step-[\w]+)"', self.stepper())
        self.assertEqual(hrefs, [f"by-step-{n}" for n in range(1, 11)])
        for h in hrefs:
            self.assertIn(f'id="{h}"', PAGE)

    def test_the_stepper_is_a_labelled_nav(self):
        self.assertRegex(steps_block(), r'<nav class="stepper-nav" aria-label="[^"]+">\s*<ol class="stepper">')


class FileEntryTests(unittest.TestCase):
    def entries(self) -> dict[str, list[str]]:
        out: dict[str, list[str]] = {}
        for n, sec in sections().items():
            out[n] = re.findall(r'<li data-stem="([^"]+)"', sec)
        return out

    def test_every_toolkit_file_appears_once_as_a_main_entry_under_its_step(self):
        have = self.entries()
        every = [s for files in have.values() for s in files]
        self.assertEqual(len(every), len(set(every)))
        self.assertEqual(len(every), 41)
        for r in ROWS:
            stem = r["key"].rsplit(".", 1)[0]
            self.assertEqual(have[r["main_step"]].count(stem), 1, r["key"])

    def test_the_loose_group_keeps_the_savings_report(self):
        self.assertEqual(self.entries()["beyond"], ["savings-report"])
        self.assertIn("Not part of a step", sections()["beyond"])

    def test_each_file_name_is_a_link_and_has_a_type_label(self):
        for n, sec in sections().items():
            for li in re.findall(r"<li data-stem=.*?</li>", sec, re.S):
                self.assertRegex(li, r'^<li data-stem="[^"]+">\s*<a href="docs/sam-toolkit/[\w-]+\.html">[^<]+</a>')
                label = re.search(r'<span class="file-type">([^<]+)</span>', li)
                self.assertIsNotNone(label, li[:60])
                self.assertIn(label.group(1), TYPES)

    def test_also_notes_match_the_map_and_link_to_other_step_sections(self):
        for r in ROWS:
            stem = r["key"].rsplit(".", 1)[0]
            li = re.search(rf'<li data-stem="{re.escape(stem)}">.*?</li>', steps_block(), re.S).group(0)
            also = re.search(r'<span class="file-also">(.*)</span>\s*</li>', li, re.S)
            if not r["also_steps"]:
                self.assertIsNone(also, stem)
                continue
            self.assertIsNotNone(also, stem)
            targets = re.findall(r'<a href="#by-step-(\d+)"', also.group(1))
            self.assertEqual(targets, r["also_steps"], stem)
            self.assertNotIn(r["main_step"], targets, stem)
            for t in targets:
                self.assertIn(f'id="by-step-{t}"', PAGE)

    def test_the_old_step_tag_is_gone(self):
        self.assertNotIn("step-tag", PAGE)


class WhereToStartTests(unittest.TestCase):
    def card(self) -> str:
        m = re.search(r'<section class="card start-card[^"]*" id="start"[^>]*>(.*?)</section>', PAGE, re.S)
        self.assertIsNotNone(m)
        return m.group(1)

    def test_the_playbook_is_the_primary_action_and_the_rest_are_still_there(self):
        card = self.card()
        self.assertRegex(card, r'<a class="button" href="docs/sam-toolkit/itam-program-playbook\.html">Read the playbook first</a>')
        for href in ("downloads/sam-toolkit/application-management-workbook.xlsx", "field-guide.html#glossary-heading",
                     "docs/sam-toolkit/guide.html", "practicum.html#about-the-demo-company"):
            self.assertIn(f'href="{href}"', card)
        for phrase in ("one order to follow", "They don't find installs", "Halden Logistics"):
            self.assertIn(phrase, card)


if __name__ == "__main__":
    unittest.main()
