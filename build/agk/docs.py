"""Publish the kit's Markdown documents and CSV templates as site pages.

Each source becomes an HTML page with the site header and footer, plus the downloads that make
sense for it: Word (.docx) for documents, Excel (.xlsx) and CSV for anything with a table. A
"Print or save as PDF" button uses the browser's own print dialog. Standard library only.
No Markdown file is linked from the site."""
import csv
import io
import os
import re
import zipfile
from html import escape
from pathlib import Path

GITHUB = "https://github.com/evemcgivern/app-governance-kit/blob/main/"
FIXED_DATE = (2020, 1, 1, 0, 0, 0)
CHOICE_HEADER = "yes / partly / no"
TALLY_CAPTION = "Work out your tier"
CHOICES = ("Yes", "Partly", "No")
TEXT_WIDTH = 10080  # twips: US Letter with 0.75 inch margins


class DocsError(Exception):
    pass


# ---------- Markdown parsing ----------

LIST_RE = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")
FILE_RE = re.compile(r"^[\w./-]+\.(md|csv)$")
INLINE_RE = re.compile(
    r"`(?P<code>[^`]+)`"
    r"|\[\[(?P<xw>XW-\d{3})\]\]"
    r"|\[(?P<ltext>[^\]]+)\]\((?P<href>[^)]*)\)"
    r"|\*\*(?P<bold>[^*]+)\*\*"
    r"|\*(?P<ital>[^*\s][^*]*)\*")


def parse_markdown(text: str) -> list[dict]:
    """Blocks: heading {level, text}, p {text}, list {ordered, items}, table {rows}.
    A list item is {text, checked, children}; checked is None unless the item starts with [ ] or [x]."""
    blocks: list[dict] = []
    para: list[str] = []
    table: list[list[str]] = []
    items: list[tuple[int, dict, bool]] = []  # (indent, item, ordered) flat, nested later

    def flush_para():
        if para:
            blocks.append({"type": "p", "text": " ".join(para)})
            para.clear()

    def flush_table():
        if table:
            blocks.append({"type": "table", "rows": [r for r in table]})
            table.clear()

    def flush_list():
        if not items:
            return
        top: list[dict] = []
        stack: list[tuple[int, dict]] = []
        for indent, item, _ in items:
            while stack and stack[-1][0] >= indent:
                stack.pop()
            (stack[-1][1]["children"] if stack else top).append(item)
            stack.append((indent, item))
        blocks.append({"type": "list", "ordered": items[0][2], "items": top})
        items.clear()

    lines = text.splitlines()
    if lines and lines[0].strip() == "---":  # front matter
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        if end is not None:
            lines = lines[end + 1:]
    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if stripped.startswith("|"):
            flush_para(); flush_list()
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if all(c and set(c) <= set("-: ") for c in cells):
                continue
            table.append(cells)
            continue
        flush_table()
        m = LIST_RE.match(line)
        if m and not (stripped.startswith("**") and not stripped.startswith("* ")):
            flush_para()
            body = m.group(3)
            checked = None
            cm = re.match(r"\[( |x|X)\]\s+(.*)$", body)
            if cm:
                checked, body = cm.group(1) != " ", cm.group(2)
            ordered = m.group(2)[0].isdigit()
            if items and len(m.group(1)) <= items[0][0] and items[0][2] != ordered:
                flush_list()  # a bulleted list after a numbered one (or the reverse) starts a new list
            items.append((len(m.group(1)), {"text": body, "checked": checked, "children": []}, ordered))
            continue
        if items and line.startswith(" ") and stripped:  # continuation of the last item
            items[-1][1]["text"] += " " + stripped
            continue
        flush_list()
        if not stripped:
            flush_para()
        elif stripped.startswith("#"):
            flush_para()
            level = len(stripped) - len(stripped.lstrip("#"))
            blocks.append({"type": "heading", "level": min(level, 4), "text": stripped[level:].strip()})
        elif stripped == "---":
            flush_para()
        else:
            para.append(stripped)
    flush_para(); flush_list(); flush_table()
    return blocks


def front_title(text: str) -> str | None:
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for line in lines[1:]:
            if line.strip() == "---":
                break
            if line.startswith("title:"):
                return line.split(":", 1)[1].strip()
    return None


def title_of(blocks: list[dict]) -> str:
    for b in blocks:
        if b["type"] == "heading" and b["level"] == 1:
            return b["text"]
    raise DocsError("no '# ' title found")


def summary_of(blocks: list[dict], max_words: int = 14) -> str:
    for b in blocks:
        if b["type"] == "p":
            text = re.sub(r"\[\[[^\]]+\]\]|[`*]", "", b["text"])
            text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
            words = text.split()
            return text if len(words) <= max_words else " ".join(words[:max_words]).rstrip(".,;:") + "…"
    return ""


def csv_blocks(text: str, title: str) -> list[dict]:
    rows = [r for r in csv.reader(io.StringIO(text))]
    return [{"type": "heading", "level": 1, "text": title}, {"type": "table", "rows": rows}]


def inline_tokens(text: str, flags: tuple = ()) -> list[tuple]:
    """Tokens: ("t", text, flags), ("a", text, href), ("xw", id)."""
    out: list[tuple] = []
    pos = 0
    for m in INLINE_RE.finditer(text):
        if m.start() > pos:
            out.append(("t", text[pos:m.start()], flags))
        if m.group("code") is not None:
            out.append(("t", m.group("code"), flags + ("code",)))
        elif m.group("xw"):
            out.append(("xw", m.group("xw")))
        elif m.group("ltext") is not None:
            out.append(("a", m.group("ltext"), m.group("href")))
        elif m.group("bold") is not None:
            out += inline_tokens(m.group("bold"), flags + ("b",))
        else:
            out += inline_tokens(m.group("ital"), flags + ("i",))
        pos = m.end()
    if pos < len(text):
        out.append(("t", text[pos:], flags))
    return out


def _choice_col(header: list[str]) -> int | None:
    for i, h in enumerate(header):
        if h.strip().lower() == CHOICE_HEADER:
            return i
    return None


MD_NAME_RE = re.compile(r"[\w./-]+\.md\b")


def unmark(text: str, files=lambda name: None) -> str:
    """Replace Markdown file names in text with the document's title, or a readable name."""
    def sub(m):
        named = files(m.group(0))
        return named[1] if named else humanize(os.path.basename(m.group(0))[:-3])
    return MD_NAME_RE.sub(sub, text)


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


# ---------- HTML ----------

def inline_html(text: str, resolve, files=lambda name: None) -> str:
    """`resolve(href)` returns the href to use, or None to show the link text only."""
    out = []
    for tok in inline_tokens(text):
        if tok[0] == "t":
            s = escape(tok[1] if "code" in tok[2] else unmark(tok[1], files))
            if "code" in tok[2]:
                named = files(tok[1]) if FILE_RE.match(tok[1]) else None
                if named:
                    s = f"<a href=\"{escape(named[0])}\">{escape(named[1])}</a>"
                elif tok[1].endswith(".md"):
                    s = escape(humanize(os.path.basename(tok[1])[:-3]))
                else:
                    s = f"<code>{s}</code>"
            if "b" in tok[2]:
                s = f"<strong>{s}</strong>"
            if "i" in tok[2]:
                s = f"<em>{s}</em>"
            out.append(s)
        elif tok[0] == "xw":
            out.append(f"<a class=\"xw-tag\" href=\"{escape(resolve('xw:' + tok[1]) or '#')}\">{tok[1]}</a>")
        else:
            href = resolve(tok[2])
            label = unmark(tok[1].replace("`", ""), files)
            out.append(f"<a href=\"{escape(href)}\">{escape(label)}</a>" if href else escape(label))
    return "".join(out)


def _list_html(block: dict, resolve, files) -> str:
    tag = "ol" if block["ordered"] else "ul"

    def items(its):
        parts = []
        for it in its:
            box = ""
            if it["checked"] is not None:
                box = "<input type=\"checkbox\" disabled" + (" checked" if it["checked"] else "") + "> "
            kids = ""
            if it["children"]:
                kids = f"<{tag}>{items(it['children'])}</{tag}>"
            parts.append(f"<li>{box}{inline_html(it['text'], resolve, files)}{kids}</li>")
        return "".join(parts)
    cls = " class=\"checklist-items\"" if any(i["checked"] is not None for i in block["items"]) else ""
    return f"<{tag}{cls}>{items(block['items'])}</{tag}>"


def _table_html(rows: list[list[str]], resolve, files, caption: str = "", index: int = 0) -> str:
    header, *data = rows
    choice = _choice_col(header)
    cap = f"<caption>{escape(caption)}</caption>" if caption else ""
    attrs = ""
    tm = re.match(r"Tier (\d)\b", caption)
    if tm and choice is not None:
        attrs = f" data-tier=\"{tm.group(1)}\""
    elif caption == TALLY_CAPTION:
        attrs = " data-tally"
    head = "".join(f"<th scope=\"col\">{escape(h)}</th>" for h in header)
    body = []
    for row in data:
        cells = []
        key = slug(row[0]) if row else str(len(body))
        for i in range(len(header)):
            cell = row[i] if i < len(row) else ""
            if i == choice:
                boxes = "".join(
                    f"<label class=\"checklist-choice\"><input type=\"radio\" name=\"q{index}-{key}\" "
                    f"value=\"{c}\"> {c}</label>" for c in CHOICES)
                cells.append(f"<td class=\"checklist-choices\">{boxes}</td>")
            elif cell:
                cells.append(f"<td>{inline_html(cell, resolve, files)}</td>")
            else:
                cells.append("<td class=\"checklist-write\"></td>")
        body.append("<tr>" + "".join(cells) + "</tr>")
    return (f"<div class=\"table-scroll\"><table class=\"checklist\"{attrs}>{cap}<thead><tr>{head}</tr></thead>"
            f"<tbody>{''.join(body)}</tbody></table></div>")


def body_html(blocks: list[dict], resolve, files=lambda name: None) -> str:
    parts = []
    last_heading = ""
    tables = 0
    for b in blocks:
        t = b["type"]
        if t == "heading":
            if b["level"] == 1:
                continue
            last_heading = unmark(b["text"], files)
            lvl = b["level"]
            parts.append(f"<h{lvl} id=\"{slug(last_heading)}\">{escape(last_heading)}</h{lvl}>")
        elif t == "p":
            parts.append(f"<p>{inline_html(b['text'], resolve, files)}</p>")
        elif t == "list":
            parts.append(_list_html(b, resolve, files))
        else:
            tables += 1
            parts.append(_table_html(b["rows"], resolve, files, last_heading, tables))
    return "\n".join(parts)


# ---------- Word ----------

W_NS = ("xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\" "
        "xmlns:w14=\"http://schemas.microsoft.com/office/word/2010/wordml\" "
        "xmlns:mc=\"http://schemas.openxmlformats.org/markup-compatibility/2006\" "
        "mc:Ignorable=\"w14\"")
XML_HEAD = "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
CONTENT_TYPES = (
    XML_HEAD + "<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\">"
    "<Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/>"
    "<Default Extension=\"xml\" ContentType=\"application/xml\"/>"
    "<Override PartName=\"/word/document.xml\" "
    "ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml\"/>"
    "<Override PartName=\"/word/styles.xml\" "
    "ContentType=\"application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml\"/></Types>")
ROOT_RELS = (
    XML_HEAD + "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">"
    "<Relationship Id=\"rId1\" "
    "Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" "
    "Target=\"word/document.xml\"/></Relationships>")
DOC_RELS = (
    XML_HEAD + "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">"
    "<Relationship Id=\"rId1\" "
    "Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles\" "
    "Target=\"styles.xml\"/></Relationships>")


def _heading_style(level: int, size: int) -> str:
    name = "Title" if level == 1 else f"Heading{level}"
    label = "Title" if level == 1 else f"heading {level}"
    outline = "" if level == 1 else f"<w:outlineLvl w:val=\"{level - 1}\"/>"
    before = "0" if level == 1 else "280"
    return (f"<w:style w:type=\"paragraph\" w:styleId=\"{name}\"><w:name w:val=\"{label}\"/>"
            "<w:basedOn w:val=\"Normal\"/><w:next w:val=\"Normal\"/><w:qFormat/>"
            f"<w:pPr><w:keepNext/><w:spacing w:before=\"{before}\" w:after=\"120\"/>{outline}</w:pPr>"
            f"<w:rPr><w:b/><w:sz w:val=\"{size}\"/></w:rPr></w:style>")


STYLES = (
    XML_HEAD + "<w:styles xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\">"
    "<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii=\"Calibri\" w:hAnsi=\"Calibri\" w:cs=\"Calibri\"/>"
    "<w:sz w:val=\"22\"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr>"
    "<w:spacing w:after=\"120\" w:line=\"264\" w:lineRule=\"auto\"/></w:pPr></w:pPrDefault></w:docDefaults>"
    "<w:style w:type=\"paragraph\" w:default=\"1\" w:styleId=\"Normal\"><w:name w:val=\"Normal\"/></w:style>"
    + _heading_style(1, 44) + _heading_style(2, 30) + _heading_style(3, 26) + _heading_style(4, 24)
    + "</w:styles>")


def _x(text: str) -> str:
    return escape(text, quote=False)


def _run(text: str, flags: tuple = ()) -> str:
    props = ""
    if "code" in flags:
        props += "<w:rFonts w:ascii=\"Consolas\" w:hAnsi=\"Consolas\"/>"
    if "b" in flags:
        props += "<w:b/>"
    if "i" in flags:
        props += "<w:i/>"
    rpr = f"<w:rPr>{props}</w:rPr>" if props else ""
    return f"<w:r>{rpr}<w:t xml:space=\"preserve\">{_x(text)}</w:t></w:r>"


def _runs(text: str, plain_link, files=lambda name: None) -> str:
    out = []
    for tok in inline_tokens(text):
        if tok[0] == "t":
            if "code" in tok[2] and FILE_RE.match(tok[1]):
                named = files(tok[1])
                if named:
                    out.append(_run(named[1], tuple(f for f in tok[2] if f != "code")))
                    continue
                if tok[1].endswith(".md"):
                    out.append(_run(humanize(os.path.basename(tok[1])[:-3]), tuple(f for f in tok[2] if f != "code")))
                    continue
            out.append(_run(tok[1] if "code" in tok[2] else unmark(tok[1], files), tok[2]))
        elif tok[0] == "xw":
            out.append(_run(tok[1], ("b",)))
        else:
            out.append(_run(unmark(tok[1].replace("`", ""), files)))
            url = plain_link(tok[2])
            if url:
                out.append(_run(f" ({url})"))
    return "".join(out)


def _para(inner: str, style: str | None = None, after: int | None = None, indent: tuple | None = None) -> str:
    props = ""
    if style:
        props += f"<w:pStyle w:val=\"{style}\"/>"
    if after is not None:
        props += f"<w:spacing w:after=\"{after}\"/>"
    if indent:
        props += f"<w:ind w:left=\"{indent[0]}\" w:hanging=\"{indent[1]}\"/>"
    ppr = f"<w:pPr>{props}</w:pPr>" if props else ""
    return f"<w:p>{ppr}{inner}</w:p>"


def _checkbox(checked: bool = False) -> str:
    glyph = "☒" if checked else "☐"
    return (
        "<w:sdt><w:sdtPr><w14:checkbox>"
        f"<w14:checked w14:val=\"{1 if checked else 0}\"/>"
        "<w14:checkedState w14:val=\"2612\" w14:font=\"MS Gothic\"/>"
        "<w14:uncheckedState w14:val=\"2610\" w14:font=\"MS Gothic\"/></w14:checkbox></w:sdtPr>"
        "<w:sdtContent><w:r><w:rPr><w:rFonts w:ascii=\"MS Gothic\" w:eastAsia=\"MS Gothic\" "
        f"w:hAnsi=\"MS Gothic\" w:hint=\"eastAsia\"/></w:rPr><w:t>{glyph}</w:t></w:r></w:sdtContent></w:sdt>")


def _list_xml(block: dict, plain_link, files, depth: int = 0, items=None) -> str:
    out = []
    for n, it in enumerate(items if items is not None else block["items"], 1):
        left = 360 * (depth + 1)
        if it["checked"] is not None:
            marker = _checkbox(it["checked"]) + _run(" ")
        else:
            marker = _run(f"{n}." if block["ordered"] else "•") + "<w:r><w:tab/></w:r>"
        out.append(_para(marker + _runs(it["text"], plain_link, files), after=60, indent=(left + 360, 360)))
        if it["children"]:
            out.append(_list_xml(block, plain_link, files, depth + 1, it["children"]))
    return "".join(out)


def _widths(header: list[str]) -> list[int]:
    if [h.strip().lower() for h in header] == ["#", "question", CHOICE_HEADER, "evidence"]:
        return [600, 4500, 1700, 3280]
    n = max(len(header), 1)
    base = TEXT_WIDTH // n
    return [base] * (n - 1) + [TEXT_WIDTH - base * (n - 1)]


def _cell(width: int, inner: str, shade: bool = False) -> str:
    shd = "<w:shd w:val=\"clear\" w:color=\"auto\" w:fill=\"D9E2E7\"/>" if shade else ""
    return f"<w:tc><w:tcPr><w:tcW w:w=\"{width}\" w:type=\"dxa\"/>{shd}</w:tcPr>{inner}</w:tc>"


def _table_xml(rows: list[list[str]], plain_link, files) -> str:
    header, *data = rows
    widths = _widths(header)
    choice = _choice_col(header)
    borders = "".join(f"<w:{s} w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"808080\"/>"
                      for s in ("top", "left", "bottom", "right", "insideH", "insideV"))
    grid = "".join(f"<w:gridCol w:w=\"{w}\"/>" for w in widths)
    out = [f"<w:tbl><w:tblPr><w:tblW w:w=\"{TEXT_WIDTH}\" w:type=\"dxa\"/><w:tblBorders>{borders}</w:tblBorders>"
           "<w:tblLayout w:type=\"fixed\"/><w:tblCellMar><w:top w:w=\"60\" w:type=\"dxa\"/>"
           "<w:left w:w=\"100\" w:type=\"dxa\"/><w:bottom w:w=\"60\" w:type=\"dxa\"/>"
           f"<w:right w:w=\"100\" w:type=\"dxa\"/></w:tblCellMar></w:tblPr><w:tblGrid>{grid}</w:tblGrid>"]
    head = "".join(_cell(w, _para(_run(h, ("b",)), after=0), True) for h, w in zip(header, widths))
    out.append(f"<w:tr><w:trPr><w:cantSplit/><w:tblHeader/></w:trPr>{head}</w:tr>")
    for row in data:
        cells = []
        for i, w in enumerate(widths):
            cell = row[i] if i < len(row) else ""
            if i == choice:
                inner = "".join(_para(_checkbox() + _run(" " + c), after=40) for c in CHOICES)
            else:
                inner = _para(_runs(cell, plain_link, files), after=0)
            cells.append(_cell(w, inner))
        out.append("<w:tr><w:trPr><w:cantSplit/><w:trHeight w:val=\"480\" w:hRule=\"atLeast\"/></w:trPr>"
                   + "".join(cells) + "</w:tr>")
    out.append("</w:tbl>")
    return "".join(out)


def docx_bytes(blocks: list[dict], plain_link=lambda href: None, files=lambda name: None) -> bytes:
    """A .docx with real Word tick boxes. Fixed timestamps keep rebuilds byte-identical."""
    body = []
    for b in blocks:
        t = b["type"]
        if t == "heading":
            style = "Title" if b["level"] == 1 else f"Heading{b['level']}"
            body.append(_para(_run(unmark(b["text"], files)), style=style))
        elif t == "p":
            body.append(_para(_runs(b["text"], plain_link, files)))
        elif t == "list":
            body.append(_list_xml(b, plain_link, files))
        else:
            body.append(_table_xml(b["rows"], plain_link, files))
            body.append(_para("", after=0))
    sect = ("<w:sectPr><w:pgSz w:w=\"12240\" w:h=\"15840\"/><w:pgMar w:top=\"1080\" w:right=\"1080\" "
            "w:bottom=\"1080\" w:left=\"1080\" w:header=\"720\" w:footer=\"720\" w:gutter=\"0\"/></w:sectPr>")
    document = XML_HEAD + f"<w:document {W_NS}><w:body>{''.join(body)}{sect}</w:body></w:document>"
    return _zip((("[Content_Types].xml", CONTENT_TYPES), ("_rels/.rels", ROOT_RELS),
                 ("word/document.xml", document), ("word/_rels/document.xml.rels", DOC_RELS),
                 ("word/styles.xml", STYLES)))


# ---------- Excel ----------

def _col_letter(i: int) -> str:
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def _sheet_names(blocks: list[dict]) -> list[tuple[str, list[list[str]]]]:
    """One sheet per table, named after the heading above it (the part before a colon)."""
    sheets, used, heading = [], set(), "Sheet"
    for b in blocks:
        if b["type"] == "heading" and b["level"] > 1:
            heading = b["text"]
        elif b["type"] == "table":
            name = re.sub(r"[\[\]:*?/\\\"']", "", heading.split(":")[0]).strip()[:31] or "Sheet"
            base, n = name, 2
            while name.lower() in used:
                name = f"{base[:28]} {n}"
                n += 1
            used.add(name.lower())
            sheets.append((name, b["rows"]))
    return sheets


def tier_rule(yes: int, partly: int, no: int, total: int) -> str:
    """Met, Not met, or Incomplete. The one rule the page, the workbook, and the Word tally share."""
    if yes + partly + no < total:
        return "Incomplete"
    return "Met" if no == 0 and partly <= 1 else "Not met"


def _tier_summary_xml(tiers: list[tuple[str, str, int]]) -> str:
    """Summary sheet for the tier self-assessment: counts and status per tier sheet, then the assumed
    tier. `tiers` holds (sheet name, answer column letter, number of questions)."""
    def cell(ref, text=None, formula=None, style=0):
        if formula is not None:
            return f"<c r=\"{ref}\" t=\"str\" s=\"{style}\"><f>{escape(formula, quote=False)}</f><v></v></c>"
        return f"<c r=\"{ref}\" t=\"inlineStr\" s=\"{style}\"><is><t xml:space=\"preserve\">{_x(text)}</t></is></c>"

    rows = ["<row r=\"1\">" + "".join(cell(f"{c}1", h, style=1) for c, h in zip(
        "ABCDEFG", ("Tier", "Questions", "Yes", "Partly", "No", "Answered", "Status"))) + "</row>"]
    for i, (name, col, count) in enumerate(tiers, 2):
        rng = f"'{name}'!{col}2:{col}{count + 1}"
        rows.append(
            f"<row r=\"{i}\">" + cell(f"A{i}", name) + f"<c r=\"B{i}\"><v>{count}</v></c>"
            + "".join(cell(f"{c}{i}", formula=f"COUNTIF({rng},\"{w}\")") for c, w in zip("CDE", CHOICES))
            + cell(f"F{i}", formula=f"C{i}+D{i}+E{i}")
            + cell(f"G{i}", formula=f"IF(F{i}<B{i},\"Incomplete\",IF(AND(E{i}=0,D{i}<=1),\"Met\",\"Not met\"))")
            + "</row>")
    last = len(tiers) + 1
    g = f"G2:G{last}"
    nest_assumed = "\"Tier " + str(len(tiers)) + "\""
    for i in range(len(tiers), 0, -1):
        nest_assumed = f"IF(G{i + 1}<>\"Met\",\"{'Below tier 1' if i == 1 else 'Tier ' + str(i - 1)}\",{nest_assumed})"
    nest_next = f"\"None: every tier is met\""
    for i in range(len(tiers), 0, -1):
        nest_next = f"IF(G{i + 1}<>\"Met\",\"Tier {i}\",{nest_next})"
    r1, r2 = last + 2, last + 3
    rows.append(f"<row r=\"{r1}\">" + cell(f"A{r1}", "Assumed tier", style=1)
                + cell(f"B{r1}", formula=f"IF(COUNTIF({g},\"Incomplete\")>0,\"Answer every question to see your tier\",{nest_assumed})",
                       style=1) + "</row>")
    rows.append(f"<row r=\"{r2}\">" + cell(f"A{r2}", "Next piece of work", style=1)
                + cell(f"B{r2}", formula=f"IF(COUNTIF({g},\"Incomplete\")>0,\"\",{nest_next})") + "</row>")
    rows.append(f"<row r=\"{r2 + 2}\">" + cell(
        f"A{r2 + 2}", "A tier is met when no answer is No and at most one is Partly. Your assumed tier is the highest "
        "tier you meet, with every tier below it also met.") + "</row>")
    return ("<worksheet xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\">"
            "<cols><col min=\"1\" max=\"1\" width=\"22\" customWidth=\"1\"/><col min=\"2\" max=\"7\" width=\"16\" "
            f"customWidth=\"1\"/></cols><sheetData>{''.join(rows)}</sheetData></worksheet>")


def _data_sheet_xml(rows: list[list[str]]) -> str:
    header = rows[0]
    choice = _choice_col(header)
    ncols = max(len(r) for r in rows)
    cols = "".join(
        f"<col min=\"{c + 1}\" max=\"{c + 1}\" width=\"{_width_for(rows, c)}\" customWidth=\"1\"/>"
        for c in range(ncols))
    sheet_rows = []
    for r, row in enumerate(rows, 1):
        cells = "".join(
            f"<c r=\"{_col_letter(c)}{r}\" t=\"inlineStr\" s=\"{1 if r == 1 else 0}\">"
            f"<is><t xml:space=\"preserve\">{_x(_plain(v))}</t></is></c>" for c, v in enumerate(row))
        sheet_rows.append(f"<row r=\"{r}\">{cells}</row>")
    validation = ""
    if choice is not None and len(rows) > 1:
        col = _col_letter(choice)
        validation = (f"<dataValidations count=\"1\"><dataValidation type=\"list\" allowBlank=\"1\" "
                      f"showErrorMessage=\"1\" sqref=\"{col}2:{col}{len(rows)}\">"
                      f"<formula1>\"{','.join(CHOICES)}\"</formula1></dataValidation></dataValidations>")
    return ("<worksheet xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\">"
            "<sheetViews><sheetView workbookViewId=\"0\"><pane ySplit=\"1\" topLeftCell=\"A2\" "
            "activePane=\"bottomLeft\" state=\"frozen\"/></sheetView></sheetViews>"
            f"<cols>{cols}</cols><sheetData>{''.join(sheet_rows)}</sheetData>{validation}</worksheet>")


def xlsx_bytes(blocks: list[dict], tier_summary: bool = False) -> bytes:
    sheets = _sheet_names(blocks)
    if tier_summary:  # the Summary sheet replaces the by-hand tally
        sheets = [(n, r) for n, r in sheets if n != TALLY_CAPTION]
    if not sheets:
        raise DocsError("no table to put in a workbook")
    xml_sheets = [(name, XML_HEAD + _data_sheet_xml(rows)) for name, rows in sheets]
    if tier_summary:
        tiers = [(name, _col_letter(_choice_col(rows[0])), len(rows) - 1) for name, rows in sheets
                 if re.fullmatch(r"Tier \d", name) and _choice_col(rows[0]) is not None]
        if not tiers:
            raise DocsError("no tier sheets found for the summary")
        xml_sheets.insert(0, ("Summary", XML_HEAD + _tier_summary_xml(tiers)))
    n = len(xml_sheets)
    parts = [("[Content_Types].xml", (
        XML_HEAD + "<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\">"
        "<Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/>"
        "<Default Extension=\"xml\" ContentType=\"application/xml\"/>"
        "<Override PartName=\"/xl/workbook.xml\" "
        "ContentType=\"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml\"/>"
        "<Override PartName=\"/xl/styles.xml\" "
        "ContentType=\"application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml\"/>"
        + "".join(f"<Override PartName=\"/xl/worksheets/sheet{i}.xml\" "
                  "ContentType=\"application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml\"/>"
                  for i in range(1, n + 1)) + "</Types>")),
        ("_rels/.rels", (
            XML_HEAD + "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">"
            "<Relationship Id=\"rId1\" "
            "Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" "
            "Target=\"xl/workbook.xml\"/></Relationships>")),
        ("xl/workbook.xml", (
            XML_HEAD + "<workbook xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\" "
            "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\"><sheets>"
            + "".join(f"<sheet name=\"{escape(nm, quote=True)}\" sheetId=\"{i}\" r:id=\"rId{i}\"/>"
                      for i, (nm, _) in enumerate(xml_sheets, 1)) + "</sheets><calcPr fullCalcOnLoad=\"1\"/></workbook>")),
        ("xl/_rels/workbook.xml.rels", (
            XML_HEAD + "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">"
            + "".join(f"<Relationship Id=\"rId{i}\" "
                      "Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet\" "
                      f"Target=\"worksheets/sheet{i}.xml\"/>" for i in range(1, n + 1))
            + f"<Relationship Id=\"rId{n + 1}\" "
            "Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles\" "
            "Target=\"styles.xml\"/></Relationships>")),
        ("xl/styles.xml", (
            XML_HEAD + "<styleSheet xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\">"
            "<fonts count=\"2\"><font><sz val=\"11\"/><name val=\"Calibri\"/></font>"
            "<font><b/><sz val=\"11\"/><name val=\"Calibri\"/></font></fonts>"
            "<fills count=\"3\"><fill><patternFill patternType=\"none\"/></fill>"
            "<fill><patternFill patternType=\"gray125\"/></fill>"
            "<fill><patternFill patternType=\"solid\"><fgColor rgb=\"FFD9E2E7\"/></patternFill></fill></fills>"
            "<borders count=\"1\"><border><left/><right/><top/><bottom/><diagonal/></border></borders>"
            "<cellStyleXfs count=\"1\"><xf numFmtId=\"0\" fontId=\"0\" fillId=\"0\" borderId=\"0\"/></cellStyleXfs>"
            "<cellXfs count=\"2\"><xf numFmtId=\"0\" fontId=\"0\" fillId=\"0\" borderId=\"0\" xfId=\"0\" "
            "applyAlignment=\"1\"><alignment vertical=\"top\" wrapText=\"1\"/></xf>"
            "<xf numFmtId=\"0\" fontId=\"1\" fillId=\"2\" borderId=\"0\" xfId=\"0\" applyFont=\"1\" "
            "applyFill=\"1\" applyAlignment=\"1\"><alignment vertical=\"top\" wrapText=\"1\"/></xf></cellXfs>"
            "</styleSheet>"))]
    for i, (_, xml) in enumerate(xml_sheets, 1):
        parts.append((f"xl/worksheets/sheet{i}.xml", xml))
    return _zip(tuple(parts))


def _plain(text: str) -> str:
    text = re.sub(r"\[\[(XW-\d{3})\]\]", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    return re.sub(r"[`*]", "", text)


def _width_for(rows: list[list[str]], col: int) -> int:
    longest = max((len(_plain(r[col])) for r in rows if col < len(r)), default=8)
    return max(10, min(60, longest + 2))


def _zip(parts: tuple) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, xml in parts:
            info = zipfile.ZipInfo(filename=name, date_time=FIXED_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, xml.encode("utf-8"))
    return buf.getvalue()


# ---------- Site pages ----------

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Eve McGivern</title>
<meta name="description" content="{description}">
<meta name="author" content="Eve McGivern">
<link rel="icon" href="{up}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{up}apple-touch-icon.png">
<link rel="stylesheet" href="{up}style.css">
<script src="{up}nav.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{header}
<main id="main" class="doc-page">
  <p class="doc-back"><a href="{back_href}">&larr; {back_label}</a></p>
  <h1>{title}</h1>
  <div class="visual-actions doc-actions">
{actions}
  </div>
{extra}
  <div class="doc-body prose prose-wide">
{body}
  </div>
</main>
{footer}
</body>
</html>
"""

HREF_RE = re.compile(r"""(href|src)="(?!https?:|mailto:|#|data:|tel:)([^"]+)\"""")


def chrome(index_html: str, up: str) -> tuple[str, str]:
    """The site header (with the support bar) and footer, copied from the home page with
    relative links re-based so they work from a page `up` levels below the site root."""
    a = index_html.index("<div class=\"support-bar\">")
    b = index_html.index("</header>", a) + len("</header>")
    c = index_html.index("<footer class=\"site-footer\">")
    d = index_html.index("</body>", c)

    def rebase(m):
        return f"{m.group(1)}=\"{up}{m.group(2)}\""
    return HREF_RE.sub(rebase, index_html[a:b]), HREF_RE.sub(rebase, index_html[c:d])


TIER_EXTRA = """  <div class="tier-bar" role="status" aria-live="polite">
    <p><strong>Your assumed tier:</strong> <span id="tier-result">Answer every question to see your tier.</span></p>
    <button type="button" class="visual-actions__link" id="tier-clear">Clear answers</button>
  </div>
  <script>
document.addEventListener("DOMContentLoaded", function () {
  "use strict";
  var tiers = [].slice.call(document.querySelectorAll("table[data-tier]"));
  var tally = document.querySelector("table[data-tally]");
  var out = document.getElementById("tier-result");
  function count(table) {
    var rows = table.querySelectorAll("tbody tr"), c = {Yes: 0, Partly: 0, No: 0, total: rows.length};
    rows.forEach(function (r) { var x = r.querySelector("input:checked"); if (x) { c[x.value] += 1; } });
    return c;
  }
  // The rule: Met when every question is answered, none is No, and at most one is Partly.
  function status(c) {
    if (c.Yes + c.Partly + c.No < c.total) { return "Incomplete"; }
    return c.No === 0 && c.Partly <= 1 ? "Met" : "Not met";
  }
  function update() {
    var st = [], answered = 0, total = 0;
    tiers.forEach(function (t, i) {
      var c = count(t), s = status(c);
      st.push(s); answered += c.Yes + c.Partly + c.No; total += c.total;
      var row = tally && tally.querySelectorAll("tbody tr")[i];
      if (row) {
        var cells = row.querySelectorAll("td");
        cells[1].textContent = c.Yes; cells[2].textContent = c.Partly; cells[3].textContent = c.No; cells[4].textContent = s;
      }
    });
    if (st.indexOf("Incomplete") !== -1) {
      out.textContent = "Answer every question to see your tier (" + answered + " of " + total + " answered).";
      return;
    }
    if (!st.length) { return; }
    var met = 0;
    while (met < st.length && st[met] === "Met") { met += 1; }
    out.textContent = (met === 0 ? "Below tier 1" : "Tier " + met) +
      (met < st.length ? ". Your next piece of work is tier " + (met + 1) + "." : ". Every tier is met.");
  }
  document.addEventListener("change", update);
  document.getElementById("tier-clear").addEventListener("click", function () {
    document.querySelectorAll("table[data-tier] input:checked").forEach(function (i) { i.checked = false; });
    update();
  });
  update();
});
  </script>"""


def humanize(stem: str) -> str:
    return stem.replace("-", " ").replace("_", " ").capitalize()


class Doc:
    def __init__(self, src: Path, kind: str, group: str, name: str, back: tuple[str, str], title: str | None = None):
        self.src, self.kind, self.group, self.name, self.back, self._title = src, kind, group, name, back, title
        self.blocks: list[dict] = []
        self.title = ""

    @property
    def page(self) -> str:
        return f"docs/{self.group}/{self.name}.html"


def collect(root: Path) -> list[Doc]:
    docs: list[Doc] = []
    sam = root / "sam-toolkit"
    if sam.is_dir():
        back = ("sam-toolkit.html", "SAM toolkit")
        for f in sorted(sam.glob("*.md")):
            docs.append(Doc(f, "md", "sam-toolkit", f.stem, back))
        for f in sorted(sam.glob("*.csv")):
            docs.append(Doc(f, "csv", "sam-toolkit", f.stem, back, humanize(f.stem) + " template"))
        for f in sorted((sam / "examples").glob("*.csv")) if (sam / "examples").is_dir() else []:
            docs.append(Doc(f, "csv", "sam-toolkit", f.stem, back, humanize(f.stem)))
    methods = root / "methods"
    if methods.is_dir():
        back = ("tools.html", "Tools")
        for tool in sorted(p for p in methods.iterdir() if p.is_dir()):
            for name in ("method", "checklist", "sop", "template", "platform-guide"):
                f = tool / f"{name}.md"
                if f.is_file():
                    docs.append(Doc(f, "md", tool.name, name, back))
            ex = tool / "example"
            for f in sorted(ex.iterdir()) if ex.is_dir() else []:
                if f.suffix == ".md":
                    docs.append(Doc(f, "md", tool.name, f"example-{f.stem}", back))
                elif f.suffix == ".csv":
                    docs.append(Doc(f, "csv", tool.name, f"example-{f.stem}", back,
                                    f"{humanize(f.stem)} (example data)"))
            t = tool / "template.csv"
            if t.is_file():
                docs.append(Doc(t, "csv", tool.name, "template", back, f"{humanize(tool.name)} template"))
    prac = root / "practicum"
    if prac.is_dir():
        back = ("practicum.html", "Practicum")
        for f in sorted(prac.glob("*.md")):
            name = "overview" if f.stem.lower() == "readme" else f.stem
            docs.append(Doc(f, "md", "practicum", name, back))
    lq = root / "dist" / "lifecycle-questions.md"
    if lq.is_file():
        docs.append(Doc(lq, "md", "lifecycle", "questions", ("lifecycle.html", "Lifecycle")))
    return docs


def _relpath(from_page: str, to: str) -> str:
    return os.path.relpath(to, os.path.dirname(from_page)).replace(os.sep, "/")


def write_docs(root: Path) -> list[str]:
    """Write site/docs/** from the Markdown and CSV sources. Returns warnings."""
    site = root / "site"
    index = site / "index.html"
    if not index.is_file():
        return []
    docs = collect(root)
    if not docs:
        return []
    warnings: list[str] = []
    out_root = site / "docs"
    import shutil
    if out_root.exists():
        shutil.rmtree(out_root)
    by_path = {d.src.resolve(): d for d in docs}
    methods_dir = root / "methods"

    for d in docs:
        text = d.src.read_text(encoding="utf-8")
        d.blocks = parse_markdown(text) if d.kind == "md" else None
        if d.kind == "md":
            if not any(b["type"] == "heading" and b["level"] == 1 for b in d.blocks):
                d.blocks.insert(0, {"type": "heading", "level": 1, "text": front_title(text) or humanize(d.name)})
            d.title = title_of(d.blocks)
        else:
            d.title = d._title or humanize(d.name)
            d.blocks = csv_blocks(text, d.title)

    header_cache: dict[str, tuple[str, str]] = {}
    index_html = index.read_text(encoding="utf-8")
    for d in docs:
        up = "../" * (d.page.count("/"))
        page_dir = d.src.parent

        def resolve(href: str, d=d, up=up, page_dir=page_dir):
            if href.startswith("xw:"):
                return up + "crosswalk.html"
            if re.match(r"https?:|mailto:", href) or href.startswith("#"):
                return href
            target_name = href.split("#")[0]
            frag = ("#" + href.split("#", 1)[1]) if "#" in href else ""
            target = (page_dir / target_name).resolve()
            if target in by_path:
                return _relpath(d.page, by_path[target].page) + frag
            if target.name == "crosswalk.csv":
                return up + "downloads/crosswalk.csv"
            if target.is_dir() and methods_dir.resolve() in target.parents:
                return up + f"tools.html#{target.name}"
            return None

        def files(name: str, d=d, page_dir=page_dir):
            hit = by_path.get((page_dir / name).resolve()) or by_path.get((root / name).resolve())
            return (_relpath(d.page, hit.page), hit.title) if hit else None

        def plain_link(href: str, resolve=resolve):
            r = resolve(href)
            return r if r and re.match(r"https?:", r) else None

        if up not in header_cache:
            header_cache[up] = chrome(index_html, up)
        header, footer = header_cache[up]
        base = d.page[:-5]
        actions = []
        out_dir = site / os.path.dirname(d.page)
        out_dir.mkdir(parents=True, exist_ok=True)
        stem = d.name
        if d.kind == "md":
            (out_dir / f"{stem}.docx").write_bytes(docx_bytes(d.blocks, plain_link, files))
            actions.append(f"    <a class=\"visual-actions__link\" href=\"{stem}.docx\">Download Word (.docx)</a>")
        has_table = any(b["type"] == "table" for b in d.blocks)
        if has_table:
            (out_dir / f"{stem}.xlsx").write_bytes(
                xlsx_bytes(d.blocks, tier_summary=(d.group, d.name) == ("sam-toolkit", "tier-self-assessment")))
            actions.append(f"    <a class=\"visual-actions__link\" href=\"{stem}.xlsx\">Download Excel (.xlsx)</a>")
        if d.kind == "csv":
            (out_dir / f"{stem}.csv").write_text(d.src.read_text(encoding="utf-8"), encoding="utf-8")
            actions.append(f"    <a class=\"visual-actions__link\" href=\"{stem}.csv\">Download CSV</a>")
        actions.append("    <button type=\"button\" class=\"visual-actions__link doc-print\" "
                       "onclick=\"window.print()\">Print or save as PDF</button>")
        extra = TIER_EXTRA if (d.group, d.name) == ("sam-toolkit", "tier-self-assessment") else ""
        body = body_html(d.blocks, resolve, files)
        (out_dir / f"{stem}.html").write_text(PAGE.format(
            title=escape(d.title), description=escape(summary_of(d.blocks) or d.title, quote=True), up=up,
            header=header, footer=footer, back_href=up + d.back[0], back_label=escape(d.back[1]),
            actions="\n".join(actions), extra=extra, body=body), encoding="utf-8")
    return warnings
