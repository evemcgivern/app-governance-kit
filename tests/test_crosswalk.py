import tempfile
import unittest
from pathlib import Path

from agk.crosswalk import CrosswalkError, load_crosswalk
from tests.helpers import XW_HEADER, XW_ROW


class CrosswalkTests(unittest.TestCase):
    def write(self, text):
        p = Path(tempfile.mkdtemp()) / "crosswalk.csv"
        p.write_text(text, encoding="utf-8")
        return p

    def test_loads_rows_by_id(self):
        rows = load_crosswalk(self.write(XW_HEADER + XW_ROW))
        self.assertEqual(rows["XW-001"]["cobit2019"], "BAI09.01")

    def test_rejects_wrong_columns(self):
        with self.assertRaisesRegex(CrosswalkError, "columns"):
            load_crosswalk(self.write("id,theme\nXW-001,x\n"))

    def test_rejects_bad_id(self):
        with self.assertRaisesRegex(CrosswalkError, "line 2"):
            load_crosswalk(self.write(XW_HEADER + XW_ROW.replace("XW-001", "XW-1")))

    def test_rejects_duplicate_id(self):
        with self.assertRaisesRegex(CrosswalkError, "duplicate"):
            load_crosswalk(self.write(XW_HEADER + XW_ROW + XW_ROW))

    def test_rejects_row_mapping_to_no_framework(self):
        row = "XW-002,Empty,,,,,Nothing,2026-09-24\n"
        with self.assertRaisesRegex(CrosswalkError, "no framework"):
            load_crosswalk(self.write(XW_HEADER + row))

    def test_rejects_unverified_row(self):
        with self.assertRaisesRegex(CrosswalkError, "not verified"):
            load_crosswalk(self.write(XW_HEADER + XW_ROW.replace("2026-09-24", "")))
