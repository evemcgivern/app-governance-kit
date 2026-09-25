import importlib.util
import tempfile
import unittest
from pathlib import Path

from agk.grade import MAX_EXTRA
from agk.practicum import ORDER, PracticumError, practicum_payload

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("generate", ROOT / "demo-estate" / "generate.py")
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)

XW = {"XW-001": {"id": "XW-001", "theme": "Inventory", "summary": "s", "iso27001": "A.5.9"}}


def write_exercises(d: Path, skip: str = "", no_scenario: str = "") -> Path:
    d.mkdir(parents=True, exist_ok=True)
    for n, tool in enumerate(ORDER, start=1):
        if tool == skip:
            continue
        body = "" if tool == no_scenario else "## Scenario\n\nYou are Halden's new lead.\n\n"
        (d / f"{n:02d}-{tool}.md").write_text(f"# Exercise {n}: {tool}\n\n{body}## Files\n\nx\n")
    return d


class PayloadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp())
        gen.generate(cls.tmp / "demo")

    def test_order_has_seven_tools_matching_graded_tools(self):
        self.assertEqual(len(ORDER), 7)
        self.assertIn("hardware-lifecycle", ORDER)
        payload = practicum_payload(self.tmp / "demo", write_exercises(self.tmp / "ex1"), XW)
        self.assertEqual([e["tool"] for e in payload["exercises"]], list(ORDER))
        self.assertEqual({k["tool"] for k in payload["key"]}, set(ORDER))

    def test_carries_tables_texts_and_grading_rule(self):
        payload = practicum_payload(self.tmp / "demo", write_exercises(self.tmp / "ex2"), XW)
        self.assertEqual(len(payload["tables"]["apps"]), 60)
        self.assertEqual(len(payload["tables"]["devices"]), 60)
        self.assertIn("council-draft", payload["texts"])
        self.assertEqual(payload["max_extra"], MAX_EXTRA)
        self.assertEqual(payload["exercises"][0]["scenario"], "You are Halden's new lead.")

    def test_crosswalk_carries_only_id_and_theme(self):
        payload = practicum_payload(self.tmp / "demo", write_exercises(self.tmp / "ex3"), XW)
        self.assertEqual(payload["crosswalk"], [{"id": "XW-001", "theme": "Inventory"}])

    def test_missing_exercise_raises(self):
        with self.assertRaisesRegex(PracticumError, "ai-intake"):
            practicum_payload(self.tmp / "demo", write_exercises(self.tmp / "ex4", skip="ai-intake"), XW)

    def test_missing_scenario_raises(self):
        with self.assertRaisesRegex(PracticumError, "Scenario"):
            practicum_payload(self.tmp / "demo", write_exercises(self.tmp / "ex5", no_scenario="crosswalk"), XW)


if __name__ == "__main__":
    unittest.main()
