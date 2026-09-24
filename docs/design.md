# app-governance-kit — Design Spec

**Date:** 2026-09-24 · **Owner:** Eve McGivern · **Status:** Draft for review · **Phase:** 1 (portfolio)

## Plain-English summary

Eve is an application governance manager. This project builds a public, career-first portfolio that proves that expertise, made of working tools she also uses in her day job.

It covers three areas: the application portfolio (what software the company owns, what it costs, what to retire), AI governance (what AI systems are in use and how risky they are), and security controls (who has access to what, and the evidence auditors ask for). Everything ties back to the ISO/IEC 19770 standard for IT asset management, and to COBIT 2019 and ISO 27001 where they fit.

There are six tools, including a "how to stand it up" tool for launching a governance program such as a software governance council. Each one is written once and then published in three forms: a Claude skill, a Codex skill, and a Microsoft Copilot version (an agent plus a copy-paste prompt). Eve can use them at home and at work, where only Copilot 365 is allowed. Each tool also comes with a checklist, a standard operating procedure (SOP), a blank template, and a guide to doing the same process in ServiceNow and Flexera.

No real work data is used. The demos run on a made-up company, Halden Logistics, whose data has known problems hidden in it; a tool passes only if it finds them. Case studies from Eve's real work are anonymized. Standards text from ISO and COBIT is copyrighted, so the tools cite clause numbers and paraphrase, never quote.

The portfolio is a six-page site on GitHub Pages under Eve's own name. Its flagship page is an interactive "crosswalk" that shows how the four frameworks map onto each other. Consulting work is a possible later phase, once people are using the tools.

## 1. Goals and non-goals

**Goals**
- Show hiring managers and practitioners real governance judgment, not claims.
- Give Eve tools she uses daily in Claude, Codex, and Copilot 365.
- Every process step traceable to a framework clause.

**Non-goals (phase 1)**
- Selling anything. No pricing, no consulting offer on the site.
- Integrating with live ServiceNow or Flexera instances.
- Any employer data, names, or documents.

## 2. Decisions made during brainstorming

| Decision | Choice |
|---|---|
| Areas | Application portfolio (APM/ITAM), AI governance, security/risk controls |
| Frameworks | ISO/IEC 19770 (anchor), COBIT 2019, ISO/IEC 27001, ISO/IEC 42001; EU AI Act and NIST AI RMF for the AI tool |
| Direction | Career-first; consulting is a later phase |
| Work material | Anonymized patterns only |
| Copilot at work | Agent Builder agents and chat prompts both available |
| Approach | Write each method once, publish three ways |
| Data governance | A lens across the existing tools, not a separate tool in phase 1 |
| Repo home | `github.com/eve-mcgivern/app-governance-kit`, public under Eve's name |

## 3. Repository layout

```
app-governance-kit/
  methods/<tool>/       method.md, checklist.md, sop.md, template.(md|csv), platform-guide.md, example/
  demo-estate/          Halden Logistics data + answer key of planted problems
  build/                build.py (Python standard library only)
  dist/claude/          plugin: one skill per tool + governance-reviewer agent
  dist/codex/           one skill per tool + AGENTS.md
  dist/copilot/<tool>/  agent-instructions.md, knowledge/, chat-prompt.md, test-script.md
  site/                 self-contained HTML pages
  case-studies/         anonymized write-ups
```

`methods/` is the only hand-edited source for tool content. `dist/` is generated and committed so users can download without running the build.

## 4. The six tools

| Tool | Input | Output | Frameworks cited |
|---|---|---|---|
| Crosswalk | A control or requirement | Matching clauses per framework, plus gaps | ISO 19770-1, COBIT 2019, ISO 27001, ISO 42001 |
| ITAM maturity check | Guided questionnaire answers | Maturity score per process area, top 3 gaps, 90-day plan | ISO 19770-1, COBIT BAI09 |
| Rationalization | Application inventory spreadsheet | Tolerate/invest/migrate/eliminate per app; savings and risk summary | ISO 19770-1, COBIT APO |
| AI system intake | Description of an AI use case | Risk tier, required controls, AI-inventory record | EU AI Act, NIST AI RMF, ISO 42001 |
| Access review pack | User and role export | Exceptions, evidence summary, auditor-ready memo | ISO 27001 Annex A, COBIT DSS05 |
| Program setup (how to stand it up) | The governance body to launch (e.g. software governance council) and its context, or a draft charter | Charter, decision-rights table, intake and escalation path, meeting cadence and agenda, 90-day launch plan, success measures; or the gaps in a draft charter | ISO 19770-1 leadership and roles, COBIT EDM01/APO01, ISO 27001 clause 5 |

**Behavior rules for all tools**
- Show the reasoning behind each conclusion.
- Mark every point where a human must decide; never make that decision.
- Flag any figure the tool could not verify from the input.
- Cite clause numbers; paraphrase clause meaning; never quote ISO or COBIT text.

**Data governance lens.** Application governance manages the software; data governance manages the information inside it. The tools cover the places where the two meet:
- Rationalization records what data each app holds and, for every retire or migrate call, the archive/migrate/delete decision and retention period (a decision for the data owner).
- Access review orders its work by the data sensitivity of each app, most sensitive first.
- AI intake records whether the system uses personal data and where its data came from.
- The field guide explains where application governance ends and data governance begins.
- Crosswalk row XW-028 covers data classification and handling.

**Governance-reviewer agent (Claude only):** reviews any governance document against the crosswalk and reports missing controls and claims without evidence. Read-only.

## 5. The five pieces per tool (all six tools)

1. **AI tool** — Claude skill, Codex skill, Copilot agent instructions plus knowledge files, Copilot chat prompt.
2. **Checklist** — one page, usable without AI.
3. **SOP** — roles, steps, frequency, evidence to retain.
4. **Template** — the blank form the process fills in.
5. **Platform guide** — where each step, record, and field lives in ServiceNow (SAM Pro, APM, IRM) and Flexera One. Products named nominatively; no screenshots; no vendor documentation reproduced.

Every checklist and SOP step carries a clause tag from the crosswalk.

Word and Excel versions of checklists, SOPs, and templates are produced with the existing Markdown converter in `cmdb_package`. This is a separate export step; the skills themselves have no third-party runtime dependencies.

## 6. Build

`build/build.py` reads `methods/` and writes `dist/`. It stops with an error when:
- a tool is missing any of its five pieces;
- a Copilot agent's instructions exceed Copilot's instruction-length limit (the limit value is verified against Microsoft's current documentation during planning);
- a checklist or SOP step has no clause tag;
- a clause tag does not exist in the crosswalk.

## 7. Demo company: Halden Logistics

A fictional mid-size logistics firm with about 60 applications, license records, AI systems, and a user/role export. The data contains planted problems, recorded in an answer key:
- 5 duplicate applications
- 3 orphaned accounts
- 2 expired licenses
- 1 AI system that should rate high-risk
- 1 draft governance council charter with 3 flaws: no decision rights, no executive sponsor, 14 voting members

Each tool must find all of its planted problems.

## 8. Portfolio site

GitHub Pages at `eve-mcgivern.github.io/app-governance-kit`. Self-contained HTML, no build step.

1. **Home** — who Eve is, the three areas, what's different about her approach.
2. **Crosswalk explorer** — click a control, see matching clauses across the four frameworks. Flagship page.
3. **Tools** — one card per tool: Halden example result and downloads for all five pieces.
4. **Case studies** — three anonymized write-ups (problem, approach, outcome as a range). Built from interviews with Eve; drafted by the voice-eve agent.
5. **About** — CV summary, certifications, contact.
6. **Field guide** — certifications and their practical application, standards overview, glossary (section 8b).

**Before going public:** full-history secret scan with the full-starter gitleaks config, MIT license, README a stranger can follow, CI running the tests, SEO and AI-search basics, Search Console setup — per the workspace going-public checklist. Making the repo public requires Eve's go-ahead.

## 8b. Field guide

A plain-language guide for Eve and for the people she briefs, in `field-guide/` and on a sixth site page.

- **Certifications:** IAITAM's CAMP (Certified Asset Management Professional, the beginner-level overview), CSAM (Certified Software Asset Manager), and CHAMP (Certified Hardware Asset Management Professional), plus IAPP's AIGP. For each one: who it is for, what it covers (taken from the certifying body's public pages only), and its **practical application**: three concrete on-the-job tasks it prepares you for, each linked to the kit tool that practices that task.
- **Standards:** what each part of ISO/IEC 19770 is for, and how COBIT 2019, ISO/IEC 27001, and ISO/IEC 42001 relate, in our own words.
- **Data governance boundary:** where application governance ends and data governance begins, the four places they meet (retirement, sensitivity, AI data, asset-record quality), and the main data frameworks (DAMA-DMBOK, ISO 8000) described in our own words.
- **Glossary:** ITAM, SAM, HAM, APM terms (for example effective license position, entitlement, true-up, reconciliation, TIME model), each with a one-line example from Halden Logistics.
- **Naming rule:** always spell out "Certified Software Asset Manager (CSAM)" on first use. The bare acronym has an unrelated, very different meaning in general web search, so the long form keeps the page from being misread and from being filtered by search engines.
- Course materials from IAITAM, IAPP, ISO, and ISACA are never reproduced. Names are used for reference only.

## 9. Testing

1. The build produces all three versions of every tool, or stops with an error.
2. The build fails when a Copilot version is too long, or when a checklist or SOP step lacks a valid clause tag.
3. Each tool finds all of its planted problems in Claude and in Codex.
4. Copilot versions are tested by Eve at work using each tool's two-minute test script; results are recorded in the repo.
5. Before any publish: a scan finds zero hits against Eve's private word list (employer name, internal systems, colleagues), stored outside the repo; and a compliance review finds no quoted ISO or COBIT text.
6. Site pages work at phone width and in dark mode, and pass an accessibility check.

## 10. Risks

| Risk | Mitigation |
|---|---|
| Copyrighted standards text leaks into content | Clause-number-and-paraphrase rule; compliance review before publish |
| Employer details leak into case studies | Private word-list scan; anonymized patterns only |
| Copilot tools drift from Claude/Codex versions | Single source in `methods/`; build regenerates all versions |
| AI law goes stale | Date-stamp legal content; list "last reviewed" on the AI intake tool |
| Scope creep past six tools | New tools go to a phase-2 list, not phase 1 |

## 11. Later phases (not designed here)

- Phase 2: more tools (vendor risk, end-of-life tracking, license true-up, data classification and retention).
- Phase 3: consulting offer, run through the new-project validation gate first.
