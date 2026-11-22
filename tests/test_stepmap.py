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


from agk.stepmap import (CSV_NOTE, case_line, feeds_line, practice_line, reading_line, reading_minutes,
                         related_line, required_line, step_words, text_words)


def row(kind="file", key="x.csv", main="3", also=(), freq="Monthly", note=""):
    return {"kind": kind, "key": key, "main_step": main, "also_steps": list(also), "frequency": freq, "note": note}


class LineTests(unittest.TestCase):
    def test_step_words(self):
        self.assertEqual(step_words(["9"]), "step 9")
        self.assertEqual(step_words(["6", "9"]), "steps 6 and 9")
        self.assertEqual(step_words(["2", "3", "5"]), "steps 2, 3, and 5")

    def test_feeds_line(self):
        self.assertEqual(feeds_line(row()),
                         "Feeds step 3. Review: Monthly. Keep it in the versioned place your records policy "
                         "names, with access limited.")
        self.assertIn("Feeds step 6. Also step 9. Review:", feeds_line(row(main="6", also=["9"])))
        self.assertIn("Also steps 6 and 9.", feeds_line(row(main="3", also=["6", "9"])))
        self.assertTrue(feeds_line(row(main="beyond")).startswith("Not part of a step. Review:"))

    def test_feeds_line_has_no_retention_wording(self):
        text = feeds_line(row()).lower()
        for word in ("retention", "counsel", "shared place"):
            self.assertNotIn(word, text)

    def test_csv_note_and_required_columns(self):
        self.assertEqual(CSV_NOTE, "Not found means no source record was located; never put an estimate there.")
        self.assertIn("contract_end, notice_days, notice_deadline, decision_owner, and decided_on",
                      required_line("renewal-calendar"))
        self.assertEqual(required_line("asset-record"), "")

    def test_required_columns_exist_in_the_template(self):
        header = (TOOLKIT / "renewal-calendar.csv").read_text(encoding="utf-8").splitlines()[0].split(",")
        for col in ("contract_end", "notice_days", "notice_deadline", "decision_owner", "decided_on"):
            self.assertIn(col, header)

    def test_reading_time(self):
        self.assertEqual(reading_minutes(1000), 5)
        self.assertEqual(reading_minutes(1500), 8)
        self.assertEqual(reading_minutes(50), 1)
        self.assertEqual(reading_line(900), "")
        self.assertEqual(reading_line(2000),
                         "About 10 minutes to read (an estimate at 200 words per minute).")

    def test_text_words_counts_headings_lists_and_tables(self):
        blocks = [{"type": "heading", "level": 2, "text": "Two words"},
                  {"type": "p", "text": "one two three"},
                  {"type": "list", "items": [{"text": "a b", "children": [{"text": "c", "children": []}]}]},
                  {"type": "table", "rows": [["h1", "h2"], ["x y", "z"]]}]
        self.assertEqual(text_words(blocks), 2 + 3 + 3 + 5)

    def test_practice_and_case_lines(self):
        p = row("practicum", "01-program-setup", "2")
        self.assertEqual(practice_line(p), "Practice for playbook step 2.")
        self.assertEqual(practice_line(row("practicum", "08", "3", ["8"])), "Practice for playbook steps 3 and 8.")
        self.assertEqual(practice_line(row("practicum", "03", "beyond")),
                         "Practice for work beyond the ten steps.")
        self.assertEqual(case_line(row("case", "renewals", "3")), "This is what step 3 output looks like.")
        self.assertEqual(case_line(row("case", "audit-response", "3", ["8"])),
                         "This is what step 3 and step 8 output looks like.")
        self.assertEqual(case_line(row("case", "rationalization", "beyond")),
                         "This case is beyond the ten steps.")

    def test_related_line(self):
        rows = [row("practicum", "01-program-setup", "2", note="Program setup"),
                row("case", "renewals", "3", note="Renewals"),
                row("practicum", "08-audit-response", "3", ["8"], note="Audit response"),
                row("term", "Sponsor", "2"), row("term", "Notice deadline", "3")]
        self.assertEqual(related_line(rows, 2),
                         "- Related: [exercise 01: Program setup](../practicum/01-program-setup.md); "
                         "[glossary](../field-guide/glossary.md): Sponsor.")
        self.assertEqual(related_line(rows, 3),
                         "- Related: [exercise 08: Audit response](../practicum/08-audit-response.md); "
                         "case study [Renewals](../site/case-studies.html#case-renewals); "
                         "[glossary](../field-guide/glossary.md): Notice deadline.")
        self.assertEqual(related_line(rows, 8),
                         "- Related: [exercise 08: Audit response](../practicum/08-audit-response.md).")
        self.assertEqual(related_line(rows, 4), "")


class SourceTextTests(unittest.TestCase):
    def test_playbook_related_lines_match_the_map(self):
        rows = load_map(ROOT)
        play = (TOOLKIT / "itam-program-playbook.md").read_text(encoding="utf-8")
        expected = [related_line(rows, n) for n in range(1, 11)]
        found = [l for l in play.splitlines() if l.startswith("- Related:")]
        self.assertEqual(found, [e for e in expected if e])


if __name__ == "__main__":
    unittest.main()
