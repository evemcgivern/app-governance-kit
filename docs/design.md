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
| Repo home | `github.com/evemcgivern/app-governance-kit`, public under Eve's name |

## 3. Repository layout

```
app-governance-kit/
  methods/<tool>/       method.md, checklist.md, sop.md, template.(md|csv), platform-guide.md, example/
  demo-estate/          Halden Logistics data + answer key of planted problems
  build/                build.py (Python standard library only)
  dist/claude/          plugin: one skill per tool + governance-advisor agent
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

**Key work per theme.** Each of the 28 crosswalk themes has a short description in `methods/crosswalk/themes.md`, in our own words: what it means, the key work involved, the evidence it produces, and who usually owns it. The build fails if any theme lacks one. The descriptions appear in the crosswalk explorer when a theme is clicked, travel with every tool as a reference file, and are part of the governance advisor's reference files.

**How the crosswalk is verified (decided 2026-09-24).** Each clause reference is checked against the standard's publicly published table of contents (ISO's Online Browsing Platform and the official preview pages; ISACA's published COBIT 2019 objective list), with the source link recorded per row in `methods/crosswalk/sources.md`. A research agent does the check; Eve reads the evidence and confirms each clause title fits its theme. The `verified` date means "checked against the published table of contents on this date". A cell with no public evidence stays blank rather than guessed. The site and README say so plainly and note that the crosswalk does not replace the standards. If Eve later buys the standards, rows can be re-checked and the method note updated.

**Data governance lens.** Application governance manages the software; data governance manages the information inside it. The tools cover the places where the two meet:
- Rationalization records what data each app holds and, for every retire or migrate call, the archive/migrate/delete decision and retention period (a decision for the data owner).
- Access review orders its work by the data sensitivity of each app, most sensitive first.
- AI intake records whether the system uses personal data and where its data came from.
- The field guide explains where application governance ends and data governance begins.
- Crosswalk row XW-028 covers data classification and handling.

**Governance advisor (Claude, Codex, and Copilot):** a framework expert with two jobs. It answers governance questions ("How do ISO/IEC 19770 and COBIT overlap on license compliance?", "What should our council decide versus delegate?") and reviews governance documents for missing controls and claims without evidence. Its reference files are the verified crosswalk, the lifecycle questions, the field guide, and an index of the kit's tools, so it can point people to the right tool and lifecycle stage. It cites clause numbers only from the crosswalk and says "not in the kit's crosswalk — check the standard" rather than guessing. It never quotes standards text. An eval of eleven questions fails on any invented crosswalk row or clause, a wrong or missing tool, or a long quote. Read-only.

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

GitHub Pages at `evemcgivern.github.io/app-governance-kit`. Self-contained HTML, no build step.

1. **Home** — who Eve is, the three areas, what's different about her approach, and the lifecycle wheel (section 8a).
2. **Crosswalk explorer** — click a control, see matching clauses across the four frameworks. Flagship page.
3. **Tools** — one card per tool: Halden example result and downloads for all five pieces.
4. **Case studies** — three anonymized write-ups (problem, approach, outcome as a range). Built from interviews with Eve; drafted by the voice-eve agent.
5. **About** — CV summary, certifications, contact.
**Two audiences, one site (UX recommendation, accepted 2026-09-24).** Visitors are never asked to choose a path. Hiring managers usually arrive through a shared link to a tool, case study, or About page, so a "Try it in 2 minutes" link sits in every page's header and goes straight to the rationalization exercise. The home page opens with that link and a case-study teaser, then the lifecycle wheel and tool depth. Tools stays first in the navigation for repeat visitors. There is no login: the working path stays private by where it lives (Copilot in the employer's Microsoft 365, local Claude and Codex, a private repo for notes).

7. **Practicum** — the interactive exercises (section 8c).
6. **Field guide** — certifications and their practical application, standards overview, glossary (section 8b), and a link to the practicum (section 8c).

**Before going public:** full-history secret scan with the full-starter gitleaks config, MIT license, README a stranger can follow, CI running the tests, SEO and AI-search basics, Search Console setup — per the workspace going-public checklist. Making the repo public requires Eve's go-ahead.

## 8a. Application lifecycle wheel

The home page's centerpiece is a clickable wheel of the application lifecycle in six stages: Plan and request, Acquire, Deploy, Operate, Review and optimize, Retire. Clicking a stage shows the questions to ask at that stage. Each question names the crosswalk row it satisfies and links to the tool that handles it.

- The questions live in one file, `lifecycle/questions.csv` (stage, question, tool, crosswalk row). The build checks that every stage has questions, every tool exists, and every crosswalk row exists.
- The build also turns the questions into a checklist, `dist/lifecycle-questions.md` (plus a Word version), grouped by stage. It works on its own at work: attach it to any Copilot agent, or print it for a review meeting.
- **Rules and how the stages connect.** Each stage also states what happens there, the rules that apply (each tagged with its crosswalk row), the gate to move on, which stage or stages it hands off to, and who decides. Hand-offs include the loops: Review and optimize can send an application back to Plan (reinvest or replace) or on to Retire. A short "How it works together" explanation sits above the wheel: the lifecycle is the spine, the governance council owns the gates, the tools do the work at each stage, and the crosswalk shows which framework each rule satisfies. The build checks that every stage has every part, every rule is tagged, and every hand-off points at a real stage.
- **Linked steps (UX recommendation, accepted with the overlay).** Individual rules and questions link to rules and questions in other stages with four link types: refers to (context), may impact (a decision here changes what is needed there), blocks (the target cannot pass its gate until this is resolved), and leads to (only for the loops the wheel does not show by default). Each link is written once in `lifecycle/links.csv`; the reverse ("referenced by", "may be impacted by", "blocked by", "led from") is generated. Following a link opens the target stage, moves focus to the exact rule or question, shows a one-step "Back to …" link, and works with the browser's back button; every rule and question has a shareable address. Typed links appear as text in the stage panel, not as arrows on the wheel; an optional "Show what this affects" toggle lights up the linked stages on the wheel. The build rejects links to anything that does not exist.
- Questions cover the data lens too (for example, "What data does it hold, and will we archive, migrate, or delete it?" at Retire).

## 8b. Field guide

A plain-language guide for Eve and for the people she briefs, in `field-guide/` and on a sixth site page.

- **Certifications:** IAITAM's CAMP (Certified Asset Management Professional, the beginner-level overview), CSAM (Certified Software Asset Manager), and CHAMP (Certified Hardware Asset Management Professional), plus IAPP's AIGP. For each one: who it is for, what it covers (taken from the certifying body's public pages only), and its **practical application**: three concrete on-the-job tasks it prepares you for, each linked to the kit tool that practices that task.
- **Standards:** what each part of ISO/IEC 19770 is for, and how COBIT 2019, ISO/IEC 27001, and ISO/IEC 42001 relate, in our own words.
- **Data governance boundary:** where application governance ends and data governance begins, the four places they meet (retirement, sensitivity, AI data, asset-record quality), and the main data frameworks (DAMA-DMBOK, ISO 8000) described in our own words.
- **Glossary:** ITAM, SAM, HAM, APM terms (for example effective license position, entitlement, true-up, reconciliation, TIME model), each with a one-line example from Halden Logistics.
- **Naming rule:** always spell out "Certified Software Asset Manager (CSAM)" on first use. The bare acronym has an unrelated, very different meaning in general web search, so the long form keeps the page from being misread and from being filtered by search engines.
- Course materials from IAITAM, IAPP, ISO, and ISACA are never reproduced. Names are used for reference only.

## 8c. Halden practicum

Six hands-on exercises that use the Halden Logistics demo company. This is the practical application the certification courses leave out, and it shows Eve can teach the work, not just do it.

- **One exercise per tool,** in an order that follows the certifications: program setup and ITAM maturity (CAMP level), then crosswalk, rationalization, and access review (CSAM level), then AI intake (AIGP level).
- **Each exercise has:** a scenario ("You are Halden's new ITAM lead..."), the demo files to use, the checklist to work through by hand, what to hand in, three reflection questions, and which certification topics it practices.
- **Self-check:** the learner writes their findings in the same findings format the tools use, then runs the grader to see what they missed.
- **Interactive version on the site:** a Practicum page shows each exercise's Halden data as tables. The learner clicks rows to flag problems, picks tiers and gaps from lists, then presses Check to see what they found, missed, and over-flagged, with a hint for each miss. It runs entirely in the browser, with no install and no account. A hiring manager can finish one exercise in about five minutes. The Markdown exercises stay as the printable version.
- **The answer key is public** in the repo, so the practicum is for self-study. A graded classroom version would need the key kept private; that is out of scope for phase 1.

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

- Phase 2: more tools (vendor risk, end-of-life tracking, license true-up, data classification and retention); an AI practicum coach usable in Claude, Codex, and Copilot; optionally a sign-in area for colleagues (for example Cloudflare Access in front of a second site).
- Phase 3: consulting offer, run through the new-project validation gate first.
