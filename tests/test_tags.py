import unittest

from agk.tags import check_tags

KNOWN = {"XW-001", "XW-002"}


class TagTests(unittest.TestCase):
    def test_tagged_steps_pass(self):
        self.assertEqual(check_tags("1. Do it [[XW-001]]\n- [ ] Check [[XW-002]]\n", KNOWN, "c"), [])

    def test_untagged_numbered_step_fails(self):
        self.assertEqual(check_tags("Intro\n1. Do it\n", KNOWN, "c"), ["c:2: step has no clause tag"])

    def test_untagged_checkbox_fails(self):
        self.assertEqual(len(check_tags("- [x] Done\n", KNOWN, "c")), 1)

    def test_indented_substep_needs_tag(self):
        self.assertEqual(check_tags("1. Top [[XW-001]]\n   2. Sub\n", KNOWN, "c"),
                         ["c:2: step has no clause tag"])

    def test_steps_inside_code_fence_ignored(self):
        self.assertEqual(check_tags("```\n1. not a step\n```\n", KNOWN, "c"), [])

    def test_unknown_tag_fails(self):
        self.assertEqual(check_tags("1. Do it [[XW-999]]\n", KNOWN, "c"),
                         ["c:1: unknown clause tag XW-999"])

    def test_plain_bullets_are_not_steps(self):
        self.assertEqual(check_tags("- a note\n", KNOWN, "c"), [])
