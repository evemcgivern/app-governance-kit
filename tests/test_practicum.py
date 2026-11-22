import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRACTICUM = ROOT / "practicum"


class PracticumTests(unittest.TestCase):
    def test_every_graded_tool_has_one_exercise(self):
        key = json.loads((ROOT / "demo-estate" / "answer-key.json").read_text())
        tools = sorted({k["tool"] for k in key} - {"cert-prep"})  # cert-prep drills reuse other exercises
        for tool in tools:
            matches = list(PRACTICUM.glob(f"[0-9][0-9]-{tool}.md"))
            self.assertEqual(len(matches), 1, f"expected one exercise for {tool}")

    def test_each_exercise_has_required_sections_and_practicum_link(self):
        for ex in sorted(PRACTICUM.glob("[0-9][0-9]-*.md")):
            tool = ex.stem.split("-", 1)[1]
            text = ex.read_text()
            for heading in ("## Scenario", "## Files", "## Work through", "## Hand in",
                            "## Check yourself", "## Reflect", "## Certification link"):
                self.assertIn(heading, text, f"{ex.name} missing {heading}")
            self.assertIn(f"practicum.html#{tool}", text, ex.name)
            self.assertNotIn("python3 -m agk.grade", text, f"{ex.name} still asks a learner to run Python")
            self.assertNotIn("```findings", text, f"{ex.name} still asks a learner to hand-write a JSON findings block")
            self.assertNotIn("answer-key.json", text.split("## Check yourself")[0],
                             f"{ex.name} points at the answer key before the self-check section")

    def test_readme_lists_exercises_in_order(self):
        readme = (PRACTICUM / "README.md").read_text()
        names = [ex.name for ex in sorted(PRACTICUM.glob("[0-9][0-9]-*.md"))]
        positions = [readme.index(n) for n in names]
        self.assertEqual(positions, sorted(positions))

    def test_there_are_nine_exercises_and_the_readme_says_so(self):
        self.assertEqual(len(list(PRACTICUM.glob("[0-9][0-9]-*.md"))), 9)
        readme = (PRACTICUM / "README.md").read_text()
        self.assertIn("Nine hands-on exercises", readme)
        self.assertIn("## The nine exercises, in order", readme)
        self.assertIn("| 2 | [02-as-is-assessment.md](02-as-is-assessment.md) | CAMP |", readme)
        self.assertNotIn("Eight", readme)

    def test_as_is_exercise_ties_the_gut_check_to_the_evidence_score(self):
        text = (PRACTICUM / "02-as-is-assessment.md").read_text()
        self.assertTrue(text.startswith("# Exercise 02: As-is assessment"))
        self.assertIn("**Level:** CAMP", text)
        for needle in ("demo-estate/as-is-evidence.csv", "application-management-self-assessment.md",
                       "itam-program-playbook.md", "five-minute gut check", "no evidence",
                       "one level lower", "playbook step 1", "playbook step 5"):
            self.assertIn(needle, text)
        self.assertNotIn("\u2014", text)

    def test_practicum_page_lists_and_builds_the_as_is_exercise(self):
        html = (ROOT / "site" / "practicum.html").read_text(encoding="utf-8")
        self.assertIn('<li><a href="#as-is-assessment">2. As-is assessment</a></li>', html)
        self.assertIn('id="as-is-assessment"', html)
        self.assertIn('BUILDERS["as-is-assessment"]', html)
        self.assertIn('COLLECTORS["as-is-assessment"]', html)
        self.assertIn("Nine exercises on Halden", html)
        self.assertNotIn("Eight hands-on", html)

    def test_exercise_files_run_in_the_expected_order(self):
        names = [ex.stem for ex in sorted(PRACTICUM.glob("[0-9][0-9]-*.md"))]
        self.assertEqual(names, ["01-program-setup", "02-as-is-assessment", "03-itam-maturity", "04-crosswalk",
                                 "05-rationalization", "06-access-review", "07-ai-intake",
                                 "08-hardware-lifecycle", "09-audit-response"])

    def test_each_title_carries_its_file_number(self):
        for ex in sorted(PRACTICUM.glob("[0-9][0-9]-*.md")):
            self.assertTrue(ex.read_text().startswith(f"# Exercise {ex.name[:2]}: "), ex.name)

    def test_practicum_page_lists_exercises_in_order_with_numbers(self):
        html = (ROOT / "site" / "practicum.html").read_text(encoding="utf-8")
        tools = ["program-setup", "as-is-assessment", "itam-maturity", "crosswalk", "rationalization",
                 "access-review", "ai-intake", "hardware-lifecycle", "audit-response"]
        pos = []
        for n, tool in enumerate(tools, start=1):
            link = html.find(f'<li><a href="#{tool}">{n}. ')
            self.assertGreater(link, -1, f"jump link {n} {tool}")
            pos.append(link)
        self.assertEqual(pos, sorted(pos))
        sections = [html.index(f'id="pr-{t}-heading">Exercise {n}: ') for n, t in enumerate(tools, start=1)]
        self.assertEqual(sections, sorted(sections))

    def test_no_place_still_says_eight_exercises(self):
        for place in ("README.md", "AGENTS.md", "site/field-guide.html", "site/llms.txt"):
            text = (ROOT / place).read_text(encoding="utf-8")
            self.assertNotRegex(text, r"(?i)\beight (hands-on )?exercises", place)

