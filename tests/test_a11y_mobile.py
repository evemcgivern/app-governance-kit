import re
import unittest
from pathlib import Path

from agk.docs import TIER_EXTRA, body_html, parse_markdown, write_docs
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


if __name__ == "__main__":
    unittest.main()
