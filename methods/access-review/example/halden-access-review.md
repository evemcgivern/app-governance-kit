# Access review: Halden Logistics, application accounts

**Inputs:** `accounts.csv` (120 accounts, 72 distinct people, 60 apps), `employees.csv` (80 HR records), `apps.csv` (data sensitivity). I checked every account in a script, not a sample.

**Unverified: gaps in the inputs**
- **No export date.** Last logins run from 2026-08-01 to 2026-08-28. I tested dormancy against today (2026-09-24), so the 90-day cutoff is 2026-06-26.
- **No application owner column.** I can't say who approves each exception.
- **No segregation-of-duties rules.** Step 6 (XW-019) was not done.
- **The export may be incomplete.** `apps.csv` shows far more users per app than the export holds. For example, APP-044 Payflow lists 748 users but the export has 2 accounts. The export has only 1 or 2 accounts per app, so it looks like a sample or partial extract. Check that it is the full population before relying on it.
- **Only one HR field for leaving.** `employees.csv` has status and a termination date. It doesn't show leave of absence or role changes.

## Sensitivity order (step 2)

I reviewed the 10 **confidential** apps first: APP-002, 003, 004, 006, 009, 011, 027, 044, 045 and 047, which hold 20 accounts. The other 50 internal apps came after. Two of the three orphaned accounts are on confidential apps.

## Exceptions table

| Account | Person | App (sensitivity) | Role | Last login | Issue | Recommended action |
|---|---|---|---|---|---|---|
| **ACC-063** | EMP-072 | APP-003 Staffhub HRIS (confidential) | user | 2026-08-08 | **Orphaned: leaver.** Terminated 2026-07-02, and **the account was used 37 days after leaving** | Remove, and investigate the login after termination |
| **ACC-104** | EMP-099 | APP-044 Payflow AP automation (confidential) | user | 2026-08-21 | **Orphaned: no matching person.** EMP-099 isn't in HR (IDs stop at EMP-080) | Investigate, then remove |
| **ACC-019** | EMP-071 | APP-019 Taskmoor Project mgmt (internal) | user | 2026-08-20 | **Orphaned: leaver.** Terminated 2026-05-15, and **the account was used 97 days after leaving** | Remove, and investigate the login after termination |
| ACC-017 | EMP-017 | APP-017 Meetrix (internal) | admin | 2026-08-18 | Privileged role | Owner to re-approve |
| ACC-034 | EMP-034 | APP-034 Ratecheck (internal) | admin | 2026-08-07 | Privileged role | Owner to re-approve |
| ACC-051 | EMP-051 | APP-051 Safeyard (internal) | admin | 2026-08-24 | Privileged role | Owner to re-approve |
| ACC-068 | EMP-068 | APP-008 Clausebase (internal) | admin | 2026-08-13 | Privileged role | Owner to re-approve |
| ACC-085 | EMP-015 | APP-025 Pulseboard (internal) | admin | 2026-08-02 | Privileged role | Owner to re-approve |
| ACC-102 | EMP-032 | APP-042 Pipewright ETL (internal) | admin | 2026-08-19 | Privileged role | Owner to re-approve |
| ACC-119 | EMP-049 | APP-059 Clickpath (internal) | admin | 2026-08-08 | Privileged role | Owner to re-approve |

**How each conclusion was reached**
- **Orphaned accounts (3).** I matched `employee_id` to the HR `id`. Two accounts belong to people HR marks as terminated (EMP-071 and EMP-072). One points to an ID that isn't in HR at all (EMP-099). The other 117 accounts match active employees.
- **Logins after termination.** Both leaver accounts were used after the leave date. This is more serious than access that was left in place: someone, or a shared or stolen login, was using these accounts. Treat both as possible security incidents, not just clean-up.
- **ACC-104.** The ID could be a typo, a service account, or a contractor who isn't in the HR feed. I can't tell which from the data. It has live access (last login 2026-08-21) to accounts payable, a confidential payments system.
- **Privileged roles (7).** These are all accounts with role `admin`. None is on a confidential app, and none belongs to a leaver.
- **Dormant accounts (0).** The oldest login is 2026-08-01, well after the 2026-06-26 cutoff. This stays zero for any export date up to 2026-10-30, but the result is **Unverified** until the export date is confirmed.
- **Segregation of duties: not tested.** No rules were supplied. One person holds two admin roles: EMP-015 on Pulseboard (ACC-085) and EMP-032 on Pipewright ETL (ACC-102). Each person has only one admin role, so no conflict is visible.

**Decisions needed**
- **Decision needed:** The APP-003 Staffhub owner decides whether to remove ACC-063, and whether to open a security incident for the login on 2026-08-08.
- **Decision needed:** The APP-044 Payflow owner decides whether to remove ACC-104 once it's clear who owns it. They should also decide whether to suspend it while that is investigated.
- **Decision needed:** The APP-019 Taskmoor owner decides whether to remove ACC-019, and whether to open a security incident for the login on 2026-08-20.
- **Decision needed:** Each owner of APP-017, 034, 051, 008, 025, 042 and 059 re-approves or revokes their admin account (ACC-017, 034, 051, 068, 085, 102 and 119).
- **Decision needed:** The review coordinator decides whether to supply SoD rules and re-run step 6, or record it as out of scope for this cycle.

## Evidence summary

| Item | Result |
|---|---|
| Accounts reviewed | 120 of 120 in the export (**Unverified:** whether the export is the full population) |
| People matched to HR | 71 of 72 distinct IDs match an HR record, and 69 of those are active |
| Confidential apps reviewed first | 10 apps, 20 accounts |
| Orphaned accounts | 3: two leavers (both used after termination) and one unknown person |
| Privileged accounts for re-approval | 7 |
| Dormant accounts (90 days) | 0 (**Unverified:** export date) |
| SoD conflicts | Not tested, because no rules were supplied |
| Owner decisions collected | 0 of 10, all pending |

## Auditor memo

**Scope.** User accounts for Halden Logistics' 60 business applications, from `accounts.csv`, checked against the HR list in `employees.csv`. The export date wasn't supplied, and dormancy was measured against 2026-09-24 (**Unverified**).

**Population.** 120 accounts held by 72 person IDs, checked against 80 HR records. The per-app user counts in `apps.csv` are much higher than the export. Completeness of the export must be confirmed before this memo can support a statement that covers every user.

**Method.** Apps were ordered by data sensitivity, and the confidential ones were reviewed first (XW-028). Every account was matched to an HR record (XW-015). Accounts belonging to leavers or to people not in HR were flagged as orphaned (XW-017). Admin roles were flagged for owner re-approval (XW-018). Accounts with no login in the 90 days before the export date were checked for dormancy (XW-016). The whole population was tested; nothing was sampled.

**Exceptions.** Three orphaned accounts:
- ACC-063 on the Staffhub HRIS (confidential). A leaver's account, used 37 days after termination.
- ACC-104 on Payflow AP (confidential). The person doesn't exist in HR.
- ACC-019 on Taskmoor (internal). A leaver's account, used 97 days after termination.

Seven admin accounts are awaiting re-approval. No dormant accounts were found.

The two logins after termination suggest leaver access removal isn't working. This is a control failure, not just housekeeping.

**Actions.** Owners decide on removal and re-approval, and the IAM team confirms each removal in the system of record. Security should be told about both logins after termination. SoD testing is pending until rules are supplied. None of the actions is complete yet.

**Clauses covered**
- **XW-016**, periodic access review (COBIT DSS05.04, ISO/IEC 27001 A.5.18). Partly met: the review has been done, but owner decisions and the export date are still outstanding.
- **XW-017**, leaver access removal (DSS05.04, A.5.18, A.6.5). Exceptions were found and raised. The control itself failed for two leavers.
- **XW-018**, privileged access (DSS05.04, A.8.2). Seven admin accounts were identified and sent for re-approval.
- **Supporting:** XW-015 (provisioning match), XW-028 (review ordered by sensitivity) and XW-020 (evidence retention, once the decisions are filed).
- **Not covered:** XW-019 (segregation of duties), because no rules were supplied.

```findings
[
  {"type": "orphaned_account", "id": "ACC-019"},
  {"type": "orphaned_account", "id": "ACC-063"},
  {"type": "orphaned_account", "id": "ACC-104"}
]
```
