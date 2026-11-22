import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))

from agk.docs import slug  # noqa: E402

TREE = ROOT / "sam-toolkit" / "audit-decision-tree.md"
PAGE = ROOT / "site" / "docs" / "sam-toolkit" / "audit-decision-tree.html"
EXPECTED = ["1", "2", "3", "A1", "A2", "B1", "B2", "B3", "B4", "B5", "C1", "C2", "C3", "C4", "C5", "C6",
            "C7", "C8", "C9", "C10", "C11", "D1", "D2", "D3", "D4", "D5", "E1", "F1"]
LABELS = ("kit rule", "judgment", "counsel decision")


def nodes() -> dict[str, str]:
    """Node id to the node's text, split at the level 2 and 3 headings."""
    text = TREE.read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"^### Node (\S+)\n(.*?)(?=^#{2,3} |\Z)", text, re.M | re.S):
        out[m.group(1)] = m.group(2)
    return out


class AuditTreeTests(unittest.TestCase):
    def test_every_node_is_present_once(self):
        text = TREE.read_text(encoding="utf-8")
        self.assertEqual(re.findall(r"^### Node (\S+)$", text, re.M), EXPECTED)

    def test_every_answer_link_lands_on_a_heading(self):
        text = TREE.read_text(encoding="utf-8")
        ids = {slug(h) for h in re.findall(r"^#{2,3} (.+)$", text, re.M)}
        links = re.findall(r"\]\(#([^)]+)\)", text)
        self.assertTrue(links)
        for target in links:
            self.assertIn(target, ids)

    def test_every_node_is_reachable_from_node_one(self):
        graph = {n: set(re.findall(r"\]\(#node-([^)]+)\)", body)) for n, body in nodes().items()}
        seen, todo = set(), ["1"]
        while todo:
            n = todo.pop()
            if n not in seen:
                seen.add(n)
                todo += [t.upper() if t != "1" else t for t in graph[n]]
        self.assertEqual(seen, set(EXPECTED))

    def test_each_node_has_label_who_and_file_line(self):
        for node, body in nodes().items():
            self.assertIn("- Who acts:", body, node)
            self.assertIn("- Open:", body, node)
            label = re.search(r"^- Label: (.+)\.$", body, re.M)
            self.assertTrue(label and label.group(1) in LABELS, node)
            self.assertRegex(body, r"\]\(#node-", node)

    def test_named_kit_files_exist(self):
        text = TREE.read_text(encoding="utf-8")
        for name in set(re.findall(r"`([\w-]+\.(?:csv|md))`", text)):
            self.assertTrue((ROOT / "sam-toolkit" / name).is_file(), name)

    def test_flags_match_the_legend(self):
        for node, body in nodes().items():
            one = r"(?:DN \([^)]+\)|FREEZE|ORIG)"
            for flag in re.findall(r"^- Flags?: (.+)$", body, re.M):
                self.assertRegex(flag, rf"^{one}(?:; {one})*\.$", node)

    def test_counsel_nodes_carry_a_decision_flag(self):
        body = nodes()
        for node in ("C4", "C7", "C11", "D4", "D5"):
            self.assertIn("DN (counsel", body[node], node)

    def test_a_publisher_goes_to_c1_from_node_2(self):
        self.assertRegex(nodes()["2"], r"publisher[^\n]*go to \[node C1\]")

    def test_freeze_legend_names_the_exception_once(self):
        text = TREE.read_text(encoding="utf-8")
        legend = text.split("- **FREEZE**", 1)[1].split("- **ORIG**", 1)[0]
        self.assertEqual(legend.count("for any exception"), 1)
        self.assertNotIn("Counsel decides any exception", legend)
        self.assertIn("until counsel closes it at D5", text)

    def test_internal_auditors_path_stops_without_agreement(self):
        self.assertIn("share nothing", nodes()["F1"])
        self.assertIn("Do not go on to node B5", nodes()["B4"])

    def test_no_em_dash(self):
        self.assertNotIn("—", TREE.read_text(encoding="utf-8"))

    @unittest.skipUnless(PAGE.is_file(), "site not built")
    def test_built_page_has_an_id_for_every_node(self):
        html = PAGE.read_text(encoding="utf-8")
        for node in EXPECTED:
            self.assertIn(f'id="node-{node.lower()}"', html)
            self.assertIn(f'href="#node-{node.lower()}"', html)


if __name__ == "__main__":
    unittest.main()
