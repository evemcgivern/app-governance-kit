# Field guide: certifications

Six certifications come up most often around this kit's three areas — portfolio, AI, and access. This page states what each one actually covers, in plain terms, and ties it to a task the kit's tools already do. It isn't a study guide, and it isn't a recommendation to sit any particular exam.

| Certification | Governing body | Best for | Typical domains | Pros | Cons |
|---|---|---|---|---|---|
| CAMP | International Association of Information Technology Asset Managers (IAITAM) | Newcomers to ITAM overall | Cross-industry; strongest pull in regulated/compliance-heavy sectors (finance, government, healthcare) where audit-readiness matters most | Foundational, broad process view; the only one of the six that doesn't assume a specialization yet | Doesn't go deep on software or hardware specifics; annual renewal |
| Certified Software Asset Manager (CSAM) | International Association of Information Technology Asset Managers (IAITAM) | Software-heavy licensing/compliance work | Large software estates facing vendor true-up risk — finance, healthcare, government, any enterprise running Microsoft/Oracle/SAP-scale license agreements | Ties directly to two of this kit's tools (`rationalization`, `itam-maturity`); most audit-relevant of the four IAITAM credentials | Annual renewal; no hardware coverage |
| Certified Hardware Asset Management Professional (CHAMP) | International Association of Information Technology Asset Managers (IAITAM) | Hardware lifecycle owners | Hardware-fleet-heavy sectors — manufacturing, healthcare (medical equipment), education (device fleets), retail/logistics (warehouse and POS hardware), government | The only one of the six covering physical assets | This kit has no tool support for hardware yet (a stated phase-1 gap); annual renewal |
| Artificial Intelligence Governance Professional (AIGP) | International Association of Privacy Professionals (IAPP) | AI governance specifically | Deliberately cross-industry by design — any sector deploying AI, in compliance/legal/risk/data-science roles rather than a particular vertical | The only AI-focused credential here; industry-agnostic; ties to `ai-intake` | Separate body/ecosystem from the IAITAM three; harder exam format (multi-select, no partial credit); one recertification detail is flagged below as unconfirmed |
| ITIL 4 Foundation | PeopleCert | Anyone working in or around IT service delivery | Complex, service-heavy IT environments — banking, insurance, healthcare, telecommunications, government, and managed-service/IT-outsourcing providers | Broad recognition outside ITAM specifically; the practice most other frameworks assume as the operating layer underneath them | Not asset-management-specific — its ties to this kit's tools are real but indirect; renewal every 3 years |
| IAM Certificate (Principles of Asset Management) | Institute of Asset Management (IAM) | People new to (or early in) formal asset management, beyond IT alone | Asset-intensive, infrastructure-heavy sectors — utilities (water, electricity, gas), transport and rail, oil and gas, mining, manufacturing, airports, government and public infrastructure | The only one of the six built on general (not just IT) asset management; the ISO 55000 series it's grounded in traces back to a standard the IAM itself helped originate | UK-centred exam logistics (Pearson-approved IAM venues); no IT- or software-specific content of its own |

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

## Certified Hardware Asset Management Professional (CHAMP)

**Who it's for:** People with little or no prior hardware asset management background who own the physical device lifecycle. (Released in 2004 — one of IAITAM's original certifications, not a recent addition.)

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

## ITIL 4 Foundation

**Who it's for:** Anyone working in or around IT service delivery who needs a shared vocabulary for how IT services get planned, built, run, and improved — PeopleCert markets it as suitable at any career stage, not asset-management-specific.

**What it covers:** ITIL 4 Foundation is PeopleCert's entry-level IT service management certification: the Service Value System and Service Value Chain, the four dimensions of service management, the seven guiding principles, and a set of ITIL practices (including configuration management, service level management, and continual improvement) plus key metrics. The exam is 40 closed-book multiple-choice questions in 60 minutes, with a 65% pass mark, available in 12 languages online-proctored or at a test centre. The certification is renewed every 3 years, either by logging 60 continuing-education points through PeopleCert Plus or by passing a different exam in the same product suite. (Source: [peoplecert.org ITIL 4 Foundation](https://www.peoplecert.org/browse-certifications/it-governance-and-service-management/ITIL-1/itil-4-foundation-2565), fetched 2026-09-25.)

**Practical application:**

| On-the-job task | What "good" looks like | Kit tool |
|---|---|---|
| Feed an accurate asset inventory into a broader configuration-management practice | The same core inventory data this kit builds is what an ITIL configuration-management practice consumes — not a second, separate system | `itam-maturity` |
| Manage supplier relationships as part of service delivery, not just cost | Contract terms, risk, and renewal dates are tracked the same way ITIL's supplier-management practice expects | `rationalization` (vendor and contract check) |
| Govern the technical change or release itself | — | Out of this kit's scope; this kit governs whether and why an application exists or changes hands, not the operational mechanics of deploying a change |

## IAM Certificate (Principles of Asset Management)

**Who it's for:** People new to asset management, or with some initial experience in an asset-management role — no entry prerequisites beyond IAM registration.

**What it covers:** The IAM Certificate (its exam is titled "Principles of Asset Management") is the entry-level qualification from the UK's Institute of Asset Management, covering asset management beyond IT alone: five compulsory modules — Principles of Asset Management, Asset Management Policy/Strategy/Planning, Managing Asset Life Cycle Decisions and Activities, Assessing and Managing Asset Management Risks, and Finance and Business Impact. The exam is 60 closed-book multiple-choice questions over 2 hours, delivered at approved IAM exam venues, needing at least 65% overall and a minimum of 50% in every module; roughly 150 study hours are recommended. (Source: [theiam.org IAM Certificate](https://theiam.org/professional-development/qualifications/iam-certificate/), fetched 2026-09-25.) The certificate's own page doesn't cite the ISO 55000 series directly, but the IAM (with the British Standards Institution) originally developed PAS 55 — the asset-management specification ISO used as the direct basis for the 55000/55001/55002 series when it launched in 2014 — so the certificate's syllabus follows the same asset-management-system logic this kit's ISO/IEC 19770-1 citations already rely on. (Source: [Wikipedia, ISO 55000](https://en.wikipedia.org/wiki/ISO_55000), checked 2026-09-25 — a tertiary source, cited here for the historical PAS 55 connection specifically, not for the certificate's own content.)

**Practical application:**

| On-the-job task | What "good" looks like | Kit tool |
|---|---|---|
| Treat the application portfolio as a managed asset base, not just an inventory | Every decision (retain, invest, retire) is tied to a stated value and risk case, not just a cost line | `rationalization` |
| Set an asset management policy with real scope and rules | The policy states what counts as a managed asset and who owns the rules, matching this kit's own program-setup step | `program-setup` |
| Score how well the organization's asset management system actually functions, not just its inventory accuracy | Evidence-backed process scoring, the same discipline ISO 55001's clauses 9-10 (performance evaluation, improvement) ask for | `itam-maturity` |

## Suggested order for someone new

CAMP first — it's the foundational program-and-process view everything else builds on. From there, pick CSAM or CHAMP by which asset type you actually own (software versus hardware) rather than doing both by default. The IAM Certificate is worth adding if your remit reaches beyond IT into physical or infrastructure assets generally; ITIL 4 Foundation is worth adding if your organization already runs formal IT service management and you need its vocabulary. AIGP sits apart from all of these; take it when AI governance specifically is the job, regardless of where you are on the ITAM path.

---

Names are used for reference only. No affiliation with or endorsement by IAITAM, IAPP, PeopleCert/AXELOS, or the Institute of Asset Management.
