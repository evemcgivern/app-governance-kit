import tempfile
import unittest
from pathlib import Path

from agk.lifecycle import STAGES, LifecycleError, load_stages, render_checklist

XW = {"XW-001", "XW-027"}


def stage(slug: str, handoff: str = "", rule: str = "- Nothing skips intake. [[XW-027]]", skip: str = "") -> str:
    nxt = handoff or {"plan": "acquire", "acquire": "deploy", "deploy": "operate",
                      "operate": "optimize", "optimize": "plan, retire", "retire": "plan"}[slug]
    parts = {"What happens": "Work happens.", "Gate to move on": "Owner approves.",
             "Hands off to": f"{nxt} — the record moves on.", "Who decides": "The council."}
    lines = [f"## {slug} — Stage", ""] + [f"- **{k}:** {v}" for k, v in parts.items() if k != skip]
    return "\n".join(lines) + f"\n\n### Rules that apply\n\n{rule}\n\n"


def full(**over) -> str:
    return "# Lifecycle\n\n## How it works together\n\nThe stages form a loop.\n\n" + \
        "".join(over.get(s, stage(s)) for s, _ in STAGES)


class StagesTests(unittest.TestCase):
    def write(self, text):
        p = Path(tempfile.mkdtemp()) / "stages.md"
        p.write_text(text, encoding="utf-8")
        return p

    def test_loads_all_stages(self):
        data = load_stages(self.write(full()), XW)
        self.assertEqual(list(data["stages"]), [s for s, _ in STAGES])
        self.assertEqual(data["stages"]["optimize"]["Hands off to"], ["plan", "retire"])
        self.assertEqual(data["stages"]["plan"]["rules"][0]["xw"], ["XW-027"])
        self.assertEqual(data["together"], "The stages form a loop.")

    def test_missing_together_fails(self):
        with self.assertRaisesRegex(LifecycleError, "How it works together"):
            load_stages(self.write(full().replace("The stages form a loop.", "")), XW)

    def test_missing_stage_fails(self):
        with self.assertRaisesRegex(LifecycleError, "no section for stage: retire"):
            load_stages(self.write(full(retire="")), XW)

    def test_missing_part_fails(self):
        with self.assertRaisesRegex(LifecycleError, "deploy: missing 'Who decides'"):
            load_stages(self.write(full(deploy=stage("deploy", skip="Who decides"))), XW)

    def test_untagged_rule_fails(self):
        with self.assertRaisesRegex(LifecycleError, "acquire: rule has no clause tag"):
            load_stages(self.write(full(acquire=stage("acquire", rule="- Buy carefully."))), XW)

    def test_unknown_tag_fails(self):
        with self.assertRaisesRegex(LifecycleError, "unknown crosswalk row XW-999"):
            load_stages(self.write(full(acquire=stage("acquire", rule="- Buy. [[XW-999]]"))), XW)

    def test_stage_without_rules_fails(self):
        with self.assertRaisesRegex(LifecycleError, "operate: no rules"):
            load_stages(self.write(full(operate=stage("operate", rule=""))), XW)

    def test_handoff_to_unknown_stage_fails(self):
        with self.assertRaisesRegex(LifecycleError, "retire: hands off to unknown stage 'archive'"):
            load_stages(self.write(full(retire=stage("retire", handoff="archive"))), XW)

    def test_checklist_includes_rules_and_gate(self):
        data = load_stages(self.write(full()), XW)
        rows = [{"stage": s, "question": f"Ask {s}?", "tool": "rationalization", "xw": "XW-001"} for s, _ in STAGES]
        text = render_checklist(rows, data["stages"])
        plan = text.split("## Plan and request")[1].split("## Acquire")[0]
        self.assertIn("Nothing skips intake. [[XW-027]]", plan)
        self.assertIn("Gate to move on: Owner approves.", plan)
        self.assertIn("Hands off to: acquire", plan)
