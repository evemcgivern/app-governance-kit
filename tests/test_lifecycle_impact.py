import tempfile
import unittest
from pathlib import Path

from agk.lifecycle_impact import LifecycleImpactError, load_lifecycle_impact

HEADER = "xw_id,primary_stages,secondary_stages\n"
XW = {"XW-001", "XW-002"}


def two_rows():
    return (HEADER
            + 'XW-001,"acquire;deploy;operate","plan;optimize;retire"\n'
            + 'XW-002,"plan;optimize","acquire;deploy;operate;retire"\n')


class LifecycleImpactTests(unittest.TestCase):
    def write(self, text):
        p = Path(tempfile.mkdtemp()) / "lifecycle-impact.csv"
        p.write_text(text, encoding="utf-8")
        return p

    def test_loads_a_valid_file(self):
        impact = load_lifecycle_impact(self.write(two_rows()), XW)
        self.assertEqual(impact["XW-001"]["primary"], ["acquire", "deploy", "operate"])
        self.assertEqual(impact["XW-001"]["secondary"], ["plan", "optimize", "retire"])
        self.assertEqual(impact["XW-002"]["primary"], ["plan", "optimize"])
        self.assertEqual(impact["XW-002"]["secondary"], ["acquire", "deploy", "operate", "retire"])

    def test_rejects_missing_xw_row(self):
        only_one = HEADER + 'XW-001,"acquire;deploy;operate","plan;optimize;retire"\n'
        with self.assertRaisesRegex(LifecycleImpactError, "XW-002"):
            load_lifecycle_impact(self.write(only_one), XW)

    def test_rejects_unknown_xw_id(self):
        text = two_rows() + 'XW-999,"plan",""\n'
        with self.assertRaisesRegex(LifecycleImpactError, "unknown crosswalk row XW-999"):
            load_lifecycle_impact(self.write(text), XW)

    def test_rejects_unknown_stage_slug(self):
        text = HEADER + 'XW-001,"launch","plan"\nXW-002,"plan","acquire"\n'
        with self.assertRaisesRegex(LifecycleImpactError, "unknown stage 'launch'"):
            load_lifecycle_impact(self.write(text), XW)

    def test_rejects_stage_in_both_primary_and_secondary(self):
        text = HEADER + 'XW-001,"plan;acquire","acquire;retire"\nXW-002,"plan","acquire"\n'
        with self.assertRaisesRegex(LifecycleImpactError, "acquire"):
            load_lifecycle_impact(self.write(text), XW)

    def test_rejects_row_with_both_lists_empty(self):
        text = HEADER + 'XW-001,"",""\nXW-002,"plan","acquire"\n'
        with self.assertRaisesRegex(LifecycleImpactError, "XW-001"):
            load_lifecycle_impact(self.write(text), XW)

    def test_rejects_wrong_columns(self):
        with self.assertRaisesRegex(LifecycleImpactError, "columns"):
            load_lifecycle_impact(self.write("xw_id,primary\nXW-001,plan\n"), XW)
