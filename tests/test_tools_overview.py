import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = (ROOT / "site" / "tools.html").read_text(encoding="utf-8")
METHODS = ROOT / "methods"
FIELDS = ["What it does", "You give it", "You get", "Use it when", "Decision stays with", "Where it runs"]
FORMS = ("Claude skill", "Codex skill", "Copilot agent")


def method_keys() -> list[str]:
    return sorted(p.name for p in METHODS.iterdir() if (p / "method.md").exists())


def method_title(key: str) -> str:
    text = (METHODS / key / "method.md").read_text(encoding="utf-8")
    return re.search(r"(?m)^title: (.+)$", text).group(1).strip()


def overview() -> str:
    m = re.search(r'<section[^>]*id="overview"[^>]*>(.*?)</section>', PAGE, re.S)
    assert m, "overview section not found"
    return m.group(1)


def band() -> str:
    """Everything from the band's opening tag to the heading of the routed tools."""
    o = overview()
    return o[o.index('class="supervisor-band"'):o.index('id="routed-heading"')]


def routed_group() -> str:
    o = overview()
    return o[o.index('id="routed-tools"'):o.index('id="also-heading"')]


def other_group() -> str:
    o = overview()
    return o[o.index('id="also-in-kit"'):]


def cards(html: str) -> list[str]:
    return re.findall(r'<(?:li|article) class="card tool-card[^"]*"[^>]*>(.*?)</(?:li|article)>', html, re.S)


def entries() -> list[str]:
    """Every method card: the router (in the band), the nine routed tools, the study coach."""
    router = [c for c in cards(band()) if 'href="#app-governance"' in c]
    return router + cards(routed_group()) + cards(other_group())


def card_key(html: str) -> str:
    return re.search(r'<h4><a href="#([a-z-]+)">', html).group(1)


def text_of(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).strip()


class ToolsOverviewTests(unittest.TestCase):
    def test_one_entry_per_method(self):
        keys = [card_key(e) for e in entries()]
        self.assertEqual(sorted(keys), method_keys())
        self.assertEqual(len(keys), len(set(keys)))

    def test_each_entry_links_to_an_existing_card(self):
        for e in entries():
            self.assertRegex(PAGE, rf'<article class="card" id="{card_key(e)}">')

    def test_entry_name_matches_the_method_title(self):
        for e in entries():
            m = re.search(r'<h4><a href="#([a-z-]+)">([^<]+)</a></h4>', e)
            self.assertEqual(m.group(2), method_title(m.group(1)))

    def test_six_fields_in_order_and_not_empty(self):
        for e in cards(band()) + cards(routed_group()) + cards(other_group()):
            labels = re.findall(r"<dt>([^<]+)</dt>", e)
            self.assertEqual(labels, FIELDS, e[:80])
            for dd in re.findall(r"<dd>(.*?)</dd>", e, re.S):
                self.assertGreaterEqual(len(text_of(dd)), 8, e[:80])

    def test_every_card_says_where_it_runs(self):
        for e in entries():
            runs = text_of(re.findall(r"<dd>(.*?)</dd>", e, re.S)[5])
            for form in FORMS:
                self.assertIn(form, runs, card_key(e))

    def test_overview_comes_before_install(self):
        self.assertLess(PAGE.index('id="overview"'), PAGE.index('id="install"'))
        self.assertLess(PAGE.index('id="overview"'), PAGE.index('<article class="card" id='))

    def test_headings_nest_and_regions_are_labelled(self):
        self.assertRegex(PAGE, r'<section aria-labelledby="overview-heading" id="overview">\s*<h2 id="overview-heading">What each tool does</h2>')
        self.assertEqual(PAGE.count("<h1"), 1)
        o = overview()
        self.assertNotIn("<h5", o)
        self.assertEqual(len(re.findall(r"<h4>", o)), len(method_keys()) + 1)  # the cards, plus the agent
        for hid in ("supervisor-heading", "routed-heading", "also-heading"):
            self.assertRegex(o, rf'<h3 id="{hid}">')
        self.assertRegex(o, r'<div class="supervisor-band" role="region" aria-labelledby="supervisor-heading">')
        self.assertRegex(o, r'<ul[^>]*id="routed-tools"[^>]*aria-labelledby="routed-heading"')
        self.assertRegex(o, r'<ul[^>]*id="also-in-kit"[^>]*aria-labelledby="also-heading"')

    def test_no_em_dashes_in_overview(self):
        self.assertNotIn("—", overview())

    def test_title_and_description_rules_still_hold(self):
        title = re.search(r"<title>(.*?)</title>", PAGE).group(1)
        self.assertTrue(title.endswith(" | App Governance Kit"))
        desc = re.search(r'<meta name="description" content="([^"]+)"', PAGE).group(1)
        self.assertGreater(len(desc), 60)
        self.assertIn("nine governance tools, plus a router and a study coach", PAGE)

    def test_decision_cells_name_a_role_or_say_not_found(self):
        for e in entries():
            dd = re.findall(r"<dd>(.*?)</dd>", e, re.S)[4]
            self.assertTrue(re.search(r"owner|counsel|sponsor|approver|learner|Legal|you|lead|Not found", text_of(dd), re.I), text_of(dd))


class SupervisorBandTests(unittest.TestCase):
    def test_intro_is_the_first_line_and_says_tools_work_alone(self):
        first = text_of(re.search(r"<p[^>]*>(.*?)</p>", overview(), re.S).group(1))
        self.assertIn("nine governance tools each work on their own", first)
        self.assertIn("only picks one for you", first)

    def test_order_is_chart_then_band_then_tools_then_study_coach(self):
        o = overview()
        self.assertLess(o.index('class="org-chart'), o.index('class="supervisor-band"'))
        self.assertLess(o.index('class="supervisor-band"'), o.index('id="routed-tools"'))
        self.assertLess(o.index('id="routed-tools"'), o.index('id="also-in-kit"'))

    def test_band_says_start_here(self):
        self.assertIn("Start here if you have not picked a tool.", text_of(band()))

    def test_band_holds_router_and_agent_facts(self):
        t = text_of(band())
        self.assertIn("Application governance router", t)
        self.assertIn("App governance agent", t)
        self.assertIn("read-only", t)
        self.assertIn("decides nothing", t)
        self.assertIn("Read, Grep, Glob and Skill", t)
        self.assertIn("loads the router skill", t.lower())
        self.assertIn("Claude Code agent", t)

    def test_band_makes_no_unverified_claims(self):
        t = text_of(band()).lower()
        for word in ("parallel", "autonomous", "in the background", "automatically"):
            self.assertNotIn(word, t)

    def test_connector_label_is_real_text(self):
        self.assertIn("Routes to these tools", text_of(overview()))

    def test_routed_group_has_the_nine_governance_tools(self):
        keys = [card_key(e) for e in cards(routed_group())]
        self.assertEqual(sorted(keys), sorted(set(method_keys()) - {"app-governance", "cert-prep"}))
        self.assertEqual(len(keys), 9)

    def test_study_coach_sits_in_its_own_labelled_row(self):
        self.assertEqual([card_key(e) for e in cards(other_group())], ["cert-prep"])
        self.assertNotIn('id="cert-prep"', routed_group())
        self.assertIn("Also in the kit", text_of(overview()))

    def test_the_router_method_names_every_tool_the_chart_draws(self):
        method = (METHODS / "app-governance" / "method.md").read_text(encoding="utf-8")
        for key in method_keys():
            if key != "app-governance":
                self.assertIn(f"`{key}`", method, key)


class SupervisorChartTests(unittest.TestCase):
    def chart(self, layout):
        m = re.search(rf'<svg[^>]*class="org-chart org-chart--{layout}".*?</svg>', PAGE, re.S)
        self.assertTrue(m, layout)
        return m.group(0)

    def test_both_layouts_have_title_and_desc(self):
        for layout in ("wide", "narrow"):
            svg = self.chart(layout)
            self.assertRegex(svg, rf'<title id="org-title-{layout}">[^<]+</title>')
            self.assertRegex(svg, rf'<desc id="org-desc-{layout}">[^<]+</desc>')
            self.assertIn(f'aria-labelledby="org-title-{layout} org-desc-{layout}"', svg)
            self.assertNotIn('role="img"', svg)  # role=img would hide the links

    def test_supervisor_above_tools_above_study_coach_group(self):
        for layout in ("wide", "narrow"):
            svg = self.chart(layout)
            order = [svg.index(c) for c in ("org-you", "org-supervisor", "org-tools", "org-also")]
            self.assertEqual(order, sorted(order), layout)

    def test_each_tool_box_is_present_once_with_a_link(self):
        for layout in ("wide", "narrow"):
            svg = self.chart(layout)
            for key in method_keys():
                self.assertEqual(svg.count(f'href="#{key}"'), 1, (layout, key))
            names = re.findall(r'<a [^>]*aria-label="([^"]+)"', svg)
            self.assertEqual(len(names), len(method_keys()) + 1)  # plus the agent

    def test_study_coach_is_in_the_dashed_group_not_the_routed_group(self):
        for layout in ("wide", "narrow"):
            svg = self.chart(layout)
            tools_part = svg[svg.index("org-tools"):svg.index("org-also")]
            also_part = svg[svg.index("org-also"):]
            self.assertNotIn('href="#cert-prep"', tools_part)
            self.assertIn('href="#cert-prep"', also_part)
            self.assertIn("Also in the kit", text_of(also_part))

    def test_connector_label_and_supervisor_text_are_in_the_drawing(self):
        for layout in ("wide", "narrow"):
            t = text_of(self.chart(layout))
            self.assertIn("Routes to these tools", t)
            self.assertIn("decides nothing", t)
            self.assertIn("read-only", t)
            self.assertIn("every decision stays with you", t)

    def test_inline_chart_matches_the_generator(self):
        from agk.org_chart import supervisor_chart_svg
        for layout in ("wide", "narrow"):
            self.assertEqual(self.chart(layout), supervisor_chart_svg(layout, standalone=False))

    def test_download_and_print_actions_exist(self):
        self.assertIn('href="downloads/supervisor-chart.svg"', PAGE)
        self.assertIn('href="downloads/supervisor-chart-print.html"', PAGE)

    def test_css_shows_one_layout_at_a_time(self):
        css = (ROOT / "site" / "style.css").read_text(encoding="utf-8")
        self.assertRegex(css, r"\.org-chart--wide\s*\{\s*display:\s*none")
        self.assertRegex(css, r"@media \(min-width: 64rem\)")


if __name__ == "__main__":
    unittest.main()
