import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRACTICUM = ROOT / "practicum"


class PracticumTests(unittest.TestCase):
    def test_every_graded_tool_has_one_exercise(self):
        key = json.loads((ROOT / "demo-estate" / "answer-key.json").read_text())
        tools = sorted({k["tool"] for k in key})
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
