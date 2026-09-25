import tempfile
import unittest
from pathlib import Path

from agk.links import TYPES, LinkError, link_items, load_links

QUESTIONS = [{"id": "q-plan-data", "stage": "plan", "question": "What data will it hold?", "tool": "t", "xw": "XW-028"}]
STAGES = {"retire": {"rules": [{"id": "r-retire-data", "text": "Decide the data's fate.", "xw": ["XW-028"]}]},
          "acquire": {"rules": [{"id": "r-acquire-exit", "text": "Review exit terms.", "xw": ["XW-013"]}]}}
HEADER = "from_id,type,to_id,note\n"


class LinkTests(unittest.TestCase):
    def setUp(self):
        self.items = link_items(QUESTIONS, STAGES)

    def write(self, rows: str) -> Path:
        p = Path(tempfile.mkdtemp()) / "links.csv"
        p.write_text(HEADER + rows, encoding="utf-8")
        return p

    def test_items_index_questions_rules_and_stages(self):
        self.assertEqual(self.items["q-plan-data"], {"stage": "plan", "kind": "question", "text": "What data will it hold?"})
        self.assertEqual(self.items["r-retire-data"]["kind"], "rule")
        self.assertEqual(self.items["optimize"]["kind"], "stage")

    def test_duplicate_item_id_fails(self):
        with self.assertRaisesRegex(LinkError, "id r-retire-data used twice"):
            link_items(QUESTIONS + [{"id": "r-retire-data", "stage": "plan", "question": "Q", "tool": "t", "xw": "x"}], STAGES)

    def test_forward_and_generated_reverse(self):
        links = load_links(self.write('r-retire-data,refers_to,q-plan-data,"fate depends on sensitivity"\n'), self.items)
        self.assertEqual(links["r-retire-data"], [{"label": "Refers to", "type": "refers_to", "target": "q-plan-data",
                                                   "note": "fate depends on sensitivity", "inverse": False}])
        self.assertEqual(links["q-plan-data"][0]["label"], "Referenced by")
        self.assertTrue(links["q-plan-data"][0]["inverse"])

    def test_every_type_has_a_reverse_label(self):
        self.assertEqual(set(TYPES), {"refers_to", "may_impact", "blocks", "leads_to"})
        self.assertEqual(TYPES["blocks"], ("Blocks", "Blocked by"))

    def test_unknown_type_fails(self):
        with self.assertRaisesRegex(LinkError, "line 2: unknown link type 'causes'"):
            load_links(self.write("r-retire-data,causes,q-plan-data,x\n"), self.items)

    def test_unknown_step_fails(self):
        with self.assertRaisesRegex(LinkError, "line 2: unknown step 'r-nope'"):
            load_links(self.write("r-nope,blocks,q-plan-data,x\n"), self.items)

    def test_self_link_fails(self):
        with self.assertRaisesRegex(LinkError, "links to itself"):
            load_links(self.write("q-plan-data,refers_to,q-plan-data,x\n"), self.items)

    def test_leads_to_only_between_stages(self):
        self.assertIn("optimize", load_links(self.write("optimize,leads_to,plan,reinvest\n"), self.items))
        with self.assertRaisesRegex(LinkError, "leads_to links stages only"):
            load_links(self.write("r-retire-data,leads_to,plan,x\n"), self.items)

    def test_duplicate_link_fails(self):
        with self.assertRaisesRegex(LinkError, "line 3: duplicate link"):
            load_links(self.write("r-acquire-exit,may_impact,r-retire-data,x\nr-acquire-exit,may_impact,r-retire-data,y\n"), self.items)

    def test_wrong_columns_fail(self):
        p = Path(tempfile.mkdtemp()) / "links.csv"
        p.write_text("from,to\na,b\n")
        with self.assertRaisesRegex(LinkError, "columns"):
            load_links(p, self.items)
