# SAM toolkit guide

Thirteen working files to support a software and IT asset management (SAM/ITAM) practice. They are blank templates and checklists. Open the CSV files in Excel, Google Sheets, or any spreadsheet; they are plain text, so nothing is locked. All data in the examples is fictional (the Halden Logistics demo estate).

The files follow ISO/IEC 19770-1:2017. Most files trace to a clause of the standard; the purchasing and savings files (`invoice-verification.csv`, `savings-report.csv`) trace to crosswalk rows instead. The text is paraphrased and does not replace the standard. No affiliation with or endorsement by ISO or IEC.

## Where to start

1. `tier-self-assessment.md`: find out which tier you are at.
2. `statement-of-applicability.csv`: decide which processes are in scope.
3. `asset-record.csv` and `license-position.csv`: get the data right first (tier 1).
4. `proof-of-purchase-check.csv`: back each entitlement with acceptable proof.
5. `renewal-calendar.csv`, `authorization-log.csv`, `vendor-contract-register.csv`: add the records that keep it right.
6. `contract-terms-check.csv`: list the contract terms to confirm with counsel or the vendor.
7. `acquisition-gate-checklist.md`: stop unplanned purchases at the door.
8. `invoice-verification.csv` and `savings-report.csv`: check invoices before payment, then report what the practice saved.
9. `audit-and-review-checklist.md`: check the system on a schedule.

## The files

### license-position.csv (clause 8.4)

One row per product. Reconcile what you own against what is in use.

- `entitlements_owned`: the count of licenses you hold, in the vendor's license metric (`license_metric`: user, device, core, and so on).
- `in_use_count`: installs, users or cores in use, in the same metric. Do not mix metrics in one row.
- `position`: `entitlements_owned` minus `in_use_count`. Negative is a shortfall.
- `status`: shortfall, surplus or balanced.
- `evidence_source`, `checked_on`, `reviewer`: where the numbers came from, when, and who checked.

A user count is not always the licensed quantity. Confirm the vendor's metric before acting on a shortfall. See `examples/license-position-example.csv`.

### proof-of-purchase-check.csv (clause 8.4, crosswalk XW-006, XW-007, XW-020)

One row per product (per publisher, product and version). This is the evidence behind `entitlements_owned` in `license-position.csv`.

A count of installs is not a position. A license counts only when acceptable proof of purchase backs it. Keep proofs for as long as the license and any upgrade rights depend on them, and as long as your records schedule requires. **Decision needed: records owner or counsel** for the period. A later upgrade is only as good as the original purchase behind it. A certificate of authenticity or a license key alone shows a copy exists, not that you have the right to use it.

- `installs_found`, `count_in_metric`, `proofs_located`, `quantity_proven`: what discovery found, the count in the license metric (assigned users for named-user licenses, devices for device licenses), how many proofs you located, and the quantity those proofs add up to. `term_start`, `term_end`: the current subscription or support term the proof shows.
- `proof_ref`: invoice or purchase order numbers. Separate several with a semicolon.
- `result`: short if `quantity_proven` is below `count_in_metric`, even if equal, over if above.
- `shows_purchase_date`, `shows_full_product_description`, `shows_version`, `shows_quantity`, `shows_vendor`, `shows_buyer_entity`, `shows_price`, `payment_proof_on_file`: yes or no. Answer yes only if every proof you counted shows that item. A "no" means the proof may not count; ask the vendor for a reissue.
- `license_metric`: the unit the contract counts (named users, devices, cores). Reconcile in that metric, not in a raw install count.
- `license_type`: full, upgrade or competitive upgrade. For an upgrade or a competitive upgrade, `upgrade_chain_complete` is yes only when the original qualifying purchase is also on file. Use "not applicable" for a full license.
- `evidence_location`, `checked_on`, `reviewer`: where an auditor can find the proofs, when you checked, and who checked.

Downgrade rights may let a newer license cover older installs; confirm with counsel. For a subscription, the proof must show the current term. The agreement defines what counts as acceptable proof; licensing-portal and reseller records can count. If `quantity_proven` differs from `entitlements_owned`, use the proven number until the gap is explained. See `examples/proof-of-purchase-check-example.csv`.

### contract-terms-check.csv (clause 8.4, crosswalk XW-013)

One row per contract term or definition you checked. Link each row to its contract through `contract_id`, which matches `contract_ref` in `vendor-contract-register.csv`, and copy `notice_deadline` from `renewal-calendar.csv` into `renewal_notice_deadline` so a term that changes the renewal is not missed.

Read license terms as permissions: anything not clearly granted is treated as not permitted until counsel or the vendor confirms. This file does not interpret contracts or give legal advice. It finds what to ask counsel.

- `term_or_definition`, `clause_ref`: what you read and where, for example the definition of "device" or the transfer clause.
- `clear`: yes, no or maybe. Put what is unclear in `what_is_unclear`.
- `which_document_governs`: record which document claims precedence and where it says so. Send any conflict between documents to counsel. **Decision needed: counsel**.
- `counsel_needed`: yes or no. `owner` and `checked_on` say who is following it up and when.

### acquisition-gate-checklist.md (crosswalk XW-009, XW-011, XW-013, XW-021)

A checklist every software request passes before any purchase. It asks whether you already own it, whether it is installed and unused, which path it takes, whether it duplicates an existing product (see the rationalization method), and whether it uses AI or handles organizational data (see the AI intake method). It ends with a check of spend outside procurement, such as expense cards and department budgets. The rule is: no purchase outside this path.

### invoice-verification.csv (crosswalk XW-012, XW-013)

One row per invoice line check. Compare the invoice to the contract and purchase order before payment, not after, when a correction is cheaper.

- Begin the back-review with your biggest suppliers and the invoices that are hardest to read.
- `payment_terms_match_contract`, `quantity_invoiced` against `quantity_agreed`, and `unit_price` against `negotiated_unit_price`: the common places where an invoice drifts from the agreement.
- `line_math_ok`, `subtotal_ok`, `tax`, `shipping`, `total`: check the arithmetic and the add-ons.
- `matched`: yes or no. If no, say why in `discrepancy` and record `amount_at_issue` and `resolved_on`.

Chart discrepancy categories over time. The pattern is what supports a change in practice to management.

### savings-report.csv (crosswalk XW-012)

One row per savings type per period: invoice errors recovered, purchases avoided by redeploying, contract terms, negotiation, maintenance cancelled and unused licenses reclaimed.

- `baseline_cost`, `amount_saved`, `percent_saved`: the cost before and what you saved. Leave `percent_saved` blank if there is no baseline.
- `evidence_ref`: the record that supports the number, such as a row in `invoice-verification.csv`.
- `adverse_trend_note`: report bad news too, such as rising error rates or reclaimed licenses being requested again. A report with only wins is not trusted.
- `reported_to`, `reported_on`: who saw it and when.

### renewal-calendar.csv (clause 8.4, crosswalk XW-008)

One row per license or contract.

- `notice_deadline`: `contract_end` minus `notice_days`. This is the date that matters, not the end date.
- `auto_renews`: yes or no.
- `in_use_last_90_days`: usage before you decide, so you do not renew shelfware.
- `decision`: renew, reduce or cancel. Record `reason`, `decision_owner`, `approver` and `decided_on`.

### asset-record.csv (clause 8.3, 7.6.2)

The core data record. One row per asset (software, hardware, or an IT service).

- `owner`: the named person accountable. `custodian`: who looks after it day to day.
- `authorized`: yes or no, with `authorization_ref` pointing to the entry in the authorization log.
- `status`: for example requested, in use, retiring, retired. Add `retired_on` when it leaves use.
- `source_system` and `last_verified_on`: where the data came from and when it was last checked.

The standard requires accurate data for every core asset through its life and a record of whether each asset is authorized.

### authorization-log.csv (clause 7.6.3)

Record who made each authorization, when, and why. Record who carried it out, when, and against which authorization.

- `authorization_type`: financial, security, operational or managerial.
- `scope`: the organization, a unit, a group of people, one asset or a class of assets.
- `valid_until`: leave blank if there is no end date.
- An example of an execution is installing authorized software; put the ticket or change reference in `execution_ref`.

### statement-of-applicability.csv (clause 6.2.2)

Pre-filled with the 15 processes in Annex A. For each, say whether it is in scope and why. The standard asks for a justification for every inclusion and exclusion.

- Change, core data, license and security management are marked "always included". The standard says their objectives are already part of clause 8.
- `tier`: fill in from Annex B, Figure B.2 of your copy of the standard.
- `evidence_location`: where an auditor can see the process working.

### vendor-contract-register.csv (clause 8.7, crosswalk XW-013)

One row per supplier contract that affects ITAM.

- `activities_outsourced`: the scope and boundaries of what the supplier does.
- `mixed_responsibilities`: where you and the supplier share ownership of devices, servers, software or data, say so. This is where the risk sits.
- `risk_assessed_on`, `risk_rating`, `risk_owner`: the standard requires you to assess the risk of outsourcing.
- `knowledge_sharing_arrangement`: how information is shared with the supplier.
- `performance_reviewed_on` and `contract_terms_verified_on`: monitor performance, and check compliance with terms beyond licensing.

### tier-self-assessment.md (Annex A and B)

A yes/partly/no check across three tiers, with a place for evidence.

### audit-and-review-checklist.md (clauses 9.2, 9.3, 10.1)

A plan-and-record checklist for the internal audit, and a pack list for the management review.

## Limits

These are templates, not a platform. They do not discover installs, read vendor license terms, or tell you what a license permits. They do not interpret contracts or give legal advice; verify license terms against the contract and ask counsel where a term is unclear. A proof-of-purchase check shows what you can document, not what a vendor will accept in an audit. A governance decision still needs a person to make it.
