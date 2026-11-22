# Operating calendar and first 90 days

A schedule for the toolkit files: what to do monthly, quarterly, and yearly, what sets off an extra task, and how the first 90 days (about 13 weeks) line up with the steps of `itam-program-playbook.md`. The playbook sets the order; this calendar follows it and adds dates. The files are templates, so none of this happens unless someone owns it. Put each routine in a named person's calendar.

Clause references are to the shared crosswalk (`XW-` rows). Frequencies are practical suggestions, not requirements of any standard. Adjust them to your size and risk.

**Stop point.** A small program that stops after playbook step 5 (the first five rows of the table below, which the playbook puts at about 2 to 3 months) is still worth having: it has a sponsor, a scope, a baseline, a renewal calendar, and an audit roster. If time runs out, stop there and keep the routines below running.

## Routines

| When | Routine | File | Owner role |
| --- | --- | --- | --- |
| Every day or week | Triage new requests at the gate [[XW-009]] | `acquisition-gate-checklist.md` | Asset manager |
| Every day or week | Check each invoice against the contract and order before payment [[XW-012]] | `invoice-verification.csv` | Finance partner |
| Every day or week | Reclaim licenses from leavers and movers once the contract owner confirms [[XW-017]] | `joiner-mover-leaver-procedure.md` | Asset manager |
| Every day or week | Review discovery exceptions [[XW-005]] | `asset-record.csv` | Asset manager |
| Monthly | Review open gaps; close or reschedule each [[XW-020]] | `documentation-gaps-log.csv` | Asset manager |
| Monthly | List renewals due in 180 days; record decisions [[XW-008]] | `renewal-calendar.csv` | Application owner |
| Monthly | Check spend made outside procurement [[XW-012]] | `acquisition-gate-checklist.md` | Finance partner |
| Monthly | Compare the HR leaver list with sign-in logs; log each leaver who still has an account [[XW-017]] | `joiner-mover-leaver-procedure.md`, `internal-check-log.csv` | Asset manager |
| Quarterly | Review the risk register; re-rate open risks and close only treated ones [[XW-024]] | `risk-register.csv` | Governance lead |
| Quarterly | Refresh license positions against use [[XW-007]] | `license-position.csv` | Asset manager |
| Quarterly | Compare copies of data across systems [[XW-026]] | `source-of-truth-map.csv` | Data owner |
| Quarterly | Review strategic suppliers [[XW-013]] | `vendor-scorecard.csv` | Vendor manager |
| Quarterly | Run two or three small internal checks [[XW-025]] | `rolling-internal-check.md` | Asset manager |
| Quarterly | Report to leaders [[XW-025]] | `leadership-report.md` | Governance lead |
| Quarterly | Confirm each audit role has a ready backup [[XW-004]] | `audit-response-roles.csv` | Asset manager |
| Yearly | Re-score the program; update the gap plan [[XW-025]] | `application-management-gap-plan.csv` | Governance lead |
| Yearly | Check the tier you meet [[XW-025]] | `tier-self-assessment.md` | Asset manager |
| Yearly | Run an internal audit and management review [[XW-025]] | `audit-and-review-checklist.md` | Sponsor |
| Yearly | Review the policy and the scope [[XW-003]] | `statement-of-applicability.csv` | Governance lead |
| Yearly, and when a new rule is announced | What changed outside the company (laws, regulations, vendor terms)? Record what applies and who acts on it [[XW-003]] | `policy-lifecycle-sop.md` | Program owner and Legal |
| Yearly | Update the one-page road map of outside factors named in the charter | `program-setup` method (`template.md`) | Governance lead |

## Events that start a task

| Event | Do this | File |
| --- | --- | --- |
| A purchase request arrives | Run it through the gate before any money moves [[XW-009]] | `acquisition-gate-checklist.md` |
| An invoice arrives | Check it against the contract and order before paying [[XW-012]] | `invoice-verification.csv` |
| An application or device is retired | Collect the sign-offs and the evidence [[XW-010]] | `retirement-signoff-checklist.md` |
| A publisher sends an audit letter | Hand it to Legal at once; follow the audit method [[XW-004]] | `audit-response-roles.csv` |
| An owner changes | Reassign, then re-confirm the business need [[XW-002]] | `asset-record.csv` |
| A contract or its terms change | Review the affected applications [[XW-013]] | `contract-terms-check.csv` |
| A new or changed law, regulation, or contract rule that touches how software is bought, used, or kept | Ask Legal what applies, and bring forward the review of the affected policy [[XW-003]] | `policy-lifecycle-sop.md` |
| A merger or restructure happens | Re-run the self-assessment and the process maps [[XW-025]] | `application-management-self-assessment.md` |
| A record is found missing | Log it with an owner and a date [[XW-020]] | `documentation-gaps-log.csv` |

## First 90 days

This follows the playbook's steps. Each row names the step, so use the playbook for the why and the done-when boxes. The first column is the week in which you start a step, in order. It is not how long the step takes, and a step is not finished by the next row's week. The playbook gives the time for each step as expert judgment, not measured: steps 1 to 5 are about 30 to 60 hours of effort over 2 to 3 months, and the whole program runs 9 to 18 months part-time. Steps overlap, and steps 6 to 9 run well past week 13; the table shows where to start them.

| Start in week | Playbook step | Goal | Files | Done when |
| --- | --- | --- | --- | --- |
| 1 | 1 Read the map | Know the terms and your biggest worry | `itam-program-playbook.md`, `guide.md` | You can say your biggest worry in two sentences |
| 1 | 2 Sponsor, problem statement, light charter | Name a sponsor and a small group | `customer-expectations.csv`, the `program-setup` method | A sponsor with budget has agreed one line on the problem |
| 1 | 3 Stop the bleeding | Catch renewals and name an audit contact | `renewal-calendar.csv`, `audit-response-roles.csv` | Every renewal in 180 days has an owner and a notice date, and each audit task has a holder |
| 3 | 4 Set the scope | Bound assets and processes | `statement-of-applicability.csv`, `policy-template.md` section 2 | A written scope with exclusions, seen by the sponsor |
| 4 | 5 Baseline and targets | Know where you stand and where you need to be | `what-good-looks-like.md`, `application-management-self-assessment.md`, `application-management-gap-plan.csv` | Every dimension has an As-Is score with evidence and a To-Be target; stop here if you must |
| 6 | 6 The policy set | Draft the umbrella policy and the acquisition policy first | `policy-template.md`, `policy-checklist.md`, `policy-lifecycle-sop.md` | Two policies passed the checklist and have sponsor approval |
| 7 | 7 Build one inventory | Start one trusted inventory | `source-of-truth-map.csv`, `asset-record.csv`, `process-map-worksheet.md` | Each application in scope has an owner and one authoritative record |
| 9 | 8 Proof, then the position | Back entitlements with proof for your largest publishers | `proof-of-purchase-check.csv`, `license-position.csv`, `documentation-gaps-log.csv`, `contract-terms-check.csv` | Every shortfall has proof or a logged gap with an owner |
| 12 | 9 Put controls in place, and 10 Measure and review | Start the gate; show leaders the result | `acquisition-gate-checklist.md`, `invoice-verification.csv`, `benefits-tracker.csv`, `leadership-report.md` | The sponsor has the first report and has chosen the next three gaps |
| If you only have 2 hours a week | Steps 1 to 3 first | Do steps 1 to 3 first. Steps 1 to 5 take 30 to 60 hours of effort (expert judgment), and 30 to 60 hours at 2 hours a week is 15 to 30 weeks, about 4 to 7 months | The files for steps 1 to 3 in the rows above | A sponsor, a renewal calendar, and an audit roster are in place |

## Decision

| Decision | Owner | Approver | Date |
| --- | --- | --- | --- |
| Calendar adopted, with the owner and date for each routine | | | |
