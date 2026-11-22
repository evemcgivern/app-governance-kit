# Audit response SOP

This SOP describes a practice and gives no legal advice. **Decision needed: counsel** marks every point where Legal decides. The order follows the kit's audit decision tree, `sam-toolkit/audit-decision-tree.md`; node ids such as C1 point into it.

## Purpose

Let the organization answer a software publisher's audit or compliance letter through counsel, with evidence ready.

## Scope

Applies to any audit, compliance review, or license verification request from a software publisher or its agent, whether or not the contract gives the publisher an audit right. It covers software only. Hardware is reviewed here only to the extent it helps explain the install counts.

## Roles

Each row ties a role to the tree nodes where it acts. The names behind each role go in `sam-toolkit/audit-response-roles.csv`.

| Nodes | Role | What it does | Who decides |
| --- | --- | --- | --- |
| 1, C1 | Anyone who receives the letter | Pass it to Legal the same day and reply to no one | No one: forward only |
| C2 | Asset manager, Legal | The asset manager tells every team touching in-scope software to stop changes; Legal sets any exception | Legal |
| C3 | Legal, asset manager, executive sponsor | Legal speaks for the organization; the asset manager keeps the dated case file; the sponsor is told | Legal |
| C4, C5 | Legal, contract owner | Test the audit right and scope; choose to reply, ask for more time, or narrow the scope | Legal |
| C6, C9 | Asset manager | Build the first position, then the full reconciliation, and brief Legal and the sponsor | The asset manager reports |
| C7 | IT security, Legal | Review any request to run the auditor's own tool | Legal |
| C8 | Procurement, finance contact, technical lead, hardware asset manager | Find proofs, payment records, and discovery output; compare hardware data where it explains counts | The asset manager |
| C10, C11 | Legal, IT security | Legal decides what is released and attends meetings and site visits; IT security advises on data requests | Legal |
| D1 | Legal | Receives the findings and keeps all contact | Legal |
| D2 | Asset manager, Legal | The asset manager tests each claim; Legal decides what is sent | Legal |
| D3 | Executive sponsor, Legal, contract owner, Finance | Decide true-up, purchase, or settlement | Sponsor with counsel, the contract owner, and Finance |
| D4 | Legal, asset manager | Legal names the duties after settlement; the asset manager puts them on the calendar | Legal |
| D5 | Legal | Closes the audit and lifts the freeze in writing | Legal |
| E1 | Asset manager, executive sponsor | Review, fix, and update the records | The asset manager |
| A2, B1 | Legal, contract owner, asset manager | Legal decides what to ask for at renewal and whether readiness work goes ahead | Legal |
| B2 | Asset manager, contract owner | Name the metric the contract counts; send unclear terms to counsel | The contract owner confirms; counsel for unclear terms |
| B3, B4 | Asset manager, Procurement | Check proofs and build the position | The asset manager reports |
| B5 | Asset manager, contract owner, Finance | Propose how to close a gap; approve buying, reclaiming, or retiring | Finance and the contract owner |
| F1 | Asset manager, Legal, Finance | Handle a request from internal or financial auditors; nothing is shared until both agree | Counsel and Finance |

Department managers answer questions about the software their teams use, as needed.

## Frequency

Prepare once, review the plan and roster every year and after any leadership change. Run the response sequence each time a letter arrives. Run a readiness check against the proofs and use counts every year.

## Prepare ahead

- **Audit response plan.** Who receives letters (mail room, support desk, and executives know to pass them to Legal at once), the communication rule, and the roster in `audit-response-roles.csv`.
- **One roster.** Keep one roster in `audit-response-roles.csv`. Update names when people join or leave, and put a dated printout with phone numbers in the case file.
- **Records brief for counsel.** One page on where proofs, contracts, discovery data, and inventory records live, who keeps each, and how current each is.

## Steps

1. **Legal the same day (C1).** The letter goes straight to Legal. Nobody replies, calls, or forwards it outside the team. Note the reply date. [[XW-004]] [[XW-020]]
2. **Freeze (C2).** No uninstalling, reconfiguring, reassigning, retiring, or buying in-scope licenses, and cleanup scripts pause. Counsel decides any exception, routine renewals included. **Decision needed: counsel** [[XW-029]]
3. **Single contact and case file (C3).** Counsel is the only contact. The asset manager opens a dated case file, and Legal and the asset manager tell the executives who need to know and name the sponsor. [[XW-004]] [[XW-027]]
4. **Audit right and scope (C4, C5).** Legal tests whether this party holds an audit right, including by assignment, and whether the letter asks for more than the agreement allows. Counsel then chooses whether to reply by the date, ask for more time, or narrow the scope. All three go through counsel. **Decision needed: counsel** [[XW-013]] [[XW-007]]
5. **Quick first position (C6).** Give counsel a rough count in the agreement's metric before anyone discusses details with the publisher. [[XW-007]]
6. **Auditor tools (C7).** If the auditor wants to run its own tool or script, IT security reviews it and counsel decides. Nothing runs until then. **Decision needed: counsel** [[XW-029]]
7. **Gather within counsel's scope (C8).** Collect proofs of any age, contracts, and payment records. Use existing discovery reports, and keep each as it stood on the day it ran. Installing a new agent is a system change that needs counsel. Run a hardware comparison only where it explains the counts. Work from copies and keep originals in house. Narrow the use data to the agreed products, entities, and period; do not narrow the proofs, since a proof older than the period still backs today's use. [[XW-005]] [[XW-006]] [[XW-020]] [[XW-026]]
8. **Reconcile and brief (C9).** Count use against proofs per product and version in the metric the agreement counts, with `sam-toolkit/proof-of-purchase-check.csv`: assigned users for a named-user product, devices for a device product, not raw installs. Label each short, even, or over. List downgrade rights for counsel to confirm. Check each proof against the details below, then brief Legal and the sponsor on gaps, risks, and open decisions. [[XW-006]] [[XW-007]] [[XW-024]] [[XW-027]]
9. **Release decisions (C10, C11).** Counsel decides what goes out. By default hold back device lists, raw exports, and internal gap notes. Counsel attends every meeting and site visit. Nobody calls the publisher about license wording while a notice is open. **Decision needed: counsel** [[XW-013]] [[XW-020]]
10. **Findings (D1, D2).** Until findings arrive, the freeze stays. When they do, ask for each claim itemized and test it: the metric counted, downgrade rights, the proofs, and errors in the auditor's data. Give rebuttal evidence to counsel. [[XW-007]]
11. **Settlement (D3, D4).** True-up, purchase, or settlement is for counsel, the contract owner, and Finance. Settling does not by itself end every claim, so counsel says what it covers. Put any duties after settlement on the calendar. **Decision needed: counsel** [[XW-013]]
12. **Close (D5, E1).** The audit is over when counsel closes it and lifts the freeze in writing. Then hold a review, send fixes through change control, and update the roster, renewal calendar, gaps log, and contract terms. Expect the auditor back. [[XW-025]]

## Proof details to check

Group what a proof must show by the question it answers. The agreement and license terms say which details this publisher accepts, and the contract owner confirms them. **Unverified:** until counsel confirms the terms.

- **Who the buyer was.** The buyer's legal name, and the vendor or authorized seller.
- **What was bought and how many.** The product, the version, and the quantity. For an upgrade, the base license it builds on; an upgrade uses up that base, so the base cannot also count for installs of its own version, and an upgrade whose base has no proof is not a proof on its own.
- **The license terms and metric.** The unit the agreement counts (named user, device, core) and any term of use.
- **When it applies.** The purchase date, and for a subscription the current term, not only the first order. A proof dated after the install may be a true-up: true-up agreements often date purchases after the use they cover. Confirm which it is.
- **Whether it can be shown today.** Price and evidence of payment where the agreement asks for them, and a record you can produce. Licensing-portal and authorized-reseller records can count. A certificate of authenticity or a product key alone shows that a copy exists, not a right to use it.

## Rules

- Only counsel talks to the publisher. Everyone else sends questions to Legal.
- Stay accurate and cooperative, but non-committal. Do not guess, speculate, or admit anything outside what counsel approves.
- Do not delete software or change configuration while a notice is open unless counsel agrees.
- Once a notice is open, keep every record as it stands: proofs, contracts, discovery output, emails and notes. Do not delete, edit or back-date any of them. Fix an error by adding a dated note, never by overwriting. **Decision needed: counsel**, for any exception.
- Whether to reply, ask for more time, or narrow the scope is for counsel to decide. **Decision needed: counsel.**
- Never hand over device-level detail beyond what counsel releases.

## Questions to ask

- Does the letter cite a contract clause, and does the contract give the publisher an audit right?
- Was the agreement assigned to the current publisher, and does it give an audit right? **Decision needed: counsel.**
- Which entities, products, and period of use does the letter cover, and which does the agreement cover?
- Which license metric does the agreement count for each product, and what does it accept as proof?
- What level of detail does the agreement say may be released: counts, or device lists?
- Which proof stands behind each installed product and version?
- Which installs have no proof, and is there an explanation (a lapsed record, an acquisition, a vendor name change, a true-up)?
- Who else outside the team might have received this letter?

## Mistakes to avoid

- Replying to the publisher before Legal has read the letter.
- Uninstalling software to look compliant. It can look like destroying evidence.
- Reconciling the whole estate when the agreed scope is three products.
- Counting a proof that lacks a detail the agreement requires, such as the buyer's legal name, or an upgrade whose base has no proof.
- Counting an upgrade and its base license both.
- Reconciling raw installs when the agreement counts named users or devices.
- Treating a subscription's first order as proof without the current term.
- Leaving out proofs older than the audit period. They still back current use.
- Relying on a proof dated after the install without confirming whether it is a true-up or a later purchase.
- Keeping the readiness material in one person's mailbox.

## Who decides

People decide: the asset manager reports, and Legal decides every legal point (the claim, the scope, the reply, and what is released). The executive sponsor decides, with counsel, on spend, true-up, and settlement, and IT security decides what may be exposed. No tool or agent makes any of these calls.

## Evidence to retain

- The letter, with the date and time it arrived and who passed it to Legal.
- The case file: who was told, and when.
- The proofs gathered, and the checklist result for each. Keep proofs for as long as the license and any upgrade rights depend on them, and as long as the records schedule requires. **Decision needed: records owner or counsel** for the exact period.
- The discovery output and any hardware comparison, dated.
- The reconciliation per product and version, and the list of gaps.
- Counsel's decisions on scope, time frame, changes, and release, and the approvers.
- What was handed over, to whom, and when.
- The review notes and the changes that followed.

## Related

- The audit decision tree, `sam-toolkit/audit-decision-tree.md`
- [Governance framework crosswalk](../crosswalk/) (`crosswalk`)
- [ITAM maturity check](../itam-maturity/) (`itam-maturity`)
- [Application rationalization](../rationalization/) (`rationalization`)
- [Hardware lifecycle check](../hardware-lifecycle/) (`hardware-lifecycle`)
- [Stand up a governance program](../program-setup/) (`program-setup`)
