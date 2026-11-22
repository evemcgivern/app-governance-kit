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
        self.assertIn("| 9 | [09-as-is-assessment.md](09-as-is-assessment.md) | CAMP |", readme)
        self.assertNotIn("Eight", readme)

    def test_as_is_exercise_ties_the_gut_check_to_the_evidence_score(self):
        text = (PRACTICUM / "09-as-is-assessment.md").read_text()
        self.assertTrue(text.startswith("# Exercise 09: As-is assessment"))
        self.assertIn("**Level:** CAMP", text)
        for needle in ("demo-estate/as-is-evidence.csv", "application-management-self-assessment.md",
                       "itam-program-playbook.md", "five-minute gut check", "no evidence",
                       "one level lower", "playbook step 1", "playbook step 5"):
            self.assertIn(needle, text)
        self.assertNotIn("\u2014", text)

    def test_practicum_page_lists_and_builds_the_as_is_exercise(self):
        html = (ROOT / "site" / "practicum.html").read_text(encoding="utf-8")
        self.assertIn('<li><a href="#as-is-assessment">9. As-is assessment</a></li>', html)
        self.assertIn('id="as-is-assessment"', html)
        self.assertIn('BUILDERS["as-is-assessment"]', html)
        self.assertIn('COLLECTORS["as-is-assessment"]', html)
        self.assertIn("Nine hands-on", html)
        self.assertNotIn("Eight hands-on", html)

    def test_no_place_still_says_eight_exercises(self):
        for place in ("README.md", "AGENTS.md", "site/field-guide.html", "site/llms.txt"):
            text = (ROOT / place).read_text(encoding="utf-8")
            self.assertNotRegex(text, r"(?i)\beight (hands-on )?exercises", place)

