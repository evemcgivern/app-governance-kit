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

    def test_sixty_devices(self):
        self.assertEqual(len(rows(self.out / "devices.csv")), 60)

    def test_only_planted_devices_overdue_refresh(self):
        devices = rows(self.out / "devices.csv")
        overdue = {d["device_id"] for d in devices
                   if d["status"] == "active" and d["refresh_due_date"] < d["checked_on"]}
        self.assertEqual(overdue, self.expected("overdue_refresh"))
        self.assertEqual(len(overdue), 3)

    def test_only_planted_retired_devices_unwiped(self):
        devices = rows(self.out / "devices.csv")
        unwiped = {d["device_id"] for d in devices
                   if d["status"] == "retired" and d["data_wipe_confirmed"] != "yes"}
        self.assertEqual(unwiped, self.expected("unwiped_retired_device"))
        self.assertEqual(len(unwiped), 2)

    def test_audit_scenario_has_planted_problems_only(self):
        proofs = rows(self.out / "proofs-of-purchase.csv")
        installs = rows(self.out / "audit-installs.csv")
        self.assertEqual(len(proofs), 6)
        license_ids = {l["id"] for l in rows(self.out / "licenses.csv")}
        self.assertTrue({p["license_id"] for p in proofs} <= license_ids)
        no_buyer = {p["proof_id"] for p in proofs if not p["buyer_entity"]}
        self.assertEqual(no_buyer, self.expected("proof_missing_buyer"))
        no_payment = {p["proof_id"] for p in proofs if p["payment_proof"] != "yes"}
        self.assertEqual(no_payment, self.expected("payment_proof_missing"))
        no_original = {p["proof_id"] for p in proofs
                       if p["license_type"] == "upgrade" and p["upgrade_chain_complete"] != "yes"}
        self.assertEqual(no_original, self.expected("upgrade_without_original"))
        short, late = set(), set()
        for i in installs:
            match = [p for p in proofs if p["license_id"] == i["license_id"] and p["version"] == i["version"]]
            self.assertTrue(all(p["license_metric"] == i["license_metric"] for p in match))
            if sum(int(p["quantity"]) for p in match) < int(i["count_in_metric"]):
                short.add(i["license_id"])
            earliest = min(match, key=lambda p: p["purchase_date"])
            if earliest["purchase_date"] > i["first_install_date"]:
                late.add(earliest["proof_id"])
        self.assertEqual(short, self.expected("install_shortfall"))
        self.assertEqual(late, self.expected("proof_after_install"))
        self.assertEqual(self.expected("letter_scope_overreach"), {"letter-scope"})
        expiry = {l["id"]: l["expiry"] for l in rows(self.out / "licenses.csv")}
        for p in proofs:
            self.assertEqual(p["term_end"], expiry[p["license_id"]])
        for p in proofs:
            if p["license_type"] == "upgrade":
                self.assertFalse(any(q["product"] + " " + q["version"] == p["upgrade_base"] for q in proofs))
        self.assertIn("Brightvale", (self.out / "audit-letter.md").read_text())

    def test_generation_is_deterministic(self):
        other = Path(tempfile.mkdtemp())
        gen.generate(other)
        for f in self.out.iterdir():
            self.assertEqual(f.read_bytes(), (other / f.name).read_bytes(), f.name)
