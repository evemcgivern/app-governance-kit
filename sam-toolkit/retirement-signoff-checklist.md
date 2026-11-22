# Retirement sign-off checklist

A checklist to complete before a software application or a device is closed out as retired. Complete one copy per asset, or per batch of identical assets, and keep it with the asset record. Retirement is not done until every function below has signed, or a named person has accepted a recorded exception.

Clause references are to ISO/IEC 19770-1:2017 (paraphrased) and to the shared crosswalk (`XW-` rows). This checklist does not interpret contracts or give legal advice; ask counsel where a term is unclear.

**Asset:** ______________________  **Owner:** ______________________  **Date:** ___________

## Part 1: Is it ready to retire?

| # | Question | Result | Evidence |
| --- | --- | --- | --- |
| R1 | Has the owner confirmed in writing that the business need has ended, or has been replaced? [[XW-010]] | | |
| R2 | Is there a retirement decision on record, with the decider and date? Use `authorization-log.csv`. [[XW-010]] [[XW-020]] | | |
| R3 | If a contract covers it, has the notice deadline been checked, so you are not paying for it after it is retired? Check `renewal-calendar.csv`. [[XW-008]] [[XW-013]] | | |

## Part 2: Sign-offs

Each function confirms its own part. One person can hold more than one role in a small organization, but the question still needs its own answer.

| # | Function | What they confirm | Signed by | Date |
| --- | --- | --- | --- | --- |
| R4 | IT | Access is removed, the asset is out of service, and dependent systems are not affected. [[XW-010]] | | |
| R5 | Finance | The asset is off the books, any write-down is recorded, and the final cost is known. [[XW-012]] | | |
| R6 | HR | No current employee still depends on it, and any leaver records are updated where the asset held them. | | |
| R7 | Procurement | Contract end, notice, and any return, buy-back, or termination terms are handled. [[XW-013]] | | |
| R8 | Legal | Retention duties, holds, and contract exit terms are met, and no open audit or dispute depends on the asset. **Decision needed:** counsel, where in doubt. [[XW-020]] | | |

## Part 3: Evidence

| # | Question | Result | Evidence |
| --- | --- | --- | --- |
| R9 | For software: were the licenses it used released back to the pool, or recorded as ended, in `license-position.csv`? Check the contract's reassignment rights first, because some licenses cannot move to another user or device. Have the contract owner confirm. [[XW-007]] | | |
| R10 | For hardware: were any software licenses tied to the device reclaimed before it left? Check the contract's reassignment rights first, because device-tied licenses may not move. Have the contract owner confirm. [[XW-007]] [[XW-010]] | | |
| R11 | Was data wiped or destroyed by a method suited to the asset, with a certificate kept? Encryption alone is not wiping. [[XW-010]] | | |
| R12 | Was the data it held archived, migrated, or deleted as agreed with the data owner, with a retention period? [[XW-028]] | | |
| R13 | Is the asset record updated to retired, with `retired_on` filled in? Use `asset-record.csv`. (8.3) [[XW-001]] | | |
| R14 | Is the final cost recorded, so the savings or ROI can be reported later? Use `savings-report.csv`. [[XW-012]] | | |
| R15 | Are the wipe certificate and sign-offs filed where an auditor can find them, for as long as the records schedule requires? [[XW-020]] | | |

## Decision

| Decision | Owner | Approver | Date |
| --- | --- | --- | --- |
| Close out, hold open, or accept an exception | | | |

Source: ISO/IEC 19770-1:2017 clauses 7.6.3, 8.3 and 8.4, and the shared crosswalk. Paraphrased; this is not a substitute for the standard.
