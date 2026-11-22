# Policy template

A fill-in template for one ITAM policy. Use it for the umbrella policy first, then again for each policy in the set described in `policy-lifecycle-sop.md`. Replace each prompt in brackets with your own text, and delete any prompt that does not apply. Every example is fictional and comes from Halden Logistics, the demo estate; do not copy an example into your own policy as if it were your rule.

A policy states what the organization requires and who answers for it. Detail that changes often, such as approved titles and versions, belongs in a standard (`policy-standard-template.md`) that the policy points to. Before you send the draft for approval, test it against `policy-checklist.md`. For a draft with known weaknesses to practice on, see `demo-estate/policy-draft.md`.

Clause references are to ISO/IEC 19770-1:2017 (paraphrased) and to the shared crosswalk (`XW-` rows). This template does not give legal advice; the parts that touch discipline, retention, or contract duties need review by counsel.

## Control block

| Field | Entry |
| --- | --- |
| Policy ID | [Your numbering scheme, for example ITAM-POL-001] |
| Title | [Short, plain title] |
| Version | [Version number and one line on what changed] |
| Owner | [A role, not a team name. Example: ITAM manager] [[XW-004]] |
| Approver | [A role with authority over the whole scope. Example: executive sponsor] [[XW-027]] |
| Effective date | [Date the policy binds people] |
| Next review | [Date, and the events that bring it forward] [[XW-025]] |
| Status | [Draft, approved, or withdrawn] |

## 1. Purpose

[Two or three sentences: the problem this policy addresses and what it requires of people. Say what goes wrong without it.] (5.2)

Example (fictional): Halden Logistics buys software through many hands. This policy sets one set of rules so that every license is owned, recorded, and used within its terms, and so that staff know what is expected of them.

## 2. Scope and exclusions

State who and what is covered, and list what is left out, with the reason for each exclusion. A scope that says where appropriate does not bound anything. [[XW-003]]

| Item | In scope | Reason or limit |
| --- | --- | --- |
| [People: employees, contractors, temporary staff] | [Yes or no] | [Reason] |
| [Assets: purchased software, subscriptions, free software, AI features] | [Yes or no] | [Reason] |
| [Locations, business units, subsidiaries] | [Yes or no] | [Reason] |
| [Staff-owned devices] | [Yes or no] | [Reason] |

Example (fictional): Covers all Halden employees and contractors, and all software and subscriptions used for Halden work, on any device. Excludes software used only in a closed lab with no company data, which the Halden security lead reviews each year.

## 3. Definitions

Define each term a reader could argue about. Keep the list short and use each term the same way throughout.

| Term | Meaning in this policy |
| --- | --- |
| [Software asset] | [What counts] |
| [License] | [Right to use, in the vendor's metric] |
| [Standard software] | [Software on the approved catalog; see the related standard] |
| [Exception] | [A recorded, time-limited permission to depart from this policy] |
| [Individual user] | [Anyone who uses covered assets] |

## 4. Policy statements

Write each statement so a person can meet it and a reviewer can test it. If a statement cannot be tested, rewrite it or move it to the purpose.

### 4.1 Objectives

[List the objectives the program works toward, each with a way to tell whether it was met. Say who reviews progress and how often.] (5.2) [[XW-025]]

Example (fictional): Every purchased license has proof of purchase on file, reviewed each quarter by the ITAM manager.

### 4.2 Commitments

[State that the organization will meet the legal, contract, and policy requirements that apply to its software, and that it will keep improving the way it manages assets.] (5.2)

### 4.3 License compliance

[State that the organization uses software only within the rights it holds, in the contract's metric; that it keeps proof of what it holds; and that it compares use with entitlement on a schedule.] [[XW-006]] [[XW-007]]

### 4.4 Acceptable use

[State what people may and may not do with covered software: install, copy, share accounts, move to personal devices, use free or trial versions for company work, and use outside tools with company data.]

Example (fictional): Halden staff do not install software that is not on the Halden approved catalog. They request it through the acquisition and exceptions policy.

### 4.5 Individual and organizational responsibility

[Say what each person answers for, such as using only licensed software and reporting misuse, and what the organization answers for, such as providing licensed tools, tracking entitlement, and responding to vendor audits. Make clear that one person's breach can also create a liability for the organization.]

## 5. Roles and responsibilities

Give each activity one accountable role. Add the other roles that do, advise on, or must be told about it. [[XW-004]] (5.3)

R is responsible for doing the work, A is accountable for the result (one per row), C is consulted, I is informed.

| Activity | Sponsor | ITAM manager | Legal | Security | Procurement | Finance | HR | Business lead |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Approve this policy] | A | R | C | C | I | I | I | I |
| [Maintain the license position] | I | A and R | C | | C | C | | I |
| [Handle exception requests] | I | R | C | C | C | | | A |
| [Apply penalties] | I | C | C | | | | A | R |

Change the columns and the letters to match your own organization. The rows above are placeholders that show the shape.

## 6. Related standards and procedures

List what sits under this policy. Each item has a name, an owner, and a place it is published.

| Document | Type | Owner | Location |
| --- | --- | --- | --- |
| [Software standards catalog] | Standard (`policy-standard-template.md`) | [Role] | [Link] |
| [Acquisition gate] | Procedure (`acquisition-gate-checklist.md`) | [Role] | [Link] |
| [Retirement procedure] | Procedure (`retirement-signoff-checklist.md`; the `hardware-lifecycle` method for devices) | [Role] | [Link] |
| [AI tool intake] | Procedure (the `ai-intake` method) | [Role] | [Link] |

### Records and retention

Find your company's records retention schedule, or ask the records owner or legal where it is written, and copy each rule with its source. [[XW-020]] (7.6.5)

| Record type | Retention rule (from the company's schedule) | Source | Rule owner | Confirmed by | Date |
| --- | --- | --- | --- | --- | --- |
| Proofs of entitlement, with the contracts and terms that grant them | | | | | |
| Orders and invoices | | | | | |
| Audit correspondence and records gathered for an audit | | | | | |
| Discovery and usage reports, kept as they stood on the day they ran | | | | | |
| Disposal and wipe certificates | | | | | |
| Approval records | | | | | |
| Renewal notices | | | | | |

**Decision needed: records owner or counsel.** Have counsel review. This template sets no period.

## 7. Exceptions

An exception is a permission to depart from this policy, granted for a reason and for a limited time. Anyone may ask. [[XW-009]]

- Request: [Where and how a request is made, and what it must say: what, why, risk, and the end date wanted.]
- Approver: [A named role, different from the requester, with escalation by cost or risk.] [[XW-019]]
- Expiry: [Each exception ends on a stated date. Say what happens at the end: renew after a fresh review, or stop.]
- Record: [Every granted exception is entered in `authorization-log.csv`, with the approver, the date, the reason, and `valid_until`.] [[XW-019]]

## 8. Enforcement and penalties

[State the consequences of breaking this policy, who decides them, and how a person can raise a concern or appeal. Keep the wording consistent with existing discipline rules.]

**Decision needed: counsel.** Have counsel and HR review this section, including any named penalty, before it is approved. This template does not set a penalty.

## 9. Communication and awareness

Say how people learn the policy and how you know they understood it. Awareness continues after onboarding. [[XW-003]] (7.3, 7.4)

| Question | Answer |
| --- | --- |
| What is communicated | [The policy, what changed, and what it means for the reader] |
| When | [At hire, at each new version, and on a yearly refresher] |
| To whom | [All covered people, and extra material for managers and buyers] |
| How | [Channel and format] |
| Acknowledgment | [How a person confirms they read it, and where the record is kept] |
| Who checks | [Role that follows up on missing acknowledgments] |

## 10. Measures

Pick a few measures that show the policy is followed, not only that it exists. [[XW-025]]

| Measure | Target | Source | Reviewed by | How often |
| --- | --- | --- | --- | --- |
| [Share of staff with a current acknowledgment] | [Your target] | [System or record] | [Role] | [Cycle] |
| [Purchases with a gate result on file] | [Your target] | [Record] | [Role] | [Cycle] |
| [Exceptions open past their end date] | [Your target] | `authorization-log.csv` | [Role] | [Cycle] |

## 11. Consistency with other policies

List each related policy, such as security, procurement, records, privacy, and acceptable use of company systems. Say whether this policy agrees with it. Record any conflict and who resolves it. [[XW-003]]

| Other policy | Agrees? | Conflict and resolution | Resolved by |
| --- | --- | --- | --- |
| [Policy name] | [Yes, no, or partly] | [What conflicts and how it was settled] | [Role and date] |

## 12. Review and change history

Review at least yearly, and sooner when a trigger occurs: a vendor audit, a merger, a move to cloud, a change of sponsor, or a finding from an internal check. [[XW-025]] Keep every version, and withdraw superseded ones so they cannot be found by mistake. [[XW-020]] (7.6.5)

| Version | Date | Change | Changed by | Approved by |
| --- | --- | --- | --- | --- |
| [1.0] | [Date] | [Initial issue] | [Role] | [Role] |

## 13. Approval

| Decision | Owner | Approver | Date |
| --- | --- | --- | --- |
| Approve this policy as written | [Owner role] | [Approver role] | |

Source: ISO/IEC 19770-1:2017 clauses 5.2, 5.3, 7.3, 7.4 and 7.6.5, and the shared crosswalk. Paraphrased; this is not a substitute for the standard.
