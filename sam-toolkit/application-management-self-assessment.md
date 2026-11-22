# Application management program self-assessment

A self-assessment for an IT application management program: the work of deciding what applications the organization has, who is accountable for each, what to buy, renew, change, or retire, and how to prove it. It records two states for each part of the program: where you are now (the As-Is state) and where you need to be (the To-Be state). The gap between them is your plan.

Use it before the full `itam-maturity` check, or alongside `tier-self-assessment.md`. The tier check asks whether your asset data meets a standard's tiers; the maturity check scores nine asset management areas with evidence; this one looks at the application management program as a whole and asks where you want it to go. Record your answers in `application-management-gap-plan.csv`.

Clause references are to the shared crosswalk (`XW-` rows). Nothing here comes from a standard's text, and the scale is this kit's own.

## The scale

Score each dimension from 0 to 3. Use the evidence rule: if you cannot show the evidence for a level, score one level lower.

| Level | Meaning | What you can show |
| --- | --- | --- |
| 0 | Not done | Nothing: nobody does this. |
| 1 | Ad hoc | It happens sometimes, depends on who is asked, and is not written down. |
| 2 | Defined | It is written down, has a named owner, and is followed. You can show a recent example. |
| 3 | Measured | It is defined and followed, a number tells you how well it works, and the number has led to a change. |

Not every dimension needs to reach 3. Level 2 is a strong result for a small organization. Choose each To-Be level for a reason: a risk you must reduce, a cost you want to save, or a requirement you must meet.

## The dimensions

| # | Dimension | Level 1 looks like | Level 2 looks like | Level 3 looks like | Kit file that helps |
| --- | --- | --- | --- | --- | --- |
| 1 | Policy, scope, and decision rights | People follow habits. No written rule says what counts as a managed application. | A written, approved policy names scope, an accountable role, defined terms, enforcement, and a review cycle. [[XW-003]] | Acknowledgment is tracked, the policy is reviewed on schedule, and review changes are recorded. | `policy-template.md`, `policy-checklist.md`, `process-map-worksheet.md` |
| 2 | Roles and ownership | Some applications have an owner by habit; others do not. | Every application has a named accountable owner, set by role, with a backup. [[XW-002]] [[XW-004]] | Owner changes trigger a reassignment and a review, and the share of applications with a valid owner is tracked. | `asset-record.csv` |
| 3 | Inventory and data quality | A list exists but is out of date and kept in several places. | One inventory is the record of authority, with an owner per application and a stated refresh schedule. [[XW-001]] [[XW-026]] | Records are verified against discovery data on schedule, mismatches are logged and fixed, and accuracy is measured. | `source-of-truth-map.csv` |
| 4 | Intake and acquisition | Teams buy what they need and tell IT afterward, if at all. | One request path runs before every purchase: already owned, redeployable, duplicate, approved. The record is created before the purchase. [[XW-009]] [[XW-011]] | Purchases outside the path are found on a schedule, counted, and traced to why the path was skipped. | `acquisition-gate-checklist.md` |
| 5 | Lifecycle and periodic review | Applications stay in use until something breaks. | Each application has a lifecycle state and a review date, and the owner confirms it still meets a business need. [[XW-009]] | Reviews also run on events (owner change, contract change, major upgrade), and overdue reviews are tracked. | `renewal-calendar.csv` |
| 6 | Licenses, contracts, and renewals | Licenses and contracts live in mailboxes and in people's heads. | Entitlements, proofs of purchase, and renewal dates are recorded; notice deadlines are known; positions are compared with use in the contract's metric. [[XW-006]] [[XW-007]] [[XW-008]] [[XW-013]] | Every renewal has a decision before its notice deadline, and documentation gaps are logged, owned, and closed. | `license-position.csv`, `documentation-gaps-log.csv` |
| 7 | Cost, value, and rationalization | Cost is known only from invoices. Duplicates are found by chance. | Cost and users are recorded per application; duplicates are reviewed; each application gets a keep, change, or retire call with a reason. [[XW-011]] [[XW-012]] | Savings are recorded with evidence, adverse trends are reported beside them, and renewal decisions use total cost and measured return. | `savings-report.csv` |
| 8 | Risk, security, and AI use | Risk is considered when someone raises it. | Each application has a data-sensitivity rating; new tools that use AI or hold organizational data go through a review before approval. [[XW-021]] [[XW-024]] [[XW-028]] | Risks are tiered, treatments are tracked to completion, and support-end dates and known-exploited flags are checked on schedule. | `acquisition-gate-checklist.md` |
| 9 | Retirement and data disposition | Retired applications are switched off; data and licenses are forgotten. | A retirement procedure covers sign-offs, license release, data archive or deletion, and closing the record. [[XW-010]] | Retirements are checked against the procedure, wipe or destruction evidence is kept, and the final cost is recorded. | `retirement-signoff-checklist.md` |
| 10 | Measures and leadership reporting | Reports are produced when asked, from whatever data is at hand. | A short set of measures, each with a definition, an owner, and a data source, is reported to leaders on a schedule. [[XW-025]] | Each measure has a target and a set response when it is missed, and reports tie results to money saved or risk reduced. | `leadership-report.md` |
| 11 | Communication and education | Owners hear about the rules when something goes wrong. | Owners are told what is expected, and the message is repeated at onboarding and when roles change. | Owners show they understand it (a check or sign-off), and feedback changes how the program communicates. | `process-map-worksheet.md` |

## How to run it

1. Agree scope: which applications, business units, and teams the program covers. Write it down.
2. Score As-Is for each dimension with the people who do the work. For each score, write the evidence you could show an auditor or a leader. Apply the evidence rule.
3. Choose To-Be for each dimension. Write why you chose it and by when. Leave a dimension where it is if it is not worth the effort.
4. Work out the gap: To-Be minus As-Is. Rank the gaps by the risk or cost of leaving them. A gap of two or more is a candidate for a first-quarter project; a gap of one may fit into routine work.
5. Name an owner and a first action for each gap you will close. Limit yourself to three at a time. **Decision needed:** the sponsor chooses which gaps to fund first.
6. Record everything in `application-management-gap-plan.csv`. Repeat the assessment at least yearly, and after a merger, a platform change, or a change of sponsor. Keep each year's copy so you can show movement.

## Common mistakes

- Scoring by intent. A written policy nobody follows is level 1, not level 2.
- Setting every To-Be to 3. A target you cannot afford to reach is a wish, not a plan.
- Scoring without the people who do the work. A sponsor's view of the program often differs from the practitioner's.
- Skipping the evidence column. Without evidence the score cannot be challenged later.
- Treating the assessment as the end. Its output is a short plan with owners and dates.

## Decision

| Decision | Owner | Approver | Date |
| --- | --- | --- | --- |
| Gaps funded this quarter / deferred / accepted as risk | | | |
