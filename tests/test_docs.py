import io
import re
import shutil
import subprocess
import tempfile
import unittest
import xml.dom.minidom
import zipfile
from pathlib import Path

from agk.docs import (DocsError, _download_link, _prompt_html, form_blocks, gap_rows_of, template_blocks, body_html, csv_blocks, docx_bytes, front_title, inline_tokens, parse_markdown,
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


class PromptBlockTests(unittest.TestCase):
    def test_prompt_block_marks_placeholders_and_adds_a_hidden_copy_button(self):
        html = _prompt_html("Rules: help with [PROCESS] today.", 1, "Prompt 3: Map a process", lambda h: h, lambda n: None)
        self.assertIn('<div class="prompt-block">', html)
        self.assertIn('<mark class="prompt-ph">[PROCESS]</mark>', html)
        self.assertIn('<div class="prompt-text" id="prompt-3-text">', html)
        self.assertIn('data-target="prompt-3-text"', html)
        self.assertIn('data-n="3"', html)
        self.assertIn('aria-describedby="prompt-3-map-a-process"', html)
        self.assertRegex(html, r'<button type="button"[^>]* hidden [^>]*>Copy prompt 3</button>')
        self.assertIn("Prompt 3: copy and paste", html)

    def test_prompt_without_a_number_in_its_heading_uses_its_position(self):
        html = _prompt_html("Text.", 2, "Other heading", lambda h: h, lambda n: None)
        self.assertIn('id="prompt-2-text"', html)
        self.assertIn(">Copy prompt 2<", html)

    def test_paste_this_paragraph_becomes_a_prompt_block_in_a_page(self):
        blocks = parse_markdown("## Prompt 1: Set the scene\n\n**Paste this:** Ask about [YOUR ROLE].\n\nPlain text.\n")
        html = body_html(blocks, lambda h: h)
        self.assertEqual(html.count('class="prompt-block"'), 1)
        self.assertIn('<mark class="prompt-ph">[YOUR ROLE]</mark>', html)
        self.assertNotIn("Paste this", html)
        self.assertIn("<p>Plain text.</p>", html)


RULE = ("Use only an assistant your organization has approved for confidential data; otherwise use the Halden "
        "data, column headings only, or redacted rows; never paste passwords, license keys, or employee names "
        "and emails; and once an audit letter exists, nothing about it goes to any assistant unless Legal agrees.")
PROMPT_MD = ("| Playbook step | Prompts |\n| --- | --- |\n| 2 Sponsor | 8 (charter), 11 |\n| 4 Scope | No prompt. |\n"
             "| 6 Policy | 8 (policy) |\n\n"
             f"**Privacy rule for every prompt:** {RULE}\n\n"
             "## Prompt 8: Set up governance\n\n**Paste this:** Review [DRAFT].\n\n"
             "## Prompt 11: Map customers\n\n**Paste this:** Map [CUSTOMERS].\n")


class PromptPrivacyTests(unittest.TestCase):
    def test_prompt_step_table_gives_each_prompts_steps_in_order(self):
        from agk.docs import prompt_steps
        self.assertEqual(prompt_steps(parse_markdown(PROMPT_MD)), {"8": ["2", "6"], "11": ["2"]})

    def test_rule_and_step_link_render_above_each_copy_button_from_one_source_line(self):
        steps = {"8": [("2", "Get a sponsor", "pb.html#step-2"), ("6", "The policy set", "pb.html#step-6")]}
        html = _prompt_html("Text.", 1, "Prompt 8: Set up", lambda h: h, lambda n: None, rule=RULE, steps=steps["8"])
        self.assertLess(html.index('class="prompt-rule"'), html.index("prompt-copy"))
        self.assertIn(RULE, html)
        self.assertIn('<a href="pb.html#step-2">Which step is this?</a> Playbook step 2, Get a sponsor.', html)
        self.assertIn('Also <a href="pb.html#step-6">step 6</a>.', html)

    def test_body_uses_the_marked_line_for_every_prompt(self):
        html = body_html(parse_markdown(PROMPT_MD), lambda h: h,
                         prompt_steps_by_label={"8": [("2", "S", "p.html#a")]})
        self.assertEqual(html.count('class="prompt-rule"'), 2)
        self.assertEqual(html.count("Which step is this?"), 1)

    def test_real_prompts_each_have_a_rule_and_a_step_and_the_table_explains_step_four(self):
        text = (ROOT / "sam-toolkit" / "setup-prompts.md").read_text(encoding="utf-8")
        self.assertEqual(text.count("Use only an assistant your organization has approved"), 1)
        from agk.docs import prompt_steps
        got = prompt_steps(parse_markdown(text))
        self.assertEqual(sorted(got, key=int), [str(n) for n in range(1, 14)])
        self.assertRegex(text, r"\| 4 Set the scope \| No prompt")
        self.assertNotIn("Step 4 has no prompt of its own.", text)


class DownloadLinkTests(unittest.TestCase):
    def test_csv_links_to_the_csv_and_the_page(self):
        html = _download_link("renewal-calendar.csv", "renewal-calendar.html", "Renewal calendar")
        self.assertEqual(html, '<a href="renewal-calendar.csv">Renewal calendar (CSV)</a> '
                               '(<a href="renewal-calendar.html">view</a>)')

    def test_markdown_links_to_the_word_file(self):
        html = _download_link("guide.md", "../sam-toolkit/guide.html", "Guide")
        self.assertIn('<a href="../sam-toolkit/guide.docx">Guide (Word)</a>', html)
        self.assertIn('<a href="../sam-toolkit/guide.html">view</a>', html)

    def test_other_file_types_and_non_page_hrefs_have_no_download(self):
        self.assertIsNone(_download_link("book.xlsx", "book.html", "Book"))
        self.assertIsNone(_download_link("guide.md", "guide.pdf", "Guide"))

    def test_title_is_escaped(self):
        self.assertIn("A &lt;b&gt; (CSV)", _download_link("a.csv", "a.html", "A <b>"))

    def test_attach_paragraph_links_downloads_and_other_paragraphs_link_pages(self):
        files = lambda name: ("renewal-calendar.html", "Renewal calendar") if name == "renewal-calendar.csv" else None
        blocks = parse_markdown("**Attach (optional):** `renewal-calendar.csv`.\n\nSee `renewal-calendar.csv`.\n")
        html = body_html(blocks, lambda h: h, files)
        first, second = html.split("\n")
        self.assertIn('<a href="renewal-calendar.csv">Renewal calendar (CSV)</a>', first)
        self.assertIn('(<a href="renewal-calendar.html">view</a>)', first)
        self.assertEqual(second, '<p>See <a href="renewal-calendar.html">Renewal calendar</a>.</p>')


class FillableFallbackTests(unittest.TestCase):
    def _page(self, body: str) -> str:
        root = tmp_repo(extra={"operating-calendar.md": body})
        write_docs(root)
        return built(root, "operating-calendar.html")

    def test_document_with_nothing_to_fill_in_has_no_answers_button_or_note(self):
        html = self._page("# Calendar\n\nJust text.\n\n- one\n- two\n")
        self.assertNotIn("answers-doc", html)
        self.assertNotIn("stays in this browser", html)

    def test_document_with_a_checklist_table_keeps_the_answers_button_and_note(self):
        html = self._page("# Calendar\n\n| # | Question | Yes / partly / no | Evidence |\n"
                          "| --- | --- | --- | --- |\n| 1 | Is it done? | | |\n")
        self.assertIn("answers-doc", html)
        self.assertIn("stays in this browser", html)


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


INDEX = ("<html><body><header><div class=\"support-bar\">s</div></header>"
         "<footer class=\"site-footer\">f</footer></body></html>")

PLAYBOOK = """# Playbook

Intro.

## The ten steps

### Step 1: Read the map

- Files: `guide.md`.

### Step 2: Get a sponsor

- Files: `renewal-calendar.csv` and [the calendar](operating-calendar.md).

### Step 3: Stop <the> bleeding

- Files: `audit-response-roles.csv`, `renewal-calendar.csv`.

### Stuck, or inherited a mess?

Text with `loose-file.md` that belongs to no step.

### Step 4: Set the scope

- Files: `policy-template.md`.
"""


def tmp_repo(playbook: str | None = PLAYBOOK, extra: dict | None = None) -> Path:
    root = Path(tempfile.mkdtemp())
    (root / "site").mkdir()
    (root / "site" / "index.html").write_text(INDEX, encoding="utf-8")
    (root / "site" / "field-guide.html").write_text("<html></html>", encoding="utf-8")
    sam = root / "sam-toolkit"
    sam.mkdir()
    if playbook is not None:
        (sam / "itam-program-playbook.md").write_text(playbook, encoding="utf-8")
    files = {"guide.md": "# Guide\n\nSee the [glossary](../../field-guide.html#glossary-heading).\n",
             "operating-calendar.md": "# Calendar\n\nBody.\n",
             "policy-template.md": "# Policy\n\nBody.\n",
             "loose-file.md": "# Loose\n\nBody.\n",
             "audit-response-roles.csv": "task,holder\nA,\n",
             "renewal-calendar.csv": "app,date\n"}
    files.update(extra or {})
    for name, text in files.items():
        (sam / name).write_text(text, encoding="utf-8")
    return root


def built(root: Path, name: str) -> str:
    return (root / "site" / "docs" / "sam-toolkit" / name).read_text(encoding="utf-8")


class SiteLinkTests(unittest.TestCase):
    def test_link_to_hand_kept_site_page_becomes_a_working_link(self):
        root = tmp_repo()
        write_docs(root)
        html = built(root, "guide.html")
        self.assertIn('<a href="../../field-guide.html#glossary-heading">glossary</a>', html)

    def test_link_to_missing_site_page_stays_plain_text(self):
        root = tmp_repo(extra={"guide.md": "# Guide\n\nSee the [gone](../../nope.html#x).\n"})
        write_docs(root)
        html = built(root, "guide.html")
        self.assertNotIn("nope.html", html)
        self.assertIn("gone", html)

    def test_link_to_missing_site_page_warns_with_file_and_link(self):
        root = tmp_repo(extra={"guide.md": "# Guide\n\nSee the [gone](../../nope.html#x).\n"})
        warnings = write_docs(root)
        self.assertEqual(len(warnings), 1, warnings)
        self.assertIn("guide.md", warnings[0])
        self.assertIn("../../nope.html#x", warnings[0])

    def test_link_into_the_site_folder_becomes_a_working_link(self):
        root = tmp_repo(extra={"guide.md": "# Guide\n\nSee the [guide](../site/field-guide.html#top).\n"})
        warnings = write_docs(root)
        self.assertEqual(warnings, [])
        self.assertIn('<a href="../../field-guide.html#top">guide</a>', built(root, "guide.html"))

    def test_working_links_give_no_warnings(self):
        self.assertEqual(write_docs(tmp_repo()), [])

    def test_link_to_field_guide_markdown_becomes_the_generated_page(self):
        root = tmp_repo(extra={"guide.md": "# Guide\n\nSee the [glossary](../field-guide/glossary.md).\n"})
        (root / "field-guide").mkdir()
        (root / "field-guide" / "glossary.md").write_text("# Glossary\n", encoding="utf-8")
        warnings = write_docs(root)
        self.assertEqual(warnings, [])
        html = built(root, "guide.html")
        self.assertIn('<a href="../../field-guide.html#glossary-heading">glossary</a>', html)
        self.assertNotIn(".md", html.split("<main")[1].split("</main>")[0])

    def test_word_download_keeps_link_text_only_for_field_guide_markdown(self):
        root = tmp_repo(extra={"guide.md": "# Guide\n\nSee the [glossary](../field-guide/glossary.md).\n"})
        (root / "field-guide").mkdir()
        (root / "field-guide" / "glossary.md").write_text("# Glossary\n", encoding="utf-8")
        write_docs(root)
        docx = (root / "site" / "docs" / "sam-toolkit" / "guide.docx").read_bytes()
        xml = parts(docx)["word/document.xml"]
        self.assertIn("glossary", xml)
        self.assertNotIn("field-guide", xml)


class BackLabelTests(unittest.TestCase):
    def test_methods_pages_say_ai_skills(self):
        root = tmp_repo()
        m = root / "methods" / "t"
        m.mkdir(parents=True)
        (m / "method.md").write_text("# T\n\nBody.\n", encoding="utf-8")
        write_docs(root)
        html = (root / "site" / "docs" / "t" / "method.html").read_text(encoding="utf-8")
        self.assertIn("&larr; AI skills</a>", html)
        self.assertNotIn("&larr; Tools</a>", html)


class WayfindingTests(unittest.TestCase):
    def test_page_in_step_two_shows_position_and_neighbors(self):
        root = tmp_repo()
        write_docs(root)
        html = built(root, "operating-calendar.html")
        pb = "itam-program-playbook.html"
        self.assertIn("Used in playbook step 2 of 4: ", html)
        self.assertIn(f'href="{pb}#step-2-get-a-sponsor"', html)
        self.assertIn(f'href="{pb}#step-1-read-the-map"', html)
        self.assertIn(f'href="{pb}#step-3-stop-the-bleeding"', html)
        # the ids exist on the playbook page
        play = built(root, pb)
        for anchor in ("step-1-read-the-map", "step-2-get-a-sponsor", "step-3-stop-the-bleeding"):
            self.assertIn(f'id="{anchor}"', play)

    def test_first_step_wins_and_title_is_escaped(self):
        root = tmp_repo()
        write_docs(root)
        html = built(root, "renewal-calendar.html")
        self.assertIn("Used in playbook step 2 of 4: ", html)
        self.assertRegex(html, r'Also used in <a href="[^"]*#step-3-stop-the-bleeding">step 3</a>')
        html3 = built(root, "audit-response-roles.html")
        self.assertIn("Used in playbook step 3 of 4: ", html3)
        self.assertIn("Stop &lt;the&gt; bleeding", html3)
        self.assertNotIn("Stop <the>", html3)

    def test_first_and_last_steps_omit_missing_neighbor(self):
        root = tmp_repo()
        write_docs(root)
        first = built(root, "guide.html")
        self.assertIn("step 1 of 4", first)
        self.assertNotIn("Previous step", first)
        self.assertIn("Next step", first)
        last = built(root, "policy-template.html")
        self.assertIn("step 4 of 4", last)
        self.assertNotIn("Next step", last)

    def test_page_in_no_step_and_the_playbook_show_nothing(self):
        root = tmp_repo()
        write_docs(root)
        self.assertNotIn("Used in playbook", built(root, "loose-file.html"))
        self.assertNotIn("Used in playbook", built(root, "itam-program-playbook.html"))

    def test_step_count_comes_from_the_playbook(self):
        root = tmp_repo(playbook=PLAYBOOK + "\n### Step 5: One more\n\n- Files: `loose-file.md`.\n")
        write_docs(root)
        self.assertIn("step 1 of 5", built(root, "guide.html"))
        self.assertIn("step 5 of 5", built(root, "loose-file.html"))

    def test_output_is_deterministic(self):
        root = tmp_repo()
        write_docs(root)
        first = {p: p.read_bytes() for p in (root / "site" / "docs").rglob("*.html")}
        write_docs(root)
        second = {p: p.read_bytes() for p in (root / "site" / "docs").rglob("*.html")}
        self.assertEqual(first, second)

    def test_missing_or_malformed_playbook_builds_without_the_line_and_warns(self):
        for playbook in (None, "# Playbook\n\n### Step x: nope\n\n- `guide.md`\n", ""):
            root = tmp_repo(playbook=playbook)
            warnings = write_docs(root)
            self.assertNotIn("Used in playbook", built(root, "guide.html"))
            self.assertEqual(len(warnings), 1, (playbook, warnings))
            self.assertIn("itam-program-playbook.md", warnings[0])
            self.assertIn("wayfinding", warnings[0])

    def test_working_playbook_gives_no_wayfinding_warning(self):
        self.assertEqual(write_docs(tmp_repo()), [])

    def test_no_sam_toolkit_means_no_wayfinding_warning(self):
        root = tmp_repo()
        shutil.rmtree(root / "sam-toolkit")
        m = root / "methods" / "t"
        m.mkdir(parents=True)
        (m / "method.md").write_text("# T\n\nBody.\n", encoding="utf-8")
        self.assertEqual(write_docs(root), [])


MAP = ("kind,key,main_step,also_steps,frequency,note\n"
       "file,renewal-calendar.csv,3,8,Monthly,\n"
       "file,audit-response-roles.csv,3,,Quarterly,\n"
       "file,policy-template.md,4,6;9,Yearly,\n"
       "file,guide.md,1,,Not on the calendar,\n"
       "file,savings-report.csv,beyond,,Not on the calendar,\n"
       "practicum,01-program-setup,2,,,Program setup\n"
       "practicum,04-crosswalk,beyond,,,Crosswalk\n")


def mapped_repo(extra: dict | None = None) -> Path:
    root = tmp_repo(extra=extra)
    (root / "steps").mkdir()
    (root / "steps" / "step-map.csv").write_text(MAP, encoding="utf-8")
    (root / "sam-toolkit" / "savings-report.csv").write_text("period,amount\n", encoding="utf-8")
    (root / "sam-toolkit" / "examples").mkdir()
    (root / "sam-toolkit" / "examples" / "renewal-calendar-example.csv").write_text("app,date\nA,1\n",
                                                                                  encoding="utf-8")
    (root / "practicum").mkdir()
    (root / "practicum" / "01-program-setup.md").write_text("# Exercise 01\n\nBody.\n", encoding="utf-8")
    (root / "practicum" / "04-crosswalk.md").write_text("# Exercise 04\n\nBody.\n", encoding="utf-8")
    return root


class StepMapPageTests(unittest.TestCase):
    def test_feeds_line_is_its_own_paragraph_with_frequency(self):
        root = mapped_repo()
        write_docs(root)
        html = built(root, "renewal-calendar.html")
        self.assertRegex(html, r'<p class="meta doc-feeds">Feeds step 3\. Also step 8\. Review: Monthly\. '
                               r'Keep it in the versioned place your records policy names, with access limited\.</p>')
        self.assertIn("Also steps 6 and 9.", built(root, "policy-template.html"))
        self.assertIn("Not part of a step.", built(root, "savings-report.html"))

    def test_no_feeds_line_on_playbook_unmapped_files_or_without_a_map(self):
        root = mapped_repo()
        write_docs(root)
        self.assertNotIn("doc-feeds", built(root, "itam-program-playbook.html"))
        self.assertNotIn("doc-feeds", built(root, "loose-file.html"))
        plain = tmp_repo()
        write_docs(plain)
        self.assertNotIn("doc-feeds", built(plain, "guide.html"))

    def test_feeds_line_has_no_retention_or_shared_place_wording(self):
        root = mapped_repo()
        write_docs(root)
        html = built(root, "renewal-calendar.html")
        line = html[html.index('class="meta doc-feeds"'):].split("</p>")[0].lower()
        self.assertNotIn("retention", line)
        self.assertNotIn("shared place", line)

    def test_csv_pages_get_the_not_found_note_and_renewal_required_columns(self):
        root = mapped_repo()
        write_docs(root)
        html = built(root, "renewal-calendar.html")
        self.assertIn("Not found means no source record was located; never put an estimate there.", html)
        self.assertIn("contract_end, notice_days, notice_deadline, decision_owner, and decided_on", html)
        other = built(root, "audit-response-roles.html")
        self.assertIn("Not found means", other)
        self.assertNotIn("Required columns", other)
        self.assertNotIn("Not found means", built(root, "guide.html"))
        self.assertNotIn("Not found means", built(root, "renewal-calendar-example.html"))

    def test_filled_example_link_only_where_an_example_exists(self):
        root = mapped_repo()
        write_docs(root)
        self.assertIn('href="renewal-calendar-example.html">See a filled example</a>',
                      built(root, "renewal-calendar.html"))
        self.assertNotIn("See a filled example", built(root, "audit-response-roles.html"))
        self.assertNotIn("See a filled example", built(root, "guide.html"))

    def test_practice_line_on_practicum_pages(self):
        root = mapped_repo()
        write_docs(root)
        html = (root / "site" / "docs" / "practicum" / "01-program-setup.html").read_text(encoding="utf-8")
        self.assertIn('<p class="meta doc-practice">Practice for playbook step 2.</p>', html)
        beyond = (root / "site" / "docs" / "practicum" / "04-crosswalk.html").read_text(encoding="utf-8")
        self.assertIn("Practice for work beyond the ten steps.", beyond)

    def test_long_pages_show_a_labeled_reading_time_and_short_pages_do_not(self):
        long_text = "# Long\n\n" + ("word " * 2000) + "\n"
        root = mapped_repo(extra={"loose-file.md": long_text})
        write_docs(root)
        self.assertIn('<p class="meta doc-reading">About 10 minutes to read (an estimate at 200 words per '
                      'minute).</p>', built(root, "loose-file.html"))
        self.assertNotIn("doc-reading", built(root, "guide.html"))


class ToolkitByStepTests(unittest.TestCase):
    def test_section_lists_each_file_once_under_its_main_step_with_a_tag(self):
        from agk.docs import toolkit_steps_html
        steps = [{"n": 3, "title": "Stop the bleeding", "id": "step-3-stop"},
                 {"n": 8, "title": "Proof first", "id": "step-8-proof"}]
        rows = [{"kind": "file", "key": "renewal-calendar.csv", "main_step": "3", "also_steps": ["8"],
                 "frequency": "", "note": ""},
                {"kind": "file", "key": "savings-report.csv", "main_step": "beyond", "also_steps": [],
                 "frequency": "", "note": ""},
                {"kind": "term", "key": "Sponsor", "main_step": "3", "also_steps": [], "frequency": "",
                 "note": ""}]
        html = toolkit_steps_html(rows, steps, {"renewal-calendar.csv": "Renewal calendar"})
        self.assertEqual(html.count('data-stem="renewal-calendar"'), 1)
        self.assertIn('<h3 id="by-step-3"><a href="docs/sam-toolkit/itam-program-playbook.html#step-3-stop">'
                      'Step 3: Stop the bleeding</a></h3>', html)
        self.assertIn('<a href="docs/sam-toolkit/renewal-calendar.html">Renewal calendar</a> '
                      '<span class="step-tag">Step 3, also step 8</span>', html)
        self.assertIn('<h3 id="by-step-beyond">Not part of a step</h3>', html)
        self.assertIn('data-stem="savings-report"', html.split("by-step-beyond")[1])
        self.assertNotIn("Sponsor", html)
        self.assertNotIn("by-step-8", html)

    def test_write_docs_fills_the_marked_region_of_the_toolkit_page(self):
        root = mapped_repo()
        page = root / "site" / "sam-toolkit.html"
        page.write_text("<html><body><!--STEPS-->old<!--/STEPS--><p>keep</p></body></html>", encoding="utf-8")
        write_docs(root)
        html = page.read_text(encoding="utf-8")
        self.assertNotIn("old", html)
        self.assertIn('data-stem="renewal-calendar"', html)
        self.assertIn("<p>keep</p>", html)
        first = html
        write_docs(root)
        self.assertEqual(page.read_text(encoding="utf-8"), first)


if __name__ == "__main__":
    unittest.main()
