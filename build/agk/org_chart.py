"""The org-chart style diagram on site/tools.html: you, the supervisor (router
skill and agent), the nine governance tools it routes to, and the study coach.

One generator feeds three places: the two inline layouts in tools.html (wide
and narrow, colored by CSS variables), and the standalone download, which has
its colors inlined. A test checks the page against this generator, so the
hand-kept page cannot drift from the downloads.

Facts drawn here come from methods/app-governance/method.md (the router's
routing table names all nine tools and cert-prep) and agents/app-governance-agent.md
(read-only; tools Read, Grep, Glob, Skill; loads the router skill)."""
import re
from html import escape

SITE_BASE = "https://evemcgivern.github.io/app-governance-kit/"

# (slug, title) in the order of the tool cards on the page.
TOOLS = [
    ("program-setup", "Stand up a governance program"),
    ("itam-maturity", "ITAM maturity check"),
    ("crosswalk", "Governance framework crosswalk"),
    ("rationalization", "Application rationalization"),
    ("access-review", "Access review pack"),
    ("ai-intake", "AI system intake and risk tiering"),
    ("hardware-lifecycle", "Hardware lifecycle check"),
    ("audit-response", "Software audit response check"),
    ("software-lifecycle", "Software lifecycle check"),
]
COACH = ("cert-prep", "Certification study coach")
ROUTER = ("app-governance", "Application governance router")
AGENT_ANCHOR = "supervisor-agent"

DESC = ("You sit at the top: every decision stays with you. Below you is the supervisor, the "
        "application governance router skill and the app governance agent for Claude Code. It picks a "
        "tool, runs it, and decides nothing. Below the supervisor are the nine governance tools it "
        "routes to; each is a link to its card. Set apart in a dashed group, labeled Also in the kit, "
        "is the certification study coach, which the router also names. The cards below the chart "
        "give the same structure as text.")

STYLE = """
.org-box { fill: var(--surface); stroke: var(--control-border); stroke-width: 1.5; }
.org-box--you { fill: var(--chip-bg); }
.org-super { fill: var(--chip-bg); stroke: var(--accent); stroke-width: 2; }
.org-super-box { fill: var(--surface); stroke: var(--control-border); stroke-width: 1.5; }
.org-group { fill: none; stroke: var(--muted); stroke-width: 1.5; stroke-dasharray: 6 4; }
.org-line { fill: none; stroke: var(--muted); stroke-width: 1.5; }
.org-line--dashed { stroke-dasharray: 6 4; }
.org-arrow { fill: var(--muted); }
.org-text { fill: var(--fg); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-weight: 600; }
.org-text--muted { fill: var(--muted); font-weight: 400; }
.org-link .org-text { fill: var(--accent); }
.org-link { cursor: pointer; }
.org-link:hover .org-box, .org-link:hover .org-super-box { stroke: var(--accent); stroke-width: 2.5; }
.org-link:focus-visible { outline: 3px solid var(--focus); outline-offset: 2px; }
"""

LIGHT = {
    "--surface": "#ffffff", "--control-border": "#767f89", "--chip-bg": "#eef3f5",
    "--accent": "#1f4c5e", "--muted": "#4d5762", "--fg": "#1a212b", "--focus": "#1f4c5e",
}


def standalone_style() -> str:
    return re.sub(r"var\((--[a-z-]+)\)", lambda m: LIGHT[m.group(1)], STYLE)


def wrap(text: str, width: int) -> list[str]:
    lines: list[str] = []
    for word in text.split(" "):
        if lines and len(lines[-1]) + 1 + len(word) <= width:
            lines[-1] += " " + word
        else:
            lines.append(word)
    return lines


def _text(cx: float, y: float, lines: list[str], size: float, cls: str = "org-text", pitch: float | None = None) -> str:
    pitch = pitch or size * 1.2
    spans = "".join(f'<tspan x="{cx:g}" y="{y + i * pitch:g}">{escape(line)}</tspan>' for i, line in enumerate(lines))
    return f'<text class="{cls}" font-size="{size:g}" text-anchor="middle">{spans}</text>'


def _rect(x, y, w, h, cls, rx=8) -> str:
    return f'<rect class="{cls}" x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}"/>'


def _line(d: str, dashed=False) -> str:
    cls = "org-line org-line--dashed" if dashed else "org-line"
    return f'<path class="{cls}" d="{d}" aria-hidden="true"/>'


def _arrow(x: float, y: float) -> str:
    """Arrow head pointing down, tip at (x, y)."""
    return f'<path class="org-arrow" d="M {x - 5:g} {y - 8:g} L {x + 5:g} {y - 8:g} L {x:g} {y:g} Z" aria-hidden="true"/>'


def _link(href: str, label: str, inner: str) -> str:
    return f'<a class="org-link" href="{href}" aria-label="{escape(label, quote=True)}">{inner}</a>'


def supervisor_chart_svg(layout: str = "wide", standalone: bool = False) -> str:
    """layout: 'wide' (one row of nine boxes, from 64rem) or 'narrow' (two columns, below)."""
    wide = layout == "wide"
    anchor = (lambda slug: f"{SITE_BASE}tools.html#{slug}") if standalone else (lambda slug: f"#{slug}")
    agent_href = anchor(AGENT_ANCHOR)
    p: list[str] = []

    if wide:
        W, size, cx = 1000, 12.5, 500
        you_w, you_y, you_h = 340, 8, 40
        sup_x, sup_y, sup_w, sup_h = 100, 80, 800, 124
        rail_y, box_y, box_w, box_h, gap = 250, 280, 100, 66, 8
        xs = [4 + i * (box_w + gap) for i in range(9)]
        centers = [x + box_w / 2 for x in xs]
        lines_w = 14
    else:
        W, size, cx = 360, 13, 180
        you_w, you_y, you_h = 300, 8, 44
        sup_x, sup_y, sup_w, sup_h = 4, 84, 352, 206
        box_w, box_h = 150, 54
        trunk = 14
        xs_col = [30, 190]
        lines_w = 19

    # Level 0: you
    you_x = cx - you_w / 2
    p.append('<g class="org-you">')
    p.append(_rect(you_x, you_y, you_w, you_h, "org-box org-box--you"))
    p.append(_text(cx, you_y + you_h / 2 + size * 0.35, ["You: every decision stays with you"], size + 1))
    p.append("</g>")
    p.append(_line(f"M {cx:g} {you_y + you_h:g} V {sup_y - 9:g}"))
    p.append(_arrow(cx, sup_y))

    # Level 1: the supervisor
    p.append('<g class="org-supervisor">')
    p.append(_rect(sup_x, sup_y, sup_w, sup_h, "org-super", 10))
    p.append(_text(cx, sup_y + 22, ["Supervisor: picks a tool, runs it, decides nothing"], size + 1))
    router_label = f"{ROUTER[1]}, a skill"
    if wide:
        bw, bh, by = 372, 76, sup_y + 36
        rx_, ax_ = sup_x + 16, sup_x + sup_w - 16 - bw
        p.append(_link(anchor(ROUTER[0]), router_label,
                       _rect(rx_, by, bw, bh, "org-super-box")
                       + _text(rx_ + bw / 2, by + 26, [ROUTER[1]], size + 1)
                       + _text(rx_ + bw / 2, by + 46, ["A skill: picks the tool, asks for the data"], size, "org-text org-text--muted")
                       + _text(rx_ + bw / 2, by + 64, ["Claude, Codex and Copilot"], size, "org-text org-text--muted")))
        p.append(_link(agent_href, "App governance agent, Claude Code, read-only, see its card",
                       _rect(ax_, by, bw, bh, "org-super-box")
                       + _text(ax_ + bw / 2, by + 26, ["App governance agent"], size + 1)
                       + _text(ax_ + bw / 2, by + 46, ["Claude Code agent, read-only"], size, "org-text org-text--muted")
                       + _text(ax_ + bw / 2, by + 64, ["Loads the router skill"], size, "org-text org-text--muted")))
    else:
        bx, bw, bh = sup_x + 12, sup_w - 24, 74
        by1, by2 = sup_y + 38, sup_y + 38 + 74 + 10
        p.append(_link(anchor(ROUTER[0]), router_label,
                       _rect(bx, by1, bw, bh, "org-super-box")
                       + _text(cx, by1 + 24, [ROUTER[1]], size + 1)
                       + _text(cx, by1 + 43, ["A skill: picks the tool, asks for data"], size, "org-text org-text--muted")
                       + _text(cx, by1 + 61, ["Claude, Codex and Copilot"], size, "org-text org-text--muted")))
        p.append(_link(agent_href, "App governance agent, Claude Code, read-only, see its card",
                       _rect(bx, by2, bw, bh, "org-super-box")
                       + _text(cx, by2 + 24, ["App governance agent"], size + 1)
                       + _text(cx, by2 + 43, ["Claude Code agent, read-only"], size, "org-text org-text--muted")
                       + _text(cx, by2 + 61, ["Loads the router skill"], size, "org-text org-text--muted")))
    p.append("</g>")

    def tool_box(i_x, i_y, slug, title, lines_width):
        lines = wrap(title, lines_width)
        top = i_y + (box_h - len(lines) * size * 1.2) / 2 + size * 0.95
        return _link(anchor(slug), title,
                     _rect(i_x, i_y, box_w, box_h, "org-box") + _text(i_x + box_w / 2, top, lines, size))

    note_lines = ["The agent can't run it:", "you run the tool."]
    sup_bottom = sup_y + sup_h
    p.append('<g class="org-tools">')
    if wide:
        p.append(_line(f"M {cx:g} {sup_bottom:g} V {rail_y:g}"))
        p.append(_line(f"M {centers[0]:g} {rail_y:g} H {centers[-1]:g}"))
        for c, x, (slug, title) in zip(centers, xs, TOOLS):
            p.append(_line(f"M {c:g} {rail_y:g} V {box_y - 9:g}"))
            p.append(_arrow(c, box_y))
            p.append(tool_box(x, box_y, slug, title, lines_w))
        p.append(_text(cx + 10, rail_y - 14, ["Routes to these tools"], size, "org-text org-text--muted").replace(
            'text-anchor="middle"', 'text-anchor="start"').replace(f'x="{cx:g}"', f'x="{cx + 10:g}"'))
        p.append(_text(centers[-1], box_y + box_h + 18, note_lines, size - 0.5, "org-text org-text--muted", 14))
    else:
        row_pitch = box_h + 22
        first_rail = sup_bottom + 36
        rows = [TOOLS[i:i + 2] for i in range(0, len(TOOLS), 2)]
        last_rail = first_rail + (len(rows) - 1) * row_pitch
        p.append(_line(f"M {trunk:g} {sup_bottom:g} V {last_rail:g}"))
        p.append(_text(trunk + 14, first_rail - 12, ["Routes to these tools"], size, "org-text org-text--muted").replace(
            'text-anchor="middle"', 'text-anchor="start"').replace(f'x="{cx:g}"', f'x="{trunk + 14:g}"'))
        for r, row in enumerate(rows):
            rail = first_rail + r * row_pitch
            cs = [xs_col[c] + box_w / 2 for c in range(len(row))]
            p.append(_line(f"M {trunk:g} {rail:g} H {cs[-1]:g}"))
            for c, (slug, title) in enumerate(row):
                p.append(_line(f"M {cs[c]:g} {rail:g} V {rail + 9:g}"))
                p.append(_arrow(cs[c], rail + 17))
                p.append(tool_box(xs_col[c], rail + 17, slug, title, lines_w))
        slc_y = first_rail + (len(rows) - 1) * row_pitch + 17
        p.append(_text(xs_col[1] + box_w / 2, slc_y + 22, note_lines, size - 0.5, "org-text org-text--muted", 15))
    p.append("</g>")

    # Also in the kit: the study coach, routed too, but outside the nine
    p.append('<g class="org-also">')
    if wide:
        gx, gy, gw, gh = 720, 404, 240, 92
        route_x = W - 6
        p.append(_line(f"M {centers[-1]:g} {rail_y:g} H {route_x:g} V {gy + gh / 2:g} H {gx + gw:g}", dashed=True))
        p.append(_rect(gx, gy, gw, gh, "org-group", 10))
        p.append(_text(gx + gw / 2, gy + 20, ["Also in the kit"], size, "org-text org-text--muted"))
        p.append(_link(anchor(COACH[0]), COACH[1],
                       _rect(gx + 16, gy + 30, gw - 32, 48, "org-box")
                       + _text(gx + gw / 2, gy + 30 + 21, wrap(COACH[1], 18), size)))
        height = gy + gh + 8
    else:
        rail_last = first_rail + (len(rows) - 1) * row_pitch
        gy = slc_y + box_h + 36
        gx, gw, gh = 4, 352, 100
        p.append(_line(f"M {trunk:g} {rail_last:g} V {gy:g}", dashed=True))
        p.append(_rect(gx, gy, gw, gh, "org-group", 10))
        p.append(_text(cx, gy + 22, ["Also in the kit: routed too, outside the nine"], size, "org-text org-text--muted"))
        p.append(_link(anchor(COACH[0]), COACH[1],
                       _rect(gx + 40, gy + 36, gw - 80, 48, "org-box")
                       + _text(cx, gy + 36 + 29, [COACH[1]], size)))
        height = gy + gh + 8
    p.append("</g>")

    title = "Who does what: you, the supervisor, and the tools"
    xmlns = ' xmlns="http://www.w3.org/2000/svg"' if standalone else ""
    head = (f'<svg class="org-chart org-chart--{layout}"{xmlns} viewBox="0 0 {W} {height:g}" '
            f'aria-labelledby="org-title-{layout} org-desc-{layout}">')
    body = (f'<title id="org-title-{layout}">{escape(title)}</title><desc id="org-desc-{layout}">{escape(DESC)}</desc>')
    style = f"<style>{standalone_style()}</style>" if standalone else ""
    return head + body + style + "".join(p) + "</svg>"
