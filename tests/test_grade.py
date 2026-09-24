import unittest

from agk.grade import GradeError, grade, parse_findings

KEY = [
    {"tool": "rationalization", "type": "duplicate_app", "id": "APP-008+APP-041"},
    {"tool": "rationalization", "type": "expired_license", "id": "LIC-017"},
    {"tool": "access-review", "type": "orphaned_account", "id": "ACC-019"},
]


def output(json_text):
    return f"Report text\n\n```findings\n{json_text}\n```\n"


class GradeTests(unittest.TestCase):
    def test_parses_findings_block(self):
        f = parse_findings(output('[{"type": "expired_license", "id": "LIC-017"}]'))
        self.assertEqual(f, {("expired_license", "LIC-017")})

    def test_pair_ids_are_order_insensitive(self):
        f = parse_findings(output('[{"type": "duplicate_app", "id": "APP-041 + APP-008"}]'))
        self.assertEqual(f, {("duplicate_app", "APP-008+APP-041")})

    def test_uses_last_findings_block(self):
        text = output("[]") + output('[{"type": "expired_license", "id": "LIC-017"}]')
        self.assertEqual(len(parse_findings(text)), 1)

    def test_missing_block_raises(self):
        with self.assertRaisesRegex(GradeError, "no findings block"):
            parse_findings("Just prose.")

    def test_malformed_json_raises(self):
        with self.assertRaisesRegex(GradeError, "not valid JSON"):
            parse_findings(output("[{type: oops}]"))

    def test_wrong_shape_raises(self):
        with self.assertRaisesRegex(GradeError, "type"):
            parse_findings(output('[{"id": "LIC-017"}]'))

    def test_all_found_passes(self):
        f = {("duplicate_app", "APP-008+APP-041"), ("expired_license", "LIC-017")}
        self.assertTrue(grade(f, KEY, "rationalization")["passed"])

    def test_a_miss_fails(self):
        r = grade({("expired_license", "LIC-017")}, KEY, "rationalization")
        self.assertFalse(r["passed"])
        self.assertEqual(r["missed"], [["duplicate_app", "APP-008+APP-041"]])

    def test_too_many_extras_fails(self):
        f = {("duplicate_app", "APP-008+APP-041"), ("expired_license", "LIC-017"),
             ("expired_license", "LIC-001"), ("expired_license", "LIC-002")}
        self.assertFalse(grade(f, KEY, "rationalization")["passed"])

    def test_other_tools_keys_ignored(self):
        f = {("duplicate_app", "APP-008+APP-041"), ("expired_license", "LIC-017")}
        self.assertEqual(grade(f, KEY, "rationalization")["missed"], [])

    def test_unknown_tool_raises(self):
        with self.assertRaisesRegex(GradeError, "no answer-key entries"):
            grade(set(), KEY, "nope")

    def test_unexpected_finding_type_counts_as_extra(self):
        f = {("duplicate_app", "APP-008+APP-041"), ("expired_license", "LIC-017"),
             ("made_up", "X-001"), ("made_up", "X-002")}
        r = grade(f, KEY, "rationalization")
        self.assertFalse(r["passed"])
        self.assertEqual(len(r["extra"]), 2)
        self.assertIn(["made_up", "X-001"], r["extra"])
        self.assertIn(["made_up", "X-002"], r["extra"])
