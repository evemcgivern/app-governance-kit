# Field guide: certifications

Four certifications come up most often around this kit's three areas — portfolio, AI, and access. This page states what each one actually covers, in plain terms, and ties it to a task the kit's tools already do. It isn't a study guide, and it isn't a recommendation to sit any particular exam.

## Certified Asset Management Professional (CAMP)

**Who it's for:** People new to IT asset management who need the foundational program and process picture before they specialize.

**What it covers:** CAMP is IAITAM's entry-level credential, organized around the association's 12 Key Process Areas — inventory and asset identification, acquisition, compliance, disposal, financial management, vendor management, policy, and program management, among others — plus how ITAM fits alongside IT service management. No prior ITAM experience is assumed. It's taught as an 8-hour live-online session plus 10-12 hours of self-study, or a 90-day self-paced course, ending in a 100-question, 3-hour exam with an 85% pass mark and two included attempts. The credential is renewed yearly; renewing within six months of expiry only requires the exam again, and after that the full course has to be retaken. (Source: [iaitam.org/camp](https://iaitam.org/camp/), fetched 2026-09-25.)

**Practical application:**

| On-the-job task | What "good" looks like | Kit tool |
|---|---|---|
| Stand up an ITAM program and its governance council | A charter with a named sponsor, written decision rights and thresholds, and a 90-day launch plan — not just a meeting schedule | `program-setup` |
| Baseline the program's process maturity | Every process area carries an evidence citation, not a self-rating alone, and named gaps | `itam-maturity` |
| Get real ownership assigned across the inventory | Every application has a named owner, not "unassigned" | `rationalization` |

## Certified Software Asset Manager (CSAM)

**Who it's for:** People with little or no prior software asset management background who need to run licensing, compliance, and audit response day to day.

**What it covers:** CSAM shares CAMP's exam format (100 questions, 3-hour limit, 85% pass mark, two attempts, live or self-paced delivery, annual renewal with a 6-month grace window) but turns the curriculum toward software specifically: discovery and harvesting tools, license types and negotiation, EULA interpretation, compliance enforcement, and audit procedures. (Source: [iaitam.org/csam](https://iaitam.org/csam/), fetched 2026-09-25.)

**Practical application:**

| On-the-job task | What "good" looks like | Kit tool |
|---|---|---|
| Establish an effective license position before a vendor audit | The position compares entitlements to actual deployment/usage, not just user counts, and states what's unverified | `rationalization` + `itam-maturity` |
| Find duplicate or underused applications to consolidate | Duplicates are matched by category and function, and a keep/retire call is made with a stated reason | `rationalization` |
| Score software-process maturity ahead of a compliance review | Evidence is collected per process area and gaps are ranked, not just listed | `itam-maturity` |

## CHAMP

**Who it's for:** People with little or no prior hardware asset management background who own the physical device lifecycle.

**What it covers:** CHAMP is IAITAM's hardware-focused counterpart to CSAM — the same 12 Key Practice Areas framing and the same course/exam structure (8-hour live or 90-day self-paced, 100-question/85%-pass/3-hour exam, annual renewal with a 6-month grace period) — but the subject matter is the physical hardware lifecycle: acquisition, deployment, maintenance, refresh, and disposal. (Source: [iaitam.org/champ](https://iaitam.org/champ/), fetched 2026-09-25.)

**Practical application:**

| On-the-job task | What "good" looks like | Kit tool |
|---|---|---|
| Retire hardware with disposal and data-wipe evidence | — | Out of this kit's phase-1 scope; no tool here covers physical hardware disposition |
| Track a hardware refresh cycle against budget | — | Out of this kit's phase-1 scope; no tool here tracks hardware refresh |
| Name hardware alongside software when scoping a maturity baseline | The scope statement says explicitly which asset types — software, hardware, or both — are in view before scoring starts | `itam-maturity` (its scoping step is asset-type-agnostic even though this kit's own example dataset is software-only) |

## Artificial Intelligence Governance Professional (AIGP)

**Who it's for:** Anyone who needs to understand and carry out responsible AI governance, across any industry, not only technical AI roles.

**What it covers:** AIGP is IAPP's AI-governance credential — a different body and a different subject than the three above. Its body of knowledge covers how AI systems and their use cases work, AI's impacts and the responsible-AI principles meant to manage them, current and emerging AI law, the major governance frameworks, the AI lifecycle and its risk management, and open debates in the field. The exam runs 100 questions over 2 hours 45 minutes, with a 15-minute break, delivered at a Pearson VUE test center or via OnVUE remote proctoring; some questions are multi-select with no partial credit. (Source: [iapp.org/certify/aigp](https://iapp.org/certify/aigp/), fetched 2026-09-25.) Recertification runs on continuing-education credits plus a maintenance fee (a flat per-term fee, or covered by an IAPP membership) rather than a yearly retest (Source: [iapp.org/certify/faqs](https://iapp.org/certify/faqs), fetched 2026-09-25). Secondary sources describe the term as two years with 20 credits required (e.g. [archuz.com](https://www.archuz.com/blog/aigp-recertification-cpe-requirements-and-renewal-guide), checked 2026-09-25) — IAPP's own CPE-policy PDF could not be read during this research pass, so treat that specific figure as reported by a secondary source, not confirmed directly against IAPP's document.

**Practical application:**

| On-the-job task | What "good" looks like | Kit tool |
|---|---|---|
| Tier a new AI use case for risk | The tier is stated with reasoning tied to the system's actual decisions and who it affects, not just its category | `ai-intake` |
| Record data provenance and rule out prohibited practices | Data source and personal-data use are logged; a prohibited-practice check is done or explicitly escalated to legal | `ai-intake` |
| Assign controls and a re-review date for the tier | Controls match the tier, and the re-review date is also triggered by any change of use, not only the calendar | `ai-intake` |

## Suggested order for someone new

CAMP first — it's the foundational program-and-process view everything else builds on. From there, pick CSAM or CHAMP by which asset type you actually own (software versus hardware) rather than doing both by default. AIGP sits apart from the other three; take it when AI governance specifically is the job, regardless of where you are on the ITAM path.

---

Names are used for reference only. No affiliation with or endorsement by IAITAM or IAPP.
