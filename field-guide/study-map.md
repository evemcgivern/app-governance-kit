# Field guide: study map for CAMP and CSAM

Use this page to see which of the kit's tools, drills, and practicum exercises practice each topic a CAMP or CSAM course covers. It also shows where the kit has no practice yet, so you know to study that topic another way.

The kit has no exam questions; this is a map of topics. The process areas and topics below come from the topic lists on the certification body's public pages ([CAMP](https://iaitam.org/camp/), [CSAM](https://iaitam.org/csam/), fetched 2026-11-21), described here in plain words. For what each certification is and who it suits, see [certifications.md](certifications.md).

## Exam format

Both pages state the same format, so it applies to CAMP and to CSAM: a 3-hour timed exam of 100 randomized questions, passed at 85% or higher, that cannot be paused once started. The course comes with two attempts, and both must fall inside the 14 calendar days after the exam opens. Everything must finish within 90 days of enrollment. Certification renews every year; an expired one can be renewed with a new exam package for up to 6 months, and after that the course and exam must be retaken. Prices and attempt rules change, so check the page before you book.

To use it, pick the certification, find a topic you're weak on, run the drill with the `cert-prep` tool, and do the matching practicum exercise by hand. "Not covered" means the kit has no drill or exercise for that topic yet.

## CAMP: the 12 key process areas

CAMP is organized around 12 key process areas (see [key process area vs. key performance indicator](glossary.md)). The table lists all 12.

| Process area | What it's about | Kit tool | `cert-prep` drill | Practicum |
|---|---|---|---|---|
| Program management | The standing effort that builds and measures the asset management practice. It has no end date. | `program-setup`, `itam-maturity` | Stand up program governance and a council; baseline process maturity with evidence | 01, 02 |
| Policy management | Writing, approving, publishing, and reviewing the rules. | `program-setup`; `sam-toolkit/policy-template.md`, `policy-standard-template.md`, `policy-checklist.md`, `policy-lifecycle-sop.md` | Review a draft policy for scope, accountable role, defined terms, enforcement, and review cycle | 01 |
| Communication and education | Making sure people know the rules and show they understand them. | Partly: the communication and awareness parts of `sam-toolkit/policy-template.md` and `policy-checklist.md` plan what, when, to whom, and acknowledgment; nothing teaches education | No dedicated drill | Not covered |
| Acquisition management | Controlling what enters the estate, so a record exists before the purchase. | `sam-toolkit/acquisition-gate-checklist.md`; `itam-maturity` checks that a gate exists | No dedicated drill | 02 (partly) |
| Asset identification | Giving every asset a unique identity and confirming it is really there. | `hardware-lifecycle` works on device records | No dedicated drill | 07 (partly) |
| Disposal management | Removing assets properly, with wipe or destruction evidence. | `hardware-lifecycle`; `sam-toolkit/retirement-signoff-checklist.md` | Retire hardware with data-wipe evidence | 07 |
| Documentation management | Keeping contracts, proofs of purchase, and records where they can be found. | `audit-response`; `sam-toolkit/proof-of-purchase-check.csv`, `documentation-gaps-log.csv` | Respond to a publisher audit letter with prepared evidence | 08 |
| Compliance management | Checking your own estate against the rules and contracts you must follow. | `audit-response`, `rationalization` | Respond to a publisher audit letter; establish a license position before an audit | 08, 04 |
| Legislation management | Watching outside laws and standards and telling the people they affect. | Not covered (the `crosswalk` maps standards, not laws) | Not covered | 03 (neighboring topic only) |
| Financial management | Cost data for assets: budgets, invoices, total cost and return. | `rationalization`, `hardware-lifecycle`; `sam-toolkit/invoice-verification.csv`, `savings-report.csv` | Track refresh against budget | 04, 07 |
| Project management | One-off efforts with a start, a plan, and an end. | Not covered | Not covered (see pair 1 in [confusable pairs](confusable-pairs.md)) | Not covered |
| Vendor management | How well you communicate and negotiate with suppliers over time. | `sam-toolkit/vendor-contract-register.csv` and `vendor-scorecard.csv`; `rationalization` needs contract terms as input | Manage suppliers and renewals (ITIL 4 Foundation drill) | 04 |

Two CAMP topics have no practice yet: legislation management and project management. Communication and education has a toolkit template but no drill or exercise. Until the kit covers them, study them from the certification body's own course material.

## CSAM: the software topics

The CSAM course turns the same foundation toward software. These rows follow the course's topics in the order a learner meets them.

| Topic | What it's about | Kit tool | `cert-prep` drill | Practicum |
|---|---|---|---|---|
| What counts as software, and managing licenses strategically, including reclaiming unused licenses | Knowing what you own and what you use | `rationalization`, `itam-maturity` | Establish a license position before an audit; find duplicate or underused applications | 04 |
| The right to audit, and reactive versus proactive posture | Preparing before a letter arrives | `audit-response` | Respond to a publisher audit letter with prepared evidence | 08 |
| Reading an audit letter and license records, and enforcing compliance | Matching what is installed to what you can prove | `audit-response` | Same drill | 08 |
| Reading license agreements (EULAs) | Knowing what a contract lets you do | Partly: `sam-toolkit/contract-terms-check.csv` records which terms are clear; the demo audit letter carries Halden's notes on its agreement | No dedicated drill | 08 (partly) |
| Due diligence, negotiation, and contract terms | What to check in a contract | Partly: `sam-toolkit/contract-terms-check.csv` lists terms to confirm; nothing teaches negotiation | Not covered | Not covered |
| Automation and choosing a discovery tool | Collecting inventory data without doing it by hand | Partly: `software-lifecycle` checks an inventory export; it does not teach tool selection | No dedicated drill | Not covered |
| The asset repository, and hardware and organizational impacts | One trusted inventory and who it touches | `rationalization`, `hardware-lifecycle` | Assign real ownership across the inventory | 04, 07 |
