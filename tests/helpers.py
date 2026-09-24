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
    (tmp / "methods" / "crosswalk" / "themes.md").write_text(
        "## XW-001 Inventory\n\n- **What it means:** m\n- **Key work:** k\n"
        "- **Evidence it produces:** e\n- **Usually owned by:** o\n", encoding="utf-8")
    (tmp / "agents").mkdir()
    (tmp / "agents" / "governance-reviewer.md").write_text(
        "---\nname: governance-reviewer\ndescription: test\n---\nReview.\n", encoding="utf-8")
    return tmp
