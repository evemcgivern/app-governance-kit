import tempfile
import unittest
from pathlib import Path

from agk.lifecycle import STAGES, LifecycleError, load_questions, render_checklist
from agk.tags import check_tags

HEADER = "stage,question,tool,xw\n"
TOOLS = {"rationalization", "access-review"}
XW = {"XW-001", "XW-016"}


def full_bank() -> str:
    return HEADER + "".join(f'{slug},"Question for {slug}?",rationalization,XW-001\n' for slug, _ in STAGES)


class LifecycleTests(unittest.TestCase):
    def write(self, text):
        p = Path(tempfile.mkdtemp()) / "questions.csv"
        p.write_text(text, encoding="utf-8")
        return p

    def test_six_stages_in_order(self):
        self.assertEqual([s for s, _ in STAGES], ["plan", "acquire", "deploy", "operate", "optimize", "retire"])

    def test_loads_a_complete_bank(self):
        rows = load_questions(self.write(full_bank()), TOOLS, XW)
        self.assertEqual(len(rows), 6)

    def test_rejects_unknown_stage(self):
        with self.assertRaisesRegex(LifecycleError, "line 8: unknown stage 'launch'"):
            load_questions(self.write(full_bank() + 'launch,"Q?",rationalization,XW-001\n'), TOOLS, XW)

    def test_rejects_unknown_tool(self):
        with self.assertRaisesRegex(LifecycleError, "unknown tool 'nope'"):
            load_questions(self.write(full_bank() + 'plan,"Q?",nope,XW-001\n'), TOOLS, XW)

    def test_rejects_unknown_crosswalk_row(self):
        with self.assertRaisesRegex(LifecycleError, "unknown crosswalk row XW-999"):
            load_questions(self.write(full_bank() + 'plan,"Q?",rationalization,XW-999\n'), TOOLS, XW)

    def test_rejects_empty_question(self):
        with self.assertRaisesRegex(LifecycleError, "empty question"):
            load_questions(self.write(full_bank() + 'plan,"",rationalization,XW-001\n'), TOOLS, XW)

    def test_rejects_stage_with_no_questions(self):
        text = HEADER + 'plan,"Q?",rationalization,XW-001\n'
        with self.assertRaisesRegex(LifecycleError, "no questions for stage"):
            load_questions(self.write(text), TOOLS, XW)

    def test_rejects_wrong_columns(self):
        with self.assertRaisesRegex(LifecycleError, "columns"):
            load_questions(self.write("stage,question\nplan,Q\n"), TOOLS, XW)

    def test_checklist_groups_by_stage_in_order_and_passes_tag_check(self):
        rows = load_questions(self.write(full_bank()), TOOLS, XW)
        text = render_checklist(rows)
        labels = [label for _, label in STAGES]
        positions = [text.index(f"## {label}") for label in labels]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("- [ ] Question for plan? [[XW-001]] (tool: `rationalization`)", text)
        self.assertEqual(check_tags(text, XW, "lifecycle"), [])
