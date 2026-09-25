import argparse
import re
import shutil
import sys
from html import escape
from pathlib import Path

from agk.crosswalk import CrosswalkError, load_crosswalk
from agk.doclinks import broken_doc_links
from agk.downloads import write_downloads
from agk.lifecycle import LifecycleError, load_questions, load_stages, render_checklist
from agk.lifecycle_impact import LifecycleImpactError, load_lifecycle_impact
from agk.links import LinkError, link_items, load_links
from agk.methods import MethodError, load_method, method_dirs
from agk.practicum import PracticumError, practicum_payload
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
    try:
        lifecycle_impact = load_lifecycle_impact(methods_dir / "crosswalk" / "lifecycle-impact.csv", known)
    except (LifecycleImpactError, FileNotFoundError) as e:
        return [f"lifecycle-impact: {e}"], []
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
    questions_csv = root / "lifecycle" / "questions.csv"
    if questions_csv.exists():
        try:
            questions = load_questions(questions_csv, {m.name for m in methods}, known)
        except LifecycleError as e:
            errors.append(f"lifecycle: {e}")
        else:
            stages_md = root / "lifecycle" / "stages.md"
            try:
                stages = load_stages(stages_md, known) if stages_md.exists() else None
            except LifecycleError as e:
                errors.append(f"lifecycle: {e}")
                stages = None
            lc_items = None
            lc_links = None
            links_csv = root / "lifecycle" / "links.csv"
            if links_csv.exists():
                lc_items = link_items(questions, stages["stages"] if stages else {})
                try:
                    lc_links = load_links(links_csv, lc_items)
                except LinkError as e:
                    errors.append(f"lifecycle links: {e}")
            (dist / "lifecycle-questions.md").write_text(
                render_checklist(questions, stages["stages"] if stages else None, lc_links, lc_items),
                encoding="utf-8")
            lifecycle_page = root / "site" / "lifecycle.html"
            if lifecycle_page.exists():
                lc_payload = [{"questions": questions, "stages": stages["stages"] if stages else None,
                               "items": lc_items, "links": lc_links}]
                page_text = inject_data(lifecycle_page.read_text(encoding="utf-8"), "LC", lc_payload)
                together_re = re.compile(r"<!--LC-TOGETHER-->.*?<!--/LC-TOGETHER-->", re.S)
                if stages and together_re.search(page_text):
                    together_html = (f'<!--LC-TOGETHER--><p class="lc-together">{escape(stages["together"])}'
                                      f'</p><!--/LC-TOGETHER-->')
                    page_text = together_re.sub(lambda _: together_html, page_text)
                lifecycle_page.write_text(page_text, encoding="utf-8")
    explorer = root / "site" / "crosswalk.html"
    if explorer.exists():
        rows = [dict(r, key_work=themes[r["id"]], stages=lifecycle_impact[r["id"]]) for r in known.values()]
        explorer.write_text(inject_data(explorer.read_text(encoding="utf-8"), "XW", rows),
                            encoding="utf-8")
    impact_map = root / "site" / "impact-map.html"
    if impact_map.exists():
        im_rows = [{"id": r["id"], "theme": r["theme"], "stages": lifecycle_impact[r["id"]]} for r in known.values()]
        impact_map.write_text(inject_data(impact_map.read_text(encoding="utf-8"), "IM", im_rows),
                              encoding="utf-8")
    practicum_page = root / "site" / "practicum.html"
    if practicum_page.exists():
        try:
            payload = practicum_payload(root / "demo-estate", root / "practicum", known)
        except (PracticumError, FileNotFoundError) as e:
            errors.append(f"practicum: {e}")
        else:
            practicum_page.write_text(
                inject_data(practicum_page.read_text(encoding="utf-8"), "PR", [payload]), encoding="utf-8")
    if (root / "site").is_dir():
        warnings += write_downloads(root)
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
