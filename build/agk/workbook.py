"""Build the application management workbook (.xlsx) with the standard library only.

One workbook carries a program from the As-Is assessment to measurement: Start, Assess, Plan,
Measures, Scorecard, and Re-score. Calculated cells are formulas, so it works in Excel, Google Sheets,
and LibreOffice with no macros. Every status is a word; color is extra. Nothing is locked.
Output is deterministic: the same inputs give the same bytes.
"""
from __future__ import annotations

import datetime as dt
from html import escape

from agk.docs import XML_HEAD, _col_letter, _zip

# ---------- content ----------

DIMENSIONS = [
    "Policy and decision rights",
    "Roles and ownership",
    "Inventory and data quality",
    "Intake and acquisition",
    "Lifecycle and periodic review",
    "Licenses, contracts, and renewals",
    "Cost, value, and rationalization",
    "Risk, security, and AI use",
    "Retirement and data disposition",
    "Measures and leadership reporting",
    "Communication and education",
]
N = len(DIMENSIONS)
FIRST = 5                      # first data row on every working sheet
LAST = FIRST + N - 1           # last dimension row
MEAS_ROWS = 15                 # measure rows on Measures
MFIRST, MLAST = FIRST, FIRST + MEAS_ROWS - 1
ROUNDS = 4                     # Re-score rounds after the baseline

LEVELS = ["0 not done", "1 ad hoc", "2 defined", "3 measured"]
DECISIONS = "Fund now,Defer,Accept as risk"
STATUSES = "baseline only,forecast,achieved,not achieved"
EFFECTS = "cost saved,cost avoided,risk reduced,time saved"

QUESTIONS = [
    "Do applications have an accountable owner?",
    "How much renewal spend is still undecided?",
    "What spend could be reduced or retired?",
    "Which license gaps could become audit exposure?",
    "Which gaps need escalation?",
    "What did we save, and what is the proof?",
]

# ---------- styles ----------

S_DEFAULT, S_TITLE, S_HINT, S_HEADER, S_LABEL = 0, 1, 2, 3, 4
S_IN_TEXT, S_IN_DATE, S_IN_NUM = 5, 6, 7
S_CALC, S_CALC_PCT, S_CALC_DATE = 8, 9, 10
S_BAND, S_BODY = 11, 12

NUMFMT_DATE = 164

STYLES = (
    XML_HEAD + "<styleSheet xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\">"
    f"<numFmts count=\"1\"><numFmt numFmtId=\"{NUMFMT_DATE}\" formatCode=\"yyyy\\-mm\\-dd\"/></numFmts>"
    "<fonts count=\"5\">"
    "<font><sz val=\"11\"/><name val=\"Calibri\"/></font>"
    "<font><b/><sz val=\"11\"/><name val=\"Calibri\"/></font>"
    "<font><b/><sz val=\"11\"/><color rgb=\"FFFFFFFF\"/><name val=\"Calibri\"/></font>"
    "<font><b/><sz val=\"14\"/><name val=\"Calibri\"/></font>"
    "<font><i/><sz val=\"11\"/><color rgb=\"FF595959\"/><name val=\"Calibri\"/></font></fonts>"
    "<fills count=\"6\">"
    "<fill><patternFill patternType=\"none\"/></fill>"
    "<fill><patternFill patternType=\"gray125\"/></fill>"
    "<fill><patternFill patternType=\"solid\"><fgColor rgb=\"FF1F3864\"/><bgColor indexed=\"64\"/></patternFill></fill>"
    "<fill><patternFill patternType=\"solid\"><fgColor rgb=\"FFFFF2CC\"/><bgColor indexed=\"64\"/></patternFill></fill>"
    "<fill><patternFill patternType=\"solid\"><fgColor rgb=\"FFE7E6E6\"/><bgColor indexed=\"64\"/></patternFill></fill>"
    "<fill><patternFill patternType=\"solid\"><fgColor rgb=\"FFD9E2E7\"/><bgColor indexed=\"64\"/></patternFill></fill></fills>"
    "<borders count=\"2\"><border><left/><right/><top/><bottom/><diagonal/></border>"
    "<border><left style=\"thin\"><color rgb=\"FF767F89\"/></left><right style=\"thin\"><color rgb=\"FF767F89\"/></right>"
    "<top style=\"thin\"><color rgb=\"FF767F89\"/></top><bottom style=\"thin\"><color rgb=\"FF767F89\"/></bottom>"
    "<diagonal/></border></borders>"
    "<cellStyleXfs count=\"1\"><xf numFmtId=\"0\" fontId=\"0\" fillId=\"0\" borderId=\"0\"/></cellStyleXfs>"
    "<cellXfs count=\"13\">"
    # 0 default
    "<xf numFmtId=\"0\" fontId=\"0\" fillId=\"0\" borderId=\"0\" xfId=\"0\" applyAlignment=\"1\">"
    "<alignment vertical=\"top\" wrapText=\"1\"/></xf>"
    # 1 title
    "<xf numFmtId=\"0\" fontId=\"3\" fillId=\"0\" borderId=\"0\" xfId=\"0\" applyFont=\"1\"/>"
    # 2 hint
    "<xf numFmtId=\"0\" fontId=\"4\" fillId=\"0\" borderId=\"0\" xfId=\"0\" applyFont=\"1\" applyAlignment=\"1\">"
    "<alignment vertical=\"top\" wrapText=\"1\"/></xf>"
    # 3 header
    "<xf numFmtId=\"0\" fontId=\"2\" fillId=\"2\" borderId=\"1\" xfId=\"0\" applyFont=\"1\" applyFill=\"1\" "
    "applyBorder=\"1\" applyAlignment=\"1\"><alignment vertical=\"top\" wrapText=\"1\"/></xf>"
    # 4 label
    "<xf numFmtId=\"0\" fontId=\"1\" fillId=\"0\" borderId=\"0\" xfId=\"0\" applyFont=\"1\" applyAlignment=\"1\">"
    "<alignment vertical=\"top\" wrapText=\"1\"/></xf>"
    # 5 input text
    "<xf numFmtId=\"0\" fontId=\"0\" fillId=\"3\" borderId=\"1\" xfId=\"0\" applyFill=\"1\" applyBorder=\"1\" "
    "applyAlignment=\"1\"><alignment vertical=\"top\" wrapText=\"1\"/></xf>"
    # 6 input date
    f"<xf numFmtId=\"{NUMFMT_DATE}\" fontId=\"0\" fillId=\"3\" borderId=\"1\" xfId=\"0\" applyNumberFormat=\"1\" "
    "applyFill=\"1\" applyBorder=\"1\" applyAlignment=\"1\"><alignment vertical=\"top\" wrapText=\"1\"/></xf>"
    # 7 input number
    "<xf numFmtId=\"0\" fontId=\"0\" fillId=\"3\" borderId=\"1\" xfId=\"0\" applyFill=\"1\" applyBorder=\"1\" "
    "applyAlignment=\"1\"><alignment horizontal=\"left\" vertical=\"top\" wrapText=\"1\"/></xf>"
    # 8 calculated text
    "<xf numFmtId=\"0\" fontId=\"0\" fillId=\"4\" borderId=\"1\" xfId=\"0\" applyFill=\"1\" applyBorder=\"1\" "
    "applyAlignment=\"1\"><alignment horizontal=\"left\" vertical=\"top\" wrapText=\"1\"/></xf>"
    # 9 calculated percent
    "<xf numFmtId=\"9\" fontId=\"0\" fillId=\"4\" borderId=\"1\" xfId=\"0\" applyNumberFormat=\"1\" applyFill=\"1\" "
    "applyBorder=\"1\" applyAlignment=\"1\"><alignment horizontal=\"left\" vertical=\"top\"/></xf>"
    # 10 calculated date
    f"<xf numFmtId=\"{NUMFMT_DATE}\" fontId=\"0\" fillId=\"4\" borderId=\"1\" xfId=\"0\" applyNumberFormat=\"1\" "
    "applyFill=\"1\" applyBorder=\"1\" applyAlignment=\"1\"><alignment horizontal=\"left\" vertical=\"top\"/></xf>"
    # 11 band
    "<xf numFmtId=\"0\" fontId=\"1\" fillId=\"5\" borderId=\"0\" xfId=\"0\" applyFont=\"1\" applyFill=\"1\" "
    "applyAlignment=\"1\"><alignment vertical=\"top\"/></xf>"
    # 12 body (fixed text in a table)
    "<xf numFmtId=\"0\" fontId=\"0\" fillId=\"0\" borderId=\"1\" xfId=\"0\" applyBorder=\"1\" applyAlignment=\"1\">"
    "<alignment vertical=\"top\" wrapText=\"1\"/></xf></cellXfs>"
    "<cellStyles count=\"1\"><cellStyle name=\"Normal\" xfId=\"0\" builtinId=\"0\"/></cellStyles>"
    "<dxfs count=\"2\">"
    "<dxf><font><color rgb=\"FF7F2A00\"/></font><fill><patternFill patternType=\"solid\">"
    "<fgColor rgb=\"FFFCE4D6\"/><bgColor rgb=\"FFFCE4D6\"/></patternFill></fill></dxf>"
    "<dxf><font><color rgb=\"FF1E4620\"/></font><fill><patternFill patternType=\"solid\">"
    "<fgColor rgb=\"FFE2EFDA\"/><bgColor rgb=\"FFE2EFDA\"/></patternFill></fill></dxf></dxfs>"
    "</styleSheet>")


# ---------- sheet model ----------

def serial(day: str) -> int:
    """Excel date serial for an ISO date."""
    return (dt.date.fromisoformat(day) - dt.date(1899, 12, 30)).days


class Sheet:
    def __init__(self, name: str, widths: list[int]):
        self.name = name
        self.widths = widths
        self.cells: dict[tuple[int, int], tuple[str, object, int]] = {}
        self.freeze: tuple[int, int] | None = None   # (columns frozen, rows frozen)
        self.validations: list[str] = []
        self.cond: list[str] = []
        self.print_title_row: int | None = None
        self.tab = ""

    def text(self, ref: str, value: str, style: int = S_DEFAULT):
        self._put(ref, "s", value, style)

    def num(self, ref: str, value: float, style: int = S_IN_NUM):
        self._put(ref, "n", value, style)

    def formula(self, ref: str, f: str, style: int = S_CALC):
        self._put(ref, "f", f, style)

    def blank(self, ref: str, style: int):
        self._put(ref, "b", "", style)

    def _put(self, ref: str, kind: str, value, style: int):
        col = 0
        i = 0
        while ref[i].isalpha():
            col = col * 26 + (ord(ref[i]) - 64)
            i += 1
        self.cells[(int(ref[i:]), col - 1)] = (kind, value, style)

    def validate(self, sqref: str, kind: str, title: str, prompt: str, error: str, *args):
        """kind 'whole' takes (low, high); kind 'list' takes (comma separated values)."""
        head = (f"<dataValidation type=\"{kind}\" allowBlank=\"1\" showInputMessage=\"1\" showErrorMessage=\"1\" "
                f"errorTitle=\"Value not allowed\" error=\"{escape(error, quote=True)}\" "
                f"promptTitle=\"{escape(title, quote=True)}\" prompt=\"{escape(prompt, quote=True)}\" sqref=\"{sqref}\"")
        if kind == "whole":
            self.validations.append(f"{head} operator=\"between\"><formula1>{args[0]}</formula1>"
                                    f"<formula2>{args[1]}</formula2></dataValidation>")
        else:
            self.validations.append(f"{head}><formula1>\"{escape(args[0], quote=False)}\"</formula1></dataValidation>")

    def highlight(self, sqref: str, first: str, formula: str, dxf: int):
        self.cond.append((sqref, first, formula, dxf))

    def xml(self) -> str:
        rows: dict[int, list[tuple[int, tuple]]] = {}
        for (r, c), v in self.cells.items():
            rows.setdefault(r, []).append((c, v))
        out = []
        for r in sorted(rows):
            cells = []
            for c, (kind, value, style) in sorted(rows[r]):
                ref = f"{_col_letter(c)}{r}"
                if kind == "s":
                    cells.append(f"<c r=\"{ref}\" s=\"{style}\" t=\"inlineStr\"><is><t xml:space=\"preserve\">"
                                 f"{escape(str(value), quote=False)}</t></is></c>")
                elif kind == "n":
                    cells.append(f"<c r=\"{ref}\" s=\"{style}\"><v>{value}</v></c>")
                elif kind == "f":
                    cells.append(f"<c r=\"{ref}\" s=\"{style}\"><f>{escape(str(value), quote=False)}</f></c>")
                else:
                    cells.append(f"<c r=\"{ref}\" s=\"{style}\"/>")
            out.append(f"<row r=\"{r}\">{''.join(cells)}</row>")
        cols = "".join(f"<col min=\"{i}\" max=\"{i}\" width=\"{w}\" customWidth=\"1\"/>"
                       for i, w in enumerate(self.widths, 1))
        pane = ""
        if self.freeze:
            xs, ys = self.freeze
            top_left = f"{_col_letter(xs)}{ys + 1}"
            pane = (f"<pane xSplit=\"{xs}\" ySplit=\"{ys}\" topLeftCell=\"{top_left}\" activePane=\"bottomRight\" "
                    "state=\"frozen\"/>")
        sel = "<selection pane=\"bottomRight\"/>" if self.freeze else ""
        cond = ""
        for i, (sqref, first, formula, dxf) in enumerate(self.cond, 1):
            cond += (f"<conditionalFormatting sqref=\"{sqref}\"><cfRule type=\"expression\" dxfId=\"{dxf}\" "
                     f"priority=\"{i}\"><formula>{escape(formula, quote=False)}</formula></cfRule></conditionalFormatting>")
        dv = (f"<dataValidations count=\"{len(self.validations)}\">{''.join(self.validations)}</dataValidations>"
              if self.validations else "")
        return (XML_HEAD + "<worksheet xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\">"
                "<sheetPr><pageSetUpPr fitToPage=\"1\"/></sheetPr>"
                f"<sheetViews><sheetView workbookViewId=\"0\"{' tabSelected=\"1\"' if self.tab else ''}>{pane}{sel}"
                "</sheetView></sheetViews>"
                "<sheetFormatPr defaultRowHeight=\"15\"/>"
                f"<cols>{cols}</cols><sheetData>{''.join(out)}</sheetData>{cond}{dv}"
                "<pageMargins left=\"0.5\" right=\"0.5\" top=\"0.75\" bottom=\"0.75\" header=\"0.3\" footer=\"0.3\"/>"
                "<pageSetup orientation=\"landscape\" fitToWidth=\"1\" fitToHeight=\"0\"/>"
                "<headerFooter><oddFooter>&amp;A  page &amp;P of &amp;N</oddFooter></headerFooter></worksheet>")


def headers(sheet: Sheet, row: int, labels: list[str]):
    for i, label in enumerate(labels):
        sheet.text(f"{_col_letter(i)}{row}", label, S_HEADER)


def rng(sheet: str, col: str, a: int = FIRST, b: int = LAST) -> str:
    q = f"'{sheet}'" if "-" in sheet else sheet
    return f"{q}!${col}${a}:${col}${b}"


# ---------- sheets ----------

def build_start(example: bool, settings_row: int) -> Sheet:
    s = Sheet("Start", [34, 52, 18, 20])
    s.tab = "1"
    s.text("A1", "Application management program workbook", S_TITLE)
    s.text("A2", "Assess where your program is, decide where it needs to be, plan the gaps, and measure progress. "
                 "Yellow cells are for typing. Gray cells are calculated, so do not type in them.", S_HINT)
    s.text("A4", "Program name (input)", S_LABEL); s.blank("B4", S_IN_TEXT)
    s.text("A5", "Scope: which applications and teams (input)", S_LABEL); s.blank("B5", S_IN_TEXT)
    s.text("A6", "Sponsor (input)", S_LABEL); s.blank("B6", S_IN_TEXT)
    s.text("A7", "First assessed on (calculated)", S_LABEL)
    s.formula("B7", "IF(ISNUMBER(Assess!$B$3),Assess!$B$3,\"Not assessed yet\")", S_CALC_DATE)

    s.text("A9", "The six steps", S_BAND); s.blank("B9", S_BAND); s.blank("C9", S_BAND); s.blank("D9", S_BAND)
    headers(s, 10, ["Step", "What to do", "Sheet", "About how long"])
    steps = [
        ("1 Assess", "Score each dimension 0 to 3 for today. Write the evidence you could show. If you cannot show it, "
                     "score one level lower. Score with someone who does the work.", "Assess", "30 minutes"),
        ("2 Set the To-Be", "Choose a target level for each dimension you care about, with a reason and a date. Level 2 "
                            "is a strong result; not everything needs 3.", "Assess", "15 minutes"),
        ("3 Choose three gaps", "Decide which gaps to fund now, no more than three at a time. Name an owner, a first "
                                "action, and a date for each.", "Plan", "15 minutes"),
        ("4 Define measures", "For each gap you fund, record one starting number with its date, a target, and where "
                              "the proof will be filed. Measure first, then set the target.", "Measures", "15 minutes"),
        ("5 Report", "Read the Scorecard. Show the sponsor. Write one decision for each target you are missing.",
         "Scorecard", "10 minutes"),
        ("6 Re-score", "Update measures every quarter. Re-score all dimensions once a year, and after a merger or a "
                       "change of sponsor. Type each round in its own column.", "Measures, Re-score", "20 minutes"),
    ]
    for i, row in enumerate(steps, 11):
        for j, v in enumerate(row):
            s.text(f"{_col_letter(j)}{i}", v, S_BODY)

    s.text("A18", "The scale", S_BAND); s.blank("B18", S_BAND); s.blank("C18", S_BAND); s.blank("D18", S_BAND)
    headers(s, 19, ["Level", "What it means", "What you can show", ""])
    scale = [("0 Not done", "Nobody does this.", "Nothing."),
             ("1 Ad hoc", "It happens sometimes and is not written down.", "An example, if someone remembers one."),
             ("2 Defined", "It is written down, owned, and followed.", "A recent example and the written rule."),
             ("3 Measured", "A number shows how well it works, and the number led to a change.",
              "The number, its history, and the change it led to.")]
    for i, row in enumerate(scale, 20):
        for j, v in enumerate(row):
            s.text(f"{_col_letter(j)}{i}", v, S_BODY)

    s.text("A25", "Status words you will see", S_BAND); s.blank("B25", S_BAND); s.blank("C25", S_BAND)
    s.blank("D25", S_BAND)
    headers(s, 26, ["Word", "What it means", "", ""])
    words = [("Not scored", "You have not entered the numbers this needs. Blank never means zero."),
             ("Needs input", "A required yellow cell is empty."),
             ("Needs evidence", "A level of 1 or more has no evidence written beside it."),
             ("Baseline only", "You have a starting number but no later measurement."),
             ("Forecast", "An estimate. It is not a benefit and is never added to achieved results."),
             ("Achieved", "Measured again, with a value, a date, and evidence filed. Otherwise it reads Not yet proven.")]
    for i, (a, b) in enumerate(words, 27):
        s.text(f"A{i}", a, S_BODY); s.text(f"B{i}", b, S_BODY)

    s.text("A34", "Words used here", S_BAND); s.blank("B34", S_BAND); s.blank("C34", S_BAND); s.blank("D34", S_BAND)
    headers(s, 35, ["Word", "Meaning", "", ""])
    vocab = [("As-Is", "Where the program is today, scored with evidence."),
             ("To-Be", "Where you need it to be, by a date, for a reason."),
             ("Gap", "To-Be level minus current level, never below zero."),
             ("Baseline", "The value you measured before the change, on a named date."),
             ("Target", "The value you want, and the date you want it."),
             ("Evidence", "A record someone else could check: a document, a report, a log.")]
    for i, (a, b) in enumerate(vocab, 36):
        s.text(f"A{i}", a, S_BODY); s.text(f"B{i}", b, S_BODY)

    s.text(f"A{settings_row - 2}", "Settings you can change", S_BAND)
    for c in "BCD":
        s.blank(f"{c}{settings_row - 2}", S_BAND)
    headers(s, settings_row - 1, ["Setting", "Used for", "Value", ""])
    settings = [("Days before an assessment is stale", "Marks the last assessment as stale on the Scorecard.", 365),
                ("Days before a measurement is stale", "Marks the last measurement as stale on the Scorecard.", 90),
                ("Evidence share that counts as partly evidenced", "Share of measures with a value and evidence.", 0.5),
                ("Evidence share that counts as evidenced", "Share of measures with a value and evidence.", 0.9)]
    for i, (a, b, v) in enumerate(settings, settings_row):
        s.text(f"A{i}", a, S_BODY); s.text(f"B{i}", b, S_BODY)
        s.num(f"C{i}", v, S_IN_NUM)

    base = settings_row + len(settings) + 2
    s.text(f"A{base}", "How this workbook relates to the kit's files", S_BAND)
    for c in "BCD":
        s.blank(f"{c}{base}", S_BAND)
    headers(s, base + 1, ["Sheet", "Replaces or feeds", "", ""])
    rel = [("Assess", "application-management-self-assessment.md and the as-is columns of the gap plan."),
           ("Plan", "The plan columns of application-management-gap-plan.csv."),
           ("Measures", "benefits-tracker.csv. Same meaning, plain labels."),
           ("Scorecard", "The chain and the six questions in leadership-report.md."),
           ("Re-score", "Yearly re-scoring from operating-calendar.md."),
           ("Ideas", "Credible, hard-to-fake measures to pick from. Reference only.")]
    for i, (a, b) in enumerate(rel, base + 2):
        s.text(f"A{i}", a, S_BODY); s.text(f"B{i}", b, S_BODY)
    t = base + 2 + len(rel) + 1
    s.text(f"A{t}", "Need help? Use setup prompts 2 (baseline), 6 (renewals), and 10 (report) in setup-prompts.md. "
                     "To sort or filter, select a header row and turn on Filter (Excel: Ctrl+Shift+L; Sheets and "
                     "LibreOffice: Data menu), and include every column when you sort.", S_HINT)
    return s


def dim_rows(sheet: Sheet, col_name: str = "B"):
    for i, name in enumerate(DIMENSIONS):
        r = FIRST + i
        sheet.num(f"A{r}", i + 1, S_BODY)
        sheet.text(f"{col_name}{r}", name, S_BODY)


def build_assess(data: dict | None) -> Sheet:
    s = Sheet("Assess", [5, 30, 16, 40, 16, 40, 16, 34])
    s.freeze = (2, 4)
    s.text("A1", "Assess: where the program is, and where it needs to be", S_TITLE)
    s.text("A2", "Score what you can show today, not what you plan. With no evidence, score one level lower. "
                 "Level 2 is a strong target. You can finish this in about 30 minutes; leave unknowns blank.", S_HINT)
    s.text("A3", "Assessment date (yyyy-mm-dd, required input)", S_LABEL)
    s.blank("B3", S_IN_DATE)
    headers(s, 4, ["No.", "Dimension", "As-Is level 0 to 3 (required input)", "As-Is evidence you could show "
               "(required input)", "To-Be level 0 to 3 (required input)", "Why this target, and by when (input)",
               "Gap (calculated, do not type)", "Check (calculated, do not type)"])
    dim_rows(s)
    for r in range(FIRST, LAST + 1):
        s.blank(f"C{r}", S_IN_NUM); s.blank(f"D{r}", S_IN_TEXT); s.blank(f"E{r}", S_IN_NUM); s.blank(f"F{r}", S_IN_TEXT)
        s.formula(f"G{r}", f"IF(AND(ISNUMBER(C{r}),ISNUMBER(E{r})),MAX(0,E{r}-C{r}),\"\")")
        s.formula(f"H{r}",
                  f"IF(NOT(ISNUMBER(C{r})),\"Needs input\",IF(AND(C{r}>=1,LEN(D{r})=0),\"Needs evidence: add it, or score "
                  f"one level lower\",IF(NOT(ISNUMBER(E{r})),\"Set a target\",IF(E{r}<C{r},\"Target is below today's "
                  f"score\",\"\"))))")
    t = LAST + 1
    s.text(f"B{t}", "Total gap points", S_LABEL)
    s.formula(f"G{t}", f"IF(COUNT(G{FIRST}:G{LAST})=0,\"Not scored\",SUM(G{FIRST}:G{LAST}))")
    s.validate(f"C{FIRST}:C{LAST} E{FIRST}:E{LAST}", "whole", "Level 0 to 3",
               "0 not done, 1 ad hoc, 2 defined, 3 measured. Score what you can show today.",
               "Enter 0, 1, 2, or 3, or leave the cell empty.", 0, 3)
    s.highlight(f"H{FIRST}:H{LAST}", f"H{FIRST}", f"LEN(H{FIRST})>0", 0)
    if data:
        s.num("B3", serial(data["date"]), S_IN_DATE)
        for i, d in enumerate(data["assess"]):
            r = FIRST + i
            s.num(f"C{r}", d[0], S_IN_NUM); s.text(f"D{r}", d[1], S_IN_TEXT)
            s.num(f"E{r}", d[2], S_IN_NUM); s.text(f"F{r}", d[3], S_IN_TEXT)
    return s


def build_plan(data: dict | None) -> Sheet:
    s = Sheet("Plan", [5, 30, 14, 14, 18, 22, 40, 16, 16, 34])
    s.freeze = (2, 4)
    s.text("A1", "Plan: which gaps you will close", S_TITLE)
    s.text("A2", "Choose three gaps to fund now; the rest wait. A funded gap needs an owner, a first action, and a "
                 "date. Priority 1 is first, 3 is last; several gaps can share a priority.", S_HINT)
    headers(s, 4, ["No.", "Dimension (calculated, do not type)", "Gap (calculated, do not type)",
                   "Priority 1 to 3 (input)", "Decision (input)", "Owner role (input)", "First action (input)",
                   "Due on (yyyy-mm-dd, input)", "Last reviewed (yyyy-mm-dd, input)",
                   "Check (calculated, do not type)"])
    for i in range(N):
        r = FIRST + i
        s.num(f"A{r}", i + 1, S_BODY)
        s.formula(f"B{r}", f"Assess!B{r}")
        s.formula(f"C{r}", f"Assess!G{r}")
        s.blank(f"D{r}", S_IN_NUM); s.blank(f"E{r}", S_IN_TEXT); s.blank(f"F{r}", S_IN_TEXT)
        s.blank(f"G{r}", S_IN_TEXT); s.blank(f"H{r}", S_IN_DATE); s.blank(f"I{r}", S_IN_DATE)
        s.formula(f"J{r}",
                  f"IF(AND(E{r}=\"Fund now\",OR(LEN(F{r})=0,LEN(G{r})=0,LEN(H{r})=0)),\"Add owner, action, and date\","
                  f"IF(AND(E{r}=\"Fund now\",NOT(ISNUMBER(C{r}))),\"Score this dimension first\","
                  f"IF(AND(E{r}=\"Fund now\",C{r}=0),\"No gap to close\","
                  f"IF(AND(ISNUMBER(H{r}),E{r}=\"Fund now\",H{r}<TODAY()),\"This date has passed: pick a new date\",\"\"))))")
    s.validate(f"D{FIRST}:D{LAST}", "whole", "Priority", "1 is first, 3 is last.",
               "Enter 1, 2, or 3, or leave the cell empty.", 1, 3)
    s.validate(f"E{FIRST}:E{LAST}", "list", "Decision", "Fund now, Defer, or Accept as risk.",
               "Choose Fund now, Defer, or Accept as risk.", DECISIONS)
    s.highlight(f"J{FIRST}:J{LAST}", f"J{FIRST}", f"LEN(J{FIRST})>0", 0)
    if data:
        for i, d in enumerate(data["plan"]):
            r = FIRST + i
            s.num(f"D{r}", d[0], S_IN_NUM); s.text(f"E{r}", d[1], S_IN_TEXT); s.text(f"F{r}", d[2], S_IN_TEXT)
            s.text(f"G{r}", d[3], S_IN_TEXT); s.num(f"H{r}", serial(d[4]), S_IN_DATE)
    return s


MEAS_HEAD = ["Measure ID (input)", "Practice (input)", "Measure (input)", "Unit (input)", "Baseline value (input)",
             "Baseline date (yyyy-mm-dd, input)", "Target value (input)", "Target date (yyyy-mm-dd, input)",
             "Latest value (input)", "Measured on (yyyy-mm-dd, input)", "Evidence reference (input)",
             "Status (input)", "Effect type (input)", "Effect amount (input)", "Owner role (input)", "Notes (input)",
             "Progress to target (calculated, do not type)", "Check (calculated, do not type)",
             "Answers leadership question 1 to 6 (input)", "Counted with evidence (calculated, do not type)",
             "Proven achieved (calculated, do not type)"]


def build_measures(data: dict | None) -> Sheet:
    s = Sheet("Measures", [12, 28, 34, 14, 14, 16, 14, 16, 14, 16, 26, 16, 16, 14, 20, 34, 16, 30, 16, 18, 18])
    s.freeze = (1, 4)
    s.text("A1", "Measures: prove the program pays off", S_TITLE)
    s.text("A2", "Measure first, then set a target. A forecast is an estimate and never counts as achieved. Mark a "
                 "measure achieved only when you have a latest value, a date, and evidence filed.", S_HINT)
    headers(s, 4, MEAS_HEAD)
    for r in range(MFIRST, MLAST + 1):
        for c, st in zip("ABCDEFGHIJKLMNOPS", [S_IN_TEXT, S_IN_TEXT, S_IN_TEXT, S_IN_TEXT, S_IN_NUM, S_IN_DATE,
                                                S_IN_NUM, S_IN_DATE, S_IN_NUM, S_IN_DATE, S_IN_TEXT, S_IN_TEXT,
                                                S_IN_TEXT, S_IN_NUM, S_IN_TEXT, S_IN_TEXT, S_IN_NUM]):
            s.blank(f"{c}{r}", st)
        s.formula(f"Q{r}", f"IF(AND(ISNUMBER(E{r}),ISNUMBER(G{r}),ISNUMBER(I{r}),G{r}<>E{r}),(I{r}-E{r})/(G{r}-E{r}),"
                           f"\"\")", S_CALC_PCT)
        s.formula(f"T{r}", f"IF(AND(ISNUMBER(I{r}),LEN(K{r})>0),1,\"\")", S_CALC)
        s.formula(f"U{r}", f"IF(AND(L{r}=\"achieved\",ISNUMBER(I{r}),ISNUMBER(J{r}),LEN(K{r})>0),1,\"\")", S_CALC)
        s.formula(f"R{r}",
                  f"IF(AND(L{r}=\"achieved\",OR(NOT(ISNUMBER(I{r})),NOT(ISNUMBER(J{r})),LEN(K{r})=0)),\"Not yet proven: "
                  f"add a value, a date, and evidence\",IF(AND(L{r}=\"forecast\",ISNUMBER(N{r})),\"Forecast is not a benefit"
                  f"\",IF(AND(LEN(A{r})>0,NOT(ISNUMBER(E{r}))),\"No starting number yet\",IF(AND(LEN(A{r})>0,"
                  f"NOT(ISNUMBER(F{r}))),\"Baseline date needed\",\"\"))))")
    # row 5 is the program's own gap measure, tied to the assessment
    s.text(f"A{MFIRST}", "M-001", S_IN_TEXT)
    s.text(f"B{MFIRST}", "Application management self-assessment", S_IN_TEXT)
    s.text(f"C{MFIRST}", "Gap points across 11 dimensions", S_IN_TEXT)
    s.text(f"D{MFIRST}", "points", S_IN_TEXT)
    s.formula(f"E{MFIRST}", f"IF(ISNUMBER(Assess!G{LAST + 1}),Assess!G{LAST + 1},\"\")", S_CALC)
    s.formula(f"F{MFIRST}", "IF(ISNUMBER(Assess!B3),Assess!B3,\"\")", S_CALC_DATE)
    s.num(f"G{MFIRST}", 0, S_IN_NUM)
    s.formula(f"I{MFIRST}", f"IF(COUNT(Scorecard!F17:F27)=0,\"\",SUM(Scorecard!F17:F27))", S_CALC)
    s.text(f"K{MFIRST}", "Assess and Re-score sheets", S_IN_TEXT)
    s.text(f"L{MFIRST}", "baseline only", S_IN_TEXT)
    s.text(f"M{MFIRST}", "risk reduced", S_IN_TEXT)
    s.text(f"P{MFIRST}", "Baseline and latest come from Assess and Re-score. Re-score yearly with evidence.", S_IN_TEXT)
    s.validate(f"L{MFIRST}:L{MLAST}", "list", "Status",
               "baseline only, forecast, achieved, or not achieved. Forecast is not a benefit.",
               "Choose baseline only, forecast, achieved, or not achieved.", STATUSES)
    s.validate(f"M{MFIRST}:M{MLAST}", "list", "Effect type", "What kind of benefit this is.",
               "Choose cost saved, cost avoided, risk reduced, or time saved.", EFFECTS)
    s.validate(f"S{MFIRST}:S{MLAST}", "whole", "Leadership question", "Optional. Enter 1 to 6, as on the Scorecard.",
               "Enter a number from 1 to 6, or leave the cell empty.", 1, 6)
    s.highlight(f"R{MFIRST}:R{MLAST}", f"R{MFIRST}", f"LEN(R{MFIRST})>0", 0)
    if data:
        for i, m in enumerate(data["measures"]):
            r = MFIRST + 1 + i
            for c, v, st in m:
                if isinstance(v, str):
                    s.text(f"{c}{r}", v, st)
                else:
                    s.num(f"{c}{r}", v, st)
    return s


def build_rescore(data: dict | None) -> Sheet:
    s = Sheet("Re-score", [5, 30, 16, 14, 14, 14, 14, 3, 30, 30, 30, 30, 16, 34])
    s.freeze = (2, 4)
    s.text("A1", "Re-score: assess again and keep the history", S_TITLE)
    s.text("A2", "Fill the next empty round column, then type its date in row 3. Never overwrite an earlier round. "
                 "Do not insert or delete columns here. If you change a To-Be target, say why on the Assess sheet.", S_HINT)
    s.text("A3", "Date of each round (yyyy-mm-dd, input)", S_LABEL)
    for c in "DEFG":
        s.blank(f"{c}3", S_IN_DATE)
    headers(s, 4, ["No.", "Dimension (calculated, do not type)", "Baseline level (calculated, do not type)",
                   "Round 2 level (input)", "Round 3 level (input)", "Round 4 level (input)", "Round 5 level (input)",
                   "", "Round 2 evidence (input)", "Round 3 evidence (input)", "Round 4 evidence (input)",
                   "Round 5 evidence (input)", "Latest level (calculated, do not type)",
                   "Check (calculated, do not type)"])
    s.text("H4", "Gap", S_HEADER)
    for i in range(N):
        r = FIRST + i
        s.num(f"A{r}", i + 1, S_BODY)
        s.formula(f"B{r}", f"Assess!B{r}")
        s.formula(f"C{r}", f"IF(ISNUMBER(Assess!C{r}),Assess!C{r},\"\")")
        for c in "DEFG":
            s.blank(f"{c}{r}", S_IN_NUM)
        s.blank(f"H{r}", S_BODY)
        for c in "IJKL":
            s.blank(f"{c}{r}", S_IN_TEXT)
        s.formula(f"M{r}", f"IF(COUNT(D{r}:G{r})=0,C{r},LOOKUP(9.99E+307,D{r}:G{r}))")
        s.formula(f"N{r}", f"IF(AND(ISNUMBER(M{r}),ISNUMBER(C{r})),IF(M{r}<C{r},\"Went down: add a note\","
                           f"IF(AND(M{r}>C{r},COUNTA(I{r}:L{r})=0),\"Moved up without evidence: add it\",\"\")),\"\")")
    t = LAST + 1
    s.text(f"B{t}", "Gap points for this round", S_LABEL)
    s.formula(f"C{t}", f"Assess!G{LAST + 1}")
    for c in "DEFG":
        s.formula(f"{c}{t}",
                  f"IF(OR(COUNT({c}{FIRST}:{c}{LAST})=0,COUNT({c}{FIRST}:{c}{LAST})<COUNT(Assess!$E${FIRST}:$E${LAST})),"
                  f"\"Not all scored\",SUMPRODUCT((Assess!$E${FIRST}:$E${LAST}-{c}{FIRST}:{c}{LAST}>0)*"
                  f"(Assess!$E${FIRST}:$E${LAST}-{c}{FIRST}:{c}{LAST})))")
    s.validate(f"D{FIRST}:G{LAST}", "whole", "Level 0 to 3", "Score what you can show today.",
               "Enter 0, 1, 2, or 3, or leave the cell empty.", 0, 3)
    s.highlight(f"N{FIRST}:N{LAST}", f"N{FIRST}", f"LEN(N{FIRST})>0", 0)
    return s


def build_scorecard(settings_row: int) -> Sheet:
    s = Sheet("Scorecard", [34, 24, 26, 26, 30, 18, 20, 24, 20])
    S = f"Start!$C${settings_row}"        # stale assessment days
    M = f"Start!$C${settings_row + 1}"    # stale measurement days
    P = f"Start!$C${settings_row + 2}"    # partly evidenced
    E = f"Start!$C${settings_row + 3}"    # evidenced
    s.text("A1", "Scorecard: how the program is doing", S_TITLE)
    s.text("A2", "Last assessed", S_LABEL)
    s.formula("B2", "IF(COUNT('Re-score'!$D$3:$G$3)>0,MAX('Re-score'!$D$3:$G$3),IF(ISNUMBER(Assess!$B$3),Assess!$B$3,\"Never\"))",
              S_CALC_DATE)
    s.formula("C2", f"IF(NOT(ISNUMBER(B2)),\"Not scored\",IF(TODAY()-B2>{S},\"Stale: re-score due\",\"Current\"))")
    s.text("A3", "Last measured", S_LABEL)
    s.formula("B3", f"IF(COUNT(Measures!$J${MFIRST}:$J${MLAST})=0,\"Never\",MAX(Measures!$J${MFIRST}:$J${MLAST}))", S_CALC_DATE)
    s.formula("C3", f"IF(NOT(ISNUMBER(B3)),\"Not measured yet\",IF(TODAY()-B3>{M},\"Stale: measure again\",\"Current\"))")
    s.text("A4", "Blank means not entered, never zero. Every status is a word; color is extra.", S_HINT)

    def band(row: int, title: str):
        s.text(f"A{row}", title, S_BAND)
        for c in "BCDEFGHI":
            s.blank(f"{c}{row}", S_BAND)

    band(6, "Headlines")
    headers(s, 7, ["Headline", "Value (calculated, do not type)", "Progress bar (calculated, do not type)",
                   "Status (calculated, do not type)", "What it means"])
    both = f"COUNT(Assess!$G${FIRST}:$G${LAST})"
    nmeas = f"COUNT(Measures!$I${MFIRST}:$I${MLAST})"
    evid = f"COUNT(Measures!$T${MFIRST}:$T${MLAST})"

    def bar(x: str) -> str:
        return (f"IF(NOT(ISNUMBER({x})),\"Not measured\",REPT(\"#\",ROUND(10*{x},0))&REPT(\"-\",10-ROUND(10*{x},0))"
                f"&\" \"&TEXT({x},\"0%\"))")

    # 8 dimensions scored
    s.text("A8", "Dimensions scored", S_BODY)
    s.formula("B8", f"{both}&\" of {N}\"")
    s.formula("C8", bar(f"IF({both}=0,\"\",{both}/{N})"))
    s.formula("D8", f"IF({both}=0,\"Not scored\",IF({both}={N},\"All scored\",\"Partly scored\"))")
    s.text("E8", "How many dimensions have both an As-Is and a To-Be level.", S_BODY)
    # 9 gap points remaining
    s.text("A9", "Gap points remaining", S_BODY)
    s.formula("B9", "IF(COUNT($F$17:$F$27)=0,\"Not scored\",SUM($F$17:$F$27))")
    closure = (f"IF(OR(NOT(ISNUMBER($B$9)),NOT(ISNUMBER(Assess!$G${LAST + 1}))),\"\",IF(Assess!$G${LAST + 1}=0,\"\","
               f"1-$B$9/Assess!$G${LAST + 1}))")
    s.formula("C9", bar(closure))
    s.formula("D9", f"IF(NOT(ISNUMBER({closure})),\"Not scored\",IF({closure}<=0,\"Not started\","
                    f"IF({closure}<0.5,\"Early\",IF({closure}<1,\"On the way\",\"At target\"))))")
    s.text("E9", "To-Be minus current, added up. The bar shows how much of the first assessment's gap is closed.", S_BODY)
    # 10 at target
    s.text("A10", "Dimensions at target", S_BODY)
    s.formula("B10", "IF(COUNT($F$17:$F$27)=0,\"Not scored\",COUNTIF($F$17:$F$27,0)&\" of \"&COUNT($F$17:$F$27))")
    s.formula("C10", bar("IF(COUNT($F$17:$F$27)=0,\"\",COUNTIF($F$17:$F$27,0)/COUNT($F$17:$F$27))"))
    s.formula("D10", "IF(COUNT($F$17:$F$27)=0,\"Not scored\",IF(COUNTIF($F$17:$F$27,0)=COUNT($F$17:$F$27),\"At target\","
                     "\"Gaps open\"))")
    s.text("E10", "Dimensions where the current level has reached the To-Be level.", S_BODY)
    # 11 measures with evidence
    s.text("A11", "Measures with a value and evidence", S_BODY)
    s.formula("B11", f"IF({nmeas}=0,\"Not measured yet\",{evid}&\" of \"&{nmeas})")
    s.formula("C11", bar(f"IF({nmeas}=0,\"\",{evid}/{nmeas})"))
    s.formula("D11", f"IF({nmeas}=0,\"No measures yet\",IF({evid}/{nmeas}>={E},\"Evidenced\",IF({evid}/{nmeas}>={P},"
                     f"\"Partly evidenced\",\"Mostly unevidenced\")))")
    s.text("E11", "Measures that have a latest value and an evidence reference. Cut-offs are on the Start sheet.", S_BODY)
    # 12 measures achieved
    ndef = f"COUNTA(Measures!$A${MFIRST}:$A${MLAST})"
    s.text("A12", "Measures achieved", S_BODY)
    proven = f"COUNT(Measures!$U${MFIRST}:$U${MLAST})"
    s.formula("B12", f"IF({ndef}=0,\"No measures defined\",{proven}&\" of \"&{ndef})")
    s.formula("C12", bar(f"IF({ndef}=0,\"\",{proven}/{ndef})"))
    s.formula("D12", f"IF({ndef}=0,\"No measures yet\",IF({proven}=0,\"None achieved yet\",\"Some achieved\"))")
    s.text("E12", "Marked achieved and proven: a latest value, a date, and evidence. A forecast is never counted here.", S_BODY)
    # 13 forecast and baseline
    s.text("A13", "Forecast and baseline only", S_BODY)
    s.formula("B13", f"COUNTIF(Measures!$L${MFIRST}:$L${MLAST},\"forecast\")&\" forecast, \"&COUNTIF(Measures!$L${MFIRST}:$L${MLAST},"
                     f"\"baseline only\")&\" baseline only\"")
    s.blank("C13", S_CALC)
    s.formula("D13", f"IF(COUNTIF(Measures!$L${MFIRST}:$L${MLAST},\"forecast\")>0,\"Not yet saved\",\"Nothing forecast\")")
    s.text("E13", "Estimates and starting points. These are not benefits yet.", S_BODY)

    band(15, "By dimension")
    headers(s, 16, ["Dimension", "Baseline level", "Current level", "To-Be level", "Plan decision",
                    "Remaining gap", "Change since baseline", "Status"])
    # re-lay: A dimension, B baseline, C current, D to-be, E plan decision, F remaining gap, G change, H status
    for i in range(N):
        r = 17 + i
        a = FIRST + i
        s.formula(f"A{r}", f"Assess!B{a}")
        s.formula(f"B{r}", f"IF(ISNUMBER(Assess!C{a}),Assess!C{a},\"\")")
        s.formula(f"C{r}", f"'Re-score'!M{a}")
        s.formula(f"D{r}", f"IF(ISNUMBER(Assess!E{a}),Assess!E{a},\"\")")
        s.formula(f"E{r}", f"IF(LEN(Plan!E{a})=0,\"\",Plan!E{a})")
        s.formula(f"F{r}", f"IF(AND(ISNUMBER(C{r}),ISNUMBER(D{r})),MAX(0,D{r}-C{r}),\"\")")
        s.formula(f"G{r}", f"IF(AND(ISNUMBER(B{r}),ISNUMBER(C{r})),C{r}-B{r},\"\")")
        s.formula(f"H{r}", f"IF(NOT(ISNUMBER(F{r})),\"Not scored\",IF(F{r}=0,\"At target\",IF(F{r}=1,\"One level to go\","
                           f"\"Far from target\")))")
    s.text("A28", "Total", S_LABEL)
    s.formula("B28", "IF(COUNT(B17:B27)=0,\"Not scored\",SUM(B17:B27))")
    s.formula("C28", "IF(COUNT(C17:C27)=0,\"Not scored\",SUM(C17:C27))")
    s.formula("D28", "IF(COUNT(D17:D27)=0,\"Not scored\",SUM(D17:D27))")
    s.formula("F28", "IF(COUNT(F17:F27)=0,\"Not scored\",SUM(F17:F27))")
    s.formula("G28", "IF(COUNT(G17:G27)=0,\"Not scored\",SUM(G17:G27))")

    band(30, "Six leadership questions")
    headers(s, 31, ["Question", "Answer", "Status", "Source and note"])
    mq = f"Measures!$S${MFIRST}:$S${MLAST}"
    for k, q in enumerate(QUESTIONS, 1):
        r = 31 + k
        s.text(f"A{r}", q, S_BODY)
        idx = f"MATCH({k},{mq},0)"
        if k < 6:
            s.formula(f"B{r}", f"IF(COUNTIF({mq},{k})=0,\"Not found.\",IF(NOT(ISNUMBER(INDEX(Measures!$I${MFIRST}:$I${MLAST},{idx}))),"
                               f"\"Not measured yet\",INDEX(Measures!$I${MFIRST}:$I${MLAST},{idx})&\" \"&"
                               f"INDEX(Measures!$D${MFIRST}:$D${MLAST},{idx})))")
            s.formula(f"C{r}", f"IF(COUNTIF({mq},{k})=0,\"Not found\",INDEX(Measures!$L${MFIRST}:$L${MLAST},{idx}))")
            s.formula(f"D{r}", f"IF(COUNTIF({mq},{k})=0,\"No measure is tagged to this question.\","
                               f"INDEX(Measures!$A${MFIRST}:$A${MLAST},{idx}))")
        else:
            ach = (f"COUNTIFS(Measures!$U${MFIRST}:$U${MLAST},1,Measures!$M${MFIRST}:$M${MLAST},\"cost saved\","
                   f"Measures!$N${MFIRST}:$N${MLAST},\">0\")")
            sa = (f"SUMIFS(Measures!$N${MFIRST}:$N${MLAST},Measures!$U${MFIRST}:$U${MLAST},1,"
                  f"Measures!$M${MFIRST}:$M${MLAST},\"cost saved\")")
            sf = (f"SUMIFS(Measures!$N${MFIRST}:$N${MLAST},Measures!$L${MFIRST}:$L${MLAST},\"forecast\","
                  f"Measures!$M${MFIRST}:$M${MLAST},\"cost saved\")")
            s.formula(f"B{r}", f"IF({ach}=0,\"No achieved savings recorded\",\"Achieved, with evidence: \"&TEXT({sa},\"#,##0\"))")
            s.formula(f"C{r}", f"IF({ach}=0,\"Not proven\",\"Achieved\")")
            s.formula(f"D{r}", f"IF({sf}=0,\"No forecast amount recorded.\",\"Forecast, not counted: \"&TEXT({sf},\"#,##0\"))")
    band(39, "Checks")
    headers(s, 40, ["Check", "Result", "What to do"])
    chk = [
        ("Achieved measures that are not yet proven",
         f"COUNTIF(Measures!$L${MFIRST}:$L${MLAST},\"achieved\")-COUNT(Measures!$U${MFIRST}:$U${MLAST})",
         "B41>0", "Add a value, a date, and evidence, or change the status before you report.", "None."),
        ("Funded gaps missing an owner, action, or date",
         f"COUNTIF(Plan!$J${FIRST}:$J${LAST},\"Add owner*\")",
         "B42>0", "Name an owner, a first action, and a date for each gap you fund.", "None."),
        ("Gaps marked Fund now", f"COUNTIF(Plan!$E${FIRST}:$E${LAST},\"Fund now\")", "B43>3",
         "More than three at once.", "Within three."),
        ("Targets set at level 3", f"COUNTIF(Assess!$E${FIRST}:$E${LAST},3)", "B44>=6",
         "Most targets are 3. Pick the few that matter. Level 2 is a strong result.", "No concern."),
        ("Scores of 1 or more with no evidence",
         f"COUNTIF(Assess!$H${FIRST}:$H${LAST},\"Needs evidence*\")", "B45>0",
         "Add the evidence, or score one level lower.", "None."),
    ]
    for i, (label, f, cond, todo, ok) in enumerate(chk, 41):
        s.text(f"A{i}", label, S_BODY)
        s.formula(f"B{i}", f)
        s.formula(f"C{i}", f"IF({cond},\"{todo}\",\"{ok}\")")
    # conditional fills: words stay the signal
    s.highlight("D8:D13 H17:H27 C2:C3", "D8", "OR(ISNUMBER(SEARCH(\"At target\",D8)),ISNUMBER(SEARCH(\"Evidenced\",D8)),"
                "ISNUMBER(SEARCH(\"Current\",D8)))", 1)
    s.highlight("D8:D13 H17:H27 C2:C3", "D8", "OR(ISNUMBER(SEARCH(\"Far from\",D8)),ISNUMBER(SEARCH(\"Stale\",D8)),"
                "ISNUMBER(SEARCH(\"Mostly\",D8)),ISNUMBER(SEARCH(\"Not started\",D8)))", 0)
    s.highlight("C41:C45", "C41", "AND(LEN(C41)>0,ISERROR(SEARCH(\"None\",C41)),ISERROR(SEARCH(\"Within\",C41)),"
                "ISERROR(SEARCH(\"No concern\",C41)))", 0)
    return s



IDEAS = [
    ("Policy and decision rights", "Policy exceptions with a current approved waiver",
     "Exceptions that have an approved, unexpired waiver, divided by exceptions found.",
     "Exception log and audit findings.", "Up", "Stop looking for exceptions.", "No"),
    ("Roles and ownership", "Valid-owner rate",
     "Applications whose named owner is an active employee, divided by all applications.",
     "Inventory matched to the HR roster.", "Up", "Name a shared mailbox or a senior executive as owner.", "No"),
    ("Inventory and data quality", "Two-way sample match",
     "Of a sample of discovered items, the share found in the record; and of a sample of records, the share found "
     "in discovery.", "Discovery output and sign-in logs.", "Up", "Shrink the scope or leave out unknown items.",
     "Yes: needs discovery data"),
    ("Intake and acquisition", "Off-path spend share",
     "Software spend with no intake request, divided by all software spend.",
     "Accounts payable and expense-card data.", "Down", "Recode spend into other categories.", "No"),
    ("Lifecycle and periodic review", "Overdue reviews, and reviews that changed something",
     "Applications past their review date; and the share of completed reviews that changed a decision.",
     "Inventory review dates.", "Overdue down; changes not zero", "Confirm every review automatically.", "No"),
    ("Licenses, contracts, and renewals", "Renewals decided before the notice date",
     "Renewals decided before their notice deadline, divided by renewals that reached their notice deadline in the "
     "period.", "Renewal calendar.", "Up", "Default every decision to renew.", "No"),
    ("Licenses, contracts, and renewals", "Proof coverage",
     "Quantity you can prove, divided by quantity in use, in the license metric the contract counts.",
     "Proof-of-purchase check.", "Up", "Count keys or certificates as proof.", "No"),
    ("Cost, value, and rationalization", "Realized savings confirmed by finance",
     "Savings where finance confirms the spend stopped, shown beside the forecast.", "Accounts payable.",
     "Measured, not forecast", "Count list-price avoidance as savings.", "No"),
    ("Cost, value, and rationalization", "Unused paid seats",
     "Paid seats with no use in 90 days, divided by paid seats.", "Admin consoles and sign-in logs.", "Down",
     "Reclaim seats, then buy them again.", "Yes: needs usage data"),
    ("Risk, security, and AI use", "Sensitive applications with a current assessment",
     "High-sensitivity applications with a current risk assessment and treatments closed on time; and applications "
     "past vendor support.", "Risk register and vendor support dates.", "Up; past support down",
     "Under-rate sensitivity.", "No"),
    ("Retirement and data disposition", "Retirements closed with full evidence",
     "Retirements with license released, access removed, data disposition recorded, and wipe certificate filed, "
     "divided by retirements.", "Retirement sign-offs.", "Up", "Delay marking the asset retired.", "No"),
    ("Retirement and data disposition", "Invoices paid after retirement",
     "Invoices paid for an asset after its retirement date.", "Accounts payable.", "Down",
     "Delay marking the asset retired.", "No"),
    ("Measures and leadership reporting", "Measures that led to a decision",
     "Measures that led to a logged decision this period, divided by measures reported.", "Decision log.", "Up",
     "Log trivial decisions.", "No"),
    ("Communication and education", "New owners briefed on time",
     "New owners briefed within a set number of days of taking the role; and repeat off-path buying by briefed "
     "people.", "HR role changes and the off-path spend share.", "Up; repeat buying down",
     "Count attendance as understanding.", "No"),
]


def build_ideas() -> Sheet:
    s = Sheet("Ideas", [30, 34, 52, 34, 22, 36, 22])
    s.freeze = (2, 4)
    s.text("A1", "Ideas: measures that are hard to fake", S_TITLE)
    s.text("A2", "Pick one or two for each gap you fund, then record them on the Measures sheet. Targets depend on your "
                 "risk, so the sponsor sets each one. Every measure can be gamed; the last column says how, so you "
                 "can check for it.", S_HINT)
    headers(s, 4, ["Dimension", "Measure", "How to calculate it", "Where the data comes from",
                   "Better direction", "How people game it", "Needs a tool?"])
    for i, row in enumerate(IDEAS):
        for j, v in enumerate(row):
            s.text(f"{_col_letter(j)}{FIRST + i}", v, S_BODY)
    return s

# ---------- example data (the Halden demo estate) ----------

def example_data() -> dict:
    assess = [
        (1, "The draft policy says it applies 'where appropriate', names no accountable role, and sets no review cycle. "
            "No approval date is recorded.", 2, "A written, approved policy is needed before a publisher audit can be "
                                              "answered; by 2026-12-31."),
        (1, "apps.csv has no owner column, and the council draft names no sponsor.", 2,
         "Renewals cannot be decided without an accountable owner for each application; by 2027-03-31."),
        (1, "One list exists with cost, users, and data sensitivity for 60 applications. It has no owner and no stated "
            "refresh schedule.", 2, "The list is the base for every other dimension; by 2027-03-31."),
        (1, "The policy and the council charter both require a request form. Nothing shows how many purchases use it.", 2,
         "Unplanned purchases are the main source of duplicates; by 2027-06-30."),
        (0, "apps.csv has no lifecycle state or review date.", 2,
         "Each application needs a state and a review date before renewals can be tied to a need; by 2027-06-30."),
        (1, "licenses.csv records entitlements and expiry dates. 2 of 60 licenses were already expired on 2026-09-01. "
            "No notice period or auto-renew field exists.", 2, "Missing notice deadlines turn into silent renewals; by "
                                                              "2026-12-31."),
        (1, "Annual cost and user count are recorded for each application. No keep, change, or retire call is "
            "recorded.", 2, "Duplicate spend is the largest saving available; by 2027-03-31."),
        (1, "Data sensitivity is recorded for all 60 applications. The 6 AI systems each have a named owner and a "
            "description. No risk tier is recorded.", 2, "AI systems that touch organizational data need a tier before "
                                                        "approval; by 2027-03-31."),
        (1, "2 of the 10 retired devices in devices.csv have no wipe confirmation.", 2,
         "Unwiped devices are a data risk; by 2026-12-31."),
        (0, "The council draft lists measures. No data shows any measure is being reported.", 2,
         "Leaders cannot fund what they cannot see; by 2027-06-30."),
        (1, "The policy is available on the intranet. There is no record that owners were told what is expected.", 2,
         "Owners must know their duties before ownership is enforced; by 2027-06-30."),
    ]
    plan = [
        (1, "Fund now", "Governance lead", "Fix the draft with the policy review checklist, then get the sponsor to "
                                          "approve it.", "2026-12-31"),
        (2, "Defer", "Governance analyst", "Add an owner field and assign an owner to each of the 60 applications.",
         "2027-03-31"),
        (2, "Defer", "Governance analyst", "Name apps.csv the record of authority and set a quarterly refresh.",
         "2027-03-31"),
        (3, "Defer", "Procurement lead", "Count the share of software bought through the form, as the charter "
                                         "proposes.", "2027-06-30"),
        (3, "Defer", "Governance analyst", "Add a lifecycle state and a next-review date to the inventory.",
         "2027-06-30"),
        (1, "Fund now", "Procurement lead", "Start the renewal calendar for every license expiring in the next 180 "
                                            "days.", "2026-12-31"),
        (2, "Defer", "Finance partner", "Run the rationalization method and record a decision for each duplicate "
                                        "pair.", "2027-03-31"),
        (2, "Defer", "Security lead", "Tier each of the 6 AI systems with the AI intake method.", "2027-03-31"),
        (1, "Fund now", "Hardware asset manager", "Hold those 2 devices open and complete the retirement sign-off "
                                                  "checklist.", "2026-12-31"),
        (3, "Defer", "Governance analyst", "Pick five measures, set a baseline, and issue the first leadership "
                                           "report.", "2027-06-30"),
        (3, "Defer", "Governance lead", "Brief the new owners and record that they have read and understood their "
                                        "duties.", "2027-06-30"),
    ]
    T, N_, D = S_IN_TEXT, S_IN_NUM, S_IN_DATE
    measures = [
        [("A", "B-001", T), ("B", "Renewal calendar with owners and notice deadlines", T),
         ("C", "Licenses past expiry with no recorded decision", T), ("D", "licenses", T), ("E", 2, N_),
         ("F", serial("2026-09-01"), D), ("G", 0, N_), ("L", "baseline only", T), ("M", "risk reduced", T),
         ("O", "Procurement lead", T),
         ("P", "Baseline from licenses.csv: LIC-017 and LIC-044. The file has no owner or notice fields. Out of 60.", T)],
        [("A", "B-002", T), ("B", "Retirement sign-off checklist", T), ("C", "Retired devices without wipe confirmation", T),
         ("D", "devices", T), ("E", 2, N_), ("F", serial("2026-09-01"), D), ("G", 0, N_),
         ("L", "baseline only", T), ("M", "risk reduced", T), ("O", "Hardware asset manager", T),
         ("P", "Baseline from devices.csv: DEV-011 and DEV-042 have no confirmation. Money effect not found. Out of 10.", T)],
        [("A", "B-004", T), ("B", "AI intake and risk tiering", T), ("C", "AI systems without a recorded risk tier", T),
         ("D", "systems", T), ("E", 6, N_), ("F", serial("2026-09-01"), D), ("G", 0, N_),
         ("L", "baseline only", T), ("M", "risk reduced", T), ("O", "AI governance board", T),
         ("P", "All six systems have a named owner. No tier is recorded for any. The board sets the date. Out of 6.", T)],
        [("A", "B-005", T), ("B", "Rationalization of duplicate applications", T),
         ("C", "Annual savings achieved, backed by evidence", T), ("D", "USD a year", T), ("E", 0, N_),
         ("F", serial("2026-09-01"), D), ("L", "forecast", T), ("M", "cost saved", T), ("O", "Finance partner", T),
         ("P", "Forecast range from the tool: 250000 to 355400 a year. Count a saving only after the contract ends and "
                "the spend stops, and net out added license cost.", T), ("S", 6, N_)],
        [("A", "B-006", T), ("B", "Audit-ready proofs of purchase", T), ("C", "Proofs of purchase with an open issue", T),
         ("D", "proofs", T), ("E", 4, N_), ("F", serial("2026-08-24"), D), ("G", 0, N_),
         ("L", "baseline only", T), ("M", "risk reduced", T), ("O", "Asset manager", T),
         ("P", "Baseline from the audit response case: three proofs need repair and one needs an explanation. Out of 6.", T),
         ("S", 4, N_)],
    ]
    return {"date": "2026-09-01", "assess": assess, "plan": plan, "measures": measures}


# ---------- package ----------

def workbook_bytes(example: bool = False) -> bytes:
    data = example_data() if example else None
    settings_row = 46
    sheets = [build_start(example, settings_row), build_assess(data), build_plan(data), build_measures(data),
              build_scorecard(settings_row), build_rescore(data), build_ideas()]
    n = len(sheets)
    name_ref = lambda nm: f"'{nm}'" if "-" in nm else nm
    titles = "".join(
        f"<definedName name=\"_xlnm.Print_Titles\" localSheetId=\"{i}\">{name_ref(sh.name)}!$4:$4</definedName>"
        for i, sh in enumerate(sheets) if sh.name in ("Assess", "Plan", "Measures", "Re-score"))
    core = (XML_HEAD + "<cp:coreProperties xmlns:cp=\"http://schemas.openxmlformats.org/package/2006/metadata/"
            "core-properties\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:dcterms=\"http://purl.org/dc/terms/\" "
            "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">"
            "<dc:title>Application management program workbook</dc:title><dc:creator>Eve McGivern</dc:creator>"
            "<dc:language>en-US</dc:language>"
            "<dcterms:created xsi:type=\"dcterms:W3CDTF\">2020-01-01T00:00:00Z</dcterms:created>"
            "</cp:coreProperties>")
    parts = [
        ("[Content_Types].xml", (
            XML_HEAD + "<Types xmlns=\"http://schemas.openxmlformats.org/package/2006/content-types\">"
            "<Default Extension=\"rels\" ContentType=\"application/vnd.openxmlformats-package.relationships+xml\"/>"
            "<Default Extension=\"xml\" ContentType=\"application/xml\"/>"
            "<Override PartName=\"/xl/workbook.xml\" "
            "ContentType=\"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml\"/>"
            "<Override PartName=\"/xl/styles.xml\" "
            "ContentType=\"application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml\"/>"
            "<Override PartName=\"/docProps/core.xml\" "
            "ContentType=\"application/vnd.openxmlformats-package.core-properties+xml\"/>"
            + "".join(f"<Override PartName=\"/xl/worksheets/sheet{i}.xml\" "
                      "ContentType=\"application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml\"/>"
                      for i in range(1, n + 1)) + "</Types>")),
        ("_rels/.rels", (
            XML_HEAD + "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">"
            "<Relationship Id=\"rId1\" "
            "Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument\" "
            "Target=\"xl/workbook.xml\"/>"
            "<Relationship Id=\"rId2\" "
            "Type=\"http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties\" "
            "Target=\"docProps/core.xml\"/></Relationships>")),
        ("docProps/core.xml", core),
        ("xl/workbook.xml", (
            XML_HEAD + "<workbook xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\" "
            "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\">"
            "<bookViews><workbookView activeTab=\"0\"/></bookViews><sheets>"
            + "".join(f"<sheet name=\"{escape(sh.name, quote=True)}\" sheetId=\"{i}\" r:id=\"rId{i}\"/>"
                      for i, sh in enumerate(sheets, 1)) + f"</sheets><definedNames>{titles}</definedNames>"
            "<calcPr fullCalcOnLoad=\"1\"/></workbook>")),
        ("xl/_rels/workbook.xml.rels", (
            XML_HEAD + "<Relationships xmlns=\"http://schemas.openxmlformats.org/package/2006/relationships\">"
            + "".join(f"<Relationship Id=\"rId{i}\" "
                      "Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet\" "
                      f"Target=\"worksheets/sheet{i}.xml\"/>" for i in range(1, n + 1))
            + f"<Relationship Id=\"rId{n + 1}\" "
            "Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles\" "
            "Target=\"styles.xml\"/></Relationships>")),
        ("xl/styles.xml", STYLES),
    ]
    for i, sh in enumerate(sheets, 1):
        parts.append((f"xl/worksheets/sheet{i}.xml", sh.xml()))
    return _zip(tuple(parts))
