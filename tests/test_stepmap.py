import unittest
from pathlib import Path

from agk.stepmap import load_map

ROOT = Path(__file__).resolve().parent.parent
TOOLKIT = ROOT / "sam-toolkit"


class StepMapTests(unittest.TestCase):
    def setUp(self):
        self.rows = load_map(ROOT)

    def test_every_template_is_in_the_map_once(self):
        have = sorted(r["key"] for r in self.rows if r["kind"] == "file")
        want = sorted(f.name for f in TOOLKIT.iterdir() if f.is_file() and f.suffix in (".md", ".csv"))
        self.assertEqual(have, want)

    def test_every_step_is_1_to_10_or_beyond(self):
        ok = {str(n) for n in range(1, 11)} | {"beyond"}
        for r in self.rows:
            self.assertIn(r["main_step"], ok, r["key"])
            for s in r["also_steps"]:
                self.assertIn(s, ok - {"beyond"}, r["key"])
                self.assertNotEqual(s, r["main_step"], r["key"])

    def test_savings_report_is_not_part_of_a_step(self):
        row = next(r for r in self.rows if r["key"] == "savings-report.csv")
        self.assertEqual(row["main_step"], "beyond")

    def test_two_step_files_and_practice_follow_the_expert(self):
        by = {(r["kind"], r["key"]): r for r in self.rows}
        self.assertEqual(by["file", "authorization-log.csv"]["also_steps"], ["9"])
        self.assertEqual(by["file", "policy-template.md"]["also_steps"], ["6"])
        self.assertEqual(by["file", "process-map-worksheet.md"]["also_steps"], ["9"])
        self.assertEqual(by["practicum", "08-audit-response"]["main_step"], "3")
        self.assertEqual(by["practicum", "08-audit-response"]["also_steps"], ["8"])
        self.assertEqual(by["practicum", "03-crosswalk"]["main_step"], "beyond")
        self.assertEqual(by["case", "rationalization"]["main_step"], "beyond")

    def test_every_practicum_and_case_is_mapped(self):
        prac = sorted(r["key"] for r in self.rows if r["kind"] == "practicum")
        self.assertEqual(prac, sorted(p.stem for p in (ROOT / "practicum").glob("[0-9][0-9]-*.md")))
        self.assertEqual(len([r for r in self.rows if r["kind"] == "case"]), 6)

    def test_glossary_terms_exist(self):
        gloss = (ROOT / "field-guide" / "glossary.md").read_text(encoding="utf-8")
        for r in self.rows:
            if r["kind"] == "term":
                self.assertIn(f"**{r['key']}", gloss, r["key"])

    def test_frequency_only_from_the_calendar(self):
        cal = (TOOLKIT / "operating-calendar.md").read_text(encoding="utf-8")
        for r in self.rows:
            if r["kind"] == "file" and r["frequency"] != "Not on the calendar":
                self.assertIn(r["key"], cal, r["key"])


if __name__ == "__main__":
    unittest.main()
