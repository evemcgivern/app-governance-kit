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
