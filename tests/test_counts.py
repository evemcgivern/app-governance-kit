import re
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLKIT = ROOT / "sam-toolkit"

ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
        "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = {20: "twenty", 30: "thirty", 40: "forty", 50: "fifty", 60: "sixty", 70: "seventy", 80: "eighty",
        90: "ninety"}


def number_word(n: int) -> str:
    if n < 20:
        return ONES[n]
    tens, ones = divmod(n, 10)
    return TENS[tens * 10] + (f"-{ONES[ones]}" if ones else "")


WORDS = {number_word(n): n for n in range(1, 100)}
WORD_RE = "|".join(sorted(WORDS, key=len, reverse=True))
# "Forty templates", "forty free templates", "Forty working files", "All forty files"
CLAIM_RE = re.compile(rf"\b(?:({WORD_RE})\s+(?:free\s+)?templates|({WORD_RE})\s+working\s+files|"
                      rf"All\s+({WORD_RE})\s+files)\b", re.I)


def toolkit_file_count() -> int:
    """Documents and CSV templates in sam-toolkit/, the guide included, examples excluded."""
    return len([f for f in TOOLKIT.iterdir() if f.is_file() and f.suffix in (".md", ".csv")])


class ToolkitCountTests(unittest.TestCase):
    PLACES = ("README.md", "sam-toolkit/guide.md", "site/sam-toolkit.html", "site/llms.txt")

    def test_count_is_computed_from_the_repo(self):
        self.assertEqual(toolkit_file_count(), 40)

    def test_every_place_gives_the_true_count(self):
        want = number_word(toolkit_file_count())
        for place in self.PLACES:
            text = (ROOT / place).read_text(encoding="utf-8")
            claims = [next(g for g in m.groups() if g).lower() for m in CLAIM_RE.finditer(text)]
            self.assertTrue(claims, f"{place} states no count")
            for claim in claims:
                self.assertEqual(claim, want, f"{place} says {claim!r}, the repo has {want}")

    def test_zip_holds_the_files_examples_and_workbooks_the_page_names(self):
        examples = len(list((TOOLKIT / "examples").glob("*.csv")))
        page = (ROOT / "site" / "sam-toolkit.html").read_text(encoding="utf-8")
        self.assertIn(f"All {number_word(toolkit_file_count())} files, {number_word(examples)} examples, "
                      "and two workbooks (ZIP)", page)
        with zipfile.ZipFile(ROOT / "site" / "downloads" / "sam-toolkit.zip") as z:
            names = z.namelist()
        self.assertEqual(len(names), toolkit_file_count() + examples + 2)
        self.assertEqual(len([n for n in names if n.endswith(".xlsx")]), 2)


if __name__ == "__main__":
    unittest.main()
