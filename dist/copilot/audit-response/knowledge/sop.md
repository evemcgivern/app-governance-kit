# Audit response SOP

This SOP describes a practice. It gives no legal advice. **Decision needed: counsel** marks every point where Legal decides.

## Purpose

Let the organization answer a software publisher's audit or compliance letter calmly, with one voice and prepared evidence, instead of ignoring the letter or accepting every claim in it.

## Scope

Applies to any audit, compliance review, or license verification request from a software publisher or its agent, whether or not the contract gives the publisher an audit right. It covers software only. Hardware is reviewed here only to the extent it helps explain the install counts.

## Roles

- **IT or software asset manager** — leads the technical work: proofs, discovery, hardware audit, and reconciliation.
- **Legal** — owns every contact with the publisher and every legal call: validity of the claim, scope, time frame, limits on system changes, and settlement.
- **Procurement** — finds purchase records, contracts, and the vendor's contacts of record.
- **Executive sponsor** — receives the briefings, backs the team, and decides on spend and settlement with counsel.
- **IT security** — advises on what may be released and on any change to systems during the audit.
- **Finance contact** — finds payment records to go with each invoice.
- **Department managers** — answer questions about the software their teams use, as needed.

## Frequency

Prepare once, review the plan and roster every year and after any leadership change. Run the response sequence each time a letter arrives. Run a readiness check against the proofs and install counts every year.

## Prepare ahead

- **Audit response plan.** Who receives letters (mail room, support desk, and executives know to pass them to Legal at once), the communication rule, the team roster, and a roles-by-timeline chart.
- **Roles-by-timeline chart, two versions.** One lists roles only and lasts through staff changes. One adds names and phone numbers and is the one used in a hurry. Keep both.
- **Repository status brief for counsel.** One page on where proofs, contracts, discovery data, and inventory records live, who keeps each, and how current each is.

## Steps

1. The letter goes straight to Legal. Nobody replies, calls, or forwards it outside the team [[XW-004]] [[XW-020]]
2. Legal tells the asset manager and the response team, and the asset manager opens a dated case file [[XW-004]] [[XW-020]]
3. Legal and the asset manager tell executive leadership and name the sponsor [[XW-027]]
4. Assemble the team from the roster and walk it through the communication rule [[XW-004]]
5. Gather proofs of purchase: invoice, order, and payment record for each product, with contracts and upgrade history [[XW-006]]
6. Run discovery and keep the output as it stood on the day it ran [[XW-005]] [[XW-020]]
7. Legal tests whether the claim is valid, including whether the agreement passed to the current publisher with an audit right, then settles the scope, the period of use reviewed, and any limit on changing systems while the audit runs **Decision needed: counsel** [[XW-013]] [[XW-007]]
8. Run a hardware audit and compare it with the discovery data, so missing or extra devices are explained [[XW-005]] [[XW-026]]
9. Narrow the discovery data to the agreed scope: products, entities, and period of use. Do not narrow the proofs: a proof older than the period still backs today's use [[XW-005]] [[XW-026]]
10. Reconcile use against proofs per product and version in the license metric the agreement counts, with `sam-toolkit/proof-of-purchase-check.csv`: assigned users for a named-user product, devices for a device product, not raw installs. Label each short, even, or over, and list any downgrade rights to confirm with counsel [[XW-007]]
11. Check each proof against what the agreement and license terms accept as proof: typically buyer, vendor, product, version, metric, quantity, and date, often price and payment, the current term for a subscription, and the qualifying base behind each upgrade. Licensing-portal and reseller records can count [[XW-006]] [[XW-026]]
12. Hold every software removal and configuration change unless counsel agrees **Decision needed: counsel** [[XW-029]]
13. Brief Legal and the executive sponsor on gaps, risks, and open decisions [[XW-024]] [[XW-027]]
14. Hand everything to Legal as reconciliation exhibits, releasing no more than counsel decides **Decision needed: counsel** [[XW-013]] [[XW-020]]
15. Hold a post-audit review, then keep the documentation, configuration, and reconciliation habits going [[XW-025]]

## Rules

- Only counsel talks to the publisher. Everyone else sends questions to Legal.
- Stay accurate and cooperative, but non-committal. Do not guess, speculate, or admit anything outside what counsel approves.
- Do not delete software or change configuration during a formal audit unless counsel agrees.
- Whether scope, the period reviewed, or settlement can be negotiated is for counsel to decide. **Decision needed: counsel.**
- Never hand over device-level detail beyond what counsel releases.
- A forced audit can be answered three ways: ignore it, accept every claim, or respond with prepared evidence. The prepared response is the aim.

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
- Counting a proof that lacks a detail the agreement requires, such as the buyer's legal name, or an upgrade whose qualifying base has no proof.
- Counting an upgrade and its qualifying base license both: the upgrade uses up the base.
- Reconciling raw installs when the agreement counts named users or devices.
- Treating a subscription's first order as proof without the current term.
- Leaving out proofs older than the audit period. They still back current use.
- Relying on a proof dated after the install without confirming whether it is a true-up or a later purchase.
- Keeping the readiness material in one person's mailbox.

## Who decides

People decide. The asset manager reports. Legal decides every legal point: the claim, the scope, the reply, and what is released. The executive sponsor decides, with counsel, on spend, true-up, and settlement. IT security decides what may be exposed. No tool or agent makes any of these calls.

## Evidence to retain

- The letter, with the date and time it arrived and who passed it to Legal.
- The case file: who was told, and when.
- The proofs of purchase gathered, and the checklist result for each. Keep proofs for as long as the license and any upgrade rights depend on them, and as long as the records schedule requires. **Decision needed: records owner or counsel** for the exact period.
- The discovery output and the hardware audit output, dated.
- The reconciliation per product and version, and the list of gaps.
- Counsel's decisions on scope, time frame, changes, and release, and the approvers.
- What was handed over, to whom, and when.
- The post-audit review notes and the changes that followed.

## Related

- [Governance framework crosswalk](../crosswalk/) (`crosswalk`)
- [ITAM maturity check](../itam-maturity/) (`itam-maturity`)
- [Application rationalization](../rationalization/) (`rationalization`)
- [Hardware lifecycle check](../hardware-lifecycle/) (`hardware-lifecycle`)
- [Stand up a governance program](../program-setup/) (`program-setup`)
