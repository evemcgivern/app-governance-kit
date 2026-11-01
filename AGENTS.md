# AGENTS.md

Workspace-wide rules (commits, security, plan-before-code, approval gates) live in `/Applications/Development/Projects/AGENTS.md`; this file only adds what is specific to this project.

## Project Overview

Nine application-governance methods packaged as skills for Claude, Codex, and Microsoft Copilot: program setup, ITAM maturity, crosswalk, rationalization, access review, AI intake, hardware lifecycle, audit response, and software lifecycle. Also a public reference site and hands-on practicum exercises. MIT licensed. Third-party standards names are used for reference only, with no affiliation.

## Development Commands

From `Makefile` (Python 3, run from the repo root; CI uses 3.12):

- `make test`: run the unittest suite in `tests/`.
- `make build`: delete and regenerate `dist/`, and regenerate the data-driven parts of `site/`.
- `make scan`: fail on quoted runs longer than 15 words and on private terms leaking into public output.
- `evals/run.sh <tool> <claude|codex>`: run a built skill against the demo estate and grade the answer. Needs `make build` first; results land in `evals/results/` (ignored by git).

## Architecture

- `methods/`: one folder per tool (method, checklist, SOP, platform guide, Copilot test, example, and a template). Source of truth.
- `methods/crosswalk/`: `crosswalk.csv` is the shared source for every skill's `crosswalk.csv` copy. `sources.md` records the evidence for each cell.
- `demo-estate/`: fictional company data used by the practicum. `practicum/`: the eight exercises. `field-guide/`: reference material (Markdown only; `site/field-guide.html` is hand-kept).
- `build/agk/`: Python build system. `tests/`: its tests.
- `lifecycle/`: input data for the lifecycle checklist; the build reads it. `evals/`: skill grading.
- `agents/`: Claude agent files, copied to `dist/claude/agents` by the build. Currently `app-governance-agent.md`, a thin wrapper that loads the `app-governance` skill (`methods/app-governance/`), which holds the routing table. `case-studies/` is empty; the scan still covers it, and the case studies page is hand-kept in `site/`.
- `dist/`, `site/`: generated output (plus some hand-kept pages in `site/`). Published via `.github/workflows/pages.yml` on pushes to `main`.

## Releases

`release-please` (`.github/workflows/release-please.yml`) keeps a release PR open on `main`. Merging it bumps `version.txt` and the version line in `README.md`, updates `CHANGELOG.md`, and tags the release. The version lives in `.release-please-manifest.json` and `version.txt`; never edit them by hand. The bump follows the conventional-commit types (`feat` is a minor bump, `fix` a patch, `!` or `BREAKING CHANGE` a major bump; minor while below 1.0).

## Common Gotchas

- Do not hand-edit `dist/` or generated parts of `site/`. Edit sources, then run `make build`.
- CI (`.github/workflows/ci.yml`) runs `make test` and `make build`, then fails on `git diff --exit-code dist/` and `site/`. Commit regenerated output with the source change. `git diff` ignores untracked files, so `git add` any new generated file yourself.
- Crosswalk edits: each row needs a `verified` date and at least one framework cell. Record the evidence in `methods/crosswalk/sources.md`. Cite clause numbers and titles only; paraphrase standards text.
- Spelling: American English everywhere (license, organization, color, program). See `.claude/guidances/spelling.md`; exact wording in URLs and quoted outside titles stays as is.
- Commit subjects: conventional-commit format, 50 characters or fewer.
- `.gitignore` excludes tool and editor files (`.claude/`, `.superpowers/`, `*.code-workspace`), `dist/office/`, `evals/results/*.md`, and `docs/` (local design notes and plans, not published). Check it before assuming a new file is tracked.
