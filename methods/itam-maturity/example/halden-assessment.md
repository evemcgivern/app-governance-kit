# ITAM maturity assessment: Halden Logistics (baseline, 2026-09-24)

**Main caveat:** `maturity-answers.csv` gives only a score for each area. There is no evidence column, so every score below is self-reported and **Unverified:**. To test the scores, I checked them against the demo estate files (`apps.csv`, `licenses.csv`, `accounts.csv`, `employees.csv`). I only lowered a score when that data contradicted the question the area actually asks.

## Score table

| Area | Stated | Assessed | Crosswalk (ISO/IEC 19770-1 · COBIT 2019 · ISO 27001) | Reasoning |
|---|---|---|---|---|
| governance | 3 | 3 **Unverified:** | XW-003 (4.3, 5.2 · APO01 · A.5.1), XW-004 (5.3 · APO01 · A.5.2) | No policy was supplied. `council-draft.md` has a scope but no decision rights, quorum or sponsor, which fits 3 at best. |
| inventory | 3 | 3 **Unverified:** | XW-001, XW-005 (8.3 · BAI09.01 · A.5.9) | 60 apps are recorded with every field filled in. No discovery or reconcile date is given. |
| entitlement | 1 | **1** | XW-006/007/008 (8.4 · BAI09.05 · A.5.32) | The data supports this score. Two licences have expired but the apps are still in use (details below). For 41 of 60 apps, recorded users exceed entitlements. |
| lifecycle | 2 | **2** | XW-009 (BAI09.03 · A.5.9), XW-010 (BAI09.03 · A.8.10). No 19770-1 clause is mapped. | The data doesn't contradict this. Apps keep running after their licences lapse, and there's no retirement trail. |
| vendor | 4 | 4 **Unverified:** | XW-013 (8.7 · APO10 · A.5.19, A.5.20) | Renewal dates are on file. No vendor risk ratings are supplied, so I can't confirm the "Measured" level. |
| data-quality | 1 | **1** | XW-026 (8.3 · BAI09.01 · A.5.9) | The data supports this score. Account ACC-104 belongs to EMP-099, who isn't in the employee records. Five categories each have two overlapping products that nobody has reconciled. |
| security | 3 | 3 **Unverified:** | XW-014 (DSS05.04 · A.5.15) | Held at 3, with a serious related finding (see below). |
| cost | 4 | 4 **Unverified:** | XW-012 (APO06) | No budget-versus-actual data was supplied. |
| reporting | 3 | 3 **Unverified:** | XW-025 (9.1–9.3, 10.3 · MEA01 · 9.1, 10.1) | No metrics pack or review action was supplied. |

### Findings that affect scoring
- **Expired licences on apps still in use:**
  - LIC-044 for Payflow (APP-044, confidential data, $83,400 a year) expired on 2025-12-31. It still had a login on 2026-08-21.
  - LIC-017 for Meetrix (APP-017, $49,600 a year, 649 users) expired on 2026-03-31.
  - I count these as evidence for **entitlement**, because renewal tracking is XW-008. So they don't lower **vendor**, where renewal dates are on file.
- **Terminated staff still logging in:**
  - EMP-071 left on 2026-05-15 and logged in on 2026-08-20 (ACC-019).
  - EMP-072 left on 2026-07-02 and logged in on 2026-08-08 to the confidential HR system APP-003 (ACC-063).
  - This is a leaver-removal failure (XW-017), not the pre-go-live access check the security question asks about (XW-014). So I held security at 3.
  - **Decision needed:** should the sponsor rescore security to 2 given this finding? Separately from this assessment, these accounts need immediate action through the access review process.
- **Licence shortfall:** for 41 of 60 apps, recorded users exceed entitlements. **Unverified:** a user count isn't the same as licensed seats or installs, so this points to a problem rather than proving one.

## The three gaps

1. **entitlement (1).** This has the most direct financial and audit exposure. Two lapsed licences cover $133,000 of annual spend, and the licence position on most of the estate is unknown. That creates risk from vendor audits and true-up bills.
2. **data-quality (1).** It ties with entitlement on score. I broke the tie by business risk and put it second: its harm is indirect, but it undermines every other area. You can't fix the licence position or retire apps reliably when records have unknown owners and unreconciled duplicates.
3. **lifecycle (2).** This is the only area at 2, so no tie-break was needed for third place. Apps running past their licences show that nothing currently decides whether an app gets renewed or retired.

## 90-day plan

**Decision needed:** the sponsor must confirm the owner roles and approve a budget for each gap. The roles below are proposals, and I haven't estimated costs.

| Gap | Proposed owner role | Actions (days 0–90) | Evidence of progress |
|---|---|---|---|
| entitlement | Software asset / licence manager | 1. Resolve LIC-017 and LIC-044 within 30 days (renew or shut down). 2. Build a compliance position for the top 10 apps by cost, comparing entitlements to actual installs and seats (XW-007). 3. Set up renewal alerts 90 days before every expiry (XW-008). | A dated compliance position for the top 10 apps, no expired licences on live apps, and a renewal calendar. |
| data-quality | ITAM manager (with the HR data owner) | 1. Set the required fields and a monthly 10-record sample check. 2. Reconcile all accounts against the HR employee records. Fix or remove ACC-104 and any other account with no matching employee. 3. Review the 5 overlapping category pairs and record a keep/merge decision for each. | Sample accuracy rising month on month, zero accounts without a matching employee, and a decision log for the 5 pairs. |
| lifecycle | Application portfolio owner | 1. Document the path from request to approval, renewal and retirement (XW-009). 2. Add a decommissioning checklist covering data removal and access removal (XW-010). 3. Run one real retirement through it, for example a loser from the overlap review. | An approved process document and one retirement with its full audit trail. |

**Decision needed:** before next year's re-check, should process owners be required to supply one piece of evidence per area? Without it, the next assessment will also rest on self-reported scores.

```findings
[
  {"type": "maturity_gap", "id": "entitlement"},
  {"type": "maturity_gap", "id": "data-quality"},
  {"type": "maturity_gap", "id": "lifecycle"}
]
```
