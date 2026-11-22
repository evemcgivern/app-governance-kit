import re
import unittest
from pathlib import Path

from agk.site import broken_links

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
PAGE = (SITE / "lifecycle.html").read_text(encoding="utf-8")

HREFS = ["docs/lifecycle/questions.html", "impact-map.html", "tools.html#software-lifecycle",
         "tools.html#hardware-lifecycle"]


def cards() -> list[str]:
    m = re.search(r'<section id="lifecycle-family"[^>]*>(.*?)</section>', PAGE, re.S)
    assert m, "lifecycle-family section not found"
    return re.findall(r'<li class="card case-card">(.*?)</li>', m.group(1), re.S)


class LifecyclePageTests(unittest.TestCase):
    def test_four_items_are_cards_with_title_link_summary_kind_and_fit(self):
        found = cards()
        self.assertEqual(len(found), 4)
        for card, href in zip(found, HREFS):
            self.assertRegex(card, rf'<h3><a href="{re.escape(href)}">[^<]{{10,}}</a></h3>')
            self.assertRegex(card, r'<p class="case-card__summary">[^<]{20,}</p>')
            self.assertRegex(card, r'<p class="meta case-card__tool">(Tool|Kind): [^<]+</p>')
            self.assertRegex(card, r'<p class="meta case-card__step">Fits: [^<]+</p>')

    def test_order_is_wheel_then_cards_then_explanation(self):
        wheel = PAGE.index('class="lc-layout"')
        family = PAGE.index('id="lifecycle-family"')
        together = PAGE.index("<!--LC-TOGETHER-->")
        self.assertLess(wheel, family)
        self.assertLess(family, together)

    def test_wheel_and_its_data_are_still_present(self):
        for needle in ('id="lc-segments"', 'id="lc-panel-list"', 'id="lc-data"', "<!--LC-DATA-->"):
            self.assertIn(needle, PAGE)

    def test_explanation_is_collapsed_and_kept(self):
        self.assertRegex(PAGE, r"<details[^>]*>\s*<summary>[^<]+</summary>\s*<!--LC-TOGETHER-->")
        self.assertIn("The governance council owns the gate between each pair of stages", PAGE)

    def test_sections_are_labelled_and_headings_nest(self):
        self.assertEqual(PAGE.count("<h1"), 1)
        for sid in ("stages-heading", "lifecycle-family-heading", "loop-heading"):
            self.assertRegex(PAGE, rf'aria-labelledby="{sid}"')
            self.assertRegex(PAGE, rf'<h2 id="{sid}">')
        self.assertIn('<h3 id="lc-panel-heading"', PAGE)
        self.assertNotIn("<h2>", PAGE)

    def test_title_and_description_rules(self):
        self.assertRegex(PAGE, r"<title>Application lifecycle \| App Governance Kit</title>")
        for pattern in (r'name="description" content="([^"]*)"', r'property="og:description" content="([^"]*)"',
                        r'name="twitter:description" content="([^"]*)"'):
            text = re.search(pattern, PAGE).group(1)
            self.assertLessEqual(len(text), 160)
            self.assertGreaterEqual(len(text), 60)

    def test_no_broken_links_and_no_em_dashes(self):
        self.assertEqual([b for b in broken_links(SITE) if b.startswith("lifecycle.html")], [])
        self.assertNotIn("—", PAGE)


if __name__ == "__main__":
    unittest.main()


CSS = (SITE / "style.css").read_text(encoding="utf-8")


def css_rules(selector: str) -> str:
    """Return the joined bodies of every rule whose selector list contains `selector`."""
    bodies = []
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", CSS):
        if selector in [s.strip() for s in sel.split(",")]:
            bodies.append(body)
    return "\n".join(bodies)


class WheelAffordanceTests(unittest.TestCase):
    def test_instruction_sits_above_the_wheel(self):
        m = re.search(r'<p class="lc-instruction" id="lc-instruction"[^>]*>([^<]+)</p>', PAGE)
        self.assertIsNotNone(m, "instruction line missing")
        self.assertRegex(m.group(1), r"^Select a stage")
        self.assertLess(m.start(), PAGE.index('class="lc-layout"'))
        self.assertGreater(m.start(), PAGE.index('id="stages-heading"'))

    def test_wheel_is_described_by_the_instruction(self):
        self.assertRegex(PAGE, r'<svg class="lc-wheel"[^>]*aria-describedby="lc-instruction"')

    def test_segments_are_buttons_with_selected_state_and_mark(self):
        for needle in ('setAttribute("role", "button")', 'setAttribute("tabindex", "0")',
                       'setAttribute("aria-current", "true")', "lc-segment-mark"):
            self.assertIn(needle, PAGE)

    def test_css_has_resting_outline_hover_focus_and_selected_mark(self):
        rest = css_rules(".lc-segment")
        self.assertIn("cursor: pointer", rest)
        self.assertIn("var(--control-border)", rest)
        self.assertIn("var(--accent)", css_rules(".lc-segment:hover"))
        self.assertIn("var(--focus)", css_rules(".lc-segment:focus-visible"))
        self.assertIn("display: none", css_rules(".lc-segment-mark"))
        self.assertIn("display: inline", css_rules('.lc-segment[aria-current="true"] + .lc-segment-label + .lc-segment-mark'))

    def test_segment_motion_respects_reduced_motion(self):
        m = re.search(r"@media \(prefers-reduced-motion: reduce\)\s*\{\s*\.lc-segment\s*\{([^}]*)\}", CSS)
        self.assertIsNotNone(m)
        self.assertIn("transition: none", m.group(1))
