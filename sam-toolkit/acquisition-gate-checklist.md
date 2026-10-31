# Acquisition gate checklist

A short checklist a software request passes before anything is bought. Complete one copy per request and keep it with the purchase record. A request that fails a question waits until the answer is fixed or a named person accepts the exception in writing.

Clause references are to ISO/IEC 19770-1:2017 (paraphrased) and to the shared crosswalk (`XW-` rows). Verify license terms against the contract; this checklist does not interpret them.

**Request:** ______________________  **Requester:** ______________________  **Date:** ___________

## No purchase outside this path

Every software purchase goes through this gate, whatever the amount and whoever pays. The gate applies to purchases made on expense cards, by departments from their own budgets, and as add-ons inside a larger order. A purchase made outside the gate is recorded as an exception and reviewed (see the last part of this list).

## Part 1: Do we already have it?

| # | Question | Result | Evidence |
| --- | --- | --- | --- |
| G1 | Is the product, or an earlier version with upgrade rights, already owned? Check `license-position.csv` and the proofs on file. [[XW-006]] [[XW-007]] | | |
| G2 | If owned, is there a surplus that can be redeployed to this requester instead of buying? [[XW-007]] | | |
| G3 | Is it already installed somewhere and unused? Check discovery data for installs with no recent use. [[XW-005]] | | |
| G4 | Does an existing product already do this job? If so, send the request through the rationalization method before buying a second one. [[XW-011]] | | |

## Part 2: Which path does it take?

| # | Question | Result | Evidence |
| --- | --- | --- | --- |
| G5 | Is it on the standard list, deployed through the standard image? A standard request follows the standard path. | | |
| G6 | If it is not standard, has it gone to exception review, with the reason recorded? Non-standard requests do not skip review. [[XW-009]] | | |
| G7 | Does it use AI features, or will it handle organizational data? If yes, send it through the AI intake method before approval. [[XW-021]] [[XW-022]] [[XW-028]] | | |

## Part 3: Buy it well

| # | Question | Result | Evidence |
| --- | --- | --- | --- |
| G8 | Does the vendor have a volume threshold, bundle or enterprise agreement already in a contract that covers this? Check `vendor-contract-register.csv`. [[XW-013]] | | |
| G9 | Are the license metric and the terms that matter (use rights, transfer, upgrade) confirmed against the contract? Use `contract-terms-check.csv` where anything is unclear. | | |
| G10 | Is there a named owner for the product after purchase? [[XW-002]] | | |
| G11 | Who approves, and is that person different from the requester? The approval goes in `authorization-log.csv`. (7.6.3) [[XW-019]] | | |
| G12 | Is the proof of purchase filed where `proof-of-purchase-check.csv` expects to find it, and is the entitlement recorded in `license-position.csv`? (8.4) [[XW-006]] [[XW-020]] | | |

## Part 4: Spend outside procurement

Run this part on a schedule (monthly or quarterly), not per request.

| # | Check | Result | Evidence |
| --- | --- | --- | --- |
| S1 | Expense card and reimbursement lines reviewed for software and subscription purchases. | | |
| S2 | Department budgets and cost-center reports reviewed for software lines not seen at the gate. [[XW-012]] | | |
| S3 | Each item found is entered in the asset record and the license position, or stopped. | | |
| S4 | Each item found has its path-gap noted, so the requester knows how to use the gate next time. | | |

## Decision

| Decision | Owner | Approver | Date |
| --- | --- | --- | --- |
| Buy / redeploy / use existing / decline / exception | | | |

Source: ISO/IEC 19770-1:2017 clauses 7.6.3 and 8.4, and Annex A. Paraphrased; this is not a substitute for the standard.
