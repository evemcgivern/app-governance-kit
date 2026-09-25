import csv
import io
import math
import re
import shutil
import zipfile
from html import escape
from pathlib import Path

LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")
WHEEL_SVG_RE = re.compile(r'<svg class="lc-wheel".*?</svg>', re.S)

# Mirrors the STAGES list and drawing math in site/lifecycle.html's inline
# script exactly (segment order, angles, handoff arrows). The live page draws
# this wheel client-side from injected JSON; a static download/print export
# has no script to do that, so this reproduces the same geometry in Python.
WHEEL_STAGES = [
    ("plan", "Plan and request"),
    ("acquire", "Acquire"),
    ("deploy", "Deploy"),
    ("operate", "Operate"),
    ("optimize", "Review and optimize"),
    ("retire", "Retire"),
]
WHEEL_CX, WHEEL_CY = 200, 200
WHEEL_R_OUTER, WHEEL_R_INNER = 150, 78

WHEEL_STYLE = """
.lc-wheel-ring { stroke: #dde1e6; stroke-width: 1; fill: none; }
.lc-segment { fill: #eef3f5; stroke: #f6f7f9; stroke-width: 2; }
.lc-segment-label { fill: #1a212b; font: 600 0.72rem sans-serif; }
.lc-hub-label { fill: #4d5762; font: 600 0.85rem sans-serif; }
.lc-arrow-arc { fill: none; stroke: #4d5762; stroke-width: 2; }
.lc-arrow-head { fill: #4d5762; }
.lc-arrow-label { fill: #4d5762; font: 600 0.6rem sans-serif; }
"""


def _polar(radius: float, deg: float) -> tuple[float, float]:
    rad = math.radians(deg)
    return (WHEEL_CX + radius * math.cos(rad), WHEEL_CY + radius * math.sin(rad))


def _arc_path(start_deg: float, end_deg: float) -> str:
    o1, o2 = _polar(WHEEL_R_OUTER, start_deg), _polar(WHEEL_R_OUTER, end_deg)
    i1, i2 = _polar(WHEEL_R_INNER, start_deg), _polar(WHEEL_R_INNER, end_deg)
    return (f"M {o1[0]} {o1[1]} A {WHEEL_R_OUTER} {WHEEL_R_OUTER} 0 0 1 {o2[0]} {o2[1]} "
            f"L {i2[0]} {i2[1]} A {WHEEL_R_INNER} {WHEEL_R_INNER} 0 0 0 {i1[0]} {i1[1]} Z")


def _segment_label_svg(pos: tuple[float, float], label: str) -> str:
    words = label.split(" ")
    tspans = []
    for i, word in enumerate(words):
        dy = f"{-((len(words) - 1) * 0.55)}em" if i == 0 else "1.1em"
        tspans.append(f'<tspan x="{pos[0]}" dy="{dy}">{escape(word)}</tspan>')
    return (f'<text x="{pos[0]}" y="{pos[1]}" class="lc-segment-label" '
            f'text-anchor="middle" aria-hidden="true">{"".join(tspans)}</text>')


def _handoff_arrow_svg(tail_deg: float, tip_deg: float, radius: float,
                       label_text: str, label_radius: float) -> str:
    while tip_deg < tail_deg:
        tip_deg += 360
    tail, tip = _polar(radius, tail_deg), _polar(radius, tip_deg)
    arc = (f'<path class="lc-arrow-arc" d="M {tail[0]} {tail[1]} '
           f'A {radius} {radius} 0 0 1 {tip[0]} {tip[1]}"></path>')
    p1, p2, p3 = _polar(radius + 6, tip_deg - 6), _polar(radius - 6, tip_deg - 6), _polar(radius, tip_deg + 5)
    head = (f'<polygon class="lc-arrow-head" points="{p1[0]},{p1[1]} {p2[0]},{p2[1]} {p3[0]},{p3[1]}">'
            f'</polygon>')
    mid_deg = (tail_deg + tip_deg) / 2
    label_pos = _polar(label_radius, mid_deg)
    label = (f'<text x="{label_pos[0]}" y="{label_pos[1]}" class="lc-arrow-label" '
             f'text-anchor="middle" aria-hidden="true">{escape(label_text)}</text>')
    return arc + head + label


def generate_lifecycle_wheel_svg() -> str:
    """A complete, standalone rendering of the lifecycle wheel — six stage
    segments, their labels, and the three handoff arrows — matching what the
    live page's script draws at runtime, with colors inlined so it renders
    correctly with no external stylesheet."""
    step = 360 / len(WHEEL_STAGES)
    segments, labels = [], []
    for i, (_slug, label) in enumerate(WHEEL_STAGES):
        start = -90 + i * step
        end = start + step
        segments.append(f'<path class="lc-segment" d="{_arc_path(start, end)}"></path>')
        labels.append(_segment_label_svg(_polar((WHEEL_R_OUTER + WHEEL_R_INNER) / 2, start + step / 2), label))

    def stage_index(slug: str) -> int:
        return next(i for i, (s, _l) in enumerate(WHEEL_STAGES) if s == slug)

    outer_r, outer_label_r = WHEEL_R_OUTER + 14, WHEEL_R_OUTER + 22
    seam = stage_index("plan") * step - 90
    retire_seam = stage_index("retire") * step - 90
    optimize_start = stage_index("optimize") * step - 90
    plan_end = (stage_index("plan") + 1) * step - 90
    arrows = (
        _handoff_arrow_svg(seam - 10, seam + 10, outer_r, "closes the loop", outer_label_r)
        + _handoff_arrow_svg(retire_seam - 10, retire_seam + 10, outer_r, "retire branch", outer_label_r)
        + _handoff_arrow_svg(optimize_start + 10, plan_end - 10, WHEEL_R_INNER - 22,
                             "reinvest or replace", WHEEL_R_INNER - 34)
    )

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" class="lc-wheel" viewBox="0 0 400 400" '
        'role="img" aria-label="Application lifecycle stages">'
        f"<style>{WHEEL_STYLE}</style>"
        f'<circle cx="{WHEEL_CX}" cy="{WHEEL_CY}" r="{WHEEL_R_OUTER}" class="lc-wheel-ring"></circle>'
        f'<g>{"".join(segments)}</g>'
        f'<g>{"".join(labels)}</g>'
        f"<g>{arrows}</g>"
        f'<text x="{WHEEL_CX}" y="{WHEEL_CY}" class="lc-hub-label" text-anchor="middle" '
        f'dominant-baseline="middle">Lifecycle</text>'
        "</svg>"
    )
    return f'<?xml version="1.0" encoding="UTF-8"?>\n{svg}\n'

PRINT_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="../style.css">
</head>
<body>
<main class="print-page">
<h1>{title}</h1>
{body}
</main>
</body>
</html>
"""


class DownloadsError(Exception):
    pass


def _clean_cell(cell: str) -> str:
    cell = LINK_RE.sub(r"\1", cell).strip()
    if cell.startswith("✓"):  # ✓
        cell = "yes" + cell[1:]
    return cell


def extract_md_table(md_text: str, heading: str) -> list[list[str]]:
    """Return [header, *data_rows] for the first `|`-delimited table under `## heading`."""
    lines = md_text.splitlines()
    start = next((i for i, l in enumerate(lines) if l.strip() == f"## {heading}"), None)
    if start is None:
        raise DownloadsError(f"no '## {heading}' heading found")
    table_lines = []
    for line in lines[start + 1:]:
        stripped = line.strip()
        if stripped.startswith("|"):
            table_lines.append(stripped)
        elif table_lines:
            break
    if len(table_lines) < 3:
        raise DownloadsError(f"no table found under '## {heading}'")
    rows = [[_clean_cell(c) for c in line.strip("|").split("|")] for line in table_lines]
    header, _separator, *data = rows
    return [header] + data


def rows_to_csv(rows: list[list[str]]) -> str:
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    return buf.getvalue()


def cert_comparison_csv(md_text: str) -> str:
    return rows_to_csv(extract_md_table(md_text, "Certification comparison"))


def cert_task_matrix_csv(md_text: str) -> str:
    return rows_to_csv(extract_md_table(md_text, "Cross-certification task matrix"))


def _find_wheel_svg(html_text: str) -> str:
    m = WHEEL_SVG_RE.search(html_text)
    if not m:
        raise DownloadsError("no lc-wheel svg found")
    return m.group(0)


def extract_lifecycle_wheel_svg(html_text: str) -> str:
    svg = _find_wheel_svg(html_text)
    open_tag_end = svg.index(">")
    if "xmlns=" not in svg[:open_tag_end]:
        svg = svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n{svg}\n'


def print_page_html(title: str, body: str) -> str:
    """A standalone page with no nav/sidebar/hero, so opening it and printing (Cmd/Ctrl+P)
    prints only the one visual it contains."""
    return PRINT_PAGE_TEMPLATE.format(title=escape(title), body=body)


def csv_to_html_table(csv_text: str, caption: str) -> str:
    rows = list(csv.reader(io.StringIO(csv_text)))
    if not rows:
        return ""
    header, *data = rows
    thead = "<tr>" + "".join(f"<th>{escape(c)}</th>" for c in header) + "</tr>"
    tbody = "".join("<tr>" + "".join(f"<td>{escape(c)}</td>" for c in row) + "</tr>" for row in data)
    return f"<table><caption>{escape(caption)}</caption><thead>{thead}</thead><tbody>{tbody}</tbody></table>"


def cert_comparison_print_html(csv_text: str) -> str:
    title = "Certification comparison"
    return print_page_html(title, csv_to_html_table(csv_text, title))


def cert_task_matrix_print_html(csv_text: str) -> str:
    title = "Cross-certification task matrix"
    return print_page_html(title, csv_to_html_table(csv_text, title))


def crosswalk_print_html(csv_text: str) -> str:
    title = "Crosswalk data"
    return print_page_html(title, csv_to_html_table(csv_text, title))


def lifecycle_impact_print_html(csv_text: str) -> str:
    title = "Lifecycle impact data"
    return print_page_html(title, csv_to_html_table(csv_text, title))


def lifecycle_wheel_print_html(svg: str) -> str:
    return print_page_html("Lifecycle wheel diagram", f'<div class="lc-wheel-print">{svg}</div>')


def write_downloads(root: Path) -> list[str]:
    """Generate site/downloads/* from the repo's single sources of truth. Best-effort:
    a missing or unparsable source produces a warning, not a build error, since these
    downloads are a static convenience layered on top of pages that already work without them."""
    warnings: list[str] = []
    site = root / "site"
    if not site.is_dir():
        return warnings
    out = site / "downloads"
    out.mkdir(parents=True, exist_ok=True)
    written: list[str] = []  # filenames actually written, for the zip bundle

    crosswalk_csv_path = root / "methods" / "crosswalk" / "crosswalk.csv"
    crosswalk_csv_text = None
    if crosswalk_csv_path.is_file():
        crosswalk_csv_text = crosswalk_csv_path.read_text(encoding="utf-8")
        (out / "crosswalk.csv").write_text(crosswalk_csv_text, encoding="utf-8")
        written.append("crosswalk.csv")

    lifecycle_impact_csv_path = root / "methods" / "crosswalk" / "lifecycle-impact.csv"
    lifecycle_impact_csv_text = None
    if lifecycle_impact_csv_path.is_file():
        lifecycle_impact_csv_text = lifecycle_impact_csv_path.read_text(encoding="utf-8")
        (out / "lifecycle-impact.csv").write_text(lifecycle_impact_csv_text, encoding="utf-8")
        written.append("lifecycle-impact.csv")

    if crosswalk_csv_text is not None:
        (out / "crosswalk-print.html").write_text(crosswalk_print_html(crosswalk_csv_text), encoding="utf-8")
        written.append("crosswalk-print.html")
    if lifecycle_impact_csv_text is not None:
        (out / "lifecycle-impact-print.html").write_text(
            lifecycle_impact_print_html(lifecycle_impact_csv_text), encoding="utf-8")
        written.append("lifecycle-impact-print.html")

    certifications_md = root / "field-guide" / "certifications.md"
    if certifications_md.is_file():
        text = certifications_md.read_text(encoding="utf-8")
        try:
            comparison_csv = cert_comparison_csv(text)
            task_matrix_csv = cert_task_matrix_csv(text)
        except DownloadsError as e:
            warnings.append(f"downloads: certifications.md: {e}")
        else:
            (out / "cert-comparison.csv").write_text(comparison_csv, encoding="utf-8")
            (out / "cert-task-matrix.csv").write_text(task_matrix_csv, encoding="utf-8")
            (out / "cert-comparison-print.html").write_text(
                cert_comparison_print_html(comparison_csv), encoding="utf-8")
            (out / "cert-task-matrix-print.html").write_text(
                cert_task_matrix_print_html(task_matrix_csv), encoding="utf-8")
            written += ["cert-comparison.csv", "cert-task-matrix.csv",
                        "cert-comparison-print.html", "cert-task-matrix-print.html"]

    svg = generate_lifecycle_wheel_svg()
    (out / "lifecycle-wheel.svg").write_text(svg, encoding="utf-8")
    (out / "lifecycle-wheel-print.html").write_text(lifecycle_wheel_print_html(svg), encoding="utf-8")
    written += ["lifecycle-wheel.svg", "lifecycle-wheel-print.html"]

    if written:
        # A fixed date_time (not each file's real mtime, which changes on every
        # build) keeps the zip's bytes reproducible, so `git diff` sees a real
        # content change and nothing else -- not every CI run touching this file.
        with zipfile.ZipFile(out / "all-visuals.zip", "w", zipfile.ZIP_DEFLATED) as z:
            for name in written:
                info = zipfile.ZipInfo(filename=name, date_time=(2020, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, (out / name).read_bytes())

    return warnings
