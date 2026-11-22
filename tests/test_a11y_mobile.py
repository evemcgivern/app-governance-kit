import re
import unittest
from pathlib import Path

from agk.docs import TIER_EXTRA, body_html, parse_markdown
from test_docs import tmp_repo, built

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


if __name__ == "__main__":
    unittest.main()
