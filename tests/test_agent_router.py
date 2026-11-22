import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENT = ROOT / "agents" / "app-governance-agent.md"
ROUTER = ROOT / "methods" / "app-governance"
PLAYBOOK_URL = "https://evemcgivern.github.io/app-governance-kit/docs/sam-toolkit/itam-program-playbook.html"


def _body(text):
    return text.split("---", 2)[2]


class AgentFileTests(unittest.TestCase):
    def setUp(self):
        self.text = AGENT.read_text(encoding="utf-8")

    def test_stays_read_only(self):
        self.assertIn("tools: Read, Grep, Glob, Skill\n", self.text)

    def test_stays_short(self):
        self.assertLessEqual(len(_body(self.text).split()), 330)

    def test_required_sections(self):
        for heading in ("Role", "First questions", "If a letter is in hand", "Safe data",
                        "Limits", "Load the skill", "Answer shape"):
            self.assertRegex(self.text, rf"(?m)^## {heading}", heading)

    def test_playbook_link_and_skill_name(self):
        self.assertIn(PLAYBOOK_URL, self.text)
        self.assertIn("audit-response", self.text)

    def test_description_is_not_a_vendor_platform(self):
        self.assertNotIn("has not picked a tool", self.text)
        self.assertIn("has not picked one of the kit's skills", self.text)

    def test_local_router_fallback(self):
        self.assertIn("methods/app-governance/method.md", self.text)
        self.assertRegex(self.text, r"(?i)read and follow it exactly")
        self.assertRegex(self.text, r"(?i)do not improvise a routing table")
        self.assertLessEqual(len(_body(self.text).split()), 240)

    def test_no_em_dash(self):
        self.assertNotIn("—", self.text)


class RouterTests(unittest.TestCase):
    def setUp(self):
        self.method = (ROUTER / "method.md").read_text(encoding="utf-8")

    def test_playbook_rule_comes_first(self):
        self.assertIn("sam-toolkit/itam-program-playbook.md", self.method)
        self.assertIn(PLAYBOOK_URL, self.method)
        table = self.method.split("## Routing table", 1)[1]
        first_row = [l for l in table.splitlines() if l.startswith("| ") and "---" not in l][1]
        self.assertIn("itam-program-playbook", first_row)

    def test_audit_letter_question(self):
        self.assertRegex(self.method, r"(?i)audit or vendor letter")

    def test_license_position_has_one_home(self):
        rule = "A license position goes to `audit-response`."
        self.assertIn(rule, self.method)
        rows = [l for l in self.method.splitlines() if l.startswith("|") and "license position" in l.lower()]
        self.assertEqual(len(rows), 1, rows)
        self.assertIn("`audit-response`", rows[0])
        self.assertNotIn("rationalization", rows[0])
        self.assertIn("Which auditors", self.method)
        self.assertIn("readiness mode", self.method)
        self.assertRegex(self.method, r"Decision needed: counsel and Finance")

    def test_audit_response_has_readiness_mode(self):
        m = (ROOT / "methods" / "audit-response" / "method.md").read_text(encoding="utf-8")
        self.assertIn("## Readiness mode", m)
        t = (ROOT / "methods" / "audit-response" / "copilot-test.md").read_text(encoding="utf-8")
        self.assertRegex(t, r"(?i)readiness")

    def test_cert_prep_and_shell_note(self):
        self.assertIn("cert-prep", self.method)
        self.assertRegex(self.method, r"(?i)software-lifecycle.{0,80}shell")

    def test_reference_facts_files_exist(self):
        self.assertIn("## Reference facts", self.method)
        facts = self.method.split("## Reference facts", 1)[1].split("\n## ", 1)[0]
        names = set(re.findall(r"`([\w./-]+\.(?:csv|md))`", facts))
        self.assertGreaterEqual(len(names), 8)
        for n in names:
            self.assertTrue(
                (ROOT / "sam-toolkit" / n).is_file() or n == "hardware-lifecycle",
                n)

    def test_sop_and_checklist_cover_scope(self):
        sop = (ROUTER / "sop.md").read_text(encoding="utf-8")
        for term in ("audit", "purchase", "contract", "software lifecycle"):
            self.assertRegex(sop.split("## Roles")[0].lower(), term)
        for slug in ("audit-response", "software-lifecycle", "rationalization"):
            self.assertIn(f"(`{slug}`)", sop)

    def test_copilot_test_has_eight_checks(self):
        t = (ROUTER / "copilot-test.md").read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"(?m)^### Check \d+", t)), 10)
        self.assertNotRegex(t.split("## Behavior checks")[0], r"chooses `rationalization`")


if __name__ == "__main__":
    unittest.main()
