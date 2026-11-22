import re
import unittest
from pathlib import Path

from agk.docs import LONG_PAGE_WORDS, PROMPT_SCRIPT, TIER_EXTRA, word_count, body_html, parse_markdown, write_docs
from test_docs import tmp_repo, built

CSS = Path(__file__).resolve().parent.parent / "site" / "style.css"

TABLE_MD = """## Questions

| # | Question | Yes / partly / no | Evidence |
| --- | --- | --- | --- |
| 1.1 | Is it done? | | |
| 1.2 | Is it `owned`? | | |

## Plain table

| Name | Owner |
| --- | --- |
| Alpha | Sam |
"""


def html_of(md: str, fillable: bool = False) -> str:
    return body_html(parse_markdown(md), lambda href: href, fillable=fillable)


class TableAccessTests(unittest.TestCase):
    def test_scroll_wrapper_is_a_named_focusable_region(self):
        html = html_of(TABLE_MD)
        self.assertEqual(len(re.findall(r'<div class="table-scroll" tabindex="0" role="region" '
                                        r'aria-label="[^"]+">', html)), 2)
        self.assertIn('aria-label="Questions table, scroll sideways to see more"', html)
        self.assertIn('aria-label="Plain table table, scroll sideways to see more"', html)

    def test_wrapper_without_heading_gets_a_numbered_name(self):
        html = html_of("| A | B |\n| --- | --- |\n| 1 | 2 |\n")
        self.assertIn('aria-label="Table 1, scroll sideways to see more"', html)

    def test_first_column_is_a_row_header(self):
        html = html_of(TABLE_MD)
        self.assertIn('<th scope="row">1.1</th>', html)
        self.assertIn('<th scope="row">Alpha</th>', html)
        self.assertNotIn("<td>Alpha</td>", html)

    def test_blank_first_cell_stays_a_data_cell(self):
        html = html_of("| A | B |\n| --- | --- |\n|  | 2 |\n")
        self.assertNotIn('scope="row"', html)

    def test_radios_are_grouped_with_their_question(self):
        html = html_of(TABLE_MD)
        groups = re.findall(r'<div class="checklist-choice-group" role="radiogroup" aria-label="([^"]+)">', html)
        self.assertEqual(groups, ["1.1 Is it done?", "1.2 Is it owned?"])
        self.assertEqual(html.count('type="radio"'), 6)

    def test_tier_script_does_not_assume_the_first_cell_is_a_td(self):
        self.assertNotIn('querySelectorAll("td")', TIER_EXTRA)


class HandKeptPageTests(unittest.TestCase):
    def test_field_guide_scroll_wrappers_are_named_regions(self):
        page = (Path(__file__).resolve().parent.parent / "site" / "field-guide.html").read_text(encoding="utf-8")
        wrappers = re.findall(r'<div class="table-scroll"[^>]*>', page)
        self.assertTrue(wrappers)
        for w in wrappers:
            self.assertIn('tabindex="0"', w)
            self.assertIn('role="region"', w)
            self.assertIn("aria-label=", w)


class TaskListTests(unittest.TestCase):
    def test_task_items_are_plain_list_items_with_a_print_hook(self):
        html = html_of("- [ ] Done when the owner signs\n- [x] Done already\n")
        self.assertNotIn("<input", html)
        self.assertIn('<ul class="task-list">', html)
        self.assertIn("<li>Done when the owner signs</li>", html)

    def test_print_css_draws_an_empty_square_before_task_items(self):
        css = CSS.read_text(encoding="utf-8")
        self.assertRegex(css, r'@media print\s*\{[^@]*\.task-list li::before\s*\{[^}]*content: "\\2610')


class InputHintTests(unittest.TestCase):
    def test_generated_text_inputs_turn_off_autofill_and_hint_next(self):
        root = tmp_repo(extra={"form.md": "# Form\n\n| Task | Owner | Notes |\n| --- | --- | --- |\n| A | | |\n"})
        write_docs(root)
        html = built(root, "form.html")
        inputs = re.findall(r'<input type="text"[^>]*>', html)
        self.assertTrue(inputs)
        for tag in inputs:
            self.assertIn('autocomplete="off"', tag)
            self.assertIn('enterkeyhint="next"', tag)

    def test_inputs_use_one_rem_text_at_phone_widths(self):
        css = CSS.read_text(encoding="utf-8")
        self.assertRegex(css, r"@media \(max-width: 46rem\)\s*\{[^@]*input\[type=\"text\"\][^{]*\{[^}]*font-size: 1rem")


class ViewLinkTests(unittest.TestCase):
    def test_view_links_name_their_page(self):
        from agk.docs import _download_link
        html = _download_link("a.csv", "a.html", "Intake form")
        self.assertIn(">view the page for Intake form</a>", html)
        self.assertNotIn(">view</a>", html)


class StepChipTests(unittest.TestCase):
    def setUp(self):
        self.root = tmp_repo()
        write_docs(self.root)
        self.html = built(self.root, "operating-calendar.html")

    def test_chip_keeps_the_title_and_the_neighbors(self):
        h = self.html
        self.assertIn('<nav class="doc-step" aria-label="Playbook step">', h)
        self.assertRegex(h, r'<span class="step-chip">Step 2 of 4</span> <a href="[^"]*#step-2-get-a-sponsor">Get a sponsor</a>')
        self.assertRegex(h, r'<a class="step-nav" rel="prev" href="[^"]*#step-1-read-the-map" '
                            r'aria-label="Previous step: Read the map">Previous</a>')
        self.assertRegex(h, r'<a class="step-nav" rel="next" href="[^"]*#step-3-stop-the-bleeding" '
                            r'aria-label="Next step: Stop &lt;the&gt; bleeding">Next</a>')

    def test_also_used_in_list_remains(self):
        h = built(self.root, "renewal-calendar.html")
        self.assertRegex(h, r'Also used in <a href="[^"]*#step-3-stop-the-bleeding">step 3</a>')

    def test_nav_links_are_44_px_tall(self):
        css = CSS.read_text(encoding="utf-8")
        self.assertRegex(css, r"\.step-nav\s*\{[^}]*min-height: 44px")
        self.assertRegex(css, r"\.step-nav\s*\{[^}]*min-width: 44px")


LONG_MD = "# Long\n\n" + "".join(
    f"## Part {n}\n\n" + ("word " * 200).strip() + ".\n\n" for n in range(1, 9))


class JumpListTests(unittest.TestCase):
    def test_long_page_gets_a_jump_list_and_back_to_top(self):
        root = tmp_repo(extra={"long.md": LONG_MD})
        write_docs(root)
        html = built(root, "long.html")
        self.assertIn('<details class="doc-jump"><summary>Jump to</summary>', html)
        self.assertIn('<li><a href="#part-1">Part 1</a></li>', html)
        self.assertEqual(html.count('<li><a href="#part-'), 8)
        self.assertLess(html.index('class="doc-jump"'), html.index('class="doc-body'))
        self.assertIn('<a class="doc-to-top" href="#main">Back to top</a>', html)

    def test_short_page_gets_neither(self):
        root = tmp_repo(extra={"short.md": "# Short\n\n## A\n\nx\n\n## B\n\nx\n\n## C\n\nx\n"})
        write_docs(root)
        html = built(root, "short.html")
        self.assertNotIn("doc-jump", html)
        self.assertNotIn("doc-to-top", html)

    def test_threshold_is_in_words(self):
        self.assertEqual(LONG_PAGE_WORDS, 1500)
        self.assertEqual(word_count(parse_markdown("# T\n\none two\n\n- three four\n")), 5)

    def test_tier_bar_height_is_capped(self):
        css = CSS.read_text(encoding="utf-8")
        self.assertRegex(css, r"\.tier-bar\s*\{[^}]*max-height: 30vh[^}]*overflow-y: auto")


class CopyFallbackTests(unittest.TestCase):
    def test_failed_copy_shows_a_visible_note_and_a_select_button(self):
        self.assertIn("prompt-fail", PROMPT_SCRIPT)
        self.assertIn("Copy did not work", PROMPT_SCRIPT)
        self.assertIn("prompt-select", PROMPT_SCRIPT)
        self.assertIn("pick(el)", PROMPT_SCRIPT)

    def test_copy_failure_covers_a_rejected_promise_and_a_missing_clipboard(self):
        self.assertIn("function () { done(false); }", PROMPT_SCRIPT)
        self.assertIn("document.execCommand('copy')", PROMPT_SCRIPT)


class PhoneActionTests(unittest.TestCase):
    def test_print_and_excel_are_marked_secondary_and_csv_is_not(self):
        root = tmp_repo(extra={"calendar2.csv": "app,date\nA,B\nC,D\n", "t.md": "# T\n\n| A | B |\n| --- | --- |\n| 1 | 2 |\n"})
        write_docs(root)
        html = built(root, "t.html")
        self.assertRegex(html, r'<a class="visual-actions__link doc-secondary" href="t.xlsx">Download Excel')
        self.assertRegex(html, r'class="visual-actions__link doc-print doc-secondary"')
        self.assertNotRegex(html, r'class="[^"]*doc-secondary[^"]*" href="t.docx"')
        csv = built(root, "calendar2.html")
        self.assertNotRegex(csv, r'class="[^"]*doc-secondary[^"]*" href="calendar2.csv"')

    def test_secondary_actions_are_text_links_at_phone_widths(self):
        css = CSS.read_text(encoding="utf-8")
        self.assertRegex(css, r"@media \(max-width: 46rem\)\s*\{[^@]*\.doc-secondary\s*\{[^}]*border: 0")


def rule(css: str, selector: str) -> str:
    """The declarations of the first top-level rule whose selector list ends with `selector`."""
    m = re.search(r"(?:^|\n)(?:[^{}@\n]*,\n)*" + re.escape(selector) + r"\s*\{([^}]*)\}", css)
    return m.group(1) if m else ""


class SidewaysScrollTests(unittest.TestCase):
    def test_action_links_wrap_instead_of_forcing_the_page_wide(self):
        body = rule(CSS.read_text(encoding="utf-8"), ".visual-actions__link")
        self.assertNotIn("nowrap", body)
        self.assertIn("max-width: 100%", body)


class TouchTargetTests(unittest.TestCase):
    def test_44px_applies_at_every_phone_width(self):
        css = CSS.read_text(encoding="utf-8")
        m = re.search(r"@media \(max-width: 46rem\)\s*\{\s*/\* touch targets \*/([^@]*?)\n\}", css)
        self.assertIsNotNone(m)
        block = m.group(1)
        for sel in (".lc-link-anchor", ".checklist-choice", ".site-nav a", ".pr-pair-remove",
                    ".visual-actions__link", ".lc-handoff-btn", ".pr-inline-label"):
            self.assertIn(sel, block)
        self.assertIn("min-height: 44px", block)


class ScrollCueTests(unittest.TestCase):
    def test_overflowing_tables_show_edge_shadows(self):
        css = CSS.read_text(encoding="utf-8")
        self.assertRegex(css, r"\.table-scroll,\s*\.im-table-wrap\s*\{[^}]*radial-gradient")
        self.assertIn("local", rule(css, ".table-scroll,\n.im-table-wrap"))

    def test_swipe_hint_is_added_by_script_only_when_a_table_overflows(self):
        js = (CSS.parent / "scroll-hint.js").read_text(encoding="utf-8")
        self.assertIn("Swipe for more", js)
        self.assertIn("scrollWidth > ", js)
        self.assertIn("hint.hidden = !over", js)

    def test_hint_is_phone_only_and_hidden_in_print(self):
        css = CSS.read_text(encoding="utf-8")
        self.assertRegex(css, r"\.scroll-hint\s*\{[^}]*display: none")
        self.assertRegex(css, r"@media \(max-width: 46rem\)\s*\{[^@]*\.scroll-hint:not\(\[hidden\]\)")

    def test_pages_load_the_script(self):
        root = tmp_repo()
        write_docs(root)
        self.assertIn('<script src="../../scroll-hint.js" defer></script>', built(root, "guide.html"))
        site = CSS.parent
        for page in ("practicum.html", "field-guide.html"):
            self.assertIn('<script src="scroll-hint.js" defer></script>', (site / page).read_text(encoding="utf-8"))

    def test_data_tables_get_a_sticky_first_column(self):
        css = CSS.read_text(encoding="utf-8")
        self.assertRegex(css, r'table\.sticky-first tbody th\[scope="row"\][^{]*\{[^}]*position: sticky')
        wide = html_of("| A | B | C |\n| --- | --- | --- |\n| 1 | 2 | 3 |\n")
        narrow = html_of("| A | B |\n| --- | --- |\n| 1 | 2 |\n")
        self.assertIn("sticky-first", wide)
        self.assertNotIn("sticky-first", narrow)


PRACTICUM = CSS.parent / "practicum.html"


class PracticumTests(unittest.TestCase):
    def setUp(self):
        self.src = PRACTICUM.read_text(encoding="utf-8")

    def test_scroll_wrapper_is_a_named_focusable_region(self):
        for line in ('wrap.setAttribute("tabindex", "0");', 'wrap.setAttribute("role", "region");',
                     'wrap.setAttribute("aria-label",'):
            self.assertIn(line, self.src)

    def test_first_column_is_a_row_header(self):
        self.assertIn('var cell = document.createElement(i === 0 ? "th" : "td");', self.src)
        self.assertIn('cell.setAttribute("scope", "row");', self.src)

    def test_data_tables_keep_the_first_column_in_view_and_unshouted(self):
        self.assertIn('table.className = "sticky-first"', self.src)
        self.assertIn('.pr-controls tbody th[scope="row"]', CSS.read_text(encoding="utf-8"))

    def test_row_checkboxes_name_their_row(self):
        self.assertIn("visibleLabel[0] + \": \" + visibleLabel[1]", self.src)
        for call in ('["Weakest", row.area]', '["Select", row.id + " " + row.name]', '["Expired", row.id]',
                     '["Orphaned", row.id]', '["Overdue", row.device_id]', '["Unwiped", row.device_id]',
                     '["Short", row.license_id + " version " + row.version]'):
            self.assertIn(call, self.src)

    def test_remove_buttons_name_their_pair_and_focus_moves_on(self):
        self.assertIn('"Remove duplicate pair " + pair[0] + " and " + pair[1]', self.src)
        self.assertIn('querySelectorAll(".pr-pair-remove")', self.src)
        self.assertIn("tabindex", self.src[self.src.index("pairsHeading"):self.src.index("pairsHeading") + 400])

    def test_result_regions_stay_in_the_page_and_empty(self):
        regions = re.findall(r'<div class="pr-result"[^>]*>', self.src)
        self.assertEqual(len(regions), 8)
        for tag in regions:
            self.assertIn('role="status"', tag)
            self.assertNotIn("hidden", tag)
        self.assertNotIn("el.hidden = false", self.src)
        self.assertNotIn("result.hidden = true", self.src)
        self.assertRegex(CSS.read_text(encoding="utf-8"), r"\.pr-result:empty\s*\{")

    def test_check_moves_focus_to_the_result_heading(self):
        self.assertIn('heading.setAttribute("tabindex", "-1");', self.src)
        self.assertIn("heading.focus();", self.src)


if __name__ == "__main__":
    unittest.main()
