import tempfile
import unittest
from pathlib import Path

import re

from agk.journal import (JournalError, Post, STATUS_LABELS, load_posts, parse_front_matter, parse_post,
                        render_index, render_post)

ROOT = Path(__file__).resolve().parent.parent
INDEX_HTML = (ROOT / "site" / "index.html").read_text(encoding="utf-8")

DEFAULTS = {
    "title": "A post",
    "date": "2026-12-01",
    "status": "field-note",
    "summary": "One sentence.",
}


def write_post(directory: Path, name: str, **keys) -> Path:
    """Write a valid post; a keyword overrides a default, and None drops the key."""
    merged = dict(DEFAULTS)
    merged.update(keys)
    lines = ["---"] + [f"{k}: {v}" for k, v in merged.items() if v is not None] + ["---", "",
                                                                                    "First line of the body.", "",
                                                                                    "More."]
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / name
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


class PostTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_status_labels(self):
        self.assertEqual(STATUS_LABELS, {"field-note": "Field note", "essay": "Essay", "study-path": "Study path"})

    def test_parses_a_valid_post(self):
        path = write_post(self.dir, "2026-12-01-governance-without-the-groan.md",
                          title="Governance without the groan")
        post = parse_post(path)
        self.assertIsInstance(post, Post)
        self.assertEqual(post.slug, "governance-without-the-groan")
        self.assertEqual(post.title, "Governance without the groan")
        self.assertEqual(post.date, "2026-12-01")
        self.assertEqual(post.status, "field-note")
        self.assertEqual(post.summary, "One sentence.")
        self.assertIsNone(post.updated)
        self.assertIs(post.spine, False)
        self.assertTrue(post.body.startswith("First line of the body."))
        self.assertEqual(post.path, path)

    def test_front_matter_parser_returns_keys_and_body(self):
        keys, body = parse_front_matter("---\ntitle: T\ndate: 2026-12-01\n---\n\nBody here.\n")
        self.assertEqual(keys, {"title": "T", "date": "2026-12-01"})
        self.assertTrue(body.startswith("Body here."))

    def test_spine_flag_and_updated(self):
        path = write_post(self.dir, "2026-11-01-study-path.md", spine="true", updated="2026-12-15")
        post = parse_post(path)
        self.assertIs(post.spine, True)
        self.assertEqual(post.updated, "2026-12-15")

    def test_missing_key_is_an_error(self):
        for key in ("title", "date", "status", "summary"):
            with self.subTest(key=key):
                path = write_post(self.dir, f"2026-12-01-missing-{key}.md", **{key: None})
                with self.assertRaisesRegex(JournalError, rf"missing-{key}\.md.*{key}"):
                    parse_post(path)

    def test_rejects_bad_values(self):
        cases = {
            "2026-12-01-bad-date.md": {"date": "2026-13-40"},
            "2026-12-01-bad-status.md": {"status": "rant"},
            "2026-12-01-long-summary.md": {"summary": "x" * 201},
            "2026-12-01-bad-updated.md": {"updated": "yesterday"},
            "no-date-prefix.md": {},
        }
        for name, keys in cases.items():
            with self.subTest(name=name):
                path = write_post(self.dir, name, **keys)
                with self.assertRaises(JournalError):
                    parse_post(path)

    def test_summary_of_exactly_200_characters_is_allowed(self):
        path = write_post(self.dir, "2026-12-01-edge.md", summary="x" * 200)
        self.assertEqual(len(parse_post(path).summary), 200)

    def test_file_without_front_matter_is_an_error(self):
        path = self.dir / "2026-12-01-plain.md"
        path.write_text("Just text.\n", encoding="utf-8")
        with self.assertRaisesRegex(JournalError, "plain.md"):
            parse_post(path)

    def test_load_posts_sorts_by_date_then_slug(self):
        write_post(self.dir, "2026-12-01-b-post.md")
        write_post(self.dir, "2026-12-01-a-post.md")
        write_post(self.dir, "2026-12-15-c-post.md", date="2026-12-15")
        self.assertEqual([p.slug for p in load_posts(self.dir)], ["c-post", "a-post", "b-post"])

    def test_load_posts_rejects_duplicate_slugs(self):
        write_post(self.dir, "2026-12-01-same.md")
        write_post(self.dir, "2026-12-02-same.md", date="2026-12-02")
        with self.assertRaisesRegex(JournalError, "same"):
            load_posts(self.dir)

    def test_load_posts_rejects_two_spine_posts(self):
        write_post(self.dir, "2026-11-01-one.md", spine="true")
        write_post(self.dir, "2026-11-02-two.md", date="2026-11-02", spine="true")
        with self.assertRaisesRegex(JournalError, "spine"):
            load_posts(self.dir)

    def test_missing_directory_gives_no_posts(self):
        self.assertEqual(load_posts(self.dir / "nope"), [])


def make_post(slug="governance-without-the-groan", title="Governance without the groan", date="2026-12-01",
              updated=None, status="field-note", summary="One sentence.", spine=False,
              body="Hello **world**.\n\nSecond paragraph.\n") -> Post:
    return Post(slug=slug, title=title, date=date, updated=updated, status=status, summary=summary, spine=spine,
                body=body, path=Path(f"{date}-{slug}.md"))


def json_ld(html: str) -> str:
    return re.search(r'<script type="application/ld\+json">\n(.*?)\n</script>', html, re.S).group(1)


class RenderTests(unittest.TestCase):
    def test_post_page_has_the_expected_parts(self):
        html = render_post(make_post(), INDEX_HTML)
        self.assertIn("<h1>Governance without the groan</h1>", html)
        self.assertIn("Field note", html)
        self.assertIn("2026-12-01", html)
        self.assertIn("<strong>world</strong>", html)
        self.assertIn("MIT licensed, like the kit.", html)
        self.assertIn('<a href="../journal.html">&larr; Journal</a>', html)
        self.assertIn('href="https://evemcgivern.github.io/app-governance-kit/journal/governance-without-the-groan.html"',
                      html)
        ld = json_ld(html)
        self.assertIn('"@type": "BlogPosting"', ld)
        self.assertIn('"datePublished": "2026-12-01"', ld)
        self.assertIn('"dateModified": "2026-12-01"', ld)
        self.assertIn('"license": "https://opensource.org/licenses/MIT"', ld)
        self.assertNotIn("Updated", html)

    def test_updated_date_is_shown_and_used(self):
        html = render_post(make_post(updated="2026-12-15"), INDEX_HTML)
        self.assertIn("Updated 2026-12-15", html)
        self.assertIn('"dateModified": "2026-12-15"', json_ld(html))

    def test_title_and_summary_are_escaped(self):
        html = render_post(make_post(title='A <b> & "c" </script>', summary='Sum <i> & "d"'), INDEX_HTML)
        self.assertIn("<h1>A &lt;b&gt; &amp; &quot;c&quot; &lt;/script&gt;</h1>", html)
        self.assertIn('content="Sum &lt;i&gt; &amp; &quot;d&quot;"', html)
        self.assertNotIn("</", json_ld(html))

    def test_index_lists_spine_first_then_newest(self):
        posts = [make_post(slug="p-one", title="P one", date="2026-12-15"),
                 make_post(slug="p-two", title="P two", date="2026-12-01"),
                 make_post(slug="study-path", title="The study path", date="2026-11-01", status="study-path",
                           spine=True)]
        html = render_index(posts, INDEX_HTML)
        self.assertIn("Field notes on setting up asset management, as I learn it.", html)
        self.assertLess(html.index("Start here"), html.index("The study path"))
        self.assertLess(html.index("The study path"), html.index("Newest first"))
        self.assertLess(html.index("P one"), html.index("P two"))
        self.assertEqual(html.count("journal/study-path.html"), 1)  # listed once, not again under Newest first
        self.assertIn('href="journal/p-one.html"', html)

    def test_index_without_a_spine_post_has_no_start_here(self):
        html = render_index([make_post(slug="p-one", title="P one")], INDEX_HTML)
        self.assertNotIn("Start here", html)
        self.assertIn("Newest first", html)
        self.assertIn("P one", html)

    def test_preview_adds_banner_and_noindex(self):
        for render, args in ((render_post, (make_post(),)), (render_index, ([make_post()],))):
            with self.subTest(render=render.__name__):
                preview = render(*args, INDEX_HTML, preview=True)
                self.assertIn("Draft, not published", preview)
                self.assertIn('<meta name="robots" content="noindex">', preview)
                normal = render(*args, INDEX_HTML)
                self.assertNotIn("Draft, not published", normal)
                self.assertNotIn('name="robots"', normal)


if __name__ == "__main__":
    unittest.main()
