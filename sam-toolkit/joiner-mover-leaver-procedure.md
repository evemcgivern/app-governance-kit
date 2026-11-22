# Joiner, mover, and leaver procedure

A short procedure for what happens to software and licenses when a person joins, changes role, or leaves. It matches access to the job, returns licenses to the pool where the contract allows, and leaves a record an auditor can follow.

Clause references are to ISO/IEC 19770-1:2017 (paraphrased) and to the shared crosswalk (`XW-` rows). This procedure doesn't interpret contracts or give legal advice. Where it says have the contract owner confirm, the contract owner decides.

**Owner:** ______________________  **Approver:** ______________________  **Date:** ___________

## Roles

- **HR:** tells ITAM about each joiner, mover, and leaver, with the date it takes effect. ITAM waits for the HR notice. [[XW-004]]
- **Manager:** states what the person needs, and confirms each access a mover keeps.
- **ITAM:** acts on the notice, records the result, and returns reclaimed licenses to the pool.
- **Application owner:** removes or changes access in their application.
- **Contract owner:** confirms whether a license may be reused. Have the contract owner confirm before you reassign anything.

## Triggers from HR

Agree with HR, in writing, that each of these starts a notice to ITAM. Settle the lead time and the form (a ticket or a list). [[XW-017]]

| Event | HR sends | When |
| --- | --- | --- |
| Joiner | Name, role, department, manager, start date | Before the start date |
| Mover | Name, old and new role and department, new manager, effective date | Before the effective date |
| Leaver | Name, last day, whether the person is a contractor or an employee | As soon as the date is known, and again on the last day |

A mass hire or a layoff sends many notices at once. Treat it as an event that starts extra work, as the playbook says.

## What happens on each event

### Joiner

1. Compare the role with the approved software standard. Give the person what the standard lists for the role. [[XW-015]]
2. Anything outside the standard follows the acquisition path, with an entry in `authorization-log.csv`. [[XW-009]]
3. Record each assigned license against the person or device in the asset record.
4. Check whether an unused license can be reassigned before you buy a new one. Check the contract first (see the caution below).

### Mover

1. Compare the new role with the standard. List what the person gets and what the person no longer needs.
2. Ask the manager to confirm each access the person keeps. Access the old role needed and the new role doesn't should be removed, not left to expire.
3. Reclaim licenses the person no longer needs, using the steps below.
4. Record the change and the date in the asset record.

### Leaver

1. On the last day, disable access in every application the person used. Use the sign-in logs and the account list in `data-sources-guide.md` to find them all, not only the ones IT knows about. [[XW-017]]
2. List every license assigned to the person and every device the person returned.
3. Reclaim licenses using the steps below.
4. Check shared accounts and any account the person owned for other users. Reassign the owner.
5. Record the leaver and the date, and keep the notice with the case file.
6. Once a month, compare the HR leaver list with the sign-in logs. Any leaver with an active account is a finding to fix and to log in `internal-check-log.csv`.

## Reclaim steps

Do these in order for each license a person held.

1. **Read the contract term.** Find how the license is assigned: to a named user, to a device, or to a pool. Look for any limit on reassigning it, and for any waiting period.
2. **Have the contract owner confirm** whether the license may be moved to another person or device. Do not reuse a license on a guess. A device-tied license may stay with the device. A named-user license may not be reassignable within a set period, or at all. **Decision needed:** contract owner, and counsel where the wording is unclear.
3. **If it may be reused,** remove it from the old holder, return it to the pool, and record the date in `license-position.csv`.
4. **If it may not be reused,** record it as ended or as tied to the device or the contract term. It still counts against what you own until the term ends.
5. **Check the renewal.** If the pool now holds more than the team needs, use the date in `renewal-calendar.csv` to reduce at the next notice deadline. [[XW-008]]
6. **Record the reclaim** in `savings-report.csv` only after finance confirms the spend stopped. A license returned to the pool and then reissued saves nothing; it avoids a purchase. [[XW-012]]

## Caution: check reassignment rights first

Some contracts tie a license to a device or to one named user, and some set conditions on moving it. Moving a license without that right can put you out of compliance. Before you reclaim and reassign any license, read the clause, and have the contract owner confirm. Record the answer in `contract-terms-check.csv` so the next person doesn't have to ask again.

## Link to retirement

A leaver's device and the software on it go through `retirement-signoff-checklist.md` when the device is retired. The checklist asks HR to confirm that no one still depends on the asset (R6), and asks whether licenses were released or recorded as ended (R9 and R10). This procedure produces the evidence for those items: the notice, the reclaim record, and the contract-owner confirmation.

## Evidence to retain

- The HR notice for each event, with its date.
- The entry showing access changed or removed, with the date.
- The reclaim record in `license-position.csv`, and the contract-owner confirmation where a license was reassigned.
- The monthly comparison of leavers with sign-in logs, and the findings from it.

## Decision

| Decision | Owner | Approver | Date |
| --- | --- | --- | --- |
| Procedure adopted, with HR agreeing to send each notice | | | |

Source: ISO/IEC 19770-1:2017 clauses 7.6.3, 8.3 and 8.4, and the shared crosswalk. Paraphrased; this isn't a substitute for the standard.
