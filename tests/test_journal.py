import tempfile
import unittest
from pathlib import Path

import contextlib
import io
import os
import re
import shutil
from unittest import mock

from agk.build import build
from agk.docs import write_docs
from agk.scan import scan
from agk.site import broken_links
from agk.journal import (JournalError, Post, STATUS_LABELS, load_posts, parse_front_matter, parse_post,
                        render_index, render_post, write_journal)
from agk.journal import main as journal_main
from tests.helpers import make_method, make_repo

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
        path = write_post(self.dir, "2026-12-01-sample-post.md",
                          title="Sample post")
        post = parse_post(path)
        self.assertIsInstance(post, Post)
        self.assertEqual(post.slug, "sample-post")
        self.assertEqual(post.title, "Sample post")
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

    def test_rejects_compact_and_week_dates(self):
        for key, value in (("date", "20261201"), ("date", "2026-W49-1"), ("updated", "20261215")):
            with self.subTest(key=key, value=value):
                path = write_post(self.dir, "2026-12-01-odd-date.md", **{key: value})
                with self.assertRaisesRegex(JournalError, key):
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

    def test_load_posts_is_strict_by_default(self):
        (self.dir / "forgot-date.md").write_text("---\ntitle: T\n---\nBody\n", encoding="utf-8")
        with self.assertRaisesRegex(JournalError, "forgot-date.md"):
            load_posts(self.dir)

    def test_notes_files_are_ignored_only_when_asked(self):
        (self.dir / "IDEAS.md").write_text("Rough thoughts, no front matter.\n", encoding="utf-8")
        (self.dir / "README.md").write_text("Not a post.\n", encoding="utf-8")
        write_post(self.dir, "2026-12-01-real.md")
        self.assertEqual([p.slug for p in load_posts(self.dir, ignore_notes=True)], ["real"])
        with self.assertRaisesRegex(JournalError, "IDEAS.md"):
            load_posts(self.dir)

    def test_a_misnamed_file_that_starts_with_a_digit_is_still_an_error(self):
        write_post(self.dir, "2026-12-01 bad name.md")
        with self.assertRaisesRegex(JournalError, "bad name.md"):
            load_posts(self.dir, ignore_notes=True)

    def test_missing_directory_gives_no_posts(self):
        self.assertEqual(load_posts(self.dir / "nope"), [])


def make_post(slug="sample-post", title="Sample post", date="2026-12-01",
              updated=None, status="field-note", summary="One sentence.", spine=False,
              body="Hello **world**.\n\nSecond paragraph.\n") -> Post:
    return Post(slug=slug, title=title, date=date, updated=updated, status=status, summary=summary, spine=spine,
                body=body, path=Path(f"{date}-{slug}.md"))


def json_ld(html: str) -> str:
    return re.search(r'<script type="application/ld\+json">\n(.*?)\n</script>', html, re.S).group(1)


class RenderTests(unittest.TestCase):
    def test_post_page_has_the_expected_parts(self):
        html = render_post(make_post(), INDEX_HTML)
        self.assertIn("<h1>Sample post</h1>", html)
        self.assertIn("Field note", html)
        self.assertIn("2026-12-01", html)
        self.assertIn("<strong>world</strong>", html)
        self.assertIn("MIT licensed, like the kit.", html)
        self.assertIn('<a href="../journal.html">&larr; Journal</a>', html)
        self.assertIn('href="https://evemcgivern.github.io/app-governance-kit/journal/sample-post.html"',
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
        self.assertIn("Working notes from setting up asset management: what I try, what holds, and what doesn't.", html)
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


class WriteTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = make_repo(Path(self._tmp.name))
        make_method(self.root, "rationalization")
        (self.root / "site").mkdir()
        shutil.copyfile(ROOT / "site" / "index.html", self.root / "site" / "index.html")
        self.posts = self.root / "posts"
        self.drafts = self.root / "docs" / "journal-drafts"

    def tearDown(self):
        self._tmp.cleanup()

    def snapshot(self, folder: Path) -> dict[str, bytes]:
        return {p.relative_to(folder).as_posix(): p.read_bytes() for p in sorted(folder.rglob("*")) if p.is_file()}

    def test_no_posts_writes_nothing_and_removes_stale_output(self):
        self.assertEqual(write_journal(self.root), [])
        self.assertFalse((self.root / "site" / "journal").exists())
        self.assertFalse((self.root / "site" / "journal.html").exists())
        (self.root / "site" / "journal").mkdir()
        (self.root / "site" / "journal" / "old.html").write_text("stale", encoding="utf-8")
        (self.root / "site" / "journal.html").write_text("stale", encoding="utf-8")
        write_journal(self.root)
        self.assertFalse((self.root / "site" / "journal").exists())
        self.assertFalse((self.root / "site" / "journal.html").exists())

    def test_one_post_writes_page_and_index(self):
        write_post(self.posts, "2026-12-01-first-post.md", title="First post")
        write_journal(self.root)
        page = self.root / "site" / "journal" / "first-post.html"
        self.assertIn("<h1>First post</h1>", page.read_text(encoding="utf-8"))
        index = (self.root / "site" / "journal.html").read_text(encoding="utf-8")
        self.assertIn('href="journal/first-post.html"', index)

    def test_output_is_byte_identical_across_runs(self):
        write_post(self.posts, "2026-12-01-b-post.md", title="B post")
        write_post(self.posts, "2026-12-01-a-post.md", title="A post")
        write_journal(self.root)
        first = self.snapshot(self.root / "site")
        write_journal(self.root)
        self.assertEqual(first, self.snapshot(self.root / "site"))
        self.assertIn("journal/a-post.html", first)
        index = first["journal.html"].decode("utf-8")
        self.assertLess(index.index("A post"), index.index("B post"))

    def test_drafts_never_reach_site(self):
        write_post(self.posts, "2026-12-01-published.md", title="Published")
        write_post(self.drafts, "2026-12-02-rough.md", title="Rough", date="2026-12-02")
        write_journal(self.root)
        self.assertTrue((self.root / "site" / "journal" / "published.html").exists())
        self.assertFalse((self.root / "site" / "journal" / "rough.html").exists())
        self.assertNotIn("Rough", (self.root / "site" / "journal.html").read_text(encoding="utf-8"))
        write_journal(self.root, preview=True)
        preview = self.root / "docs" / "journal-preview"
        self.assertTrue((preview / "journal" / "rough.html").exists())
        self.assertTrue((preview / "journal" / "published.html").exists())
        self.assertIn("Draft, not published", (preview / "journal" / "rough.html").read_text(encoding="utf-8"))
        self.assertFalse((self.root / "site" / "journal" / "rough.html").exists())

    def test_a_misnamed_file_in_posts_is_an_error_not_a_silent_skip(self):
        write_post(self.posts, "forgot-date.md")
        with self.assertRaisesRegex(JournalError, "forgot-date.md"):
            write_journal(self.root)

    def test_preview_ignores_notes_in_the_drafts_folder(self):
        self.drafts.mkdir(parents=True)
        (self.drafts / "IDEAS.md").write_text("Rough thoughts.\n", encoding="utf-8")
        write_post(self.drafts, "2026-12-02-rough.md", date="2026-12-02")
        write_journal(self.root, preview=True)
        self.assertTrue((self.root / "docs" / "journal-preview" / "journal" / "rough.html").exists())

    def test_preview_rejects_a_draft_that_reuses_a_published_slug(self):
        write_post(self.posts, "2026-12-01-same.md")
        write_post(self.drafts, "2026-12-02-same.md", date="2026-12-02")
        with self.assertRaisesRegex(JournalError, "same"):
            write_journal(self.root, preview=True)

    def test_build_reports_journal_errors(self):
        write_post(self.posts, "2026-12-01-broken.md", title=None)
        errors, _ = build(self.root)
        self.assertTrue(any(e.startswith("journal:") and "title" in e for e in errors), errors)

    def test_build_writes_the_journal_when_posts_are_valid(self):
        write_post(self.posts, "2026-12-01-fine.md", title="Fine")
        errors, _ = build(self.root)
        self.assertFalse([e for e in errors if e.startswith("journal:")], errors)
        self.assertTrue((self.root / "site" / "journal" / "fine.html").exists())


class SiteChecksTests(unittest.TestCase):
    """The journal in the sitemap, the link check, and the scan."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = make_repo(Path(self._tmp.name))
        make_method(self.root, "rationalization")
        shutil.copytree(ROOT / "site", self.root / "site", ignore=shutil.ignore_patterns("downloads", "docs"))
        self.posts = self.root / "posts"

    def tearDown(self):
        self._tmp.cleanup()

    def journal_problems(self) -> list[str]:
        return [e for e in broken_links(self.root / "site") if e.startswith("journal")]

    def test_sitemap_lists_published_posts_only(self):
        write_post(self.posts, "2026-12-01-published.md")
        write_post(self.root / "docs" / "journal-drafts", "2026-12-02-rough.md", date="2026-12-02")
        write_journal(self.root)
        write_docs(self.root)
        sitemap = (self.root / "site" / "sitemap.xml").read_text(encoding="utf-8")
        base = "https://evemcgivern.github.io/app-governance-kit/"
        self.assertIn(f"<loc>{base}journal.html</loc>", sitemap)
        self.assertIn(f"<loc>{base}journal/published.html</loc>", sitemap)
        self.assertNotIn("rough", sitemap)
        self.assertLess(sitemap.index("case-studies.html"), sitemap.index("journal.html"))
        self.assertLess(sitemap.index("journal.html"), sitemap.index("about.html"))

    def test_a_good_post_has_no_link_problems(self):
        post = write_post(self.posts, "2026-12-01-good-links.md")
        post.write_text(post.read_text(encoding="utf-8") + "\n[home](../index.html) and [up](#top)\n",
                        encoding="utf-8")
        write_journal(self.root)
        self.assertEqual(self.journal_problems(), [])

    def test_broken_link_in_a_post_is_reported(self):
        post = write_post(self.posts, "2026-12-01-bad-link.md")
        post.write_text(post.read_text(encoding="utf-8") + "\n[gone](../docs/nope.html)\n", encoding="utf-8")
        write_journal(self.root)
        self.assertEqual(self.journal_problems(), ["journal/bad-link.html: ../docs/nope.html"])

    def test_a_link_that_climbs_out_of_site_is_reported(self):
        (self.root / "README.md").write_text("repo readme\n", encoding="utf-8")
        post = write_post(self.posts, "2026-12-01-climbs.md")
        post.write_text(post.read_text(encoding="utf-8") + "\n[repo](../../README.md)\n", encoding="utf-8")
        write_journal(self.root)
        self.assertEqual(self.journal_problems(), ["journal/climbs.html: ../../README.md"])

    def test_posts_folder_is_scanned(self):
        quote = "one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen"
        (self.posts).mkdir()
        (self.posts / "2026-12-01-x.md").write_text(f'Acme said "{quote}" today.\n', encoding="utf-8")
        hits = scan(self.root, ["acme"])
        self.assertTrue(any("posts/2026-12-01-x.md" in h and "private term" in h for h in hits), hits)
        self.assertTrue(any("posts/2026-12-01-x.md" in h and "quoted run" in h for h in hits), hits)


class PreviewTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = make_repo(Path(self._tmp.name))
        (self.root / "site").mkdir()
        shutil.copyfile(ROOT / "site" / "index.html", self.root / "site" / "index.html")
        self.drafts = self.root / "docs" / "journal-drafts"

    def tearDown(self):
        self._tmp.cleanup()

    def run_main(self, env: dict | None = None) -> tuple[int, str]:
        err = io.StringIO()
        clean = {k: v for k, v in os.environ.items() if k != "AGK_PRIVATE_WORDS"}
        clean.update(env or {})
        with mock.patch.dict(os.environ, clean, clear=True), contextlib.redirect_stderr(err), \
                contextlib.redirect_stdout(io.StringIO()):
            code = journal_main(["--root", str(self.root), "--preview"])
        return code, err.getvalue()

    def test_preview_with_nothing_to_show_says_so(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code = journal_main(["--root", str(self.root), "--preview"])
        self.assertEqual(code, 0)
        self.assertIn("no posts or drafts to preview", out.getvalue())
        self.assertFalse((self.root / "docs" / "journal-preview").exists())

    def test_drafts_folder_is_gitignored(self):
        lines = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
        self.assertIn("/docs/", [line.strip() for line in lines])

    def test_preview_post_links_work_inside_the_preview(self):
        draft = write_post(self.drafts, "2026-12-02-rough.md", date="2026-12-02")
        draft.write_text(draft.read_text(encoding="utf-8") + "\n[kit](../docs/x.html#top) and [here](#main)\n",
                         encoding="utf-8")
        write_journal(self.root, preview=True)
        page = (self.root / "docs" / "journal-preview" / "journal" / "rough.html").read_text(encoding="utf-8")
        site = (self.root / "site").resolve().as_uri() + "/"
        self.assertNotIn("<base", page)
        self.assertIn('href="../journal.html"', page)  # the Journal link stays inside the preview
        self.assertIn(f'href="{site}tools.html"', page)  # the site menu points at the real site
        self.assertIn(f'href="{site}style.css"', page)
        self.assertIn(f'href="{site}docs/x.html#top"', page)  # a kit link keeps its fragment
        self.assertIn('href="#main"', page)  # a fragment link stays on the page

    def test_preview_index_links_work_inside_the_preview(self):
        write_post(self.drafts, "2026-12-02-rough.md", date="2026-12-02")
        write_journal(self.root, preview=True)
        page = (self.root / "docs" / "journal-preview" / "journal.html").read_text(encoding="utf-8")
        site = (self.root / "site").resolve().as_uri() + "/"
        self.assertNotIn("<base", page)
        self.assertIn('href="journal/rough.html"', page)
        self.assertIn(f'href="{site}style.css"', page)
        self.assertIn(f'href="{site}index.html"', page)

    def test_normal_pages_are_not_rewritten(self):
        write_post(self.root / "posts", "2026-12-01-live.md")
        write_journal(self.root)
        page = (self.root / "site" / "journal" / "live.html").read_text(encoding="utf-8")
        self.assertNotIn("file://", page)
        self.assertNotIn("<base", page)
        self.assertIn('href="../style.css"', page)

    def test_preview_main_flags_private_terms_in_drafts(self):
        words = self.root / "words.txt"
        words.write_text("# private\nacme\n", encoding="utf-8")
        draft = write_post(self.drafts, "2026-12-02-rough.md", date="2026-12-02")
        code, err = self.run_main({"AGK_PRIVATE_WORDS": str(words)})
        self.assertEqual(code, 0, err)
        draft.write_text(draft.read_text(encoding="utf-8") + "\nAcme did it.\n", encoding="utf-8")
        code, err = self.run_main({"AGK_PRIVATE_WORDS": str(words)})
        self.assertEqual(code, 1)
        self.assertIn("2026-12-02-rough.md", err)
        self.assertIn("private term", err)

    def test_preview_main_without_a_word_list_warns_but_still_builds_and_checks_quotes(self):
        draft = write_post(self.drafts, "2026-12-02-rough.md", date="2026-12-02")
        code, err = self.run_main()
        self.assertEqual(code, 0, err)
        self.assertIn("private-term scan skipped", err)
        self.assertTrue((self.root / "docs" / "journal-preview" / "journal" / "rough.html").exists())
        quote = "one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen"
        draft.write_text(draft.read_text(encoding="utf-8") + f'\nShe said "{quote}".\n', encoding="utf-8")
        code, err = self.run_main()
        self.assertEqual(code, 1)
        self.assertIn("quoted run", err)


if __name__ == "__main__":
    unittest.main()
