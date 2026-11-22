import io
import re
import unittest
import zipfile
from xml.dom import minidom

from agk.workbook import (DIMENSIONS, FIRST, LAST, N, example_data, workbook_bytes)

SHEETS = ["Start", "Assess", "Plan", "Measures", "Scorecard", "Re-score", "Ideas"]


def parts(data: bytes) -> dict[str, str]:
    z = zipfile.ZipFile(io.BytesIO(data))
    return {n: z.read(n).decode("utf-8") for n in z.namelist()}


class WorkbookTests(unittest.TestCase):
    def test_output_is_deterministic(self):
        self.assertEqual(workbook_bytes(False), workbook_bytes(False))
        self.assertEqual(workbook_bytes(True), workbook_bytes(True))

    def test_every_part_is_well_formed_xml(self):
        for example in (False, True):
            for name, text in parts(workbook_bytes(example)).items():
                minidom.parseString(text.encode("utf-8"))

    def test_sheets_are_in_the_designed_order(self):
        wb = parts(workbook_bytes(False))["xl/workbook.xml"]
        names = re.findall(r'<sheet name="([^"]+)"', wb)
        self.assertEqual(names, SHEETS)

    def test_formulas_only_refer_to_existing_sheets(self):
        for name, text in parts(workbook_bytes(True)).items():
            if not name.startswith("xl/worksheets/"):
                continue
            for f in re.findall(r"<f>(.*?)</f>", text):
                for ref in re.findall(r"'?([A-Za-z][A-Za-z -]*?)'?!", f):
                    self.assertIn(ref, SHEETS, f)

    def test_no_sheet_is_locked_and_no_cells_are_merged(self):
        for name, text in parts(workbook_bytes(False)).items():
            if name.startswith("xl/worksheets/"):
                self.assertNotIn("sheetProtection", text)
                self.assertNotIn("mergeCell", text)

    def test_inputs_are_validated(self):
        sheets = {n: t for n, t in parts(workbook_bytes(False)).items() if n.startswith("xl/worksheets/")}
        joined = "".join(sheets.values())
        self.assertIn('type="whole"', joined)
        self.assertIn('type="list"', joined)
        self.assertIn("Enter 0, 1, 2, or 3", joined)

    def test_workbook_recalculates_when_opened(self):
        self.assertIn('fullCalcOnLoad="1"', parts(workbook_bytes(False))["xl/workbook.xml"])

    def test_dimensions_match_the_gap_plan_template(self):
        import csv
        from pathlib import Path
        root = Path(__file__).resolve().parent.parent
        with open(root / "sam-toolkit" / "application-management-gap-plan.csv", encoding="utf-8") as f:
            names = [r["dimension"] for r in csv.DictReader(f)]
        self.assertEqual(names, DIMENSIONS)
        self.assertEqual(len(DIMENSIONS), N)
        self.assertEqual(LAST - FIRST + 1, N)

    def test_example_gap_total_matches_the_gap_plan_example(self):
        import csv
        from pathlib import Path
        root = Path(__file__).resolve().parent.parent
        with open(root / "sam-toolkit" / "examples" / "application-management-gap-plan-example.csv",
                  encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        expected = sum(int(r["gap"]) for r in rows)
        data = example_data()
        total = sum(max(0, 2 - d[0]) for d in data["assess"])
        self.assertEqual(total, expected)
        self.assertEqual(total, 13)
        for csv_row, d in zip(rows, data["assess"]):
            self.assertEqual(int(csv_row["as_is_level_0_to_3"]), d[0])

    def test_example_funds_at_most_three_gaps(self):
        self.assertEqual(sum(1 for p in example_data()["plan"] if p[1] == "Fund now"), 3)

    def test_example_measures_keep_forecast_apart_from_achieved(self):
        statuses = [dict((c, v) for c, v, _ in m)["L"] for m in example_data()["measures"]]
        self.assertIn("forecast", statuses)
        self.assertNotIn("achieved", statuses)


if __name__ == "__main__":
    unittest.main()
