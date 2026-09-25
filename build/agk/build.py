import argparse
import shutil
import sys
from pathlib import Path

from agk.crosswalk import CrosswalkError, load_crosswalk
from agk.doclinks import broken_doc_links
from agk.methods import MethodError, load_method, method_dirs
from agk.render import (render_claude, render_claude_manifest, render_codex,
                        render_codex_agents, render_copilot)
from agk.site import broken_links, inject_data
from agk.tags import check_tags
from agk.themes import ThemesError, load_themes


def build(root: Path) -> tuple[list[str], list[str]]:
    methods_dir, dist = root / "methods", root / "dist"
    crosswalk_csv = methods_dir / "crosswalk" / "crosswalk.csv"
    try:
        known = load_crosswalk(crosswalk_csv)
    except (CrosswalkError, FileNotFoundError) as e:
        return [f"crosswalk: {e}"], []
    try:
        themes = load_themes(methods_dir / "crosswalk" / "themes.md", known)
    except (ThemesError, FileNotFoundError) as e:
        return [f"themes: {e}"], []
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
    errors += [f"doc link: {b}" for b in broken_doc_links(methods_dir)]
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
    explorer = root / "site" / "crosswalk.html"
    if explorer.exists():
        rows = [dict(r, key_work=themes[r["id"]]) for r in known.values()]
        explorer.write_text(inject_data(explorer.read_text(encoding="utf-8"), "XW", rows),
                            encoding="utf-8")
    if (root / "site").is_dir():
        errors += [f"site: broken link {b}" for b in broken_links(root / "site")]
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
