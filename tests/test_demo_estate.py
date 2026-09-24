import csv
import importlib.util
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("generate", ROOT / "demo-estate" / "generate.py")
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class DemoEstateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = Path(tempfile.mkdtemp())
        gen.generate(cls.out)
        cls.key = json.loads((cls.out / "answer-key.json").read_text())

    def expected(self, kind):
        return {k["id"] for k in self.key if k["type"] == kind}

    def test_sixty_apps(self):
        self.assertEqual(len(rows(self.out / "apps.csv")), 60)

    def test_every_app_has_a_data_sensitivity(self):
        values = {a["data_sensitivity"] for a in rows(self.out / "apps.csv")}
        self.assertEqual(values, {"confidential", "internal"})

    def test_only_planted_duplicates_share_a_category(self):
        apps = rows(self.out / "apps.csv")
        counts = Counter(a["category"] for a in apps)
        pairs = set()
        for cat, n in counts.items():
            if n > 1:
                ids = sorted(a["id"] for a in apps if a["category"] == cat)
                self.assertEqual(len(ids), 2)
                pairs.add("+".join(ids))
        self.assertEqual(pairs, self.expected("duplicate_app"))
        self.assertEqual(len(pairs), 5)

    def test_only_planted_licenses_expired(self):
        lic = rows(self.out / "licenses.csv")
        expired = {l["id"] for l in lic if l["expiry"] < l["checked_on"]}
        self.assertEqual(expired, self.expected("expired_license"))
        self.assertEqual(len(expired), 2)

    def test_only_planted_accounts_orphaned(self):
        emps = {e["id"]: e for e in rows(self.out / "employees.csv")}
        orphans = {a["id"] for a in rows(self.out / "accounts.csv")
                   if a["employee_id"] not in emps or emps[a["employee_id"]]["status"] != "active"}
        self.assertEqual(orphans, self.expected("orphaned_account"))
        self.assertEqual(len(orphans), 3)

    def test_six_ai_systems_one_high_risk(self):
        self.assertEqual(len(rows(self.out / "ai-systems.csv")), 6)
        self.assertEqual(self.expected("high_risk_ai"), {"AI-004"})

    def test_three_lowest_maturity_areas_are_the_gaps(self):
        answers = sorted(rows(self.out / "maturity-answers.csv"), key=lambda r: int(r["score"]))
        self.assertEqual({r["area"] for r in answers[:3]}, self.expected("maturity_gap"))
        self.assertLess(int(answers[2]["score"]), int(answers[3]["score"]))

    def test_council_draft_has_planted_flaws(self):
        text = (self.out / "council-draft.md").read_text()
        self.assertNotIn("sponsor", text.lower())
        self.assertNotIn("decide", text.lower())
        members = text.split("## Members (voting)\n")[1].split("\n\n")[0]
        self.assertEqual(self.expected("charter_gap"), {"decision-rights", "sponsor", "membership-size"})
        self.assertGreater(members.count(",") + members.count(";") + 1, 9)

    def test_generation_is_deterministic(self):
        other = Path(tempfile.mkdtemp())
        gen.generate(other)
        for f in self.out.iterdir():
            self.assertEqual(f.read_bytes(), (other / f.name).read_bytes(), f.name)
