import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
CSS = (SITE / "style.css").read_text(encoding="utf-8")

GROUPS = ["start", "do", "learn", "explore"]
SUFFIXES = ["", "-wash", "-hover"]


def block(opener: str) -> str:
    """Return the declarations of the first rule that starts with opener."""
    start = CSS.index(opener) + len(opener)
    return CSS[start:CSS.index("}", start)]


def tokens(body: str) -> dict:
    return dict(re.findall(r"(--[\w-]+):\s*([^;]+);", body))


THEMES = {
    "light": tokens(block(":root {")),
    "dark (system)": tokens(block(':root:not([data-theme="light"]) {')),
    "dark (switch)": tokens(block(':root[data-theme="dark"] {')),
}


def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    channels = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a: str, b: str) -> float:
    hi, lo = sorted([luminance(a), luminance(b)], reverse=True)
    return (hi + 0.05) / (lo + 0.05)


class NavGroupTokenTests(unittest.TestCase):
    def test_every_theme_defines_label_wash_and_hover_tokens_for_all_groups(self):
        for theme, toks in THEMES.items():
            for g in GROUPS:
                for s in SUFFIXES:
                    name = f"--nav-{g}{s}"
                    self.assertRegex(toks.get(name, ""), r"^#[0-9a-f]{6}$", f"{theme}: {name}")

    def test_dark_themes_use_the_same_values(self):
        for g in GROUPS:
            for s in SUFFIXES:
                name = f"--nav-{g}{s}"
                self.assertEqual(THEMES["dark (system)"][name], THEMES["dark (switch)"][name], name)

    def test_light_and_dark_values_differ(self):
        for g in GROUPS:
            self.assertNotEqual(THEMES["light"][f"--nav-{g}-wash"], THEMES["dark (switch)"][f"--nav-{g}-wash"])

    def test_text_meets_aa_on_every_tint(self):
        for theme, toks in THEMES.items():
            toks = {**THEMES["light"], **toks}
            for g in GROUPS:
                for tint in ("-wash", "-hover"):
                    bg = toks[f"--nav-{g}{tint}"]
                    for text in (toks[f"--nav-{g}"], toks["--fg"], toks["--muted"], toks["--focus"]):
                        self.assertGreaterEqual(contrast(text, bg), 4.5, f"{theme} {g}{tint} {text} on {bg}")

    def test_rail_meets_non_text_contrast_against_the_header(self):
        for theme, toks in THEMES.items():
            toks = {**THEMES["light"], **toks}
            for g in GROUPS:
                self.assertGreaterEqual(contrast(toks[f"--nav-{g}"], toks["--surface"]), 3.0, f"{theme} {g}")

    def test_groups_are_told_apart_by_more_than_label_color(self):
        # Each tint pair must differ in lightness or hue enough to be visible: no two washes equal.
        for theme, toks in THEMES.items():
            toks = {**THEMES["light"], **toks}
            washes = [toks[f"--nav-{g}-wash"] for g in GROUPS]
            self.assertEqual(len(set(washes)), 4, theme)


class NavGroupRuleTests(unittest.TestCase):
    def test_css_targets_each_group_by_its_label_id(self):
        for g in GROUPS:
            self.assertIn(f"#nav-group-{g}", CSS)
            self.assertIn(f"var(--nav-{g})", CSS)
            self.assertIn(f"var(--nav-{g}-wash)", CSS)
            self.assertIn(f"var(--nav-{g}-hover)", CSS)

    def test_group_rules_do_not_clip_tooltips(self):
        rule = block(".nav-group {")
        self.assertNotIn("overflow", rule)

    def test_current_page_link_keeps_its_own_state(self):
        self.assertIn(".nav-group a:not([aria-current]):hover", CSS)


class NavMarkupUnchangedTests(unittest.TestCase):
    def test_nav_markup_has_no_color_classes_or_inline_styles(self):
        for page in SITE.glob("*.html"):
            nav = re.search(r'<nav class="site-nav".*?</nav>', page.read_text(encoding="utf-8"), re.S).group(0)
            self.assertNotIn("style=", nav, page.name)
            self.assertEqual(nav.count('<div class="nav-group">'), 4, page.name)
            for g in GROUPS:
                self.assertIn(f'id="nav-group-{g}"', nav, page.name)


if __name__ == "__main__":
    unittest.main()
