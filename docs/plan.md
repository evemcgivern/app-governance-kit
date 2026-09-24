# app-governance-kit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a public, career-first governance toolkit: six governance methods (including how to stand up a governance program), each written once and packaged for Claude, Codex, and Copilot 365, plus a demo company with planted problems, a field guide to the certifications and their practical use, and a six-page portfolio site.

**Architecture:** Hand-written content lives in `methods/<tool>/`. A Python standard-library build (`build/agk/`) checks that content (all pieces present, every checklist and SOP step tagged to a crosswalk clause, Copilot length limits) and generates `dist/claude`, `dist/codex`, and `dist/copilot`. A grader compares each tool's findings against the demo company's answer key. The site is self-contained HTML; the build injects crosswalk data into the explorer page.

**Tech Stack:** Python 3.11+ standard library only (unittest, csv, json, zipfile, argparse); self-contained HTML/CSS/JS; `claude` and `codex` CLIs for evals; `cmdb_package` converters for Word/Excel export (export step only, never a runtime dependency).

**Spec:** `/Applications/Development/Projects/Project Notes/app-governance-kit/2026-09-24-design.md`

## Plain-English summary

We build this in five stretches.

1. **The engine (Tasks 1–4):** a small program that checks the governance content and packages it for Claude, Codex, and Copilot. It refuses to package anything incomplete, any step not tied to a framework clause, or any Copilot version that's too long.
2. **The fake company (Task 5):** Halden Logistics, with 60 apps, licenses, staff accounts, AI systems, and a maturity questionnaire. Known problems are hidden in it, including a flawed draft charter for a software governance council, and an answer key records them. A grader (Task 6) scores each tool against that key.
3. **The six tools (Tasks 7–11b):** the crosswalk first, because every other tool's steps point at it. Eve checks every ISO clause number against her own copies of the standards; the build won't accept an unchecked row.
4. **The extras (Tasks 12–13):** the Claude reviewer agent, and Word/Excel exports of each checklist, SOP, and template.
5. **The public face (Tasks 14–16):** the site with a clickable application lifecycle wheel (questions to ask at each stage, linked to the tools), a field guide (CAMP, CSAM, CHAMP, and AIGP and how each applies on the job, plus where data governance fits), a six-exercise Halden practicum with self-checking, three case studies from interviews with Eve, and the go-public checklist. The repo goes public only when Eve says so.

Timing: Tasks 1–6 take about two evenings. Each tool takes one or two evenings, mostly Eve's review time. The site and case studies take about a week of evenings.

## Global Constraints

- Python standard library only in `build/` and `demo-estate/`. No pip installs. (Memory: no third-party runtime deps in skills.)
- Repo: `/Applications/Development/Projects/app-governance-kit`; remote `github.com/eve-mcgivern/app-governance-kit`, created **private** first; public only on Eve's explicit go-ahead (Task 16).
- Never quote ISO or COBIT text. Cite clause numbers; paraphrase meaning. Quoted runs of 15+ words fail the scan.
- No employer data. The private word list lives outside the repo at the path in `AGK_PRIVATE_WORDS`; the scan fails if it is unset or missing.
- Copilot agent instructions: fail above 8,000 characters; warn above 6,000.
- Every numbered step or `- [ ]` item in `checklist.md` and `sop.md` carries at least one `[[XW-NNN]]` tag that exists in the crosswalk.
- Every crosswalk row has a non-empty `verified` date, entered by Eve after checking clause references against the standards.
- Tool outputs end with a fenced ```` ```findings ```` block holding a JSON list of `{"type": ..., "id": ...}`.
- Commits: `type(scope): imperative summary`, ≤50 chars, lowercase after colon, ending with:
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` and
  `Claude-Session: https://claude.ai/code/session_01CxthZSoP1hm8J6w9VwKbX6`
- Never commit to `main` after the initial empty commit. Work on `feat/<name>` branches; merge after review (`review-merge-pipeline`).
- Test command everywhere: `PYTHONPATH=build python3 -m unittest discover -s tests -v`

## Review Focus

1. **Files saved on Windows (CRLF endings, BOM).** Eve edits some files on a work machine. Frontmatter must still parse. Test in Task 1.
2. **Indented sub-steps.** A nested `   2. ...` step inside an SOP still needs a clause tag; steps inside code fences do not. Tests in Task 3.
3. **Tool output with no findings block, or broken JSON.** The grader must fail loudly, never report a pass. Tests in Task 6.
4. **Missing private word list.** The scan must stop with an error, never pass silently. Test in Task 4.
5. **Word files exported through `cmdb_package`.** Its templates came from a workplace, so employer names could ride along in document styles or properties. The scan reads the text inside `.docx` files. Test in Task 4; run in Task 13.

---

### Task 1: Repo, method loader, and completeness check

**Files:**
- Create: `app-governance-kit/.gitignore`, `Makefile`, `README.md` (stub), `build/agk/__init__.py`, `build/agk/methods.py`, `tests/__init__.py`, `tests/helpers.py`, `tests/test_methods.py`

**Interfaces:**
- Produces: `MethodError(Exception)`; `parse_frontmatter(text: str) -> tuple[dict[str, str], str]`; `Method` dataclass (`name, title, description: str; dir: Path; body: str; template: Path`); `load_method(d: Path) -> Method`; `method_dirs(methods_dir: Path) -> list[Path]`; `REQUIRED_FILES`.
- Test helpers: `make_repo(tmp: Path) -> Path`, `make_method(root: Path, name: str, body: str = ..., **files) -> Path` (a file value of `None` omits it).

- [ ] **Step 1: Create the repo**

```bash
mkdir -p /Applications/Development/Projects/app-governance-kit && cd $_
git init -b main
git commit --allow-empty -m "chore: initialize repository"
git switch -c feat/foundation
mkdir -p build/agk tests methods agents demo-estate site case-studies
touch build/agk/__init__.py tests/__init__.py
printf 'dist/office/\n__pycache__/\n*.redline.html\n.DS_Store\n' > .gitignore
```

`Makefile`:

```make
PY = PYTHONPATH=build python3
test:
	$(PY) -m unittest discover -s tests -v
build:
	$(PY) -m agk.build
scan:
	$(PY) -m agk.scan
.PHONY: test build scan
```

`README.md`: `# app-governance-kit\n\nGovernance methods for application portfolio, AI, and access controls. Work in progress.\n`

- [ ] **Step 2: Write the test helpers**

`tests/helpers.py`:

```python
from pathlib import Path

XW_HEADER = "id,theme,iso19770_1,cobit2019,iso27001,iso42001,summary,verified\n"
XW_ROW = "XW-001,Inventory,8.2,BAI09.01,A.5.9,,Keep an application inventory,2026-09-24\n"


def make_method(root: Path, name: str, body: str = "Do the thing.", **files) -> Path:
    d = root / "methods" / name
    d.mkdir(parents=True, exist_ok=True)
    contents = {
        "method.md": f"---\nname: {name}\ntitle: {name.title()}\ndescription: Test method\n---\n{body}\n",
        "checklist.md": "1. Record the app [[XW-001]]\n",
        "sop.md": "## Steps\n\n1. Record the app [[XW-001]]\n",
        "platform-guide.md": "Guide\n",
        "copilot-test.md": "Test\n",
        "template.md": "Template\n",
        "example/input.md": "in\n",
    }
    contents.update(files)
    for rel, text in contents.items():
        if text is None:
            continue
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return d


def make_repo(tmp: Path) -> Path:
    make_method(tmp, "crosswalk")
    (tmp / "methods" / "crosswalk" / "crosswalk.csv").write_text(XW_HEADER + XW_ROW, encoding="utf-8")
    (tmp / "agents").mkdir()
    (tmp / "agents" / "governance-reviewer.md").write_text(
        "---\nname: governance-reviewer\ndescription: test\n---\nReview.\n", encoding="utf-8")
    return tmp
```

Pass file overrides as a dict: `make_method(root, "x", **{"example/input.md": None})` omits that file.

- [ ] **Step 3: Write the failing tests**

`tests/test_methods.py`:

```python
import tempfile
import unittest
from pathlib import Path

from agk.methods import MethodError, load_method, method_dirs, parse_frontmatter
from tests.helpers import make_method


class FrontmatterTests(unittest.TestCase):
    def test_parses_keys_and_body(self):
        meta, body = parse_frontmatter("---\nname: x\ntitle: X\n---\nBody\n")
        self.assertEqual(meta, {"name": "x", "title": "X"})
        self.assertEqual(body, "Body\n")

    def test_accepts_crlf_and_bom(self):
        meta, body = parse_frontmatter("﻿---\r\nname: x\r\n---\r\nBody\r\n")
        self.assertEqual(meta["name"], "x")
        self.assertEqual(body, "Body\n")

    def test_rejects_missing_frontmatter(self):
        with self.assertRaises(MethodError):
            parse_frontmatter("Body only\n")

    def test_rejects_unterminated_frontmatter(self):
        with self.assertRaises(MethodError):
            parse_frontmatter("---\nname: x\nBody\n")


class LoadMethodTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def test_loads_complete_method(self):
        m = load_method(make_method(self.tmp, "rationalization"))
        self.assertEqual(m.name, "rationalization")
        self.assertEqual(m.template.name, "template.md")

    def test_names_every_missing_piece(self):
        d = make_method(self.tmp, "x", **{"sop.md": None, "copilot-test.md": None})
        with self.assertRaises(MethodError) as ctx:
            load_method(d)
        self.assertIn("sop.md", str(ctx.exception))
        self.assertIn("copilot-test.md", str(ctx.exception))

    def test_requires_a_template(self):
        d = make_method(self.tmp, "x", **{"template.md": None})
        with self.assertRaisesRegex(MethodError, "template"):
            load_method(d)

    def test_accepts_csv_template(self):
        d = make_method(self.tmp, "x", **{"template.md": None, "template.csv": "a,b\n"})
        self.assertEqual(load_method(d).template.name, "template.csv")

    def test_rejects_two_templates(self):
        d = make_method(self.tmp, "x", **{"template.csv": "a,b\n"})
        with self.assertRaisesRegex(MethodError, "one template"):
            load_method(d)

    def test_requires_nonempty_example(self):
        d = make_method(self.tmp, "x", **{"example/input.md": None})
        (d / "example").mkdir(exist_ok=True)
        with self.assertRaisesRegex(MethodError, "example"):
            load_method(d)

    def test_name_must_match_folder(self):
        d = make_method(self.tmp, "x", **{"method.md": "---\nname: y\ntitle: Y\ndescription: d\n---\nB\n"})
        with self.assertRaisesRegex(MethodError, "match folder"):
            load_method(d)

    def test_requires_description(self):
        d = make_method(self.tmp, "x", **{"method.md": "---\nname: x\ntitle: X\n---\nB\n"})
        with self.assertRaisesRegex(MethodError, "description"):
            load_method(d)

    def test_method_dirs_skips_hidden_and_underscored(self):
        make_method(self.tmp, "b")
        make_method(self.tmp, "a")
        (self.tmp / "methods" / "_drafts").mkdir()
        (self.tmp / "methods" / ".git").mkdir()
        self.assertEqual([p.name for p in method_dirs(self.tmp / "methods")], ["a", "b"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 4: Run tests to verify they fail**

Run: `PYTHONPATH=build python3 -m unittest discover -s tests -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'agk.methods'`

- [ ] **Step 5: Implement `build/agk/methods.py`**

```python
from dataclasses import dataclass
from pathlib import Path

REQUIRED_FILES = ("method.md", "checklist.md", "sop.md", "platform-guide.md", "copilot-test.md")
REQUIRED_META = ("name", "title", "description")


class MethodError(Exception):
    pass


@dataclass(frozen=True)
class Method:
    name: str
    title: str
    description: str
    dir: Path
    body: str
    template: Path


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    text = text.lstrip("﻿").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        raise MethodError("missing frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise MethodError("unterminated frontmatter")
    meta = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        if not sep:
            raise MethodError(f"bad frontmatter line: {line!r}")
        meta[key.strip()] = value.strip()
    return meta, text[end + 5:]


def load_method(d: Path) -> Method:
    missing = [f for f in REQUIRED_FILES if not (d / f).is_file()]
    templates = sorted(p for p in d.glob("template.*") if p.suffix in (".md", ".csv"))
    if not templates:
        missing.append("template.md or template.csv")
    example = d / "example"
    if not example.is_dir() or not any(example.iterdir()):
        missing.append("example/ (with at least one file)")
    if missing:
        raise MethodError(f"{d.name}: missing {', '.join(missing)}")
    if len(templates) > 1:
        raise MethodError(f"{d.name}: expected one template, found {[p.name for p in templates]}")
    meta, body = parse_frontmatter((d / "method.md").read_text(encoding="utf-8"))
    absent = [k for k in REQUIRED_META if not meta.get(k)]
    if absent:
        raise MethodError(f"{d.name}: method.md frontmatter missing {', '.join(absent)}")
    if meta["name"] != d.name:
        raise MethodError(f"{d.name}: frontmatter name {meta['name']!r} must match folder name")
    return Method(meta["name"], meta["title"], meta["description"], d, body, templates[0])


def method_dirs(methods_dir: Path) -> list[Path]:
    return sorted(p for p in methods_dir.iterdir()
                  if p.is_dir() and not p.name.startswith(("_", ".")))
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `PYTHONPATH=build python3 -m unittest discover -s tests -v`
Expected: all `FrontmatterTests` and `LoadMethodTests` PASS

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "feat(build): load and validate method folders" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CxthZSoP1hm8J6w9VwKbX6"
```

---

### Task 2: Crosswalk loader

**Files:**
- Create: `build/agk/crosswalk.py`, `tests/test_crosswalk.py`

**Interfaces:**
- Produces: `CrosswalkError(Exception)`; `COLUMNS` tuple; `load_crosswalk(path: Path) -> dict[str, dict[str, str]]` keyed by `XW-NNN`.

- [ ] **Step 1: Write the failing tests**

`tests/test_crosswalk.py`:

```python
import tempfile
import unittest
from pathlib import Path

from agk.crosswalk import CrosswalkError, load_crosswalk
from tests.helpers import XW_HEADER, XW_ROW


class CrosswalkTests(unittest.TestCase):
    def write(self, text):
        p = Path(tempfile.mkdtemp()) / "crosswalk.csv"
        p.write_text(text, encoding="utf-8")
        return p

    def test_loads_rows_by_id(self):
        rows = load_crosswalk(self.write(XW_HEADER + XW_ROW))
        self.assertEqual(rows["XW-001"]["cobit2019"], "BAI09.01")

    def test_rejects_wrong_columns(self):
        with self.assertRaisesRegex(CrosswalkError, "columns"):
            load_crosswalk(self.write("id,theme\nXW-001,x\n"))

    def test_rejects_bad_id(self):
        with self.assertRaisesRegex(CrosswalkError, "line 2"):
            load_crosswalk(self.write(XW_HEADER + XW_ROW.replace("XW-001", "XW-1")))

    def test_rejects_duplicate_id(self):
        with self.assertRaisesRegex(CrosswalkError, "duplicate"):
            load_crosswalk(self.write(XW_HEADER + XW_ROW + XW_ROW))

    def test_rejects_row_mapping_to_no_framework(self):
        row = "XW-002,Empty,,,,,Nothing,2026-09-24\n"
        with self.assertRaisesRegex(CrosswalkError, "no framework"):
            load_crosswalk(self.write(XW_HEADER + row))

    def test_rejects_unverified_row(self):
        with self.assertRaisesRegex(CrosswalkError, "not verified"):
            load_crosswalk(self.write(XW_HEADER + XW_ROW.replace("2026-09-24", "")))
```

- [ ] **Step 2: Run to verify failure**

Run: `PYTHONPATH=build python3 -m unittest tests.test_crosswalk -v`
Expected: FAIL with `No module named 'agk.crosswalk'`

- [ ] **Step 3: Implement `build/agk/crosswalk.py`**

```python
import csv
import re
from pathlib import Path

COLUMNS = ("id", "theme", "iso19770_1", "cobit2019", "iso27001", "iso42001", "summary", "verified")
FRAMEWORK_COLUMNS = COLUMNS[2:6]
ID_RE = re.compile(r"^XW-\d{3}$")


class CrosswalkError(Exception):
    pass


def load_crosswalk(path: Path) -> dict[str, dict[str, str]]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != COLUMNS:
            raise CrosswalkError(f"columns must be {','.join(COLUMNS)}; got {reader.fieldnames}")
        rows: dict[str, dict[str, str]] = {}
        for n, row in enumerate(reader, start=2):
            rid = row["id"].strip()
            if not ID_RE.match(rid):
                raise CrosswalkError(f"line {n}: bad id {rid!r}")
            if rid in rows:
                raise CrosswalkError(f"line {n}: duplicate id {rid}")
            if not any(row[c].strip() for c in FRAMEWORK_COLUMNS):
                raise CrosswalkError(f"line {n}: {rid} maps to no framework")
            if not row["verified"].strip():
                raise CrosswalkError(f"line {n}: {rid} not verified against the standards")
            rows[rid] = row
    return rows
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `PYTHONPATH=build python3 -m unittest tests.test_crosswalk -v`
Expected: 6 PASS

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat(build): load and validate the crosswalk" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CxthZSoP1hm8J6w9VwKbX6"
```

---

### Task 3: Clause tags, renderers, and the build command

**Files:**
- Create: `build/agk/tags.py`, `build/agk/render.py`, `build/agk/build.py`, `tests/test_tags.py`, `tests/test_build.py`

**Interfaces:**
- Consumes: `load_method`, `method_dirs`, `MethodError`, `Method` (Task 1); `load_crosswalk`, `CrosswalkError` (Task 2).
- Produces: `check_tags(text: str, known: Collection[str], label: str) -> list[str]`; `COPILOT_MAX = 8000`, `COPILOT_WARN = 6000`; `render_claude(m, root, xw)`, `render_codex(m, root, xw)`, `render_codex_agents(methods, root)`, `render_copilot(m, root, xw) -> list[str]` (warnings; raises `MethodError` over max); `build(root: Path) -> tuple[list[str], list[str]]` (errors, warnings); `main(argv=None) -> int`.
- Output layout: `dist/claude/.claude-plugin/plugin.json`, `dist/claude/skills/<name>/SKILL.md` + reference files, `dist/claude/agents/governance-reviewer.md`, `dist/codex/skills/<name>/SKILL.md` + reference files, `dist/codex/AGENTS.md`, `dist/copilot/<name>/{agent-instructions.md, chat-prompt.md, test-script.md, knowledge/}`.

- [ ] **Step 1: Write the failing tag tests**

`tests/test_tags.py`:

```python
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
```

- [ ] **Step 2: Run to verify failure**

Run: `PYTHONPATH=build python3 -m unittest tests.test_tags -v`
Expected: FAIL with `No module named 'agk.tags'`

- [ ] **Step 3: Implement `build/agk/tags.py`**

```python
import re
from collections.abc import Collection

STEP_RE = re.compile(r"^\s*(?:\d+\.|- \[[ xX]\])\s+\S")
TAG_RE = re.compile(r"\[\[(XW-\d{3})\]\]")


def check_tags(text: str, known: Collection[str], label: str) -> list[str]:
    errors: list[str] = []
    in_fence = False
    for n, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not STEP_RE.match(line):
            continue
        tags = TAG_RE.findall(line)
        if not tags:
            errors.append(f"{label}:{n}: step has no clause tag")
        errors.extend(f"{label}:{n}: unknown clause tag {t}" for t in tags if t not in known)
    return errors
```

- [ ] **Step 4: Run tag tests to verify they pass**

Run: `PYTHONPATH=build python3 -m unittest tests.test_tags -v`
Expected: 7 PASS

- [ ] **Step 5: Write the failing build tests**

`tests/test_build.py`:

```python
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
```

- [ ] **Step 6: Run to verify failure**

Run: `PYTHONPATH=build python3 -m unittest tests.test_build -v`
Expected: FAIL with `No module named 'agk.build'`

- [ ] **Step 7: Implement `build/agk/render.py`**

```python
import json
import shutil
from pathlib import Path

from agk.methods import Method, MethodError

COPILOT_MAX = 8000
COPILOT_WARN = 6000
REFERENCE_FILES = ("checklist.md", "sop.md", "platform-guide.md")


def _reference_names(m: Method) -> list[str]:
    return [*REFERENCE_FILES, m.template.name, "crosswalk.csv"]


def _copy_references(m: Method, dest: Path, crosswalk_csv: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for f in REFERENCE_FILES:
        shutil.copyfile(m.dir / f, dest / f)
    shutil.copyfile(m.template, dest / m.template.name)
    shutil.copyfile(crosswalk_csv, dest / "crosswalk.csv")


def skill_md(m: Method) -> str:
    refs = "\n".join(f"- `{f}`" for f in _reference_names(m))
    return (f"---\nname: {m.name}\ndescription: {m.description}\n---\n\n# {m.title}\n\n"
            f"{m.body.strip()}\n\n## Reference files\n\n"
            f"Read these from this skill's folder when a step needs them:\n\n{refs}\n")


def _write_skill(m: Method, skills_root: Path, crosswalk_csv: Path) -> None:
    d = skills_root / m.name
    _copy_references(m, d, crosswalk_csv)
    (d / "SKILL.md").write_text(skill_md(m), encoding="utf-8")


def render_claude(m: Method, root: Path, crosswalk_csv: Path) -> None:
    _write_skill(m, root / "skills", crosswalk_csv)


def render_codex(m: Method, root: Path, crosswalk_csv: Path) -> None:
    _write_skill(m, root / "skills", crosswalk_csv)


def render_codex_agents(methods: list[Method], root: Path) -> None:
    lines = ["# app-governance-kit", "",
             "Governance skills. Each folder under `skills/` holds a SKILL.md and its reference files.", ""]
    lines += [f"- `skills/{m.name}/SKILL.md` — {m.title}: {m.description}" for m in methods]
    root.mkdir(parents=True, exist_ok=True)
    (root / "AGENTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def render_claude_manifest(root: Path) -> None:
    d = root / ".claude-plugin"
    d.mkdir(parents=True, exist_ok=True)
    manifest = {"name": "app-governance-kit", "version": "0.1.0",
                "description": "Application portfolio, AI, and access governance methods.",
                "author": {"name": "Eve McGivern"}}
    (d / "plugin.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def render_copilot(m: Method, root: Path, crosswalk_csv: Path) -> list[str]:
    files = ", ".join(_reference_names(m))
    instructions = (f"# {m.title}\n\n{m.body.strip()}\n\n"
                    f"Use the attached knowledge files: {files}.\n")
    n = len(instructions)
    if n > COPILOT_MAX:
        raise MethodError(f"{m.name}: Copilot instructions are {n} characters; limit is {COPILOT_MAX}")
    d = root / m.name
    _copy_references(m, d / "knowledge", crosswalk_csv)
    (d / "agent-instructions.md").write_text(instructions, encoding="utf-8")
    (d / "chat-prompt.md").write_text(
        instructions + "\n## Your input\n\nPaste the data or description below this line, then send.\n",
        encoding="utf-8")
    shutil.copyfile(m.dir / "copilot-test.md", d / "test-script.md")
    if n > COPILOT_WARN:
        return [f"{m.name}: Copilot instructions are {n} characters; combined-length errors are "
                f"reported below {COPILOT_MAX}. Test at work before relying on it."]
    return []
```

- [ ] **Step 8: Implement `build/agk/build.py`**

```python
import argparse
import shutil
import sys
from pathlib import Path

from agk.crosswalk import CrosswalkError, load_crosswalk
from agk.methods import MethodError, load_method, method_dirs
from agk.render import (render_claude, render_claude_manifest, render_codex,
                        render_codex_agents, render_copilot)
from agk.tags import check_tags


def build(root: Path) -> tuple[list[str], list[str]]:
    methods_dir, dist = root / "methods", root / "dist"
    crosswalk_csv = methods_dir / "crosswalk" / "crosswalk.csv"
    try:
        known = load_crosswalk(crosswalk_csv)
    except (CrosswalkError, FileNotFoundError) as e:
        return [f"crosswalk: {e}"], []
    errors: list[str] = []
    warnings: list[str] = []
    methods = []
    for d in method_dirs(methods_dir):
        try:
            methods.append(load_method(d))
        except MethodError as e:
            errors.append(str(e))
    for m in methods:
        for f in ("checklist.md", "sop.md"):
            errors += check_tags((m.dir / f).read_text(encoding="utf-8"), known, f"{m.name}/{f}")
    if errors:
        return errors, warnings
    if dist.exists():
        shutil.rmtree(dist)
    for m in methods:
        render_claude(m, dist / "claude", crosswalk_csv)
        render_codex(m, dist / "codex", crosswalk_csv)
        try:
            warnings += render_copilot(m, dist / "copilot", crosswalk_csv)
        except MethodError as e:
            errors.append(str(e))
    render_claude_manifest(dist / "claude")
    render_codex_agents(methods, dist / "codex")
    agents_dest = dist / "claude" / "agents"
    agents_dest.mkdir(parents=True, exist_ok=True)
    for agent in sorted((root / "agents").glob("*.md")):
        shutil.copyfile(agent, agents_dest / agent.name)
    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build dist/ from methods/.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    errors, warnings = build(args.root)
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    if not errors:
        print("build ok")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 9: Run all tests**

Run: `PYTHONPATH=build python3 -m unittest discover -s tests -v`
Expected: all PASS

- [ ] **Step 10: Commit**

```bash
git add -A
git commit -m "feat(build): package methods for three tools" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CxthZSoP1hm8J6w9VwKbX6"
```

---

### Task 4: Pre-publish scan (private words, long quotes, Word files)

**Files:**
- Create: `build/agk/scan.py`, `tests/test_scan.py`, `.github/workflows/ci.yml`

**Interfaces:**
- Produces: `MAX_QUOTE_WORDS = 15`; `load_words(path: Path) -> list[str]`; `private_hits(text, words, label) -> list[str]`; `long_quotes(text, label) -> list[str]`; `docx_text(path: Path) -> str`; `scan(root: Path, words: list[str]) -> list[str]`; `main(argv=None) -> int` (0 clean, 1 hits, 2 word list unset/missing).

- [ ] **Step 1: Write the failing tests**

`tests/test_scan.py`:

```python
import os
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

from agk.scan import docx_text, load_words, long_quotes, main, private_hits, scan


def make_docx(path: Path, body: str) -> None:
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("word/document.xml", f"<w:document><w:body><w:p><w:r><w:t>{body}</w:t></w:r></w:p></w:body></w:document>")
        z.writestr("docProps/core.xml", "<cp:coreProperties><dc:creator>Author</dc:creator></cp:coreProperties>")


class ScanTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def test_load_words_skips_blank_and_comments(self):
        p = self.tmp / "w.txt"
        p.write_text("# employer\nAcmeCorp\n\nProject Falcon\n")
        self.assertEqual(load_words(p), ["AcmeCorp", "Project Falcon"])

    def test_private_hits_are_case_insensitive_whole_words(self):
        self.assertEqual(private_hits("We moved acmecorp data", ["AcmeCorp"], "f"),
                         ["f:1: private term 'AcmeCorp'"])
        self.assertEqual(private_hits("AcmeCorporate", ["AcmeCorp"], "f"), [])

    def test_long_quoted_run_flagged(self):
        quote = '"' + " ".join(["word"] * 15) + '"'
        self.assertEqual(len(long_quotes(f"Text {quote}\n", "f")), 1)

    def test_short_quote_allowed(self):
        self.assertEqual(long_quotes('Call it "tolerate" or "invest".\n', "f"), [])

    def test_long_blockquote_flagged(self):
        self.assertEqual(len(long_quotes("> " + " ".join(["w"] * 15) + "\n", "f")), 1)

    def test_docx_text_includes_properties(self):
        p = self.tmp / "a.docx"
        make_docx(p, "Hello")
        text = docx_text(p)
        self.assertIn("Hello", text)
        self.assertIn("Author", text)

    def test_scan_finds_term_inside_docx(self):
        (self.tmp / "dist" / "office").mkdir(parents=True)
        make_docx(self.tmp / "dist" / "office" / "sop.docx", "Prepared for AcmeCorp")
        self.assertTrue(any("sop.docx" in h for h in scan(self.tmp, ["AcmeCorp"])))

    def test_main_fails_without_word_list(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(main(["--root", str(self.tmp)]), 2)

    def test_main_fails_when_word_list_path_missing(self):
        with mock.patch.dict(os.environ, {"AGK_PRIVATE_WORDS": str(self.tmp / "nope.txt")}):
            self.assertEqual(main(["--root", str(self.tmp)]), 2)

    def test_main_clean_repo_passes(self):
        words = self.tmp / "w.txt"
        words.write_text("AcmeCorp\n")
        (self.tmp / "methods").mkdir()
        (self.tmp / "methods" / "a.md").write_text("Clean text\n")
        with mock.patch.dict(os.environ, {"AGK_PRIVATE_WORDS": str(words)}):
            self.assertEqual(main(["--root", str(self.tmp)]), 0)
```

- [ ] **Step 2: Run to verify failure**

Run: `PYTHONPATH=build python3 -m unittest tests.test_scan -v`
Expected: FAIL with `No module named 'agk.scan'`

- [ ] **Step 3: Implement `build/agk/scan.py`**

```python
import argparse
import os
import re
import sys
import zipfile
from pathlib import Path

MAX_QUOTE_WORDS = 15
SCAN_DIRS = ("methods", "agents", "case-studies", "site", "dist", "demo-estate", "README.md")  # Task 14b adds "field-guide"
QUOTE_DIRS = ("methods", "agents", "case-studies", "site")
TEXT_SUFFIXES = {".md", ".csv", ".html", ".json", ".txt"}
QUOTE_RE = re.compile(r"[\"“]([^\"”\n]+)[\"”]")
TAG_STRIP_RE = re.compile(r"<[^>]+>")


def load_words(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return [l.strip() for l in lines if l.strip() and not l.lstrip().startswith("#")]


def private_hits(text: str, words: list[str], label: str) -> list[str]:
    hits = []
    for n, line in enumerate(text.splitlines(), start=1):
        for w in words:
            if re.search(rf"(?<!\w){re.escape(w)}(?!\w)", line, re.IGNORECASE):
                hits.append(f"{label}:{n}: private term {w!r}")
    return hits


def long_quotes(text: str, label: str) -> list[str]:
    hits = []
    for n, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith(">") and len(line.lstrip("> ").split()) >= MAX_QUOTE_WORDS:
            hits.append(f"{label}:{n}: blockquote of {MAX_QUOTE_WORDS}+ words")
        for q in QUOTE_RE.findall(line):
            if len(q.split()) >= MAX_QUOTE_WORDS:
                hits.append(f"{label}:{n}: quoted run of {MAX_QUOTE_WORDS}+ words")
    return hits


def docx_text(path: Path) -> str:
    parts = []
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            if name.endswith(".xml"):
                parts.append(TAG_STRIP_RE.sub(" ", z.read(name).decode("utf-8", "replace")))
    return "\n".join(parts)


def _files(root: Path, entries: tuple[str, ...]):
    for entry in entries:
        p = root / entry
        if p.is_file():
            yield p
        elif p.is_dir():
            yield from (f for f in sorted(p.rglob("*")) if f.is_file())


def scan(root: Path, words: list[str]) -> list[str]:
    hits = []
    for f in _files(root, SCAN_DIRS):
        label = str(f.relative_to(root))
        if f.suffix in (".docx", ".xlsx", ".pptx"):
            hits += private_hits(docx_text(f), words, label)
        elif f.suffix in TEXT_SUFFIXES:
            hits += private_hits(f.read_text(encoding="utf-8", errors="replace"), words, label)
    for f in _files(root, QUOTE_DIRS):
        if f.suffix in (".md", ".html"):
            hits += long_quotes(f.read_text(encoding="utf-8", errors="replace"), str(f.relative_to(root)))
    return hits


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Pre-publish scan.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    words_path = os.environ.get("AGK_PRIVATE_WORDS")
    if not words_path or not Path(words_path).is_file():
        print("error: set AGK_PRIVATE_WORDS to your private word list (kept outside the repo)", file=sys.stderr)
        return 2
    hits = scan(args.root, load_words(Path(words_path)))
    for h in hits:
        print(h, file=sys.stderr)
    print("scan clean" if not hits else f"{len(hits)} hit(s)")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `PYTHONPATH=build python3 -m unittest tests.test_scan -v`
Expected: 10 PASS

- [ ] **Step 5: Add CI (tests + build; the private scan runs locally only, because the word list never leaves Eve's machine)**

`.github/workflows/ci.yml`:

```yaml
name: ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: make test
      - run: make build
      - run: git diff --exit-code dist/
```

The last line fails CI when someone edits `methods/` without rebuilding `dist/`.

- [ ] **Step 6: Eve creates her private word list** (human step, 5 minutes)

```bash
mkdir -p ~/.config/agk && touch ~/.config/agk/private-words.txt
echo 'export AGK_PRIVATE_WORDS="$HOME/.config/agk/private-words.txt"' >> ~/.zshrc
```

Eve adds: employer name and abbreviations, internal system names, colleague names, client names, one per line.

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "feat(build): scan for private terms and quotes" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CxthZSoP1hm8J6w9VwKbX6"
```

---

### Task 5: Halden Logistics demo company

**Files:**
- Create: `demo-estate/generate.py`, `demo-estate/README.md`, `tests/test_demo_estate.py`
- Generated (committed): `demo-estate/apps.csv`, `licenses.csv`, `employees.csv`, `accounts.csv`, `ai-systems.csv`, `maturity-answers.csv`, `controls.md`, `council-draft.md`, `answer-key.json`

**Interfaces:**
- Produces: `generate(out: Path) -> None`; answer-key entries `{"tool": str, "type": str, "id": str}` with types `duplicate_app` (id `APP-a+APP-b`, sorted), `expired_license`, `orphaned_account`, `high_risk_ai`, `maturity_gap` (area slug), `crosswalk_match` (`C1:XW-001`), `charter_gap` (flaw slug).

- [ ] **Step 1: Write the failing tests**

`tests/test_demo_estate.py`:

```python
import csv
import importlib.util
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("generate", ROOT / "demo-estate" / "generate.py")
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class DemoEstateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = Path(tempfile.mkdtemp())
        gen.generate(cls.out)
        cls.key = json.loads((cls.out / "answer-key.json").read_text())

    def expected(self, kind):
        return {k["id"] for k in self.key if k["type"] == kind}

    def test_sixty_apps(self):
        self.assertEqual(len(rows(self.out / "apps.csv")), 60)

    def test_every_app_has_a_data_sensitivity(self):
        values = {a["data_sensitivity"] for a in rows(self.out / "apps.csv")}
        self.assertEqual(values, {"confidential", "internal"})

    def test_only_planted_duplicates_share_a_category(self):
        apps = rows(self.out / "apps.csv")
        counts = Counter(a["category"] for a in apps)
        pairs = set()
        for cat, n in counts.items():
            if n > 1:
                ids = sorted(a["id"] for a in apps if a["category"] == cat)
                self.assertEqual(len(ids), 2)
                pairs.add("+".join(ids))
        self.assertEqual(pairs, self.expected("duplicate_app"))
        self.assertEqual(len(pairs), 5)

    def test_only_planted_licenses_expired(self):
        lic = rows(self.out / "licenses.csv")
        expired = {l["id"] for l in lic if l["expiry"] < l["checked_on"]}
        self.assertEqual(expired, self.expected("expired_license"))
        self.assertEqual(len(expired), 2)

    def test_only_planted_accounts_orphaned(self):
        emps = {e["id"]: e for e in rows(self.out / "employees.csv")}
        orphans = {a["id"] for a in rows(self.out / "accounts.csv")
                   if a["employee_id"] not in emps or emps[a["employee_id"]]["status"] != "active"}
        self.assertEqual(orphans, self.expected("orphaned_account"))
        self.assertEqual(len(orphans), 3)

    def test_six_ai_systems_one_high_risk(self):
        self.assertEqual(len(rows(self.out / "ai-systems.csv")), 6)
        self.assertEqual(self.expected("high_risk_ai"), {"AI-004"})

    def test_three_lowest_maturity_areas_are_the_gaps(self):
        answers = sorted(rows(self.out / "maturity-answers.csv"), key=lambda r: int(r["score"]))
        self.assertEqual({r["area"] for r in answers[:3]}, self.expected("maturity_gap"))
        self.assertLess(int(answers[2]["score"]), int(answers[3]["score"]))

    def test_council_draft_has_planted_flaws(self):
        text = (self.out / "council-draft.md").read_text()
        self.assertNotIn("sponsor", text.lower())
        self.assertNotIn("decide", text.lower())
        members = text.split("## Members (voting)\n")[1].split("\n\n")[0]
        self.assertEqual(self.expected("charter_gap"), {"decision-rights", "sponsor", "membership-size"})
        self.assertGreater(members.count(",") + members.count(";") + 1, 9)

    def test_generation_is_deterministic(self):
        other = Path(tempfile.mkdtemp())
        gen.generate(other)
        for f in self.out.iterdir():
            self.assertEqual(f.read_bytes(), (other / f.name).read_bytes(), f.name)
```

- [ ] **Step 2: Run to verify failure**

Run: `PYTHONPATH=build python3 -m unittest tests.test_demo_estate -v`
Expected: FAIL with `FileNotFoundError` for `demo-estate/generate.py`

- [ ] **Step 3: Implement `demo-estate/generate.py`**

```python
"""Generate the Halden Logistics demo estate. Deterministic; standard library only."""
import csv
import json
import sys
from pathlib import Path

CHECKED_ON = "2026-09-01"

CATEGORIES = [
    ("ERP", "Northbeam"), ("Payroll", "Paylane"), ("HR information system", "Staffhub"),
    ("Recruiting", "Hirewell"), ("Learning management", "Coursefield"), ("Expense management", "Receiptly"),
    ("Procurement", "Buyline"), ("Contract management", "Clausebase"), ("CRM", "Relato"),
    ("Marketing automation", "Campaignly"), ("Customer support desk", "Helpwise"), ("Live chat", "Chattera"),
    ("Survey", "Pollform"), ("E-signature", "Signwell"), ("Document management", "Docuvault"),
    ("Intranet", "Hallway"), ("Video conferencing", "Meetrix"), ("Team chat", "Threadly"),
    ("Project management", "Taskmoor"), ("Diagramming", "Shapewise"), ("Password manager", "Keyfort"),
    ("Endpoint management", "Fleetdesk"), ("Antivirus", "Shieldline"), ("Backup", "Vaultline"),
    ("Monitoring", "Pulseboard"), ("IT service management", "Servicely"), ("Identity provider", "Gatekey"),
    ("Warehouse management", "Stackyard"), ("Transport management", "Routewise"), ("Fleet telematics", "Trackmile"),
    ("Route optimization", "Pathcraft"), ("Yard management", "Dockside"), ("Customs brokerage", "Borderline"),
    ("Freight audit", "Ratecheck"), ("EDI gateway", "Tradelink"), ("Carrier portal", "Loadboard"),
    ("Demand forecasting", "Foresight"), ("Business intelligence", "Chartwell"), ("Data warehouse", "Lakeshore"),
    ("ETL", "Pipewright"), ("Spreadsheet add-in", "Cellmate"), ("Accounts payable automation", "Payflow"),
    ("Treasury", "Cashmere"), ("Tax compliance", "Levywise"), ("Audit management", "Trailmark"),
    ("GRC", "Controlroom"), ("Policy management", "Rulebook"), ("Health and safety", "Safeyard"),
    ("Visitor management", "Frontdesk"), ("Facilities booking", "Roomly"), ("Invoice OCR", "Scanwright"),
    ("Chatbot", "Askbay"), ("Email security", "Mailguard"), ("Web analytics", "Clickpath"), ("Code repository", "Commitly"),
]
# Planted duplicates: slot -> (partner slot, alternate vendor)
DUPLICATES = {41: (8, "Tallysheet"), 52: (14, "Quickink"), 37: (22, "Linkup"), 58: (29, "Routesmith"), 46: (33, "Clearport")}
CONFIDENTIAL = {"Payroll", "HR information system", "Recruiting", "CRM", "Expense management", "Treasury",
                "Tax compliance", "Identity provider", "Customer support desk", "Accounts payable automation"}
EXPIRED = {"LIC-017": "2026-03-31", "LIC-044": "2025-12-31"}
TERMINATED = {"EMP-071": "2026-05-15", "EMP-072": "2026-07-02"}
ORPHANS = {"ACC-019": "EMP-071", "ACC-063": "EMP-072", "ACC-104": "EMP-099"}
AI_SYSTEMS = [
    ("AI-001", "Email security", "Classifies inbound email as spam or phishing and quarantines it."),
    ("AI-002", "Finance", "Reads supplier invoices and extracts totals, dates, and PO numbers for review."),
    ("AI-003", "Operations", "Suggests delivery routes to dispatchers, who approve each plan."),
    ("AI-004", "HR", "Ranks job applicants' CVs and shortlists candidates for interview."),
    ("AI-005", "Customer service", "Answers customer shipment-status questions in the website chat."),
    ("AI-006", "Planning", "Forecasts weekly warehouse volume from historic shipments."),
]
MATURITY = [
    ("governance", "Governance and policy", 3), ("inventory", "Inventory and discovery", 3),
    ("entitlement", "Entitlement and license management", 1), ("lifecycle", "Lifecycle, request to retirement", 2),
    ("vendor", "Vendor and contract management", 4), ("data-quality", "Data quality and reconciliation", 1),
    ("security", "Risk and security integration", 3), ("cost", "Cost and financial management", 4),
    ("reporting", "Reporting and improvement", 3),
]
CHARTER_FLAWS = ["decision-rights", "sponsor", "membership-size"]
CHARTER_DRAFT = """# Halden Software Governance Council — draft charter

## Purpose
The council oversees software and applications at Halden Logistics.

## Members (voting)
CIO; CISO; heads of procurement, finance, legal, architecture, HR, operations, warehousing, transport, customer service, sales, marketing; and the service desk lead.

## Meetings
Monthly, 90 minutes. Minutes kept by the service desk lead.

## Scope
New software requests, renewals, retirements, and AI tools.
"""
CONTROLS = [
    ("C1", "Maintain an accurate inventory of software and who owns each application.", "XW-001"),
    ("C2", "Review user access to applications on a schedule and remove access no longer needed.", "XW-016"),
    ("C3", "Assess each AI system for risk before it is deployed.", "XW-021"),
]


def _write(path: Path, header: list[str], rows: list[list]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def generate(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    key = []
    base = iter(CATEGORIES)
    slots = {}
    for i in range(1, 61):
        if i not in DUPLICATES:
            slots[i] = next(base)
    for i, (partner, vendor) in DUPLICATES.items():
        slots[i] = (slots[partner][0], vendor)
        key.append({"tool": "rationalization", "type": "duplicate_app",
                    "id": "+".join(sorted((f"APP-{partner:03d}", f"APP-{i:03d}")))})
    apps = [[f"APP-{i:03d}", f"{slots[i][1]} {slots[i][0]}", slots[i][1], slots[i][0],
             round(5000 + (i * 7919) % 90000, -2), 20 + (i * 37) % 900,
             "confidential" if slots[i][0] in CONFIDENTIAL else "internal"] for i in range(1, 61)]
    _write(out / "apps.csv", ["id", "name", "vendor", "category", "annual_cost_usd", "users", "data_sensitivity"], apps)

    licenses = []
    for i in range(1, 61):
        lid = f"LIC-{i:03d}"
        licenses.append([lid, f"APP-{i:03d}", 25 + (i * 13) % 500, EXPIRED.get(lid, "2027-06-30"), CHECKED_ON])
    key += [{"tool": "rationalization", "type": "expired_license", "id": lid} for lid in EXPIRED]
    _write(out / "licenses.csv", ["id", "app_id", "entitlements", "expiry", "checked_on"], licenses)

    employees = [[f"EMP-{i:03d}", "terminated" if f"EMP-{i:03d}" in TERMINATED else "active",
                  TERMINATED.get(f"EMP-{i:03d}", "")] for i in range(1, 81)]
    _write(out / "employees.csv", ["id", "status", "termination_date"], employees)

    accounts = []
    for i in range(1, 121):
        aid = f"ACC-{i:03d}"
        emp = ORPHANS.get(aid, f"EMP-{(i - 1) % 70 + 1:03d}")
        accounts.append([aid, emp, f"APP-{(i - 1) % 60 + 1:03d}", "admin" if i % 17 == 0 else "user",
                         f"2026-08-{(i % 28) + 1:02d}"])
    key += [{"tool": "access-review", "type": "orphaned_account", "id": aid} for aid in ORPHANS]
    _write(out / "accounts.csv", ["id", "employee_id", "app_id", "role", "last_login"], accounts)

    _write(out / "ai-systems.csv", ["id", "owner", "description"], [list(a) for a in AI_SYSTEMS])
    key.append({"tool": "ai-intake", "type": "high_risk_ai", "id": "AI-004"})

    _write(out / "maturity-answers.csv", ["area", "label", "score"], [list(m) for m in MATURITY])
    lowest = sorted(MATURITY, key=lambda m: m[2])[:3]
    key += [{"tool": "itam-maturity", "type": "maturity_gap", "id": m[0]} for m in lowest]

    (out / "controls.md").write_text(
        "# Controls to map\n\n" + "".join(f"- **{c}**: {text}\n" for c, text, _ in CONTROLS), encoding="utf-8")
    key += [{"tool": "crosswalk", "type": "crosswalk_match", "id": f"{c}:{xw}"} for c, _, xw in CONTROLS]

    (out / "council-draft.md").write_text(CHARTER_DRAFT, encoding="utf-8")
    key += [{"tool": "program-setup", "type": "charter_gap", "id": f} for f in CHARTER_FLAWS]

    key.sort(key=lambda k: (k["tool"], k["type"], k["id"]))
    (out / "answer-key.json").write_text(json.dumps(key, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    generate(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `PYTHONPATH=build python3 -m unittest tests.test_demo_estate -v`
Expected: 9 PASS

- [ ] **Step 5: Generate the committed data and write the README**

Run: `python3 demo-estate/generate.py`
Expected: 9 files appear in `demo-estate/`.

`demo-estate/README.md`: one paragraph saying Halden Logistics is fictional, lists each file and its columns, states that `checked_on` is 2026-09-01, and says `answer-key.json` exists for grading and must not be given to a tool under test.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "feat(demo): add halden logistics demo estate" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CxthZSoP1hm8J6w9VwKbX6"
```

---

### Task 6: Grader and eval runner

**Files:**
- Create: `build/agk/grade.py`, `tests/test_grade.py`, `evals/run.sh`, `evals/prompts/<tool>.txt` (six files), `evals/results/.gitkeep`

**Interfaces:**
- Consumes: `demo-estate/answer-key.json` (Task 5).
- Produces: `GradeError(Exception)`; `MAX_EXTRA = 1`; `parse_findings(text: str) -> set[tuple[str, str]]`; `grade(findings, key: list[dict], tool: str) -> dict` with keys `passed: bool, missed: list, extra: list`; `main(argv=None) -> int`.

- [ ] **Step 1: Write the failing tests**

`tests/test_grade.py`:

```python
import unittest

from agk.grade import GradeError, grade, parse_findings

KEY = [
    {"tool": "rationalization", "type": "duplicate_app", "id": "APP-008+APP-041"},
    {"tool": "rationalization", "type": "expired_license", "id": "LIC-017"},
    {"tool": "access-review", "type": "orphaned_account", "id": "ACC-019"},
]


def output(json_text):
    return f"Report text\n\n```findings\n{json_text}\n```\n"


class GradeTests(unittest.TestCase):
    def test_parses_findings_block(self):
        f = parse_findings(output('[{"type": "expired_license", "id": "LIC-017"}]'))
        self.assertEqual(f, {("expired_license", "LIC-017")})

    def test_pair_ids_are_order_insensitive(self):
        f = parse_findings(output('[{"type": "duplicate_app", "id": "APP-041 + APP-008"}]'))
        self.assertEqual(f, {("duplicate_app", "APP-008+APP-041")})

    def test_uses_last_findings_block(self):
        text = output("[]") + output('[{"type": "expired_license", "id": "LIC-017"}]')
        self.assertEqual(len(parse_findings(text)), 1)

    def test_missing_block_raises(self):
        with self.assertRaisesRegex(GradeError, "no findings block"):
            parse_findings("Just prose.")

    def test_malformed_json_raises(self):
        with self.assertRaisesRegex(GradeError, "not valid JSON"):
            parse_findings(output("[{type: oops}]"))

    def test_wrong_shape_raises(self):
        with self.assertRaisesRegex(GradeError, "type"):
            parse_findings(output('[{"id": "LIC-017"}]'))

    def test_all_found_passes(self):
        f = {("duplicate_app", "APP-008+APP-041"), ("expired_license", "LIC-017")}
        self.assertTrue(grade(f, KEY, "rationalization")["passed"])

    def test_a_miss_fails(self):
        r = grade({("expired_license", "LIC-017")}, KEY, "rationalization")
        self.assertFalse(r["passed"])
        self.assertEqual(r["missed"], [["duplicate_app", "APP-008+APP-041"]])

    def test_too_many_extras_fails(self):
        f = {("duplicate_app", "APP-008+APP-041"), ("expired_license", "LIC-017"),
             ("expired_license", "LIC-001"), ("expired_license", "LIC-002")}
        self.assertFalse(grade(f, KEY, "rationalization")["passed"])

    def test_other_tools_keys_ignored(self):
        f = {("duplicate_app", "APP-008+APP-041"), ("expired_license", "LIC-017")}
        self.assertEqual(grade(f, KEY, "rationalization")["missed"], [])

    def test_unknown_tool_raises(self):
        with self.assertRaisesRegex(GradeError, "no answer-key entries"):
            grade(set(), KEY, "nope")
```

- [ ] **Step 2: Run to verify failure**

Run: `PYTHONPATH=build python3 -m unittest tests.test_grade -v`
Expected: FAIL with `No module named 'agk.grade'`

- [ ] **Step 3: Implement `build/agk/grade.py`**

```python
import argparse
import json
import re
import sys
from pathlib import Path

MAX_EXTRA = 1
BLOCK_RE = re.compile(r"```findings[ \t]*\n(.*?)\n```", re.S)


class GradeError(Exception):
    pass


def _norm(fid: str) -> str:
    parts = [p.strip() for p in fid.split("+")]
    return "+".join(sorted(parts)) if len(parts) > 1 else parts[0]


def parse_findings(text: str) -> set[tuple[str, str]]:
    blocks = BLOCK_RE.findall(text)
    if not blocks:
        raise GradeError("no findings block in tool output")
    try:
        data = json.loads(blocks[-1])
    except json.JSONDecodeError as e:
        raise GradeError(f"findings block is not valid JSON: {e}") from e
    if not isinstance(data, list):
        raise GradeError("findings block must be a JSON list")
    out = set()
    for item in data:
        if not isinstance(item, dict) or not isinstance(item.get("type"), str) or not isinstance(item.get("id"), str):
            raise GradeError(f"each finding needs string 'type' and 'id': {item!r}")
        out.add((item["type"], _norm(item["id"])))
    return out


def grade(findings: set[tuple[str, str]], key: list[dict], tool: str) -> dict:
    expected = {(k["type"], _norm(k["id"])) for k in key if k["tool"] == tool}
    if not expected:
        raise GradeError(f"no answer-key entries for tool {tool!r}")
    types = {t for t, _ in expected}
    missed = sorted(expected - findings)
    extra = sorted(f for f in findings - expected if f[0] in types)
    return {"passed": not missed and len(extra) <= MAX_EXTRA,
            "missed": [list(m) for m in missed], "extra": [list(e) for e in extra]}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Grade a tool's output against the answer key.")
    parser.add_argument("--tool", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--key", type=Path, default=Path("demo-estate/answer-key.json"))
    args = parser.parse_args(argv)
    try:
        result = grade(parse_findings(args.output.read_text(encoding="utf-8")),
                       json.loads(args.key.read_text(encoding="utf-8")), args.tool)
    except GradeError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `PYTHONPATH=build python3 -m unittest tests.test_grade -v`
Expected: 11 PASS

- [ ] **Step 5: Write the eval runner**

`evals/run.sh`:

```bash
#!/usr/bin/env bash
# Usage: evals/run.sh <tool> <claude|codex>
# Feeds the built SKILL.md plus the demo data to the CLI; grades the answer.
set -euo pipefail
tool="$1"; runner="$2"
root="$(cd "$(dirname "$0")/.." && pwd)"
skill="$root/dist/$runner/skills/$tool/SKILL.md"
[ -f "$skill" ] || { echo "missing $skill — run make build" >&2; exit 2; }
out="$root/evals/results/$tool-$runner-$(date +%Y%m%d-%H%M%S).md"
prompt="$(cat "$skill")

$(cat "$root/evals/prompts/$tool.txt")"
cd "$root/demo-estate"
case "$runner" in
  claude) claude -p "$prompt" --allowedTools Read > "$out" ;;
  codex)  codex exec --sandbox read-only "$prompt" > "$out" ;;
  *) echo "runner must be claude or codex" >&2; exit 2 ;;
esac
cd "$root"
PYTHONPATH=build python3 -m agk.grade --tool "$tool" --output "$out"
```

Run: `chmod +x evals/run.sh`

Prompt files (six; each tells the tool which demo files to read; none mention the answer key):

- `evals/prompts/crosswalk.txt`: `Map each control in controls.md to crosswalk rows. In the findings block, report each match as {"type": "crosswalk_match", "id": "<control>:<XW id>"}, using only the single best row per control.`
- `evals/prompts/itam-maturity.txt`: `Assess maturity-answers.csv. Report the three weakest process areas in the findings block as {"type": "maturity_gap", "id": "<area>"}.`
- `evals/prompts/rationalization.txt`: `Rationalize the portfolio in apps.csv and licenses.csv. In the findings block report duplicate applications as {"type": "duplicate_app", "id": "APP-x+APP-y"} and expired licenses as {"type": "expired_license", "id": "LIC-n"}.`
- `evals/prompts/ai-intake.txt`: `Run intake for every system in ai-systems.csv. In the findings block report each system you tier high-risk as {"type": "high_risk_ai", "id": "AI-n"}.`
- `evals/prompts/program-setup.txt`: `Review council-draft.md as a charter for a software governance council. In the findings block report each gap as {"type": "charter_gap", "id": "<slug>"}, using these slugs where they apply: decision-rights, sponsor, membership-size, intake-path, cadence, metrics, escalation.`
- `evals/prompts/access-review.txt`: `Review accounts.csv against employees.csv, using apps.csv for data sensitivity. In the findings block report each orphaned account as {"type": "orphaned_account", "id": "ACC-n"}.`

- [ ] **Step 6: Verify the runner fails cleanly before any tool exists**

Run: `evals/run.sh rationalization claude`
Expected: `missing .../dist/claude/skills/rationalization/SKILL.md — run make build`, exit 2

- [ ] **Step 7: Commit**

```bash
printf 'evals/results/*.md\n' >> .gitignore
git add -A
git commit -m "feat(evals): grade tool output against answer key" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CxthZSoP1hm8J6w9VwKbX6"
```

Then run `review-merge-pipeline` on `feat/foundation` and merge to `main`. Each tool task below starts from a fresh `feat/<tool>` branch.

---

### Shared rules for Tasks 7–11b (repeat in each task's handoff)

Every `methods/<tool>/method.md` body ends with this output contract, verbatim:

````markdown
## Output rules

- Show the reasoning behind each conclusion.
- Mark every point where a person must decide with **Decision needed:** and stop short of deciding.
- Flag any figure you could not verify from the input with **Unverified:**.
- Cite framework clauses by number from `crosswalk.csv`. Paraphrase; never quote standards text.
- End your answer with a fenced block labelled `findings` containing a JSON list of `{"type": ..., "id": ...}` objects, as the task describes. Use `[]` when there are none.
````

Each tool is done when:
1. `make test && make build` pass with no warnings for that tool.
2. `evals/run.sh <tool> claude` and `evals/run.sh <tool> codex` both print `"passed": true`.
3. Eve reads the checklist, SOP, and platform guide, and says they match how she'd actually run it.
4. Eve runs `dist/copilot/<tool>/test-script.md` at work and records the result in `methods/<tool>/copilot-results.md` (date, pass/fail, notes; no work data).

---

### Task 7: Crosswalk (content + Eve's verification)

**Files:**
- Create: `methods/crosswalk/{method.md, crosswalk.csv, checklist.md, sop.md, template.md, platform-guide.md, copilot-test.md, example/controls-mapped.md}`

**Interfaces:**
- Produces: crosswalk rows `XW-001`…`XW-028` used as tags by Tasks 8–11. Row IDs and themes below are fixed; other tasks depend on them.

- [ ] **Step 1: Write `crosswalk.csv`**

Columns: `id,theme,iso19770_1,cobit2019,iso27001,iso42001,summary,verified`. The COBIT and ISO 27001 references below are drafted; the `iso19770_1` and `iso42001` columns and the `verified` date are **filled in by Eve** from her copies of the standards (Step 2). Summaries are paraphrases written by us, one sentence each.

| id | theme | cobit2019 | iso27001 (2022) |
|---|---|---|---|
| XW-001 | Application and software inventory | BAI09.01 | A.5.9 |
| XW-002 | Asset ownership assigned | BAI09.01 | A.5.9 |
| XW-003 | Asset management policy and scope | APO01 | A.5.1 |
| XW-004 | Roles and responsibilities | APO01 | A.5.2 |
| XW-005 | Discovery and reconciliation of installs | BAI09.01 | A.5.9 |
| XW-006 | Entitlement records kept | BAI09.05 | A.5.32 |
| XW-007 | License compliance position | BAI09.05 | A.5.32 |
| XW-008 | License renewal and expiry tracking | BAI09.05 | A.5.32 |
| XW-009 | Lifecycle, request to retirement | BAI09.03 | A.5.9 |
| XW-010 | Retirement and decommissioning | BAI09.03 | A.8.10 |
| XW-011 | Portfolio value optimization (rationalization) | BAI09.04 | |
| XW-012 | Cost and budget tracking | APO06 | |
| XW-013 | Vendor and contract management | APO10 | A.5.19, A.5.20 |
| XW-014 | Access control policy | DSS05.04 | A.5.15 |
| XW-015 | Access provisioning | DSS05.04 | A.5.18 |
| XW-016 | Periodic access review | DSS05.04 | A.5.18 |
| XW-017 | Leaver access removal | DSS05.04 | A.5.18, A.6.5 |
| XW-018 | Privileged access | DSS05.04 | A.8.2 |
| XW-019 | Segregation of duties | DSS06.03 | A.5.3 |
| XW-020 | Evidence retention for audit | MEA02 | A.5.33 |
| XW-021 | AI system risk and impact assessment before deployment | APO12 | |
| XW-022 | AI system inventory | BAI09.01 | |
| XW-023 | AI supplier and third-party oversight | APO10 | A.5.19 |
| XW-024 | Risk register and treatment | APO12 | 6.1.3 |
| XW-025 | Performance review and improvement | MEA01 | 9.1, 10.1 |
| XW-026 | Data quality of asset records | BAI09.01 | A.5.9 |
| XW-027 | Governance body, sponsor, and decision rights | EDM01, APO01 | 5.1, 5.3 |
| XW-028 | Data classification and handling | APO14 | A.5.12, A.5.13 |

Leave `iso19770_1`, `iso42001`, and `verified` blank for now. `make build` will fail with "not verified" until Step 2; that failure is expected.

- [ ] **Step 2: Eve verifies every row** (human step, about 90 minutes)

For each row, Eve checks the COBIT and 27001 references, fills in the ISO/IEC 19770-1:2017 and ISO/IEC 42001:2023 clause references from her copies, corrects anything wrong, and enters today's date in `verified`. Rows with no honest mapping to a framework stay blank for that framework. Nothing here is copied from the standards; clause numbers only.

Run: `make build`
Expected: `build ok` once every row has a date.

- [ ] **Step 3: Write `method.md`**

```markdown
---
name: crosswalk
title: Governance framework crosswalk
description: Map a control, requirement, or policy statement to ISO/IEC 19770-1, COBIT 2019, ISO/IEC 27001, and ISO/IEC 42001 clauses, and show where coverage is missing. Use when writing or auditing a control, or explaining how frameworks overlap.
---

You map governance controls across four frameworks using `crosswalk.csv`.

## Steps

1. Restate the control in one plain sentence. If it bundles several obligations, split it and map each part.
2. Find the best-matching crosswalk row by theme and summary. Name a second row only if it adds a framework the first lacks.
3. For each framework, give the clause number from the row, or "no direct equivalent".
4. Name the gap: which framework has no equivalent, and what an auditor from that framework would ask for instead.
5. If no row fits, say so and propose a new row (theme and one-sentence summary). **Decision needed:** whether to add it.

## Output

A table per control: framework, clause, what it asks for in your own words. Then gaps. Then the findings block, one `crosswalk_match` per control with id `<control label>:<XW id>`.
```

Append the shared output rules block verbatim.

- [ ] **Step 4: Write `checklist.md`, `sop.md`, `template.md`, `platform-guide.md`, `copilot-test.md`, `example/controls-mapped.md`**

`checklist.md`:

```markdown
# Crosswalk checklist

1. Control restated in one sentence; bundled obligations split [[XW-003]]
2. Best-matching row chosen and recorded [[XW-003]]
3. Clause recorded for each of the four frameworks, or "no direct equivalent" [[XW-003]]
4. Gaps listed with what each framework's auditor would expect [[XW-025]]
5. Unmatched controls raised as proposed new rows [[XW-025]]
6. Mapping reviewed by a second person and dated [[XW-020]]
```

`sop.md` sections, in order: **Purpose**, **Scope**, **Roles** (control owner, governance lead, reviewer), **Frequency** (on every new or changed control; full review yearly), **Steps** (numbered, same as the checklist with one sentence of detail each, tags kept), **Evidence to retain** (dated mapping table, reviewer sign-off), **Related** (the other four tools).

`template.md`: a table with columns `Control | Plain restatement | XW row | ISO 19770-1 | COBIT 2019 | ISO 27001 | ISO 42001 | Gaps | Reviewer | Date`.

`platform-guide.md`: where mapped controls live in ServiceNow IRM (policy statements and control objectives, linked to authoritative-source content) and how to record the XW id as a reference. Before writing table and module names, fetch ServiceNow's current IRM documentation with WebFetch and use only names confirmed there; cite the doc URLs at the bottom. Flexera has no control-mapping feature; say so in one line.

`copilot-test.md`: paste C2 from `demo-estate/controls.md` into the Copilot agent; pass if it returns XW-016 with DSS05.04 and A.5.18 and a findings block. Record result in `copilot-results.md`.

`example/controls-mapped.md`: the Claude eval output for `controls.md`, copied from `evals/results/` after Step 5 passes.

- [ ] **Step 5: Build and run evals**

Run: `make build && evals/run.sh crosswalk claude && evals/run.sh crosswalk codex`
Expected: `build ok`; both graders print `"passed": true`. If a run misses, fix the method text (not the answer key) and rerun; stop after two failed attempts and report the output.

- [ ] **Step 6: Eve reviews** the checklist, SOP, and platform guide (redline session), and runs the Copilot test at work.

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "feat(crosswalk): add verified framework crosswalk" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CxthZSoP1hm8J6w9VwKbX6"
```

---

### Task 8: ITAM maturity check

**Files:**
- Create: `methods/itam-maturity/{method.md, checklist.md, sop.md, template.csv, platform-guide.md, copilot-test.md, example/halden-assessment.md}`

**Interfaces:**
- Consumes: crosswalk rows XW-001–XW-012, XW-025, XW-026.
- Produces: findings type `maturity_gap` with area slugs from `demo-estate/maturity-answers.csv`.

- [ ] **Step 1: Write `method.md`**

```markdown
---
name: itam-maturity
title: ITAM maturity check
description: Score an organization's IT asset management maturity across nine process areas, name the three biggest gaps, and produce a 90-day plan tied to ISO/IEC 19770-1 and COBIT BAI09. Use for a baseline assessment or a yearly re-check.
---

You assess IT asset management maturity on a 1–5 scale per process area.

## Scale

1 Ad hoc: no defined process. 2 Repeatable: done, but depends on individuals. 3 Defined: documented and followed. 4 Measured: tracked with metrics. 5 Improving: metrics drive change.

## Steps

1. If answers are not supplied, ask the questions in `template.csv` one area at a time, asking for one piece of evidence per area.
2. Score each area. Where the evidence doesn't support the stated score, lower it and say why.
3. Map each area to its crosswalk rows (governance XW-003/004, inventory XW-001/005, entitlement XW-006/007/008, lifecycle XW-009/010, vendor XW-013, data quality XW-026, security XW-014, cost XW-012, reporting XW-025).
4. Name the three lowest-scoring areas as the gaps. Break ties by business risk and explain the tie-break.
5. Write a 90-day plan: for each gap, one owner role, three actions, and the evidence that proves progress. **Decision needed:** owners and budget.

## Output

Score table, the three gaps with reasoning, the 90-day plan, then the findings block: one `maturity_gap` per gap with the area slug as id.
```

Append the shared output rules block verbatim.

- [ ] **Step 2: Write the supporting files**

`checklist.md`:

```markdown
# ITAM maturity checklist

1. Scope agreed: which estates, business units, and asset types [[XW-003]]
2. Answers and one evidence item collected per process area [[XW-025]]
3. Scores challenged against evidence; changes explained [[XW-025]]
4. Each area mapped to its crosswalk rows [[XW-003]]
5. Three gaps named with tie-break reasoning [[XW-025]]
6. 90-day plan drafted with owner roles and proof of progress [[XW-004]]
7. Owners and budget confirmed by the sponsor [[XW-004]]
8. Assessment filed with date for next year's comparison [[XW-020]]
```

`sop.md`: sections Purpose, Scope, Roles (ITAM manager, process owners, sponsor), Frequency (baseline, then yearly), Steps (numbered, matching the checklist, tags kept), Evidence to retain, Related.

`template.csv`: columns `area,label,question,score,evidence`; nine rows using the slugs and labels in `demo-estate/generate.py`'s `MATURITY` list, each with one plain question (for example, entitlement: "Can you show purchase records for your top ten software products and match them to what's installed?"), `score` and `evidence` blank.

`platform-guide.md`: for each process area, the ServiceNow (SAM Pro, HAM, APM) and Flexera One capability that supports it. Before writing, fetch current ServiceNow SAM/APM and Flexera One docs with WebFetch; use only module names confirmed there; cite URLs.

`copilot-test.md`: attach `demo-estate/maturity-answers.csv`; pass if the three gaps are entitlement, data-quality, lifecycle.

`example/halden-assessment.md`: the passing Claude eval output.

- [ ] **Step 3: Build and run evals**

Run: `make build && evals/run.sh itam-maturity claude && evals/run.sh itam-maturity codex`
Expected: `build ok`; both `"passed": true`. Stop after two failed fix attempts and report.

- [ ] **Step 4: Eve reviews (redline) and runs the Copilot test**

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat(itam-maturity): add maturity check" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CxthZSoP1hm8J6w9VwKbX6"
```

---

### Task 9: Rationalization

**Files:**
- Create: `methods/rationalization/{method.md, checklist.md, sop.md, template.csv, platform-guide.md, copilot-test.md, example/halden-rationalization.md}`

**Interfaces:**
- Consumes: crosswalk rows XW-001, XW-002, XW-006–XW-013, XW-028.
- Produces: findings types `duplicate_app`, `expired_license`.

- [ ] **Step 1: Write `method.md`**

```markdown
---
name: rationalization
title: Application rationalization
description: Recommend tolerate, invest, migrate, or eliminate for each application in an inventory, find duplicates and license problems, and summarize savings and risk. Use for portfolio reviews, budget cycles, or post-merger cleanup.
---

You rationalize an application portfolio using the TIME model: Tolerate, Invest, Migrate, Eliminate.

## Steps

1. Check the inventory: every app has an id, category, owner or cost. List gaps as **Unverified:**.
2. Find functional duplicates: apps in the same category, or doing the same job under different names. Report each pair once.
3. Check licenses against the `checked_on` date: expired, expiring within 90 days, and entitlements far above users.
4. Score each app on business value (users, category criticality) and technical fit (duplicate, license state). State the scoring you used.
5. Assign TIME. For each duplicate pair, recommend which app to keep and why. **Decision needed:** final keep/retire calls.
6. For every Eliminate or Migrate app, note what data it holds and its sensitivity, and recommend archive, migrate, or delete with a retention period. **Decision needed:** the data owner's disposition call.
7. Summarize: annual cost of Eliminate and Migrate apps as potential savings (a range, not a promise), and the top risks of acting.

## Output

A table of apps with TIME and one-line reason, a duplicates section, a license section, the savings and risk summary, then the findings block: `duplicate_app` per pair (`APP-x+APP-y`) and `expired_license` per expired license.
```

Append the shared output rules block verbatim.

- [ ] **Step 2: Write the supporting files**

`checklist.md`:

```markdown
# Rationalization checklist

1. Inventory pulled with owner, category, cost, and user count [[XW-001]] [[XW-002]]
2. Missing owners or costs listed and chased [[XW-026]]
3. Duplicate applications identified by category and function [[XW-011]]
4. Licenses checked for expiry and over-buying [[XW-007]] [[XW-008]]
5. Each app scored for business value and technical fit [[XW-011]]
6. Tolerate, invest, migrate, or eliminate assigned with reasons [[XW-011]]
7. Savings stated as a range and checked with finance [[XW-012]]
8. Vendor contract terms checked before any eliminate decision [[XW-013]]
9. Retirement plan raised for each eliminate decision [[XW-009]] [[XW-010]]
10. Data held by each retiring app identified; archive, migrate, or delete agreed with the data owner [[XW-010]] [[XW-028]]
11. Decisions and approvers recorded [[XW-020]]
```

`sop.md`: sections Purpose, Scope, Roles (portfolio manager, app owners, finance partner, architecture), Frequency (yearly plus before budget cycle), Steps (numbered, matching checklist, tags kept), Evidence to retain, Related.

`template.csv`: columns `app_id,name,category,owner,annual_cost,users,license_status,data_sensitivity,data_held,data_disposition,business_value,technical_fit,time_decision,reason,approver,date`.

`platform-guide.md`: where each field lives in ServiceNow APM (business applications, application portfolio assessments) and SAM Pro (entitlements, license positions), and in Flexera One (application inventory, license position). Fetch current docs with WebFetch first; use only confirmed names; cite URLs.

`copilot-test.md`: attach `demo-estate/apps.csv` and `licenses.csv`; pass if all 5 duplicate pairs and LIC-017, LIC-044 appear.

`example/halden-rationalization.md`: passing Claude eval output.

- [ ] **Step 3: Build and run evals**

Run: `make build && evals/run.sh rationalization claude && evals/run.sh rationalization codex`
Expected: `build ok`; both `"passed": true`. Stop after two failed fix attempts and report.

- [ ] **Step 4: Eve reviews (redline) and runs the Copilot test**

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat(rationalization): add rationalization method" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CxthZSoP1hm8J6w9VwKbX6"
```

---

### Task 10: AI system intake

**Files:**
- Create: `methods/ai-intake/{method.md, checklist.md, sop.md, template.md, platform-guide.md, copilot-test.md, example/halden-ai-intake.md}`

**Interfaces:**
- Consumes: crosswalk rows XW-020–XW-024, XW-028.
- Produces: findings type `high_risk_ai`.

- [ ] **Step 1: Write `method.md`**

```markdown
---
name: ai-intake
title: AI system intake and risk tiering
description: Take a description of an AI use case, assign a risk tier under the EU AI Act with NIST AI RMF and ISO/IEC 42001 controls, and produce an AI inventory record. Use whenever a team proposes a new AI tool or changes how one is used.
---

You run intake for AI systems. Legal content last reviewed: 2026-09. Say so in your answer and recommend legal review for any high-risk or prohibited result.

## Steps

1. Restate the use case: purpose, who is affected, what decisions it makes or supports, whether a person reviews each output, what data it uses, whether that includes personal data, and where the data came from.
2. Check prohibited practices first. If one might apply, stop and say **Decision needed:** legal review before anything else.
3. Check the high-risk areas (for example employment and worker management, access to essential services, education, law enforcement, critical infrastructure). Employment uses such as ranking or filtering job applicants are high-risk.
4. Otherwise tier as limited-risk (people must be told they're dealing with AI, as with chatbots) or minimal-risk.
5. List required controls for the tier, mapped through the crosswalk (XW-021 risk assessment, XW-022 inventory, XW-023 supplier oversight, XW-024 risk register) and the NIST AI RMF functions (Govern, Map, Measure, Manage).
6. Fill the inventory record from `template.md`. **Decision needed:** approval to proceed.

## Output

One section per system: restatement, tier with reasoning, required controls, inventory record. Then the findings block: one `high_risk_ai` per system tiered high-risk.
```

Append the shared output rules block verbatim.

- [ ] **Step 2: Write the supporting files**

`checklist.md`:

```markdown
# AI intake checklist

1. Use case restated: purpose, affected people, decisions, human review [[XW-021]]
2. Data used, personal data, and data provenance recorded [[XW-028]]
3. Prohibited practices ruled out, or escalated to legal [[XW-021]]
4. Risk tier assigned with reasoning [[XW-021]]
5. Required controls listed for the tier [[XW-024]]
6. Supplier and model provider identified and assessed [[XW-023]]
7. Record added to the AI inventory [[XW-022]]
8. Risk entered in the risk register with an owner [[XW-024]]
9. Approval decision and approver recorded [[XW-020]]
10. Re-review date set, and triggered on any change of use [[XW-021]]
```

`sop.md`: sections Purpose, Scope, Roles (requesting team, AI governance lead, legal, security, data protection), Frequency (every new system; every change of use; yearly re-review), Steps (numbered, matching checklist, tags kept), Evidence to retain, Related. Include "Legal content last reviewed: 2026-09" under Purpose.

`template.md`: inventory record fields: id, name, owner, purpose, affected people, decisions made or supported, human review, supplier, data used, personal data (yes/no), data provenance, risk tier, reasoning, required controls, approval, approver, date, next review.

`platform-guide.md`: where an AI inventory and AI risk assessments live in ServiceNow (AI governance / IRM capabilities) and how Flexera One can surface AI software and SaaS usage. Fetch current docs with WebFetch first; use only confirmed names; cite URLs.

`copilot-test.md`: paste the AI-004 row from `demo-estate/ai-systems.csv`; pass if tiered high-risk with employment named as the reason.

`example/halden-ai-intake.md`: passing Claude eval output.

- [ ] **Step 3: Build and run evals**

Run: `make build && evals/run.sh ai-intake claude && evals/run.sh ai-intake codex`
Expected: `build ok`; both `"passed": true` (AI-004 found; AI-005 chatbot may be tiered limited, which is not high-risk). Stop after two failed fix attempts and report.

- [ ] **Step 4: Eve reviews (redline) and runs the Copilot test**

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat(ai-intake): add ai system intake method" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CxthZSoP1hm8J6w9VwKbX6"
```

---

### Task 11: Access review pack

**Files:**
- Create: `methods/access-review/{method.md, checklist.md, sop.md, template.csv, platform-guide.md, copilot-test.md, example/halden-access-review.md}`

**Interfaces:**
- Consumes: crosswalk rows XW-014–XW-020, XW-028.
- Produces: findings type `orphaned_account`.

- [ ] **Step 1: Write `method.md`**

```markdown
---
name: access-review
title: Access review pack
description: Review application user and role exports against HR records, find orphaned, excessive, and privileged access, and produce an evidence summary and auditor-ready memo mapped to ISO/IEC 27001 and COBIT DSS05. Use for quarterly or annual access reviews.
---

You prepare an application access review.

## Steps

1. Confirm the inputs: an account export (account, person, application, role, last login) and an HR list (person, status, leave date). List missing columns as **Unverified:**.
2. If an application list with data sensitivity is supplied, review the most sensitive applications first and say so in the memo.
3. Match every account to a person. Accounts with no matching person, or whose person has left, are orphaned.
4. Flag privileged roles (admin or equivalent) for owner re-approval.
5. Flag accounts with no login in 90 days before the export date as dormant.
6. Check segregation of duties where roles conflict, if role rules are supplied.
7. Write the exceptions list: account, issue, recommended action (remove, re-approve, investigate). **Decision needed:** each removal, by the application owner.
8. Write the evidence summary and a one-page auditor memo: scope, population, method, exceptions, actions, and the clauses satisfied (XW-016, XW-017, XW-018).

## Output

Exceptions table, evidence summary, auditor memo, then the findings block: one `orphaned_account` per orphaned account.
```

Append the shared output rules block verbatim.

- [ ] **Step 2: Write the supporting files**

`checklist.md`:

```markdown
# Access review checklist

1. Review scope set: applications, period, export date [[XW-016]]
2. Account export and HR list obtained from the systems of record [[XW-016]]
3. Applications ordered by data sensitivity, most sensitive first [[XW-028]]
4. Every account matched to a person [[XW-015]]
5. Orphaned and leaver accounts flagged for removal [[XW-017]]
6. Privileged roles sent to owners for re-approval [[XW-018]]
7. Dormant accounts flagged [[XW-016]]
8. Role conflicts checked against segregation-of-duties rules [[XW-019]]
9. Owners' decisions collected and actions completed [[XW-016]]
10. Evidence pack and auditor memo filed [[XW-020]]
```

`sop.md`: sections Purpose, Scope, Roles (review coordinator, application owners, HR, IAM team, internal audit), Frequency (quarterly for privileged and in-scope systems; yearly for others), Steps (numbered, matching checklist, tags kept), Evidence to retain, Related.

`template.csv`: columns `account_id,person_id,app_id,role,last_login,issue,recommended_action,owner_decision,decided_by,date_done`.

`platform-guide.md`: how access reviews run in ServiceNow (IRM attestations or access certification capabilities) and where user-to-application data comes from; Flexera One's role (application usage data for dormant access). Fetch current docs with WebFetch first; use only confirmed names; cite URLs.

`copilot-test.md`: attach `demo-estate/accounts.csv`, `employees.csv`, and `apps.csv`; pass if ACC-019, ACC-063, ACC-104 are flagged orphaned.

`example/halden-access-review.md`: passing Claude eval output.

- [ ] **Step 3: Build and run evals**

Run: `make build && evals/run.sh access-review claude && evals/run.sh access-review codex`
Expected: `build ok`; both `"passed": true`. Stop after two failed fix attempts and report.

- [ ] **Step 4: Eve reviews (redline) and runs the Copilot test**

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat(access-review): add access review pack" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CxthZSoP1hm8J6w9VwKbX6"
```

---

### Task 11b: Program setup (how to stand up a governance body)

**Files:**
- Create: `methods/program-setup/{method.md, checklist.md, sop.md, template.md, platform-guide.md, copilot-test.md, example/halden-council-review.md}`

**Interfaces:**
- Consumes: crosswalk rows XW-003, XW-004, XW-012, XW-020, XW-024, XW-025, XW-027.
- Produces: findings type `charter_gap` with slugs `decision-rights`, `sponsor`, `membership-size`, `intake-path`, `cadence`, `metrics`, `escalation`.

- [ ] **Step 1: Write `method.md`**

```markdown
---
name: program-setup
title: Stand up a governance program
description: Design or review the launch of a governance body such as a software governance council, ITAM steering group, or AI governance board — charter, decision rights, membership, intake path, cadence, 90-day launch plan, and success measures. Use when starting a council or when an existing one has become a bottleneck or a rubber stamp.
---

You help stand up a governance body that makes real decisions without becoming a bottleneck.

## Mode

If given a draft charter, review it against the steps below and report gaps. Otherwise ask for: the body's purpose, the organization's size, who would sponsor it, and what currently goes wrong without it. Then draft.

## Steps

1. Purpose: one sentence on what goes wrong today that this body fixes.
2. Sponsor: an executive who controls the relevant budget. No sponsor means no enforcement; flag it.
3. Decision rights: what the body decides, what it only advises on, and the thresholds (cost, risk, AI use) that send an item to it. Everything below threshold is decided by a named role, not the council.
4. Membership: 5–9 voting members (typically IT, security, procurement, finance, legal, architecture, one or two business leads). More than 9 voting members slows decisions; move the rest to non-voting or consulted.
5. Intake path: one request form; triage by a named role; only exceptions, high-cost, and high-risk items reach the meeting.
6. Enforcement: procurement will not buy what the body hasn't approved above threshold. Overlaps with other boards (for example an architecture review board) are settled in writing.
7. Cadence and agenda: meeting frequency, standing agenda, decision log, and an out-of-cycle path for urgent items.
8. Escalation: where disputes go and who breaks ties.
9. Success measures: time from request to decision, share of software bought through the intake path, savings, and exceptions granted.
10. 90-day launch plan: charter approval, members named, intake live, first three meetings, first metrics review. **Decision needed:** sponsor sign-off.

## Output

Draft mode: the charter from `template.md`, the decision-rights table, and the 90-day plan. Review mode: a gap table (step, what's missing, why it matters, fix). Either way, end with the findings block: one `charter_gap` per gap found, using the slugs decision-rights, sponsor, membership-size, intake-path, cadence, metrics, escalation.
```

Append the shared output rules block verbatim.

- [ ] **Step 2: Write the supporting files**

`checklist.md`:

```markdown
# Governance program launch checklist

1. Problem statement agreed in one sentence [[XW-003]]
2. Executive sponsor with budget authority named [[XW-027]]
3. Decision rights and thresholds written down [[XW-027]]
4. Voting members named, 5 to 9 people [[XW-004]]
5. Intake form and triage owner live [[XW-027]]
6. Procurement enforcement agreed; overlaps with other boards settled [[XW-027]]
7. Cadence, standing agenda, and decision log set up [[XW-025]]
8. Escalation and tie-break path written down [[XW-027]]
9. Success measures defined with a baseline [[XW-025]]
10. Charter approved by the sponsor and published [[XW-020]]
11. First metrics review held at day 90 [[XW-025]]
```

`sop.md`: sections Purpose, Scope, Roles (sponsor, chair, secretary/triage owner, voting members, consulted members), Frequency (monthly meetings; charter reviewed yearly), Steps (numbered, matching checklist, tags kept), Evidence to retain (charter, decision log, metrics), Related.

`template.md`: charter skeleton with headings Purpose, Sponsor, Decision rights (table: decision | council decides | council advises | delegated to | threshold), Membership (voting / non-voting), Intake and triage, Enforcement, Meetings, Escalation, Success measures, Review date.

`platform-guide.md`: running intake through a ServiceNow catalog item and approval workflow, logging decisions, and using Flexera One data (spend, usage, shadow IT discovery) as meeting inputs. Fetch current docs with WebFetch first; use only confirmed names; cite URLs.

`copilot-test.md`: attach `demo-estate/council-draft.md`; pass if gaps include decision rights, sponsor, and membership size.

`example/halden-council-review.md`: passing Claude eval output.

- [ ] **Step 3: Build and run evals**

Run: `make build && evals/run.sh program-setup claude && evals/run.sh program-setup codex`
Expected: `build ok`; both `"passed": true` (the three planted gaps found; at most one extra slug beyond them). Stop after two failed fix attempts and report.

- [ ] **Step 4: Eve reviews (redline) and runs the Copilot test**

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat(program-setup): add governance launch method" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CxthZSoP1hm8J6w9VwKbX6"
```

---

### Task 12: Governance-reviewer agent

**Files:**
- Create: `agents/governance-reviewer.md`, `evals/fixtures/weak-policy.md`

**Interfaces:**
- Consumes: `crosswalk.csv` (shipped inside each skill folder in `dist/claude`).

- [ ] **Step 1: Write the fixture** — `evals/fixtures/weak-policy.md`: a one-page Halden "Application Access Policy" that states access is granted by managers, says reviews happen "regularly" with no frequency, never mentions leavers or privileged accounts, and claims "full ISO 27001 compliance" with no evidence.

- [ ] **Step 2: Write `agents/governance-reviewer.md`**

```markdown
---
name: governance-reviewer
description: Review a governance document (policy, SOP, control narrative, audit response) against the app-governance-kit crosswalk. Reports missing controls and claims without evidence. Read-only; never rewrites the document.
tools: Read, Grep, Glob
model: sonnet
---

You review governance documents. You never edit them.

1. Read the document and the crosswalk (`skills/crosswalk/crosswalk.csv` in this plugin).
2. List each obligation the document makes, with the crosswalk row it matches.
3. List crosswalk rows in the document's apparent scope that it never addresses. Explain why each matters in one sentence.
4. List every claim of compliance or completeness with no evidence behind it, quoting the claim (short quotes from the document under review are fine).
5. List vague terms that make a control untestable ("regularly", "as needed", "appropriate") and suggest the measurable version.

Return three sections: Covered, Missing, Unsupported or vague. Cite XW ids and clause numbers; never quote standards text.
```

- [ ] **Step 3: Build and try it**

Run: `make build && claude -p "$(cat dist/claude/agents/governance-reviewer.md | sed '1,/^---$/d' | sed '1,/^---$/d')

Review evals/fixtures/weak-policy.md." --allowedTools Read`
Expected: Missing includes XW-016 (no frequency), XW-017 (leavers), XW-018 (privileged); Unsupported includes the ISO 27001 compliance claim. Save output to `evals/results/reviewer-weak-policy.md` and check by eye.

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "feat(agents): add governance reviewer agent" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CxthZSoP1hm8J6w9VwKbX6"
```

---

### Task 13: Word and Excel exports

**Files:**
- Create: `build/export-office.sh`

**Interfaces:**
- Consumes: `methods/<tool>/{checklist.md, sop.md, template.*}`; `cmdb_package` at `$AGK_CMDB_PATH` (default `/Applications/Development/Projects/cmdb_package`).
- Produces: `dist/office/<tool>/{checklist.docx, sop.docx, template.docx|template.xlsx}` (git-ignored; attached to GitHub releases).

- [ ] **Step 1: Confirm the converter's interface and template content**

Run: `cd "$AGK_CMDB_PATH" && python3 md_to_word_converter.py --help && python3 csv_to_xls.py --help`
Then generate one test file with `--template technical` and run `PYTHONPATH=build python3 -c "from agk.scan import docx_text; print(docx_text(__import__('pathlib').Path('out.docx')))"`. Read the output. If any employer name, logo text, or author name appears, stop and report it to Eve before continuing; the template must be cleaned or replaced first.

- [ ] **Step 2: Write `build/export-office.sh`**

```bash
#!/usr/bin/env bash
# Export checklists, SOPs, and templates to Word/Excel using cmdb_package.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
cmdb="${AGK_CMDB_PATH:-/Applications/Development/Projects/cmdb_package}"
for dir in "$root"/methods/*/; do
  tool="$(basename "$dir")"
  case "$tool" in _*|.*) continue ;; esac
  out="$root/dist/office/$tool"; mkdir -p "$out"
  for doc in checklist sop; do
    python3 "$cmdb/md_to_word_converter.py" "$dir/$doc.md" "$out/$doc.docx" --template technical
  done
  if [ -f "$dir/template.md" ]; then
    python3 "$cmdb/md_to_word_converter.py" "$dir/template.md" "$out/template.docx" --template technical
  else
    python3 "$cmdb/csv_to_xls.py" "$dir/template.csv" "$out/template.xlsx"
  fi
done
echo "office export done"
```

If Step 1 shows `csv_to_xls.py` takes different arguments, adjust the one call to match its `--help` output.

- [ ] **Step 3: Run the export and the scan**

Run: `chmod +x build/export-office.sh && build/export-office.sh && make scan`
Expected: `office export done`; `scan clean`. Open one `.docx` and one `.xlsx` to check they look right.

- [ ] **Step 4: Commit**

```bash
git add build/export-office.sh
git commit -m "feat(build): export office documents" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CxthZSoP1hm8J6w9VwKbX6"
```

---

### Task 14: Portfolio site

**Files:**
- Create: `site/index.html`, `site/crosswalk.html`, `site/tools.html`, `site/case-studies.html`, `site/about.html`, `site/style.css`, `build/agk/site.py`, `tests/test_site.py`
- Modify: `build/agk/build.py` (call `inject_crosswalk` at the end of `build`)

**Interfaces:**
- Consumes: `load_crosswalk` (Task 2).
- Produces: `inject_data(html: str, name: str, data: list) -> str` replacing the content between `<!--{name}-DATA-->` and `<!--/{name}-DATA-->` with `<script type="application/json" id="{name lowercased}-data">…</script>` (crosswalk uses name `XW`; Task 14c uses `LC`); `broken_links(site_dir: Path) -> list[str]`.

- [ ] **Step 1: Write the failing tests**

`tests/test_site.py`:

```python
import json
import re
import tempfile
import unittest
from pathlib import Path

from agk.site import broken_links, inject_data

ROWS = [{"id": "XW-001", "theme": "Inventory", "summary": "Keep one </script> safe"}]


class SiteTests(unittest.TestCase):
    def test_injects_json_between_markers(self):
        html = "<body><!--XW-DATA--><!--/XW-DATA--></body>"
        out = inject_data(html, "XW", ROWS)
        data = re.search(r'id="xw-data">(.*?)</script>', out, re.S).group(1)
        self.assertEqual(json.loads(data.replace("<\\/", "</"))[0]["id"], "XW-001")

    def test_injection_is_repeatable(self):
        html = "<!--XW-DATA--><!--/XW-DATA-->"
        once = inject_data(html, "XW", ROWS)
        self.assertEqual(inject_data(once, "XW", ROWS), once)

    def test_names_do_not_collide(self):
        html = "<!--XW-DATA--><!--/XW-DATA--><!--LC-DATA--><!--/LC-DATA-->"
        out = inject_data(inject_data(html, "XW", ROWS), "LC", [{"stage": "plan"}])
        self.assertIn('id="xw-data"', out)
        self.assertIn('id="lc-data"', out)

    def test_escapes_script_close(self):
        out = inject_data("<!--XW-DATA--><!--/XW-DATA-->", "XW", ROWS)
        self.assertEqual(out.count("</script>"), 1)

    def test_missing_markers_raise(self):
        with self.assertRaises(ValueError):
            inject_data("<body></body>", "XW", ROWS)

    def test_broken_relative_link_reported(self):
        d = Path(tempfile.mkdtemp())
        (d / "index.html").write_text('<a href="tools.html">t</a><a href="https://x.com">x</a><a href="#top">t</a>')
        self.assertEqual(broken_links(d), ["index.html: tools.html"])
```

- [ ] **Step 2: Run to verify failure**

Run: `PYTHONPATH=build python3 -m unittest tests.test_site -v`
Expected: FAIL with `No module named 'agk.site'`

- [ ] **Step 3: Implement `build/agk/site.py`**

```python
import json
import re
from pathlib import Path

LINK_RE = re.compile(r'(?:href|src)="([^"]+)"')


def inject_data(html: str, name: str, data: list) -> str:
    pattern = re.compile(rf"<!--{name}-DATA-->.*?<!--/{name}-DATA-->", re.S)
    if not pattern.search(html):
        raise ValueError(f"page has no <!--{name}-DATA--> markers")
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    block = (f'<!--{name}-DATA--><script type="application/json" id="{name.lower()}-data">'
             f'{payload}</script><!--/{name}-DATA-->')
    return pattern.sub(lambda _: block, html)


def broken_links(site_dir: Path) -> list[str]:
    out = []
    for page in sorted(site_dir.glob("*.html")):
        for target in LINK_RE.findall(page.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if not (site_dir / target.split("#")[0]).exists():
                out.append(f"{page.name}: {target}")
    return out
```

- [ ] **Step 4: Wire it into the build**

In `build/agk/build.py`, add `from agk.site import broken_links, inject_data` and, before `return errors, warnings` at the end of `build`:

```python
    explorer = root / "site" / "crosswalk.html"
    if explorer.exists():
        explorer.write_text(inject_data(explorer.read_text(encoding="utf-8"), "XW", list(known.values())),
                            encoding="utf-8")
    if (root / "site").is_dir():
        errors += [f"site: broken link {b}" for b in broken_links(root / "site")]
```

Run: `PYTHONPATH=build python3 -m unittest discover -s tests -v`
Expected: all PASS

- [ ] **Step 5: Build the pages** (ui-engineer agent; load the `html` skill first)

All pages: self-contained HTML plus `style.css`; colors as `:root` tokens with dark-mode overrides; no external scripts or fonts; works at 360px width; shared header nav to all five pages.

- `index.html` (the lifecycle wheel is added in Task 14c): name, one-line positioning ("Application governance: portfolio, AI, and access controls, traceable to ISO/IEC 19770, COBIT 2019, ISO/IEC 27001, and ISO/IEC 42001"), three area cards, link to crosswalk explorer. Positioning copy drafted by voice-eve, approved by Eve.
- `crosswalk.html`: contains `<!--XW-DATA--><!--/XW-DATA-->`; vanilla JS reads `#xw-data`, renders a filterable list of themes; clicking one shows the four framework clauses and summary. Text filter; keyboard accessible; no quoted standards text (the data has none).
- `tools.html`: six cards, each with `id="<tool name>"` so other pages can link to `tools.html#<tool>`: what it does, the Halden example (link to `../methods/<tool>/example/`), links to Claude, Codex, Copilot, checklist, SOP, template, platform guide in the GitHub repo.
- `case-studies.html`: three sections, filled in Task 15.
- `about.html`: CV summary, certifications, contact link; content from Eve.

- [ ] **Step 6: Check it**

Run: `make build && make scan`, then open each page in the browser at phone width and in dark mode. Dispatch the accessibility-auditor agent on `site/`; fix every serious or critical finding.
Expected: `build ok`, `scan clean`, no serious accessibility findings.

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "feat(site): add portfolio site and crosswalk explorer" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CxthZSoP1hm8J6w9VwKbX6"
```

---

### Task 14c: Application lifecycle wheel and question bank

**Files:**
- Create: `lifecycle/questions.csv`, `build/agk/lifecycle.py`, `tests/test_lifecycle.py`
- Modify: `build/agk/build.py`, `site/index.html`, `build/export-office.sh`

**Interfaces:**
- Consumes: `load_crosswalk` (Task 2); loaded `Method` names (Task 1); `inject_data`, `broken_links` (Task 14).
- Produces: `STAGES` (ordered `(slug, label)` pairs); `LifecycleError(Exception)`; `load_questions(path: Path, tools: Collection[str], known_xw: Collection[str]) -> list[dict[str, str]]`; `render_checklist(rows: list[dict]) -> str`. Build writes `dist/lifecycle-questions.md` and injects the rows into `site/index.html` under name `LC`.

- [ ] **Step 1: Write the failing tests**

`tests/test_lifecycle.py`:

```python
import tempfile
import unittest
from pathlib import Path

from agk.lifecycle import STAGES, LifecycleError, load_questions, render_checklist
from agk.tags import check_tags

HEADER = "stage,question,tool,xw\n"
TOOLS = {"rationalization", "access-review"}
XW = {"XW-001", "XW-016"}


def full_bank() -> str:
    return HEADER + "".join(f'{slug},"Question for {slug}?",rationalization,XW-001\n' for slug, _ in STAGES)


class LifecycleTests(unittest.TestCase):
    def write(self, text):
        p = Path(tempfile.mkdtemp()) / "questions.csv"
        p.write_text(text, encoding="utf-8")
        return p

    def test_six_stages_in_order(self):
        self.assertEqual([s for s, _ in STAGES], ["plan", "acquire", "deploy", "operate", "optimize", "retire"])

    def test_loads_a_complete_bank(self):
        rows = load_questions(self.write(full_bank()), TOOLS, XW)
        self.assertEqual(len(rows), 6)

    def test_rejects_unknown_stage(self):
        with self.assertRaisesRegex(LifecycleError, "line 8: unknown stage 'launch'"):
            load_questions(self.write(full_bank() + 'launch,"Q?",rationalization,XW-001\n'), TOOLS, XW)

    def test_rejects_unknown_tool(self):
        with self.assertRaisesRegex(LifecycleError, "unknown tool 'nope'"):
            load_questions(self.write(full_bank() + 'plan,"Q?",nope,XW-001\n'), TOOLS, XW)

    def test_rejects_unknown_crosswalk_row(self):
        with self.assertRaisesRegex(LifecycleError, "unknown crosswalk row XW-999"):
            load_questions(self.write(full_bank() + 'plan,"Q?",rationalization,XW-999\n'), TOOLS, XW)

    def test_rejects_empty_question(self):
        with self.assertRaisesRegex(LifecycleError, "empty question"):
            load_questions(self.write(full_bank() + 'plan,"",rationalization,XW-001\n'), TOOLS, XW)

    def test_rejects_stage_with_no_questions(self):
        text = HEADER + 'plan,"Q?",rationalization,XW-001\n'
        with self.assertRaisesRegex(LifecycleError, "no questions for stage"):
            load_questions(self.write(text), TOOLS, XW)

    def test_rejects_wrong_columns(self):
        with self.assertRaisesRegex(LifecycleError, "columns"):
            load_questions(self.write("stage,question\nplan,Q\n"), TOOLS, XW)

    def test_checklist_groups_by_stage_in_order_and_passes_tag_check(self):
        rows = load_questions(self.write(full_bank()), TOOLS, XW)
        text = render_checklist(rows)
        labels = [label for _, label in STAGES]
        positions = [text.index(f"## {label}") for label in labels]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("- [ ] Question for plan? [[XW-001]] (tool: `rationalization`)", text)
        self.assertEqual(check_tags(text, XW, "lifecycle"), [])
```

- [ ] **Step 2: Run to verify failure**

Run: `PYTHONPATH=build python3 -m unittest tests.test_lifecycle -v`
Expected: FAIL with `No module named 'agk.lifecycle'`

- [ ] **Step 3: Implement `build/agk/lifecycle.py`**

```python
import csv
from collections.abc import Collection
from pathlib import Path

STAGES = (("plan", "Plan and request"), ("acquire", "Acquire"), ("deploy", "Deploy"),
          ("operate", "Operate"), ("optimize", "Review and optimize"), ("retire", "Retire"))
COLUMNS = ("stage", "question", "tool", "xw")


class LifecycleError(Exception):
    pass


def load_questions(path: Path, tools: Collection[str], known_xw: Collection[str]) -> list[dict[str, str]]:
    stage_ids = {s for s, _ in STAGES}
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if tuple(reader.fieldnames or ()) != COLUMNS:
            raise LifecycleError(f"columns must be {','.join(COLUMNS)}; got {reader.fieldnames}")
        rows = []
        for n, row in enumerate(reader, start=2):
            row = {k: (v or "").strip() for k, v in row.items()}
            if row["stage"] not in stage_ids:
                raise LifecycleError(f"line {n}: unknown stage {row['stage']!r}")
            if not row["question"]:
                raise LifecycleError(f"line {n}: empty question")
            if row["tool"] not in tools:
                raise LifecycleError(f"line {n}: unknown tool {row['tool']!r}")
            if row["xw"] not in known_xw:
                raise LifecycleError(f"line {n}: unknown crosswalk row {row['xw']}")
            rows.append(row)
    empty = [s for s, _ in STAGES if not any(r["stage"] == s for r in rows)]
    if empty:
        raise LifecycleError(f"no questions for stage(s): {', '.join(empty)}")
    return rows


def render_checklist(rows: list[dict[str, str]]) -> str:
    out = ["# Application lifecycle questions", "",
           "Questions to ask at each stage. Each names the crosswalk row it satisfies and the kit tool that handles it.", ""]
    for slug, label in STAGES:
        out += [f"## {label}", ""]
        out += [f"- [ ] {r['question']} [[{r['xw']}]] (tool: `{r['tool']}`)" for r in rows if r["stage"] == slug]
        out.append("")
    return "\n".join(out)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `PYTHONPATH=build python3 -m unittest tests.test_lifecycle -v`
Expected: 9 PASS

- [ ] **Step 5: Wire into the build**

In `build/agk/build.py`, add `from agk.lifecycle import LifecycleError, load_questions, render_checklist`, and before the site block added in Task 14:

```python
    questions_csv = root / "lifecycle" / "questions.csv"
    if questions_csv.exists():
        try:
            questions = load_questions(questions_csv, {m.name for m in methods}, known)
        except LifecycleError as e:
            errors.append(f"lifecycle: {e}")
        else:
            (dist / "lifecycle-questions.md").write_text(render_checklist(questions), encoding="utf-8")
            home = root / "site" / "index.html"
            if home.exists():
                home.write_text(inject_data(home.read_text(encoding="utf-8"), "LC", questions), encoding="utf-8")
```

Add to `tests/test_build.py`:

```python
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
```

Run: `PYTHONPATH=build python3 -m unittest discover -s tests -v` → all PASS.

- [ ] **Step 6: Write `lifecycle/questions.csv`**

```csv
stage,question,tool,xw
plan,"What problem does this solve, and do we already own an app that does it?",rationalization,XW-011
plan,"Who will own it, and who is the executive sponsor?",program-setup,XW-002
plan,"Does the request meet the council's threshold, and did it come through the intake path?",program-setup,XW-027
plan,"Does it use AI? If so, what risk tier is it?",ai-intake,XW-021
plan,"What data will it hold, and how sensitive is that data?",access-review,XW-028
acquire,"What license model applies, and how many entitlements do we need?",rationalization,XW-006
acquire,"Does the contract give audit, renewal, and exit terms we can live with?",rationalization,XW-013
acquire,"Have the supplier and any AI model provider been assessed?",ai-intake,XW-023
acquire,"Is the purchase recorded against an owner and a cost center?",itam-maturity,XW-012
deploy,"Is the app in the inventory with owner, category, and data sensitivity?",itam-maturity,XW-001
deploy,"Are access roles defined, and who approves new access?",access-review,XW-015
deploy,"Are privileged accounts limited and named?",access-review,XW-018
deploy,"For AI systems: is the inventory record complete and the risk in the register?",ai-intake,XW-022
operate,"Do installs and users stay within entitlements?",rationalization,XW-007
operate,"Is access reviewed on schedule, and are leavers removed?",access-review,XW-016
operate,"Are asset records accurate and reconciled?",itam-maturity,XW-026
operate,"Has the AI system's use changed since intake?",ai-intake,XW-021
optimize,"Is it still worth its cost: tolerate, invest, migrate, or eliminate?",rationalization,XW-011
optimize,"Is anything expiring or due for renewal in the next 90 days?",rationalization,XW-008
optimize,"Where is our asset management process weakest this year?",itam-maturity,XW-025
optimize,"Does the council's decision log show bottlenecks or rubber-stamping?",program-setup,XW-025
retire,"What data does it hold, and will we archive, migrate, or delete it?",rationalization,XW-028
retire,"Are all accounts removed and licenses cancelled or reclaimed?",access-review,XW-017
retire,"Is the contract ended on time, without auto-renewal?",rationalization,XW-013
retire,"Is the inventory record closed, with evidence kept?",itam-maturity,XW-020
```

Run: `make build`
Expected: `build ok`; `dist/lifecycle-questions.md` has six stage headings and 25 items. Eve reviews the questions in a redline session; apply her edits verbatim.

- [ ] **Step 7: Build the wheel on the home page** (ui-engineer agent; load the `html` skill first)

In `site/index.html`, add `<!--LC-DATA--><!--/LC-DATA-->` and an inline SVG wheel: six equal ring segments in stage order, clockwise from the top, each labelled with the stage name, with an arrow showing the cycle from Retire back to Plan. Each segment is a `<button>`-equivalent (`role="button"`, `tabindex="0"`, Enter/Space activate, visible focus ring, `aria-pressed` on the selected one). Selecting a stage fills a panel beside the wheel (below it at phone width) with that stage's questions from `#lc-data`; each question shows its crosswalk row (linking to `crosswalk.html`) and a link to `tools.html#<tool>`. Plan is selected on load. Colors from the `:root` tokens; works in both themes; no external scripts. Also add a "Lifecycle questions" download link to `dist/lifecycle-questions.md` in the GitHub repo.

- [ ] **Step 8: Office export**

Append to `build/export-office.sh`, before the final `echo`:

```bash
mkdir -p "$root/dist/office"
python3 "$cmdb/md_to_word_converter.py" "$root/dist/lifecycle-questions.md" "$root/dist/office/lifecycle-questions.docx" --template technical
```

- [ ] **Step 9: Check it**

Run: `make build && make scan && build/export-office.sh && make scan`
Expected: `build ok`, `scan clean`, `office export done`, `scan clean`. Open the home page in the browser at phone width and in dark mode, click every segment with the mouse and with the keyboard, and follow one tool link and one crosswalk link. Dispatch the accessibility-auditor agent on `site/index.html`; fix every serious or critical finding.

- [ ] **Step 10: Commit**

```bash
git add -A
git commit -m "feat(site): add lifecycle wheel and questions" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CxthZSoP1hm8J6w9VwKbX6"
```

---

### Task 14b: Field guide (certifications, standards, glossary)

**Files:**
- Create: `field-guide/certifications.md`, `field-guide/standards.md`, `field-guide/data-governance.md`, `field-guide/glossary.md`, `site/field-guide.html`
- Modify: `build/agk/scan.py` (add `"field-guide"` to `SCAN_DIRS` and `QUOTE_DIRS`), `tests/test_scan.py`, site nav in all pages

- [ ] **Step 1: Extend the scan to the new folder (test first)**

Add to `tests/test_scan.py`:

```python
    def test_field_guide_is_scanned(self):
        (self.tmp / "field-guide").mkdir()
        (self.tmp / "field-guide" / "g.md").write_text("Worked at AcmeCorp\n")
        self.assertTrue(any("field-guide" in h for h in scan(self.tmp, ["AcmeCorp"])))
```

Run: `PYTHONPATH=build python3 -m unittest tests.test_scan -v` → the new test FAILS. Add `"field-guide"` to both `SCAN_DIRS` and `QUOTE_DIRS` in `build/agk/scan.py`. Rerun → PASS.

- [ ] **Step 2: Research the certifications** (WebFetch; public pages only)

Fetch https://iaitam.org/certifications/, https://iaitam.org/camp/, https://iaitam.org/csam/, and the CHAMP page linked from the certifications page, plus IAPP's AIGP page. Record for each: full name, intended audience, topics listed, format, and recertification rule, with the URL and fetch date. Do not copy course text.

- [ ] **Step 3: Write `field-guide/certifications.md`**

One section per certification: CAMP, Certified Software Asset Manager (CSAM), CHAMP, AIGP. Always write "Certified Software Asset Manager (CSAM)" on first use in any page or section. Each section has:
- **Who it's for** (one sentence)
- **What it covers** (paraphrased from Step 2, with source URL and date)
- **Practical application**: a table of three on-the-job tasks, what "good" looks like, and the kit tool that practices it. For example, CSAM → "establish an effective license position before a vendor audit" → `rationalization` + `itam-maturity`; CAMP → "stand up an ITAM program and its council" → `program-setup`; AIGP → "tier a new AI use case" → `ai-intake`; CHAMP → "retire hardware with evidence" → out of phase-1 scope, say so.
- **Suggested order** for someone new: CAMP first, then CSAM or CHAMP by focus; AIGP for AI governance.

End with: "Names are used for reference only. No affiliation with or endorsement by IAITAM or IAPP."

- [ ] **Step 4: Write `field-guide/standards.md` and `field-guide/glossary.md`**

`standards.md`: what each ISO/IEC 19770 part is for, and how COBIT 2019, ISO/IEC 27001, and ISO/IEC 42001 relate, in our own words; link to the crosswalk explorer. Eve checks part numbers and purposes against her copies.

`glossary.md`: 25–40 terms (ITAM, SAM, HAM, APM, CMDB, entitlement, effective license position, true-up, reconciliation, normalization, SWID tag, shelfware, TIME model, orphaned account, access certification, segregation of duties, risk tier, and so on). Each: one-sentence definition plus a one-line Halden Logistics example.

- [ ] **Step 4b: Write `field-guide/data-governance.md`**

In our own words: application governance manages the software (inventory, ownership, cost, licensing, access, lifecycle); data governance manages the information inside it (definitions, ownership and stewardship, quality, classification, retention, privacy). A two-column comparison table (what each asks, who owns it, main frameworks: ISO/IEC 19770, COBIT BAI09, ISO/IEC 27001 versus DAMA-DMBOK, ISO 8000, privacy law). Then the four places they meet, each with a Halden example and the kit tool that covers it: retiring an app is a data decision (rationalization); data sensitivity sets access-review priority (access review); AI systems depend on their data (AI intake); asset records are themselves data (XW-026, ITAM maturity check). End with: a full data classification and retention tool is planned for phase 2.

- [ ] **Step 5: Build the page and check**

Add `site/field-guide.html` (same rules as Task 14 Step 5) with four sections rendered from the four Markdown files, and add it to every page's nav. Run `make build && make scan`; expect `build ok` and `scan clean`. Hand the four Markdown files to Eve as a redline session; apply her edits verbatim.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "docs(field-guide): add certification field guide" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CxthZSoP1hm8J6w9VwKbX6"
```

---

### Task 14e: Halden practicum

**Files:**
- Create: `practicum/README.md`, `practicum/01-program-setup.md`, `practicum/02-itam-maturity.md`, `practicum/03-crosswalk.md`, `practicum/04-rationalization.md`, `practicum/05-access-review.md`, `practicum/06-ai-intake.md`, `tests/test_practicum.py`
- Modify: `build/agk/scan.py` (add `"practicum"` to `SCAN_DIRS` and `QUOTE_DIRS`), `site/field-guide.html` (practicum section and link)

**Interfaces:**
- Consumes: `demo-estate/answer-key.json` tool names (Task 5); `agk.grade` CLI (Task 6); the six `methods/<tool>/checklist.md` files (Tasks 7–11b).

- [ ] **Step 1: Write the failing test**

`tests/test_practicum.py`:

```python
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRACTICUM = ROOT / "practicum"


class PracticumTests(unittest.TestCase):
    def test_every_graded_tool_has_one_exercise(self):
        key = json.loads((ROOT / "demo-estate" / "answer-key.json").read_text())
        tools = sorted({k["tool"] for k in key})
        for tool in tools:
            matches = list(PRACTICUM.glob(f"[0-9][0-9]-{tool}.md"))
            self.assertEqual(len(matches), 1, f"expected one exercise for {tool}")

    def test_each_exercise_has_required_sections_and_grader_command(self):
        for ex in sorted(PRACTICUM.glob("[0-9][0-9]-*.md")):
            tool = ex.stem.split("-", 1)[1]
            text = ex.read_text()
            for heading in ("## Scenario", "## Files", "## Work through", "## Hand in",
                            "## Check yourself", "## Reflect", "## Certification link"):
                self.assertIn(heading, text, f"{ex.name} missing {heading}")
            self.assertIn(f"python3 -m agk.grade --tool {tool} --output", text, ex.name)
            self.assertNotIn("answer-key.json", text.split("## Check yourself")[0],
                             f"{ex.name} points at the answer key before the self-check section")

    def test_readme_lists_exercises_in_order(self):
        readme = (PRACTICUM / "README.md").read_text()
        names = [ex.name for ex in sorted(PRACTICUM.glob("[0-9][0-9]-*.md"))]
        positions = [readme.index(n) for n in names]
        self.assertEqual(positions, sorted(positions))
```

Also add to `tests/test_scan.py`:

```python
    def test_practicum_is_scanned(self):
        (self.tmp / "practicum").mkdir()
        (self.tmp / "practicum" / "01-x.md").write_text("Worked at AcmeCorp\n")
        self.assertTrue(any("practicum" in h for h in scan(self.tmp, ["AcmeCorp"])))
```

- [ ] **Step 2: Run to verify failure**

Run: `PYTHONPATH=build python3 -m unittest tests.test_practicum tests.test_scan -v`
Expected: FAIL (no `practicum/` folder; `practicum` not in `SCAN_DIRS`).

- [ ] **Step 3: Extend the scan**

Add `"practicum"` to `SCAN_DIRS` and `QUOTE_DIRS` in `build/agk/scan.py`.

- [ ] **Step 4: Write the exercises**

Each `practicum/NN-<tool>.md` has these sections, in order:
- **## Scenario** — two or three sentences placing the learner at Halden Logistics (e.g. program setup: "Halden's CIO asks you to stand up a software governance council. A colleague has drafted a charter.").
- **## Files** — the demo files to use (program setup: `demo-estate/council-draft.md`; ITAM maturity: `maturity-answers.csv`; crosswalk: `controls.md` plus `methods/crosswalk/crosswalk.csv`; rationalization: `apps.csv`, `licenses.csv`; access review: `accounts.csv`, `employees.csv`, `apps.csv`; AI intake: `ai-systems.csv`).
- **## Work through** — "Use `methods/<tool>/checklist.md` by hand, without AI" plus two or three hints that point at where to look, never at the answers.
- **## Hand in** — the deliverable (e.g. rationalization: a TIME table, a duplicates list, a license list, a savings range), ending with a fenced `findings` block in the tool's format, with the finding types for that tool named.
- **## Check yourself** — `PYTHONPATH=build python3 -m agk.grade --tool <tool> --output my-answer.md`, what "passed", "missed", and "extra" mean, and a note that the answer key is public so looking first defeats the point.
- **## Reflect** — three questions that go past the answer key (e.g. "Which duplicate would you keep, and what would the app owners say?").
- **## Certification link** — which CAMP, Certified Software Asset Manager (CSAM), or AIGP topics the exercise practices, paraphrased from the field guide.

`practicum/README.md`: who it's for, how long each exercise takes (30–60 minutes), the six exercises in order (CAMP level: 01, 02; CSAM level: 03, 04, 05; AIGP level: 06), how self-checking works, and the self-study note about the public answer key.

Write all exercise text in our own words; no course or standards text.

- [ ] **Step 5: Run tests**

Run: `PYTHONPATH=build python3 -m unittest discover -s tests -v`
Expected: all PASS.

- [ ] **Step 6: Try one exercise end to end**

Hand-write a `findings` block for exercise 04 from the checklist alone (no AI), save it outside the repo, and run the grader command from the exercise against it. Expected: the grader runs and reports passed/missed/extra. Note in the report whether the hints were enough to find all planted problems.

- [ ] **Step 7: Site and scan**

Add a "Practicum" section to `site/field-guide.html` linking to `practicum/README.md` in the GitHub repo. Run `make build && make scan`; expect `build ok` and `scan clean`. Hand the seven Markdown files to Eve as a redline session; apply her edits verbatim.

- [ ] **Step 8: Commit**

```bash
git add -A
git commit -m "docs(practicum): add halden practicum exercises" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CKmdKvLPfRcNM16k2jQo1H"
```

---

### Task 15: Case studies

**Files:**
- Create: `case-studies/01-*.md`, `02-*.md`, `03-*.md`; Modify: `site/case-studies.html`

- [ ] **Step 1: Interview Eve, one case at a time** (about 20 minutes each). Suggested topics: one portfolio or license cleanup, one access-review or audit, one AI-intake or governance-setup story. Ask: the situation (sector and size in general terms only), the problem, what she did and why, what she decided against, the outcome as a range, and what she'd do differently.
- [ ] **Step 2: Draft each** with the voice-eve agent: sections Situation, Problem, Approach, Outcome, Lessons; 400–600 words; outcomes as ranges; no employer, system, or colleague names.
- [ ] **Step 3: Scan and review.** Run `make scan` (expect `scan clean`), then hand each draft to Eve as a redline session. Apply her edits verbatim.
- [ ] **Step 4: Publish to the page.** Add the three studies to `site/case-studies.html`; run `make build && make scan`.
- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "docs(case-studies): add three anonymized case studies" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01CxthZSoP1hm8J6w9VwKbX6"
```

---

### Task 16: Go public (only on Eve's explicit go-ahead)

- [ ] **Step 1: Create the private remote** (ask Eve first): `gh repo create eve-mcgivern/app-governance-kit --private --source . --push`
- [ ] **Step 2: Full-history secret scan** with the `full-starter` gitleaks config: `gitleaks detect --config ../full-starter/.gitleaks.toml --log-opts="--all"`. Expected: no leaks. Stop on any hit.
- [ ] **Step 3: Final checks.** `make test && make build && make scan` all clean; compliance-reviewer agent on `methods/`, `case-studies/`, `field-guide/`, `practicum/`, `site/` for quoted standards text and employer details; README a stranger can follow (what it is, install for Claude/Codex/Copilot, run the evals, license); MIT `LICENSE`; README note that ISO, IEC, COBIT, ServiceNow, and Flexera names are used for reference only and imply no endorsement.
- [ ] **Step 4: SEO and AI-search basics** (seo-gao-specialist agent): title and description, canonical, Open Graph and Twitter cards with absolute image URLs, JSON-LD (Person + SoftwareSourceCode), `sitemap.xml`, `llms.txt`. No version numbers or dates in metadata.
- [ ] **Step 5: Eve says "make it public."** Then: `gh repo edit eve-mcgivern/app-governance-kit --visibility public --accept-visibility-change-consequences`, enable GitHub Pages from `/site` on `main`.
- [ ] **Step 6: Search Console.** `eve-mcgivern.github.io` is not yet verified: prepare a URL-prefix property for `https://eve-mcgivern.github.io/app-governance-kit/` with an HTML-file verification (Eve clicks). Tell Eve the exact sitemap URL to submit, and remind her until she confirms.
- [ ] **Step 7: Portfolio card (optional, Eve's call).** If wanted, add a card on stylusnexus.github.io and update its JSON-LD, `llms.txt`, and `sitemap.xml`.
