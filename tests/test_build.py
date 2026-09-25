import json
import tempfile
import unittest
from pathlib import Path

from agk.build import build, main
from agk.render import COPILOT_MAX
from tests.helpers import make_method, make_repo


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.root = make_repo(Path(tempfile.mkdtemp()))
        make_method(self.root, "rationalization")

    def test_builds_all_three_versions(self):
        errors, _ = build(self.root)
        self.assertEqual(errors, [])
        d = self.root / "dist"
        for name in ("crosswalk", "rationalization"):
            self.assertTrue((d / "claude/skills" / name / "SKILL.md").is_file())
            self.assertTrue((d / "codex/skills" / name / "SKILL.md").is_file())
            for f in ("agent-instructions.md", "chat-prompt.md", "test-script.md",
                      "knowledge/checklist.md", "knowledge/sop.md", "knowledge/platform-guide.md",
                      "knowledge/template.md", "knowledge/crosswalk.csv"):
                self.assertTrue((d / "copilot" / name / f).is_file(), f)
        self.assertTrue((d / "claude/agents/governance-reviewer.md").is_file())
        manifest = json.loads((d / "claude/.claude-plugin/plugin.json").read_text())
        self.assertEqual(manifest["name"], "app-governance-kit")
        self.assertIn("rationalization", (d / "codex/AGENTS.md").read_text())

    def test_skill_md_has_frontmatter_and_references(self):
        build(self.root)
        text = (self.root / "dist/claude/skills/rationalization/SKILL.md").read_text()
        self.assertTrue(text.startswith("---\nname: rationalization\ndescription: Test method\n---\n"))
        self.assertIn("`crosswalk.csv`", text)

    def test_incomplete_method_stops_build(self):
        make_method(self.root, "broken", **{"sop.md": None})
        errors, _ = build(self.root)
        self.assertTrue(any("broken: missing sop.md" in e for e in errors))
        self.assertFalse((self.root / "dist").exists())

    def test_untagged_step_stops_build(self):
        make_method(self.root, "untagged", **{"checklist.md": "1. No tag here\n"})
        errors, _ = build(self.root)
        self.assertIn("untagged/checklist.md:1: step has no clause tag", errors)

    def test_copilot_over_limit_fails(self):
        make_method(self.root, "huge", body="x" * (COPILOT_MAX + 1))
        errors, _ = build(self.root)
        self.assertTrue(any("huge: Copilot instructions" in e for e in errors))

    def test_copilot_near_limit_warns(self):
        make_method(self.root, "long", body="x" * 6500)
        errors, warnings = build(self.root)
        self.assertEqual(errors, [])
        self.assertTrue(any("long" in w for w in warnings))

    def test_rebuild_removes_stale_output(self):
        build(self.root)
        stale = self.root / "dist/claude/skills/old"
        stale.mkdir()
        build(self.root)
        self.assertFalse(stale.exists())

    def test_main_exit_codes(self):
        self.assertEqual(main(["--root", str(self.root)]), 0)
        make_method(self.root, "broken", **{"sop.md": None})
        self.assertEqual(main(["--root", str(self.root)]), 1)

    def test_themes_shipped_with_every_tool(self):
        errors, _ = build(self.root)
        self.assertEqual(errors, [])
        d = self.root / "dist"
        self.assertTrue((d / "claude/skills/rationalization/themes.md").is_file())
        self.assertTrue((d / "copilot/rationalization/knowledge/themes.md").is_file())
        self.assertIn("`themes.md`", (d / "claude/skills/rationalization/SKILL.md").read_text())

    def test_missing_theme_description_stops_build(self):
        (self.root / "methods/crosswalk/themes.md").write_text("# empty\n")
        errors, _ = build(self.root)
        self.assertTrue(any(e.startswith("themes:") for e in errors))

    def test_lifecycle_bank_builds_checklist(self):
        from agk.lifecycle import STAGES
        (self.root / "lifecycle").mkdir()
        rows = "".join(f'{s},"Ask about {s}?",rationalization,XW-001\n' for s, _ in STAGES)
        (self.root / "lifecycle" / "questions.csv").write_text("stage,question,tool,xw\n" + rows)
        errors, _ = build(self.root)
        self.assertEqual(errors, [])
        self.assertIn("## Retire", (self.root / "dist" / "lifecycle-questions.md").read_text())

    def test_lifecycle_bank_errors_stop_build(self):
        (self.root / "lifecycle").mkdir()
        (self.root / "lifecycle" / "questions.csv").write_text('stage,question,tool,xw\nplan,"Q?",nope,XW-001\n')
        errors, _ = build(self.root)
        self.assertTrue(any(e.startswith("lifecycle:") for e in errors))
