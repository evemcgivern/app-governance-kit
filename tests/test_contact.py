import re
import unittest
from pathlib import Path

from agk.scan import email_hits

ROOT = Path(__file__).resolve().parent.parent
FOOTER_LINK_RE = re.compile(
    r'<a href="https://github\.com/evemcgivern/app-governance-kit/issues" id="contact-email" '
    r'data-r="([^"]+)">email me</a>')
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}$")


def site_pages():
    return sorted(p for p in (ROOT / "site").rglob("*.html") if "site-footer" in p.read_text(encoding="utf-8"))


class ContactTests(unittest.TestCase):
    """The owner's address must never appear in a form a spam harvester can read."""

    def test_no_plain_or_spelled_out_address_in_public_files(self):
        files = [p for p in (ROOT / "site").rglob("*") if p.is_file() and p.suffix in (".html", ".txt", ".xml", ".json", ".js", ".css")]
        files += [ROOT / n for n in ("README.md", "SECURITY.md", "CODE_OF_CONDUCT.md")]
        hits = []
        for f in files:
            hits += email_hits(f.read_text(encoding="utf-8", errors="replace"), str(f.relative_to(ROOT)))
        self.assertEqual(hits, [])

    def test_every_footer_uses_reversed_address_and_no_mailto(self):
        pages = site_pages()
        self.assertGreater(len(pages), 10)
        for page in pages:
            with self.subTest(page=str(page.relative_to(ROOT))):
                html = page.read_text(encoding="utf-8")
                links = FOOTER_LINK_RE.findall(html)
                self.assertEqual(len(links), 1)
                self.assertRegex(links[0][::-1].replace("|", "@"), EMAIL_RE)
                self.assertNotIn("@", links[0])
                self.assertNotIn('href="mailto:', html)
                self.assertIsNone(re.search(r"mailto:[A-Za-z0-9]", html))
                self.assertNotIn("<noscript><p>Email", html)
                self.assertIn('"pointerenter", "focus", "touchstart"', html)


if __name__ == "__main__":
    unittest.main()
