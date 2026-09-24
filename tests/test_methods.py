import tempfile
import unittest
from pathlib import Path

from agk.methods import MethodError, load_method, method_dirs, parse_frontmatter
from tests.helpers import make_method


class FrontmatterTests(unittest.TestCase):
    def test_parses_keys_and_body(self):
        meta, body = parse_frontmatter("---\nname: x\ntitle: X\n---\nBody\n")
        self.assertEqual(meta, {"name": "x", "title": "X"})
        self.assertEqual(body, "Body\n")

    def test_accepts_crlf_and_bom(self):
        meta, body = parse_frontmatter("﻿---\r\nname: x\r\n---\r\nBody\r\n")
        self.assertEqual(meta["name"], "x")
        self.assertEqual(body, "Body\n")

    def test_rejects_missing_frontmatter(self):
        with self.assertRaises(MethodError):
            parse_frontmatter("Body only\n")

    def test_rejects_unterminated_frontmatter(self):
        with self.assertRaises(MethodError):
            parse_frontmatter("---\nname: x\nBody\n")


class LoadMethodTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def test_loads_complete_method(self):
        m = load_method(make_method(self.tmp, "rationalization"))
        self.assertEqual(m.name, "rationalization")
        self.assertEqual(m.template.name, "template.md")

    def test_names_every_missing_piece(self):
        d = make_method(self.tmp, "x", **{"sop.md": None, "copilot-test.md": None})
        with self.assertRaises(MethodError) as ctx:
            load_method(d)
        self.assertIn("sop.md", str(ctx.exception))
        self.assertIn("copilot-test.md", str(ctx.exception))

    def test_requires_a_template(self):
        d = make_method(self.tmp, "x", **{"template.md": None})
        with self.assertRaisesRegex(MethodError, "template"):
            load_method(d)

    def test_accepts_csv_template(self):
        d = make_method(self.tmp, "x", **{"template.md": None, "template.csv": "a,b\n"})
        self.assertEqual(load_method(d).template.name, "template.csv")

    def test_rejects_two_templates(self):
        d = make_method(self.tmp, "x", **{"template.csv": "a,b\n"})
        with self.assertRaisesRegex(MethodError, "one template"):
            load_method(d)

    def test_requires_nonempty_example(self):
        d = make_method(self.tmp, "x", **{"example/input.md": None})
        (d / "example").mkdir(exist_ok=True)
        with self.assertRaisesRegex(MethodError, "example"):
            load_method(d)

    def test_name_must_match_folder(self):
        d = make_method(self.tmp, "x", **{"method.md": "---\nname: y\ntitle: Y\ndescription: d\n---\nB\n"})
        with self.assertRaisesRegex(MethodError, "match folder"):
            load_method(d)

    def test_requires_description(self):
        d = make_method(self.tmp, "x", **{"method.md": "---\nname: x\ntitle: X\n---\nB\n"})
        with self.assertRaisesRegex(MethodError, "description"):
            load_method(d)

    def test_method_dirs_skips_hidden_and_underscored(self):
        make_method(self.tmp, "b")
        make_method(self.tmp, "a")
        (self.tmp / "methods" / "_drafts").mkdir()
        (self.tmp / "methods" / ".git").mkdir()
        self.assertEqual([p.name for p in method_dirs(self.tmp / "methods")], ["a", "b"])


if __name__ == "__main__":
    unittest.main()
