import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUIDE = (ROOT / "STYLE-GUIDE.md").read_text(encoding="utf-8") if (ROOT / "STYLE-GUIDE.md").exists() else ""
AGENTS = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
CSS = (ROOT / "site" / "style.css").read_text(encoding="utf-8")

ROOT_BLOCK = CSS[CSS.index(":root {"):CSS.index("}", CSS.index(":root {"))]
TOKENS = re.findall(r"(--[\w-]+):", ROOT_BLOCK)
CHECKED = [t for t in TOKENS if re.match(r"--(bg|surface|fg|muted|border|accent|accent-fg|focus|code-bg|chip-bg|"
                                         r"control-border|nav-(start|do|learn|explore)(-wash|-hover)?)$", t)]

SECTIONS = ["Design tokens", "Components", "Page patterns", "Accessibility rules", "Writing rules"]


class StyleGuideTests(unittest.TestCase):
    def test_guide_exists_and_has_a_contents_list(self):
        self.assertTrue(GUIDE)
        self.assertRegex(GUIDE, r"(?m)^## Contents")

    def test_every_main_palette_and_nav_token_is_listed(self):
        self.assertGreaterEqual(len(CHECKED), 20)
        for token in CHECKED:
            self.assertIn(f"`{token}`", GUIDE, token)

    def test_required_sections_are_present(self):
        for name in SECTIONS:
            self.assertRegex(GUIDE, rf"(?m)^## {name}", name)

    def test_guide_says_it_is_public_mit_and_for_people_and_agents(self):
        head = GUIDE[:1200]
        for word in ("public", "MIT", "agents"):
            self.assertIn(word, head)

    def test_accessibility_section_names_the_pinning_tests(self):
        for name in ("test_nav_color.py", "test_a11y_mobile.py"):
            self.assertIn(name, GUIDE)

    def test_guide_has_no_em_dashes_or_private_references(self):
        self.assertNotIn("—", GUIDE)

    def test_agents_file_tells_agents_to_follow_the_guide(self):
        self.assertIn("STYLE-GUIDE.md", AGENTS)
        section = AGENTS[AGENTS.index("STYLE-GUIDE.md") - 600:AGENTS.index("STYLE-GUIDE.md") + 900].lower()
        self.assertIn("before", section)
        self.assertIn("follow", section)


if __name__ == "__main__":
    unittest.main()
