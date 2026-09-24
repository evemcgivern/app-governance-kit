import json
import shutil
from pathlib import Path

from agk.methods import Method, MethodError

COPILOT_MAX = 8000
COPILOT_WARN = 6000
REFERENCE_FILES = ("checklist.md", "sop.md", "platform-guide.md")


def _reference_names(m: Method) -> list[str]:
    return [*REFERENCE_FILES, m.template.name, "crosswalk.csv", "themes.md"]


def _copy_references(m: Method, dest: Path, crosswalk_csv: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for f in REFERENCE_FILES:
        shutil.copyfile(m.dir / f, dest / f)
    shutil.copyfile(m.template, dest / m.template.name)
    shutil.copyfile(crosswalk_csv, dest / "crosswalk.csv")
    shutil.copyfile(crosswalk_csv.parent / "themes.md", dest / "themes.md")


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
