import csv
import io
import tempfile
import unittest
import zipfile
from pathlib import Path

from agk.build import build
from agk.downloads import (DownloadsError, cert_comparison_csv, cert_comparison_print_html,
                            cert_task_matrix_csv, cert_task_matrix_print_html, crosswalk_print_html,
                            csv_to_html_table, extract_md_table, generate_lifecycle_wheel_svg,
                            lifecycle_impact_print_html, lifecycle_wheel_print_html, print_page_html,
                            write_downloads)
from tests.helpers import make_method, make_repo

ALL_DOWNLOAD_FILES = (
    "crosswalk.csv", "lifecycle-impact.csv", "cert-comparison.csv", "cert-task-matrix.csv",
    "lifecycle-wheel.svg", "crosswalk-print.html", "lifecycle-impact-print.html",
    "cert-comparison-print.html", "cert-task-matrix-print.html", "lifecycle-wheel-print.html",
)

ROOT = Path(__file__).resolve().parent.parent


def rows(csv_text):
    return list(csv.reader(io.StringIO(csv_text)))


CERT_MD = """# Field guide

## Cross-certification task matrix

| On-the-job task | [CAMP](#camp) | [CSAM](#csam) |
|---|---|---|
| Stand up program governance | ✓ | |
| Govern the release itself | | ✓* |

## Certification comparison

| Certification | Governing body | Best for |
|---|---|---|
| CAMP | IAITAM | Newcomers |
| CSAM | IAITAM | Software-heavy work |
"""

LIFECYCLE_HTML = "<html><body><div class=\"lc-wheel-wrap\"></div></body></html>"


class MarkdownTableExtractionTests(unittest.TestCase):
    def test_extracts_header_and_data_rows(self):
        table = extract_md_table(CERT_MD, "Certification comparison")
        self.assertEqual(table, [
            ["Certification", "Governing body", "Best for"],
            ["CAMP", "IAITAM", "Newcomers"],
            ["CSAM", "IAITAM", "Software-heavy work"],
        ])

    def test_missing_heading_raises(self):
        with self.assertRaises(DownloadsError):
            extract_md_table(CERT_MD, "Nonexistent section")

    def test_checkmark_and_link_syntax_cleaned(self):
        table = extract_md_table(CERT_MD, "Cross-certification task matrix")
        self.assertEqual(table[0], ["On-the-job task", "CAMP", "CSAM"])
        self.assertEqual(table[1], ["Stand up program governance", "yes", ""])
        self.assertEqual(table[2], ["Govern the release itself", "", "yes*"])


class CsvGenerationTests(unittest.TestCase):
    def test_cert_comparison_csv_row_count(self):
        r = rows(cert_comparison_csv(CERT_MD))
        self.assertEqual(len(r), 3)  # header + 2 data rows
        self.assertEqual(r[0], ["Certification", "Governing body", "Best for"])

    def test_cert_task_matrix_csv_row_count(self):
        r = rows(cert_task_matrix_csv(CERT_MD))
        self.assertEqual(len(r), 3)  # header + 2 data rows


class WheelSvgGenerationTests(unittest.TestCase):
    def test_generates_well_formed_standalone_svg(self):
        svg = generate_lifecycle_wheel_svg()
        self.assertTrue(svg.startswith('<?xml version="1.0" encoding="UTF-8"?>\n'))
        self.assertIn('class="lc-wheel"', svg)
        self.assertIn('xmlns="http://www.w3.org/2000/svg"', svg)
        self.assertTrue(svg.rstrip().endswith("</svg>"))

    def test_has_all_six_stage_segments_and_labels(self):
        svg = generate_lifecycle_wheel_svg()
        self.assertEqual(svg.count('class="lc-segment"'), 6)
        for label in ("Plan", "Acquire", "Deploy", "Operate", "Review", "Retire"):
            self.assertIn(label, svg)

    def test_has_hub_label_and_handoff_arrows(self):
        svg = generate_lifecycle_wheel_svg()
        self.assertIn(">Lifecycle<", svg)
        self.assertEqual(svg.count('class="lc-arrow-arc"'), 3)
        self.assertIn("closes the loop", svg)
        self.assertIn("retire branch", svg)
        self.assertIn("reinvest or replace", svg)

    def test_no_inline_event_handlers_or_ids_needing_script(self):
        svg = generate_lifecycle_wheel_svg()
        self.assertNotIn("onclick", svg)
        self.assertNotIn("<script", svg)


class PrintPageTests(unittest.TestCase):
    def test_csv_to_html_table_has_header_and_data_rows(self):
        table = csv_to_html_table("a,b\n1,2\n3,4\n", "Caption text")
        self.assertEqual(table.count("<table>"), 1)
        self.assertIn("<caption>Caption text</caption>", table)
        self.assertEqual(table.count("<tr>"), 3)  # 1 header + 2 data rows
        self.assertIn("<th>a</th>", table)
        self.assertIn("<td>1</td>", table)

    def test_print_page_has_no_nav_and_exactly_one_table(self):
        page = print_page_html("A title", "<table><tr><td>x</td></tr></table>")
        self.assertIn("<title>A title</title>", page)
        self.assertIn('href="../style.css"', page)
        self.assertNotIn("<nav", page)
        self.assertNotIn("site-header", page)
        self.assertEqual(page.count("<table>"), 1)

    def test_cert_comparison_print_html_contains_one_table(self):
        page = cert_comparison_print_html(cert_comparison_csv(CERT_MD))
        self.assertEqual(page.count("<table>"), 1)
        self.assertNotIn("<nav", page)

    def test_cert_task_matrix_print_html_contains_one_table(self):
        page = cert_task_matrix_print_html(cert_task_matrix_csv(CERT_MD))
        self.assertEqual(page.count("<table>"), 1)
        self.assertNotIn("<nav", page)

    def test_crosswalk_print_html_contains_one_table(self):
        page = crosswalk_print_html("id,theme\nXW-001,Inventory\n")
        self.assertEqual(page.count("<table>"), 1)
        self.assertIn("<td>XW-001</td>", page)
        self.assertNotIn("<nav", page)

    def test_lifecycle_impact_print_html_contains_one_table(self):
        page = lifecycle_impact_print_html("xw_id,primary_stages,secondary_stages\nXW-001,deploy,retire\n")
        self.assertEqual(page.count("<table>"), 1)
        self.assertNotIn("<nav", page)

    def test_lifecycle_wheel_print_html_contains_one_svg_and_no_nav(self):
        page = lifecycle_wheel_print_html(generate_lifecycle_wheel_svg())
        self.assertEqual(page.count("<svg"), 1)
        self.assertIn('class="lc-wheel"', page)
        self.assertNotIn("<nav", page)
        self.assertNotIn("site-header", page)


class WriteDownloadsTests(unittest.TestCase):
    def setUp(self):
        self.root = make_repo(Path(tempfile.mkdtemp()))
        (self.root / "site").mkdir()
        (self.root / "site" / "lifecycle.html").write_text(LIFECYCLE_HTML, encoding="utf-8")
        (self.root / "field-guide").mkdir()
        (self.root / "field-guide" / "certifications.md").write_text(CERT_MD, encoding="utf-8")

    def test_writes_all_ten_files_plus_zip(self):
        warnings = write_downloads(self.root)
        self.assertEqual(warnings, [])
        out = self.root / "site" / "downloads"
        for name in ALL_DOWNLOAD_FILES:
            self.assertTrue((out / name).is_file(), name)
        self.assertTrue((out / "all-visuals.zip").is_file())

    def test_zip_bundle_contains_every_download_file(self):
        write_downloads(self.root)
        out = self.root / "site" / "downloads"
        with zipfile.ZipFile(out / "all-visuals.zip") as z:
            names = set(z.namelist())
        self.assertEqual(names, set(ALL_DOWNLOAD_FILES))
        # and each entry's bytes match the standalone file written alongside it
        with zipfile.ZipFile(out / "all-visuals.zip") as z:
            for name in ALL_DOWNLOAD_FILES:
                self.assertEqual(z.read(name), (out / name).read_bytes(), name)

    def test_crosswalk_and_impact_copies_match_source(self):
        write_downloads(self.root)
        out = self.root / "site" / "downloads"
        self.assertEqual((out / "crosswalk.csv").read_text(),
                          (self.root / "methods/crosswalk/crosswalk.csv").read_text())
        self.assertEqual((out / "lifecycle-impact.csv").read_text(),
                          (self.root / "methods/crosswalk/lifecycle-impact.csv").read_text())

    def test_zip_bytes_are_reproducible_across_rebuilds(self):
        write_downloads(self.root)
        out = self.root / "site" / "downloads"
        first = (out / "all-visuals.zip").read_bytes()
        (out / "all-visuals.zip").unlink()
        write_downloads(self.root)
        second = (out / "all-visuals.zip").read_bytes()
        self.assertEqual(first, second)

    def test_no_site_dir_is_a_noop(self):
        root = make_repo(Path(tempfile.mkdtemp()))
        self.assertEqual(write_downloads(root), [])
        self.assertFalse((root / "site").exists())

    def test_missing_certifications_md_warns_but_does_not_crash(self):
        (self.root / "field-guide" / "certifications.md").unlink()
        warnings = write_downloads(self.root)
        self.assertEqual(warnings, [])
        self.assertFalse((self.root / "site" / "downloads" / "cert-comparison.csv").exists())

    def test_wheel_svg_written_even_without_lifecycle_html(self):
        # generate_lifecycle_wheel_svg() is a pure data-driven render, not an
        # extraction from lifecycle.html, so it has no file dependency to fail.
        (self.root / "site" / "lifecycle.html").unlink()
        warnings = write_downloads(self.root)
        self.assertEqual(warnings, [])
        self.assertTrue((self.root / "site" / "downloads" / "lifecycle-wheel.svg").is_file())


class BuildIntegrationTests(unittest.TestCase):
    def test_build_generates_downloads_and_keeps_existing_tests_green(self):
        root = make_repo(Path(tempfile.mkdtemp()))
        make_method(root, "rationalization")
        (root / "site").mkdir()
        (root / "site" / "lifecycle.html").write_text(LIFECYCLE_HTML, encoding="utf-8")
        errors, _ = build(root)
        self.assertEqual(errors, [])
        self.assertTrue((root / "site" / "downloads" / "lifecycle-wheel.svg").is_file())
        self.assertTrue((root / "site" / "downloads" / "crosswalk.csv").is_file())


class RealRepoTests(unittest.TestCase):
    """Verify the actual repo's downloads regenerate with the counts the site pages advertise."""

    @classmethod
    def setUpClass(cls):
        cls.out = Path(tempfile.mkdtemp())
        cls.warnings = write_downloads_into_copy(cls.out)

    def test_no_warnings_against_real_repo(self):
        self.assertEqual(self.warnings, [])

    def test_cert_comparison_has_six_data_rows(self):
        r = rows((self.out / "site" / "downloads" / "cert-comparison.csv").read_text())
        self.assertEqual(len(r), 7)  # header + 6 certifications
        self.assertEqual(r[0], ["Certification", "Governing body", "Best for", "Typical domains", "Pros", "Cons"])

    def test_cert_task_matrix_has_nine_data_rows(self):
        r = rows((self.out / "site" / "downloads" / "cert-task-matrix.csv").read_text())
        self.assertEqual(len(r), 10)  # header + 9 tasks
        self.assertEqual(r[0][1:], ["CAMP", "CSAM", "CHAMP", "AIGP", "ITIL 4 Foundation", "IAM Certificate"])

    def test_crosswalk_and_impact_copies_have_28_data_rows(self):
        for name in ("crosswalk.csv", "lifecycle-impact.csv"):
            r = rows((self.out / "site" / "downloads" / name).read_text())
            self.assertEqual(len(r) - 1, 28, name)

    def test_wheel_svg_is_well_formed_with_all_segments(self):
        text = (self.out / "site" / "downloads" / "lifecycle-wheel.svg").read_text()
        self.assertTrue(text.startswith('<?xml version="1.0" encoding="UTF-8"?>'))
        self.assertIn("<svg", text)
        self.assertTrue(text.rstrip().endswith("</svg>"))
        self.assertEqual(text.count('class="lc-segment"'), 6)

    def test_all_print_pages_exist_with_no_nav(self):
        out = self.out / "site" / "downloads"
        for name in ("crosswalk-print.html", "lifecycle-impact-print.html", "cert-comparison-print.html",
                     "cert-task-matrix-print.html", "lifecycle-wheel-print.html"):
            text = (out / name).read_text()
            self.assertNotIn("<nav", text, name)
            self.assertNotIn("site-header", text, name)

    def test_zip_bundle_exists_with_all_ten_files(self):
        with zipfile.ZipFile(self.out / "site" / "downloads" / "all-visuals.zip") as z:
            self.assertEqual(set(z.namelist()), set(ALL_DOWNLOAD_FILES))


def write_downloads_into_copy(out: Path) -> list:
    """Point write_downloads at the real repo's actual sources by mirroring them into a
    scratch root, so this test reads the same field-guide/site content the real build does."""
    import shutil
    (out / "methods" / "crosswalk").mkdir(parents=True)
    shutil.copyfile(ROOT / "methods/crosswalk/crosswalk.csv", out / "methods/crosswalk/crosswalk.csv")
    shutil.copyfile(ROOT / "methods/crosswalk/lifecycle-impact.csv", out / "methods/crosswalk/lifecycle-impact.csv")
    (out / "field-guide").mkdir()
    shutil.copyfile(ROOT / "field-guide/certifications.md", out / "field-guide/certifications.md")
    (out / "site").mkdir()
    shutil.copyfile(ROOT / "site/lifecycle.html", out / "site/lifecycle.html")
    return write_downloads(out)


if __name__ == "__main__":
    unittest.main()
