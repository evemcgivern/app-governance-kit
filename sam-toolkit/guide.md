# SAM toolkit guide

Eight working files to support a software and IT asset management (SAM/ITAM) practice. They are blank templates and checklists. Open the CSV files in Excel, Google Sheets, or any spreadsheet; they are plain text, so nothing is locked. All data in the examples is fictional (the Halden Logistics demo estate).

The files follow ISO/IEC 19770-1:2017. Clause numbers are given so you can trace each file back to the standard. The text is paraphrased and does not replace the standard. No affiliation with or endorsement by ISO or IEC.

## Where to start

1. `tier-self-assessment.md`: find out which tier you are at.
2. `statement-of-applicability.csv`: decide which processes are in scope.
3. `asset-record.csv` and `license-position.csv`: get the data right first (tier 1).
4. `renewal-calendar.csv`, `authorization-log.csv`, `vendor-contract-register.csv`: add the records that keep it right.
5. `audit-and-review-checklist.md`: check the system on a schedule.

## The files

### license-position.csv (clause 8.4)

One row per product. Reconcile what you own against what is in use.

- `entitlements_owned`: the count of licenses you hold, in the vendor's license metric (`license_metric`: user, device, core, and so on).
- `in_use_count`: installs, users or cores in use, in the same metric. Do not mix metrics in one row.
- `position`: `entitlements_owned` minus `in_use_count`. Negative is a shortfall.
- `status`: shortfall, surplus or balanced.
- `evidence_source`, `checked_on`, `reviewer`: where the numbers came from, when, and who checked.

A user count is not always the licensed quantity. Confirm the vendor's metric before acting on a shortfall. See `examples/license-position-example.csv`.

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

These are templates, not a platform. They do not discover installs, read vendor license terms, or tell you what a license permits. Verify license terms against the contract. A governance decision still needs a person to make it.
