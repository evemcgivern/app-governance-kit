# ITAM maturity check SOP

## Purpose

Give the organization an honest, evidence-backed picture of how mature its IT asset management practice is across nine process areas, so gaps get named and funded rather than assumed away.

## Scope

Applies to the full software and hardware estate in scope for IT asset management, across every business unit and asset type covered by the asset management policy.

## Roles

- **ITAM manager**: runs the assessment, collects evidence, and drafts the score table and 90-day plan.
- **Process owners**: answer the questions for their area and supply the evidence.
- **Sponsor**: confirms the three named gaps, approves owners and budget for the 90-day plan, and signs off the filed assessment.

## Frequency

A baseline assessment when the practice starts, then a full re-check every year. Re-run sooner if a major change hits the estate (a merger, a new business unit, or a platform migration).

## Steps

1. Agree scope with the sponsor: which estates, business units, and asset types the assessment covers [[XW-003]]
2. Collect answers and one piece of evidence per process area from the process owners, one area at a time [[XW-025]]
3. Challenge each stated score against its evidence; lower the score and explain why wherever the evidence falls short, using the evidence tests and common scoring mistakes below [[XW-025]]
4. Check that license counts are backed by proofs of purchase kept as long as the records schedule requires, using `sam-toolkit/proof-of-purchase-check.csv`; lower the score where proofs are missing [[XW-006]] [[XW-007]]
5. Check that an acquisition gate is in use and no purchase bypasses it [[XW-009]] [[XW-027]]
6. Check that invoices are reviewed against the contract before payment [[XW-012]] [[XW-013]]
7. Check that an audit response plan exists and was tested, for example by a dry run [[XW-004]] [[XW-020]]
8. Map each of the nine areas to its crosswalk rows so the assessment ties back to the frameworks it draws on [[XW-003]]
9. Name the three lowest-scoring areas as the gaps; where scores tie, break the tie by business risk and record the reasoning [[XW-025]]
10. Draft a 90-day plan for each gap: one owner role, three concrete actions, and the evidence that will prove progress [[XW-004]]
11. Take the named owners and budget to the sponsor for confirmation before the plan starts [[XW-004]]
12. File the dated assessment so next year's re-check has a baseline to compare against [[XW-020]]

## Evidence tests for the challenge step

Match the evidence to the score it can support:

- A document supports a 3: it shows the practice is defined.
- A dated review of that document, or of the practice, supports a 4: it shows the practice is checked.
- A change made after that review supports a 5: it shows the practice improves.

Apply these tests where they fit the area:

- **Governance, policy.** Accountability is set by role; each role has a current named holder. The policy also states its scope, defines its terms, says what happens when someone does not follow it, and has a review cycle. Missing parts cap the score.
- **Governance, communication plan.** The plan names the audience, the channel, how often people are told, and how the team checks that they understood. A plan with no check of understanding is a broadcast, so score it lower.
- **Lifecycle, disposal.** For software and applications, the evidence shows data removed or kept as the records schedule says, and access removed. For devices, add a wipe or destruction certificate. An item is not closed without this.
- **Reporting, measures.** Each measure is tracked against a stated purpose. A number nobody uses for a decision does not count.

## Common scoring mistakes

- Scoring a form as a process. A blank template or an approval form shows the practice is planned, not that anyone uses it.
- Scoring from self-report with no evidence. Lower the score and mark it **Unverified:**.
- Scoring a policy nobody was told about. A policy that has not reached the people it governs supports a lower score.

## KPA lens

Some readers think in IAITAM's 12 Key Process Areas (KPAs): Acquisition Management, Asset Identification Management, Communication and Education Management, Compliance Management, Disposal Management, Documentation Management, Financial Management, Legislation Management, Policy Management, Program Management, Project Management, and Vendor Management. This table shows which KPAs each of the nine areas draws on most. It is a reading aid only.

| Area | KPAs it draws on |
|---|---|
| governance | Policy, Program, Communication and Education |
| inventory | Asset Identification |
| entitlement | Compliance, Documentation |
| lifecycle | Acquisition, Asset Identification, Disposal |
| vendor | Vendor, Acquisition |
| data-quality | Documentation, Asset Identification |
| security | Compliance, Legislation |
| cost | Financial |
| reporting | Program, Project |

The security pairing is a weak fit: no KPA covers access control, so score security on its own question. The KPA names belong to IAITAM, and this kit has no affiliation with IAITAM. They are not ISO/IEC 19770-1 or COBIT BAI09 clauses, and this table is not a crosswalk. Use the crosswalk for clause citations.

## Evidence to retain

- The dated score table with the evidence cited for each area.
- The proof-of-purchase check, acquisition gate use, invoice review records, and audit response plan test cited for the four practices.
- The three named gaps and the tie-break reasoning, where used.
- The 90-day plan, including the sponsor's confirmation of owners and budget.
- The prior year's assessment, kept alongside the current one for comparison.

## Related

- [**Governance framework crosswalk**](../crosswalk/) (`crosswalk`): supplies the framework rows each maturity area maps to.
- [**Application rationalization**](../rationalization/) (`rationalization`): takes over an application flagged by a low lifecycle or entitlement score to decide keep, consolidate, or retire.
- [**AI system intake and risk tiering**](../ai-intake/) (`ai-intake`): extends this assessment's inventory and lifecycle questions to AI systems entering the estate.
- [**Access review pack**](../access-review/) (`access-review`): runs the access checks that back up the security area's score.
- [**Stand up a governance program**](../program-setup/) (`program-setup`): stands up the policy and sponsor role this assessment's governance area checks for.
