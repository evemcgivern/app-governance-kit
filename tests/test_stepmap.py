import re
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


class HandKeptPageTests(unittest.TestCase):
    def setUp(self):
        self.rows = load_map(ROOT)

    def test_each_practicum_section_has_the_mapped_practice_line(self):
        html = (ROOT / "site" / "practicum.html").read_text(encoding="utf-8")
        sections = html.split('<section class="pr-exercise" id="')[1:]
        keys = [r for r in self.rows if r["kind"] == "practicum"]
        self.assertEqual(len(sections), len(keys))
        for sec in sections:
            sec_id = sec.split('"', 1)[0]
            r = next(r for r in keys if r["key"][3:] == sec_id)
            self.assertIn(f'<p class="pr-step">{practice_line(r)}</p>', sec.split("</section>", 1)[0], sec_id)

    def test_each_case_study_has_the_mapped_tag(self):
        html = (ROOT / "site" / "case-studies.html").read_text(encoding="utf-8")
        for r in (r for r in self.rows if r["kind"] == "case"):
            start = html.index(f'<section id="case-{r["key"]}"')
            sec = html[start:html.index("</section>", start)]
            self.assertIn(f'<p class="case-step">{case_line(r)}</p>', sec, r["key"])

    def test_the_toolkit_page_lists_each_file_under_its_main_step_only(self):
        html = (ROOT / "site" / "sam-toolkit.html").read_text(encoding="utf-8")
        block = html.split("<!--STEPS-->", 1)[1].split("<!--/STEPS-->", 1)[0]
        groups = {}
        for m in re.finditer(r'<h3 id="by-step-([\w-]+)">.*?</h3>(.*?)(?=<h3 id="by-step-|\Z)', block, re.S):
            groups[m.group(1)] = re.findall(r'data-stem="([^"]+)"', m.group(2))
        for r in (r for r in self.rows if r["kind"] == "file"):
            stem = r["key"].rsplit(".", 1)[0]
            home = "beyond" if r["main_step"] == "beyond" else r["main_step"]
            for step, files in groups.items():
                if step == home:
                    self.assertEqual(files.count(stem), 1, r["key"])
                else:
                    self.assertNotIn(stem, files, r["key"])


class PlaybookAndCalendarTests(unittest.TestCase):
    def setUp(self):
        self.play = (TOOLKIT / "itam-program-playbook.md").read_text(encoding="utf-8")
        self.cal = (TOOLKIT / "operating-calendar.md").read_text(encoding="utf-8")

    def test_summary_box_sits_at_the_top_with_exactly_two_rules(self):
        self.assertLess(self.play.index("**Two standing rules**"), self.play.index("Three terms come up"))
        box = self.play.split("**Two standing rules**", 1)[1].split("\n\n")[1]
        rules = [l for l in box.splitlines() if l.startswith("- ")]
        self.assertEqual(len(rules), 2)
        self.assertIn("stop after step 5", rules[0].lower())
        self.assertIn("Steps 1 to 5 are a complete small program", rules[0])
        self.assertIn("give it to Legal and do not reply", rules[1])

    def test_practice_sentence(self):
        self.assertIn("do the matching practicum exercise on the Halden data before you do a step on real "
                      "records, and do exercise 08 before any real audit letter arrives", self.play)

    def test_calendar_weeks_show_order_not_duration(self):
        self.assertNotIn("| Weeks |", self.cal)
        self.assertIn("| Start in week |", self.cal)
        self.assertIn("30 to 60 hours", self.play)
        self.assertIn("2 to 3 months", self.play)
        self.assertIn("2 to 3 months", self.cal)

    def test_two_hours_a_week_row_uses_the_arithmetic(self):
        row = next(l for l in self.cal.splitlines() if "If you only have 2 hours a week" in l)
        self.assertIn("30 to 60 hours at 2 hours a week is 15 to 30 weeks, about 4 to 7 months", row)
        self.assertIn("steps 1 to 3 first", row.lower())
        self.assertEqual(30 / 2, 15)
        self.assertEqual(60 / 2, 30)


if __name__ == "__main__":
    unittest.main()
