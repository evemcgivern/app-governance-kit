import io
import re
import shutil
import subprocess
import tempfile
import unittest
import xml.dom.minidom
import zipfile
from pathlib import Path

from agk.docs import (DocsError, form_blocks, gap_rows_of, template_blocks, body_html, csv_blocks, docx_bytes, front_title, inline_tokens, parse_markdown,
                      summary_of, tier_rule, title_of, unmark, write_docs, xlsx_bytes)

ROOT = Path(__file__).resolve().parent.parent

SAMPLE = """# Sample checklist

Intro with **bold**, `code`, and a [link](other.md).

## Steps

1. First [[XW-001]]
2. Second
   - nested item
- [ ] open box
- [x] done box

| # | Question | Yes / partly / no | Evidence |
| --- | --- | --- | --- |
| 1.1 | Is it done? | | |
"""


def parts(blob: bytes) -> dict:
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        return {n: z.read(n).decode("utf-8") for n in z.namelist()}


class ParseTests(unittest.TestCase):
    def test_blocks_and_title(self):
        blocks = parse_markdown(SAMPLE)
        self.assertEqual(title_of(blocks), "Sample checklist")
        self.assertEqual([b["type"] for b in blocks], ["heading", "p", "heading", "list", "list", "table"])

    def test_nested_and_checkbox_items(self):
        blocks = parse_markdown(SAMPLE)
        ordered = blocks[3]
        self.assertTrue(ordered["ordered"])
        self.assertEqual(ordered["items"][1]["children"][0]["text"], "nested item")
        boxes = blocks[4]["items"]
        self.assertEqual([i["checked"] for i in boxes], [False, True])

    def test_front_matter_dropped_and_read(self):
        text = "---\nname: x\ntitle: A title\n---\n\nBody.\n"
        self.assertEqual(front_title(text), "A title")
        self.assertEqual(parse_markdown(text)[0]["text"], "Body.")

    def test_inline_tokens(self):
        kinds = [t[0] for t in inline_tokens("a `b` [[XW-002]] [c](d.md) **e**")]
        self.assertEqual(kinds, ["t", "t", "t", "xw", "t", "a", "t", "t"])

    def test_summary_limits_words(self):
        self.assertLessEqual(len(summary_of(parse_markdown("# T\n\n" + "word " * 40)).split()), 14)

    def test_unmark_replaces_markdown_names(self):
        self.assertEqual(unmark("see demo-estate/council-draft.md now"), "see Council draft now")


class HtmlTests(unittest.TestCase):
    def test_no_markdown_links_and_radio_choices(self):
        html = body_html(parse_markdown(SAMPLE), lambda href: None)
        self.assertNotIn(".md", html)
        self.assertEqual(html.count('type="radio"'), 3)
        self.assertIn('class="xw-tag"', html)
        self.assertIn('type="checkbox" disabled checked', html)


class WordTests(unittest.TestCase):
    def test_docx_is_well_formed_with_checkboxes(self):
        files = parts(docx_bytes(parse_markdown(SAMPLE)))
        for name, xml_text in files.items():
            xml.dom.minidom.parseString(xml_text)
        doc = files["word/document.xml"]
        self.assertEqual(doc.count("<w14:checkbox>"), 5)  # three answers and two list boxes
        self.assertIn("Heading2", doc)

    def test_docx_bytes_are_reproducible(self):
        self.assertEqual(docx_bytes(parse_markdown(SAMPLE)), docx_bytes(parse_markdown(SAMPLE)))


class ExcelTests(unittest.TestCase):
    def test_workbook_is_well_formed_with_answer_dropdown(self):
        files = parts(xlsx_bytes(parse_markdown(SAMPLE)))
        for name, xml_text in files.items():
            xml.dom.minidom.parseString(xml_text)
        self.assertIn('<formula1>"Yes,Partly,No"</formula1>', files["xl/worksheets/sheet1.xml"])

    def test_no_table_raises(self):
        with self.assertRaises(DocsError):
            xlsx_bytes(parse_markdown("# Only text\n\nNothing else.\n"))

    def test_csv_blocks_make_a_sheet(self):
        files = parts(xlsx_bytes(csv_blocks("a,b\n1,2\n", "Data")))
        self.assertIn("<t xml:space=\"preserve\">a</t>", files["xl/worksheets/sheet1.xml"])


class TierTests(unittest.TestCase):
    def test_rule(self):
        self.assertEqual(tier_rule(8, 0, 0, 8), "Met")
        self.assertEqual(tier_rule(7, 1, 0, 8), "Met")
        self.assertEqual(tier_rule(6, 2, 0, 8), "Not met")
        self.assertEqual(tier_rule(7, 0, 1, 8), "Not met")
        self.assertEqual(tier_rule(3, 1, 0, 8), "Incomplete")

    def test_workbook_has_summary_sheet_with_formulas(self):
        md = (ROOT / "sam-toolkit" / "tier-self-assessment.md").read_text(encoding="utf-8")
        files = parts(xlsx_bytes(parse_markdown(md), tier_summary=True))
        for name, xml_text in files.items():
            xml.dom.minidom.parseString(xml_text)
        workbook = files["xl/workbook.xml"]
        self.assertTrue(workbook.index('name="Summary"') < workbook.index('name="Tier 1"'))
        self.assertIn('fullCalcOnLoad="1"', workbook)
        summary = files["xl/worksheets/sheet1.xml"]
        self.assertIn("COUNTIF('Tier 1'!C2:C9,&quot;No&quot;)", summary.replace('"', "&quot;"))
        self.assertIn("Below tier 1", summary)
        self.assertNotIn("Work out your tier", workbook)


class GapReportTests(unittest.TestCase):
    def setUp(self):
        self.md = (ROOT / "sam-toolkit" / "tier-self-assessment.md").read_text(encoding="utf-8")
        self.blocks = parse_markdown(self.md)

    def test_every_question_has_a_gap_row_with_an_action(self):
        gaps = gap_rows_of(self.blocks)
        questions = [row[0] for b in self.blocks if b["type"] == "table" and b["rows"][0][0] == "#"
                     and b["rows"][0][2].lower() == "yes / partly / no" for row in b["rows"][1:]]
        self.assertEqual(sorted(gaps), sorted(questions))
        self.assertEqual(len(questions), 19)
        for key, row in gaps.items():
            self.assertTrue(row[3].strip(), key)

    def test_workbook_gap_sheet_has_status_formulas_and_filter(self):
        files = parts(xlsx_bytes(self.blocks, tier_summary=True))
        for name, xml_text in files.items():
            xml.dom.minidom.parseString(xml_text)
        sheet = files["xl/worksheets/sheet5.xml"]
        self.assertIn("Partial gap", sheet)
        self.assertIn("&amp;", sheet)
        self.assertIn('<autoFilter ref="A1:H20"/>', sheet)
        self.assertIn("Gaps to close", files["xl/worksheets/sheet1.xml"])
        self.assertIn("'Gap report'!E2:E20", files["xl/worksheets/sheet1.xml"])

    @unittest.skipUnless(shutil.which("node"), "node is not installed")
    def test_page_script_is_valid_javascript(self):
        html = (ROOT / "site" / "docs" / "sam-toolkit" / "tier-self-assessment.html").read_text(encoding="utf-8")
        script = re.findall(r"<script>(.*?)</script>", html, re.S)[-1]
        path = Path(tempfile.mkdtemp()) / "tier.js"
        path.write_text(script, encoding="utf-8")
        result = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_page_has_live_gap_table(self):
        html = (ROOT / "site" / "docs" / "sam-toolkit" / "tier-self-assessment.html").read_text(encoding="utf-8")
        self.assertIn("table[data-gap]", html)
        self.assertIn("data-gap", html)


class PageShapeTests(unittest.TestCase):
    def read(self, name):
        return (ROOT / "site" / "docs" / "sam-toolkit" / name).read_text(encoding="utf-8")

    def test_blank_template_lists_columns_not_a_table(self):
        html = self.read("renewal-calendar.html")
        self.assertIn("column-list", html)
        self.assertNotIn("<table", html)

    def test_header_only_csv_gets_template_blocks(self):
        blocks = template_blocks("T", ["a", "b"], [], "x")
        self.assertEqual(blocks[3]["class"], "column-list")
        self.assertEqual(len(blocks[3]["items"]), 2)

    def test_prefilled_csv_with_blank_columns_becomes_a_form(self):
        rows = [["name", "in_scope", "note"], ["A", "", ""], ["B", "", ""]]
        blocks = form_blocks("T", rows, [], "x")
        form = next(b for b in blocks if b["type"] == "form")
        self.assertEqual(form["blank_cols"], [1, 2])
        self.assertIsNone(form_blocks("T", [["a", "b"]], [], "x"))
        self.assertIsNone(form_blocks("T", [["a", "b"], ["1", "2"]], [], "x"))

    def test_statement_of_applicability_is_a_fillable_form(self):
        html = self.read("statement-of-applicability.html")
        self.assertEqual(html.count('class="record"'), 15)
        self.assertIn("form-export", html)
        self.assertIn('id="record-data"', html)

    def test_checklist_has_tick_boxes_notes_and_answer_download(self):
        html = self.read("audit-and-review-checklist.html")
        self.assertIn('class="checklist-tick"', html)
        self.assertIn("<textarea", html)
        self.assertIn("answers-doc", html)
        self.assertIn("stays in this browser", html)

    def test_every_doc_page_has_top_and_bottom_print_icons(self):
        html = self.read("guide.html")
        self.assertEqual(html.count('class="print-icon"'), 2)


class SeoFileTests(unittest.TestCase):
    BASE = "https://evemcgivern.github.io/app-governance-kit/"

    def local(self, url):
        rel = url[len(self.BASE):].split("#")[0] or "index.html"
        return ROOT / "site" / rel

    def test_every_llms_txt_link_to_the_site_resolves(self):
        text = (ROOT / "site" / "llms.txt").read_text(encoding="utf-8")
        urls = [u for u in re.findall(r"\((https://evemcgivern\.github\.io/app-governance-kit/[^)]*)\)", text)]
        self.assertGreater(len(urls), 40)
        for url in urls:
            self.assertTrue(self.local(url).is_file(), url)

    def test_llms_txt_counts_match_the_crosswalk(self):
        import csv
        rows = list(csv.DictReader(open(ROOT / "methods" / "crosswalk" / "crosswalk.csv", encoding="utf-8")))
        text = (ROOT / "site" / "llms.txt").read_text(encoding="utf-8")
        self.assertIn(f"{len(rows)}-row", text)
        self.assertIn(f"{len(rows)} governance themes", text)

    def test_sitemap_lists_every_page_and_only_real_pages(self):
        text = (ROOT / "site" / "sitemap.xml").read_text(encoding="utf-8")
        urls = re.findall(r"<loc>([^<]+)</loc>", text)
        for url in urls:
            self.assertTrue(self.local(url).is_file(), url)
        pages = [p for p in (ROOT / "site").rglob("*.html") if not p.name.startswith("google") and "downloads" not in p.parts]
        self.assertEqual(len(urls), len(pages))

    def test_doc_pages_have_canonical_and_structured_data(self):
        html = (ROOT / "site" / "docs" / "sam-toolkit" / "guide.html").read_text(encoding="utf-8")
        self.assertIn('rel="canonical" href="https://evemcgivern.github.io/app-governance-kit/docs/sam-toolkit/guide.html"', html)
        self.assertIn("BreadcrumbList", html)
        self.assertIn('property="og:title"', html)


class VersionTests(unittest.TestCase):
    def test_every_page_has_the_footer_version_link(self):
        for page in list((ROOT / "site").glob("*.html")) + [ROOT / "site" / "docs" / "sam-toolkit" / "guide.html"]:
            self.assertIn('id="site-version"', page.read_text(encoding="utf-8"), page.name)

    def test_version_file_matches_the_release_version(self):
        import json
        shown = json.loads((ROOT / "site" / "version.json").read_text(encoding="utf-8"))["version"]
        manifest = json.loads((ROOT / ".release-please-manifest.json").read_text(encoding="utf-8"))["."]
        self.assertEqual(shown, (ROOT / "version.txt").read_text(encoding="utf-8").strip())
        self.assertEqual(shown, manifest)

    def test_release_please_updates_the_version_file(self):
        import json
        extra = json.loads((ROOT / "release-please-config.json").read_text(encoding="utf-8"))["packages"]["."]["extra-files"]
        self.assertIn({"type": "json", "path": "site/version.json", "jsonpath": "$.version"}, extra)


class SiteTests(unittest.TestCase):
    def test_real_repo_pages_exist_and_link_no_markdown(self):
        site = ROOT / "site"
        self.assertTrue((site / "docs" / "sam-toolkit" / "guide.html").is_file())
        for page in site.glob("*.html"):
            text = page.read_text(encoding="utf-8")
            self.assertNotRegex(text, r'href="[^"]*\.md"', page.name) if page.name != "tools.html" else None
        tools = (site / "tools.html").read_text(encoding="utf-8")
        self.assertEqual(re.findall(r'href="[^"]*\.md"', tools), ['href="downloads/agents/app-governance-agent.md"'])

    def test_tier_page_has_live_result(self):
        html = (ROOT / "site" / "docs" / "sam-toolkit" / "tier-self-assessment.html").read_text(encoding="utf-8")
        self.assertIn('id="tier-result"', html)
        self.assertEqual(html.count("data-tier="), 3)
        self.assertIn("Download Excel", html)
        self.assertIn("Download Word", html)

    def test_write_docs_without_site_is_a_noop(self):
        self.assertEqual(write_docs(Path(tempfile.mkdtemp())), [])


if __name__ == "__main__":
    unittest.main()
