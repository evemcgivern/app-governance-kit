# Application rationalization SOP

## Purpose

Give the organization an evidence-backed TIME (Tolerate, Invest, Migrate, Eliminate) decision for every application in the portfolio, so duplicate spend and expired licenses get found and acted on rather than carried forward another year.

## Scope

Applies to every application in the software inventory in scope for portfolio management, across every business unit and category covered by the asset management policy.

## Roles

- **Portfolio manager**: runs the rationalization, pulls the inventory, scores each app, and drafts the TIME table and savings summary.
- **App owners**: confirm their app's cost, users, and data held, and respond to duplicate and eliminate findings for their apps.
- **Finance partner**: checks the stated savings range and confirms budget impact.
- **Architecture**: reviews duplicate pairs and Migrate decisions for technical dependencies before they're approved.

## Frequency

A full rationalization every year, plus a lighter pass before each budget cycle. Re-run sooner after a merger or acquisition adds a new estate to reconcile.

## Steps

1. Pull the inventory with owner, category, cost, and user count for every app; list gaps as **Unverified:** [[XW-001]] [[XW-002]]
2. Chase missing owners or costs before scoring starts [[XW-026]]
3. Identify duplicate applications by category and function, reporting each pair once [[XW-011]]
4. Check licenses against the `checked_on` date for expiry and over-buying [[XW-007]] [[XW-008]]
5. Score each app for business value and technical fit, stating the scoring used [[XW-011]]
6. Assign Tolerate, Invest, Migrate, or Eliminate with reasons; for duplicate pairs, recommend which app to keep [[XW-011]]
7. State savings as a range, not a promise, and have the finance partner check it [[XW-012]]
8. Check vendor contract terms with architecture before any eliminate decision is acted on [[XW-013]]
9. Raise a retirement plan for each eliminate decision [[XW-009]] [[XW-010]]
10. Identify the data held by each retiring or migrating app and agree its disposition (archive, migrate, or delete, with a retention period) with the data owner [[XW-010]] [[XW-028]]
11. Run every new purchase request through the acquisition gate: already owned, redeployable, or a duplicate of an app on the inventory. Use `sam-toolkit/acquisition-gate-checklist.md` [[XW-009]] [[XW-011]]
12. Verify each invoice against the contract and purchase order before it is paid, and log every mismatch in `sam-toolkit/invoice-verification.csv` [[XW-012]] [[XW-013]]
13. Report savings with the evidence behind each figure, and include adverse trends such as rising invoice errors or reclaimed licenses requested again, in `sam-toolkit/savings-report.csv` [[XW-012]]
14. Record the decisions and approvers before the rationalization is filed [[XW-020]]

## Renewal readiness

Run this alongside step 4 for every license or subscription renewing in the next 180 days. The goal is a recorded decision before the contract commits you, not after.

1. List each renewal in `sam-toolkit/renewal-calendar.csv` with its app, contract end date, notice days, notice deadline, auto-renew flag, annual cost, and a named owner. Count the windows below back from the notice deadline, not the end date. Auto-renewing contracts are the usual trap [[XW-008]] [[XW-013]]
2. Work each renewal through the windows. These are practical suggestions, not a requirement of any standard; shorten or lengthen them to fit the contract: [[XW-008]]
   - 120 to 180 days out: identify the renewal and the apps it affects.
   - 90 to 120 days out: confirm the owner is still right, check the business need still exists, and review usage, entitlement, risk, and any contract changes.
   - 60 to 90 days out: record one decision in the calendar: renew, reduce, or cancel, with the reason (for example consolidate, replace, or retire). **Decision needed:** the app owner's call, with the finance partner's view on cost.
   - 30 to 60 days out: negotiate and sign the renewal, or complete the retirement plan [[XW-012]]
   - After the decision: record the outcome, the cost avoided or realized, and where the evidence is kept.
3. Re-open the review early when something changes: the owner changes, the contract terms or permitted use change, a major upgrade or platform move is planned, the vendor or product is acquired, the organization restructures, or a material risk appears [[XW-008]]
4. Keep one calendar row per renewal, with the decision, reason, owner, approver, and date filled in, and note the cost effect in `sam-toolkit/savings-report.csv` once it is real. A renewal with no owner is a finding, not a default to renew. [[XW-020]]

## Evidence to retain

- The dated inventory used, with gaps flagged.
- The duplicate pairs found and the keep/retire recommendation for each.
- The license check results, including expired and over-entitled licenses.
- The renewal record for each renewal due in the next 180 days: owner, notice deadline, decision, decider, date, and cost effect.
- The TIME table with the scoring and reasoning behind each decision.
- The data disposition agreed for each retiring or migrating app, and who agreed it.
- The acquisition gate result for each new purchase request, the invoice checks with their mismatches, and the savings report with its evidence and adverse trends.
- The finance partner's confirmation of the savings range and architecture's review of duplicate and Migrate decisions.

## Related

- [Governance framework crosswalk](../crosswalk/) (`crosswalk`)
- [ITAM maturity check](../itam-maturity/) (`itam-maturity`)
- [AI system intake and risk tiering](../ai-intake/) (`ai-intake`)
- [Access review pack](../access-review/) (`access-review`)
- [Stand up a governance program](../program-setup/) (`program-setup`)
