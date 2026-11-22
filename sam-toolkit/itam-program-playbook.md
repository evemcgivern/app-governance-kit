# Playbook: set up and run an ITAM program

This is the one order to follow. It is for an asset manager who has to stand up, or take over, an IT asset management (ITAM) program and keep it running. Every other file in the kit is a tool you pick up at the step where this playbook names it. If another page seems to give a different order, follow this one.

Three terms come up at once. A sponsor is the executive who holds the budget and backs the program in public. A charter is a short written agreement on why the program exists, who decides what, and who sits on the group that decides. An entitlement is the right to use software that you can show you bought. Plain-language definitions of these and other terms are in the [glossary](../field-guide/glossary.md).

You do not need to do all ten steps. Steps 1 to 5 are a complete small program: a sponsor, a scope, a baseline, a renewal calendar, and an audit roster.

All ten steps together take about 250 to 450 hours of effort over 9 to 18 months, part-time, and longer if an audit lands. Add a few hours a week for the routines in the run table below. This is expert judgment for one person with other duties at a mid-size organization. It is not measured.

Clause references are to ISO/IEC 19770-1:2017 (paraphrased) and to the shared crosswalk (`XW-` rows). The standard's tiers are informative, and following them is optional.

## How each step is laid out

Each step gives the reason in one line, the files to use, the matching prompt in `setup-prompts.md` where one exists, boxes to tick when the step is done, and a rough time. Each time gives effort (your own working hours) and calendar time (how long it takes to finish, including waiting on other people). The times are expert judgment, not measurements. A large or messy estate will take longer.

## The ten steps

### Step 1: Read the map

**Why:** You need the same words as the people you will ask for help.

- Files: this playbook, the [glossary](../field-guide/glossary.md), and `guide.md` for what each file is. Prompt 1 in `setup-prompts.md` fits a plan to your hours and your biggest worry.
- Done when:
  - [ ] You have read this playbook and the glossary.
  - [ ] You can say in two sentences what your biggest worry is: audit, renewals, duplicate spend, or ownership.
- Time (expert judgment, not measured): 2 to 4 hours of effort, within 1 week.

### Step 2: Get a sponsor, a problem statement, and a light charter

**Why:** A policy or a gate that no one with budget backs gets ignored. [[XW-027]]

- Files: the `program-setup` method (`methods/program-setup/method.md` and `template.md`) and `customer-expectations.csv`. Prompt 8 reviews a draft charter and checks for a named sponsor. Prompt 11 maps who relies on your data.
- A solo manager does not need a council of five to nine members. Start with a small group of two to four people, such as you, a procurement contact, a finance contact, and a security or legal contact, and one named sponsor. Grow it when the work needs it.
- Done when:
  - [ ] A named sponsor has agreed, in writing, one sentence on the problem you are solving.
  - [ ] A one-page charter names the sponsor, the small group, what the group decides, and where disputes go. [[XW-004]]
  - [ ] Your customers and what they expect from you are listed in `customer-expectations.csv`.
- Time (expert judgment, not measured): 6 to 12 hours of effort over 2 to 6 weeks. It runs long on the sponsor's calendar and on getting the written agreement.

### Step 3: Week 1, stop the bleeding

**Why:** Missed renewal deadlines and a missing audit contact cost money before any program exists.

- Files: `renewal-calendar.csv` and `audit-response-roles.csv`. Prompt 6 finds renewals and notice deadlines. Prompt 7 builds the audit roster.
- Done when:
  - [ ] Every renewal in the next 180 days is in `renewal-calendar.csv` with its notice deadline, an owner, and a decision date. [[XW-008]]
  - [ ] `audit-response-roles.csv` names a stop-gap holder and a backup for each task, with Legal named as the only contact for a publisher. [[XW-004]]
- Time (expert judgment, not measured): 8 to 20 hours of effort over 1 to 3 weeks. Contracts sit with different teams, and notice terms are buried in them.

### Stuck, or inherited a mess?

Read this before step 4 if any of these is true.

- **No sponsor yet.** Write one sentence on the cost or risk, and use one figure from your own records, or write Not found. Take it to whoever signs your largest software invoices or carries the audit risk, and ask for 30 minutes. If you are refused, note who declined and when, and keep working on steps 3 and 4, which sit within your own authority. Prompt 8 reviews a draft charter once you have one; it does not write the request.
- **No inventory yet.** Do not try to count everything. List your five largest software publishers by spend from finance records, and do step 3 for them. The inventory comes in step 7.
- **An audit or vendor letter has already arrived.** Do not reply and do not send data. Hand the letter to Legal the same day and note the deadline it states. Do not run new discovery or remove software without Legal's say. Open a dated case file, then use the `audit-response` method and `audit-response-roles.csv`. Use Prompt 7 once Legal is involved.

### Step 4: Set the scope

**Why:** Without a boundary you try to count everything and finish nothing. [[XW-003]]

- Files: section 2 of `policy-template.md` for which assets and people are covered, and `statement-of-applicability.csv` for which processes are in scope and why. Once the scope is written, use `risk-assessment-guide.md` and `risk-register.csv` to list what could go wrong inside it, rate each risk, and name an owner and a treatment.
- Done when:
  - [ ] A written scope names what is covered and what is excluded, with a reason for each exclusion.
  - [ ] `statement-of-applicability.csv` has a yes or no and a reason for each process.
  - [ ] The sponsor has seen the scope.
  - [ ] Each risk inside the scope is in `risk-register.csv` with a rating, an owner, a treatment, and a review date. The owner has accepted what remains. [[XW-024]]
- Time (expert judgment, not measured): 3 to 6 hours of effort over 1 to 3 weeks. Expect arguments over exclusions such as subsidiaries, cloud, and plant systems.

### Step 5: Baseline and targets

**Why:** You cannot show progress or a saving against a number you never took. [[XW-025]]

- Files: `what-good-looks-like.md` first, then `application-management-self-assessment.md` and `application-management-gap-plan.csv`, or the `application-management-workbook.xlsx` that holds both. Use `tier-self-assessment.md` if you want to know which tier of the standard you meet. Prompt 12 decides what good looks like, then Prompt 2 scores the program. When you know the gaps, use `resources-and-training-plan.md` to size the people, data, training, and tools you need to close them.
- Done when:
  - [ ] You have a one-line good-enough statement for the next 12 months.
  - [ ] Every dimension has an As-Is level with evidence and a To-Be level with a reason.
  - [ ] No more than three gaps are chosen to close first, each with an owner and a date. [[XW-027]]
  - [ ] `resources-and-training-plan.md` is filled in with your own figures, and the sponsor has seen it. Training for each group that needs it is planned. [[XW-004]]
- Time (expert judgment, not measured): 10 to 20 hours of effort over 2 to 4 weeks. Other people hold the evidence.

**Stop here for now.** A small program that stops after step 5 is still worth having: it has a sponsor, a scope, a baseline, a renewal calendar, and an audit roster. Steps 1 to 5 are about 30 to 60 hours of effort over 2 to 3 months. Stop here if time or budget runs out, keep the routines in the run table running, and return to step 6 when you can.

### Step 6: The policy set

**Why:** Written rules let procurement and managers say no, and let you show an auditor what the organization required. [[XW-003]]

- Files: draft with `policy-template.md` (its section 5 holds the roles table) and `policy-standard-template.md`. Test each draft with `policy-checklist.md` before anyone reviews it. Then follow `policy-lifecycle-sop.md` for consultation, counsel review, approval, publication, and review. The smallest useful set is an umbrella policy, an acquisition and exceptions policy, a software standard, a vendor management policy, and a records and evidence policy. Retirement follows `retirement-signoff-checklist.md` and, for devices, the `hardware-lifecycle` method. AI tool intake follows the `ai-intake` method. Prompt 8 reviews a draft policy.
- Done when:
  - [ ] Each policy in your set has an owner and an approver named by role. [[XW-004]]
  - [ ] Each draft passed `policy-checklist.md`, and counsel reviewed the penalty wording and any retention period.
  - [ ] The sponsor approved each policy, dated, and it is published in one versioned place. [[XW-020]]
  - [ ] Exceptions go to `authorization-log.csv` with an approver and an end date. [[XW-019]]
- Time (expert judgment, not measured): 30 to 60 hours of effort over 2 to 4 months. Most of the wait is for counsel, consultation, and approval rounds.

### Step 7: Build one inventory

**Why:** Every later step depends on a record you trust. [[XW-001]]

- Files: `source-of-truth-map.csv` first, to decide which system wins for each kind of data, then `asset-record.csv`. Use `process-map-worksheet.md` to map intake or retirement before you change it. Prompt 4 decides where each kind of data lives. Prompt 3 maps a process. Use `data-sources-guide.md` to collect discovery output, sign-in logs, expense and purchasing data, and HR lists, and to clean product and publisher names so the counts match.
- Done when:
  - [ ] Each kind of data has one authoritative system and an owner. [[XW-026]]
  - [ ] Each application in scope has a named owner and a last-verified date. [[XW-002]]
  - [ ] Discovery results are compared with the record, and each difference is logged. [[XW-005]]
- Time (expert judgment, not measured): 40 to 120 hours of effort over 2 to 6 months. Discovery has coverage gaps, software names need cleaning, and hundreds of titles need a named owner.

### Step 8: Proof first, then the position

**Why:** A count of installs is not a position. A license counts only when proof of purchase backs it. [[XW-006]] [[XW-007]]

- Files, in this order: `proof-of-purchase-check.csv`, then `license-position.csv`, then `documentation-gaps-log.csv` and `contract-terms-check.csv`. Prompt 5 checks licenses against proof. Start with your largest publishers.
- Done when:
  - [ ] Each product of your largest publishers has proof, or a gap in `documentation-gaps-log.csv` with an owner and a date. [[XW-020]]
  - [ ] `license-position.csv` compares use with the proven entitlement in the contract's license metric.
  - [ ] Unclear contract terms are listed in `contract-terms-check.csv` and sent to counsel. [[XW-013]]
  - [ ] You know your company's record retention rule for contracts, invoices, license proofs, and audit evidence, and where it is written. [[XW-020]]
- Time (expert judgment, not measured): 15 to 40 hours of effort per publisher, or 60 to 150 hours for the top three to five publishers, over 2 to 6 months. Proofs go missing, reseller records are thin, and core or virtualization licensing terms take time to work out.

### Step 9: Put controls in place

**Why:** A control counts only when procurement and payables enforce it. [[XW-009]]

- Files: `acquisition-gate-checklist.md`, `invoice-verification.csv`, `authorization-log.csv`, `retirement-signoff-checklist.md`, `vendor-contract-register.csv`, `vendor-scorecard.csv`, and `joiner-mover-leaver-procedure.md`. Prompt 3 maps a process before you change it.
- Done when:
  - [ ] Procurement enforces the gate, and no purchase is paid without a gate result on file. [[XW-009]] [[XW-012]]
  - [ ] Invoices are checked against the contract and order before payment. [[XW-012]]
  - [ ] Authorizations are logged, and each retirement closes with a checklist and a wipe record. [[XW-010]] [[XW-019]]
  - [ ] Strategic suppliers are in `vendor-contract-register.csv` and reviewed on `vendor-scorecard.csv`. [[XW-013]]
  - [ ] HR sends a notice for each joiner, mover, and leaver, and licenses are reclaimed only where the contract owner has confirmed they may be reused. [[XW-017]]
- Time (expert judgment, not measured): 20 to 40 hours of effort to set up, then 2 to 6 months until procurement and payables enforce the controls.

### Step 10: Measure and review

**Why:** Regular checks show which routines are running and which findings are still open. [[XW-025]]

- Files: `benefits-tracker.csv`, `leadership-report.md`, `rolling-internal-check.md`, and `audit-and-review-checklist.md`, run on the schedule in `operating-calendar.md`. Prompt 10 writes the leaders' report, Prompt 13 plans the quarterly checks, and Prompt 9 turns the plan into reminders.
- Done when:
  - [ ] Each routine in `operating-calendar.md` has a named owner and a calendar date.
  - [ ] The sponsor has seen a scorecard and chosen the next three gaps.
  - [ ] Two or three small internal checks have run, and each finding has an owner.
  - [ ] A yearly internal audit and management review is booked. [[XW-025]]
- Time (expert judgment, not measured): 8 to 24 hours of effort a quarter, plus 8 to 16 hours for the first setup.

## What must exist first

- A sponsor before the policy. A policy nobody with budget backs is ignored.
- Scope before the self-assessment and the inventory. Without it you try to count everything and finish nothing.
- The contract's license metric before a license position. A user count is not always the licensed quantity.
- Proof before the position. Reconcile against what you can prove, not what you believe you own.
- Procurement enforcing the gate before the gate counts.
- A baseline before any savings claim.

## Why programs stall in the first year

This is judgment from practice, not a measured rate.

- No sponsor with budget.
- Trying to inventory everything at once.
- Buying a tool before data owners are named.
- Procurement does not enforce the gate.
- One person holds all the knowledge.
- Savings claimed without finance confirming that the spend stopped.
- A publisher audit lands mid-build and absorbs the team.

## Run: keep it alive

`operating-calendar.md` has the full schedule, mapped to these steps. In short:

| When | Routine | Use |
| --- | --- | --- |
| Every day or week | Triage new requests at the gate, check invoices, reclaim licenses from leavers and movers, and review discovery exceptions. | `acquisition-gate-checklist.md`, `invoice-verification.csv`, `joiner-mover-leaver-procedure.md` |
| Every month | Close gaps in the documentation log, review renewals due in 180 days, and check spend made outside procurement. | `documentation-gaps-log.csv`, `renewal-calendar.csv` |
| Every quarter | Refresh license positions, compare copies of data across systems, review strategic suppliers, run two or three small internal checks, update measures, and report to leaders. | `rolling-internal-check.md`, `leadership-report.md` |
| Every year | Re-score the whole program, run an internal audit and a management review, and review each policy and the scope. | `application-management-workbook.xlsx`, `audit-and-review-checklist.md`, `policy-lifecycle-sop.md` |

Events that should start work even when nothing is due:
- A publisher changes its license rules or is acquired. Check whether any audit right moved with it.
- A move to cloud or to virtualization.
- A vendor ends support, or a security advisory names a product you run.
- A price-increase notice.
- A mass hire or a layoff.
- A merger, a new sponsor, or a new owner for a large application.

## Is it working?

A healthy program shows these signs:
- Measures move, and each leads to a decision someone logged.
- Findings close, and the same ones do not come back.
- Savings reconcile to what finance confirms.
- Reviews sometimes change a decision.

A busy but ineffective program shows these:
- Reports grow longer and nobody decides anything from them.
- The documentation gaps log only gets longer.
- Forecast savings never become real savings.
- Every review is confirmed without change.

Pick measures that cannot be met by paperwork alone. The Ideas sheet in `application-management-workbook.xlsx` lists credible ones, with how people tend to game each.

## Where the standard fits

| Stage | Clauses |
| --- | --- |
| Leadership and policy | 5.1 Leadership and commitment; 5.2 Policy; 5.3 Roles, responsibilities and authorities |
| Planning | 6.1 Risk assessment and treatment; 6.2 Objectives, plans, and the statement of applicability |
| Support | 7.1 Resources; 7.2 Competence; 7.3 Awareness; 7.4 Communication; 7.6 Documented information |
| Operation | 8.3 Core data management; 8.4 License management; 8.7 Outsourcing and services |
| Evaluation | 9.1 Monitoring and measurement; 9.2 Internal audit; 9.3 Management review |
| Improvement | 10 Improvement, including corrective action |

The kit does not cover every clause. In particular it has no template for a strategic ITAM plan, preventive action, or staff-owned devices. Read the standard itself for those.

## Decision

| Decision | Owner | Approver | Date |
| --- | --- | --- | --- |
| Program steps adopted, with an owner and a date for each | | | |
