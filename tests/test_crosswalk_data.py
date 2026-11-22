import unittest
from pathlib import Path

from agk.crosswalk import load_crosswalk
from agk.lifecycle_impact import load_lifecycle_impact

ROOT = Path(__file__).resolve().parent.parent
CROSSWALK = ROOT / "methods" / "crosswalk"


class CrosswalkDataTests(unittest.TestCase):
    def setUp(self):
        self.rows = load_crosswalk(CROSSWALK / "crosswalk.csv")

    def impact(self):
        return load_lifecycle_impact(CROSSWALK / "lifecycle-impact.csv", set(self.rows))

    def test_has_thirty_two_rows(self):
        self.assertEqual(len(self.rows), 32)
        self.assertEqual(list(self.rows), [f"XW-{n:03d}" for n in range(1, 33)])

    def test_resources_and_competence_row(self):
        row = self.rows["XW-031"]
        self.assertEqual(row["theme"], "Resources and competence")
        self.assertEqual(row["iso19770_1"], "7.1, 7.2")

    def test_objectives_row(self):
        row = self.rows["XW-032"]
        self.assertEqual(row["theme"], "Objectives and statement of applicability")
        self.assertEqual(row["iso19770_1"], "6.2, 6.2.2, 6.2.3")

    def test_new_rows_impact(self):
        impact = self.impact()
        self.assertEqual(impact["XW-031"], {"primary": ["plan"], "secondary": ["optimize"]})
        self.assertEqual(impact["XW-032"], {"primary": ["plan"], "secondary": ["optimize"]})

    def test_impact_has_a_row_for_every_crosswalk_id(self):
        self.assertEqual(set(self.impact()), set(self.rows))

    def test_four_impact_changes(self):
        impact = self.impact()
        self.assertIn("operate", impact["XW-020"]["primary"])
        self.assertNotIn("operate", impact["XW-020"]["secondary"])
        self.assertIn("plan", impact["XW-025"]["secondary"])
        self.assertIn("operate", impact["XW-004"]["secondary"])
        self.assertIn("acquire", impact["XW-021"]["secondary"])


if __name__ == "__main__":
    unittest.main()
