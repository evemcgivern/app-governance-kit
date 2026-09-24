import tempfile
import unittest
from pathlib import Path

from agk.themes import PARTS, ThemesError, load_themes

KNOWN = {"XW-001", "XW-002"}


def block(rid: str, title: str = "Theme", skip: str = "") -> str:
    lines = [f"## {rid} {title}", ""]
    lines += [f"- **{label}:** text for {label.lower()}" for label in PARTS if label != skip]
    return "\n".join(lines) + "\n\n"


class ThemesTests(unittest.TestCase):
    def write(self, text: str) -> Path:
        p = Path(tempfile.mkdtemp()) / "themes.md"
        p.write_text("# Key work by theme\n\n" + text, encoding="utf-8")
        return p

    def test_loads_every_theme(self):
        themes = load_themes(self.write(block("XW-001") + block("XW-002")), KNOWN)
        self.assertEqual(themes["XW-002"]["Key work"], "text for key work")

    def test_missing_theme_fails(self):
        with self.assertRaisesRegex(ThemesError, "no description for XW-002"):
            load_themes(self.write(block("XW-001")), KNOWN)

    def test_missing_part_fails(self):
        with self.assertRaisesRegex(ThemesError, "XW-002: missing 'Evidence it produces'"):
            load_themes(self.write(block("XW-001") + block("XW-002", skip="Evidence it produces")), KNOWN)

    def test_unknown_row_fails(self):
        with self.assertRaisesRegex(ThemesError, "XW-099: not in the crosswalk"):
            load_themes(self.write(block("XW-001") + block("XW-002") + block("XW-099")), KNOWN)

    def test_duplicate_row_fails(self):
        with self.assertRaisesRegex(ThemesError, "XW-001: described twice"):
            load_themes(self.write(block("XW-001") + block("XW-001") + block("XW-002")), KNOWN)

    def test_crlf_accepted(self):
        text = (block("XW-001") + block("XW-002")).replace("\n", "\r\n")
        self.assertEqual(len(load_themes(self.write(text), KNOWN)), 2)
