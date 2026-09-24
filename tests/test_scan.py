import os
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

from agk.scan import docx_text, load_words, long_quotes, main, private_hits, scan


def make_docx(path: Path, body: str) -> None:
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("word/document.xml", f"<w:document><w:body><w:p><w:r><w:t>{body}</w:t></w:r></w:p></w:body></w:document>")
        z.writestr("docProps/core.xml", "<cp:coreProperties><dc:creator>Author</dc:creator></cp:coreProperties>")


class ScanTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def test_load_words_skips_blank_and_comments(self):
        p = self.tmp / "w.txt"
        p.write_text("# employer\nAcmeCorp\n\nProject Falcon\n")
        self.assertEqual(load_words(p), ["AcmeCorp", "Project Falcon"])

    def test_private_hits_are_case_insensitive_whole_words(self):
        self.assertEqual(private_hits("We moved acmecorp data", ["AcmeCorp"], "f"),
                         ["f:1: private term 'AcmeCorp'"])
        self.assertEqual(private_hits("AcmeCorporate", ["AcmeCorp"], "f"), [])

    def test_long_quoted_run_flagged(self):
        quote = '"' + " ".join(["word"] * 15) + '"'
        self.assertEqual(len(long_quotes(f"Text {quote}\n", "f")), 1)

    def test_short_quote_allowed(self):
        self.assertEqual(long_quotes('Call it "tolerate" or "invest".\n', "f"), [])

    def test_long_blockquote_flagged(self):
        self.assertEqual(len(long_quotes("> " + " ".join(["w"] * 15) + "\n", "f")), 1)

    def test_docx_text_includes_properties(self):
        p = self.tmp / "a.docx"
        make_docx(p, "Hello")
        text = docx_text(p)
        self.assertIn("Hello", text)
        self.assertIn("Author", text)

    def test_scan_finds_term_inside_docx(self):
        (self.tmp / "dist" / "office").mkdir(parents=True)
        make_docx(self.tmp / "dist" / "office" / "sop.docx", "Prepared for AcmeCorp")
        self.assertTrue(any("sop.docx" in h for h in scan(self.tmp, ["AcmeCorp"])))

    def test_main_fails_without_word_list(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(main(["--root", str(self.tmp)]), 2)

    def test_main_fails_when_word_list_path_missing(self):
        with mock.patch.dict(os.environ, {"AGK_PRIVATE_WORDS": str(self.tmp / "nope.txt")}):
            self.assertEqual(main(["--root", str(self.tmp)]), 2)

    def test_main_clean_repo_passes(self):
        words = self.tmp / "w.txt"
        words.write_text("AcmeCorp\n")
        (self.tmp / "methods").mkdir()
        (self.tmp / "methods" / "a.md").write_text("Clean text\n")
        with mock.patch.dict(os.environ, {"AGK_PRIVATE_WORDS": str(words)}):
            self.assertEqual(main(["--root", str(self.tmp)]), 0)

    def test_long_quote_wrapped_across_lines(self):
        # 16-word quote split over two lines should be flagged with first line number
        text = 'Say "word ' + " ".join(["word"] * 14) + '\nmore"\n'
        hits = long_quotes(text, "f")
        self.assertEqual(len(hits), 1)
        self.assertTrue(hits[0].startswith("f:1:"))

    def test_long_blockquote_wrapped_across_lines(self):
        # 16-word blockquote over three lines should be flagged once with first line number
        text = "> word " + " ".join(["word"] * 9) + "\n> " + " ".join(["word"] * 6) + "\n"
        hits = long_quotes(text, "f")
        self.assertEqual(len(hits), 1)
        self.assertTrue(hits[0].startswith("f:1:"))

    def test_multiple_short_quotes_in_separate_paragraphs(self):
        # Two separate paragraphs with short quotes should not be flagged
        text = 'First: "short" quote.\n\nSecond: "also short" text.\n'
        hits = long_quotes(text, "f")
        self.assertEqual(len(hits), 0)

    def test_scan_flags_pdf_as_unreadable(self):
        # A PDF file should produce a "cannot scan" hit
        (self.tmp / "dist").mkdir()
        (self.tmp / "dist" / "report.pdf").write_bytes(b"%PDF-1.4")
        hits = scan(self.tmp, ["dummy"])
        self.assertTrue(any("report.pdf" in h and "cannot scan" in h for h in hits))

    def test_scan_allows_png_image(self):
        # A PNG file should not produce any errors
        (self.tmp / "site").mkdir()
        (self.tmp / "site" / "logo.png").write_bytes(b"\x89PNG\r\n\x1a\n")
        hits = scan(self.tmp, ["dummy"])
        self.assertFalse(any("logo.png" in h for h in hits))

    def test_identical_quoted_lines_each_reported_at_own_line(self):
        # Two identical lines in a paragraph, each with a 16-word quote
        # should produce exactly two hits at line 1 and line 2
        quote_line = '"' + " ".join(["word"] * 16) + '"'
        text = f"{quote_line}\n{quote_line}\n"
        hits = long_quotes(text, "f")
        self.assertEqual(len(hits), 2)
        self.assertTrue(hits[0].startswith("f:1:"))
        self.assertTrue(hits[1].startswith("f:2:"))

    def test_quote_wrapping_across_lines_reported_at_start_line(self):
        # 16-word quote starting on line 2 and wrapping to line 3
        # should be reported at line 2
        text = "First line of text\n"
        text += '"word ' + " ".join(["word"] * 14) + '\n'
        text += 'more words end"\n'
        hits = long_quotes(text, "f")
        self.assertEqual(len(hits), 1)
        self.assertTrue(hits[0].startswith("f:2:"))
