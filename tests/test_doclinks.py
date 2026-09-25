import tempfile
import unittest
from pathlib import Path

from agk.doclinks import broken_doc_links


class DocLinksTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.methods = self.root / "methods"

    def _write(self, tool: str, name: str, text: str) -> None:
        d = self.methods / tool
        d.mkdir(parents=True, exist_ok=True)
        (d / name).write_text(text, encoding="utf-8")

    def test_good_relative_link_passes(self):
        self._write("crosswalk", "method.md", "See [sop.md](sop.md).\n")
        self._write("crosswalk", "sop.md", "SOP\n")
        self.assertEqual(broken_doc_links(self.methods), [])

    def test_broken_relative_link_reported(self):
        self._write("crosswalk", "method.md", "See [nope.md](nope.md).\n")
        self.assertEqual(broken_doc_links(self.methods), ["crosswalk/method.md: nope.md"])

    def test_http_and_anchor_links_ignored(self):
        self._write(
            "crosswalk", "method.md",
            "See [ext](https://example.com/x), [top](#top), and [mail](mailto:a@b.com).\n",
        )
        self.assertEqual(broken_doc_links(self.methods), [])

    def test_example_folder_skipped(self):
        d = self.methods / "crosswalk" / "example"
        d.mkdir(parents=True)
        (d / "output.md").write_text("[nope.md](nope.md)\n", encoding="utf-8")
        self.assertEqual(broken_doc_links(self.methods), [])

    def test_fragment_stripped_before_checking(self):
        self._write("crosswalk", "method.md", "[sop.md](sop.md#steps)\n")
        self._write("crosswalk", "sop.md", "SOP\n")
        self.assertEqual(broken_doc_links(self.methods), [])

    def test_folder_link_to_another_tool_resolves(self):
        (self.methods / "rationalization").mkdir(parents=True)
        self._write(
            "crosswalk", "sop.md",
            "- [Application rationalization](../rationalization/)\n",
        )
        self.assertEqual(broken_doc_links(self.methods), [])


if __name__ == "__main__":
    unittest.main()
