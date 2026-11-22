# Risk assessment guide

A short method for finding, rating, treating, and recording ITAM risks, so that each one has an owner and a decision. Use it once when you set the program's scope and baseline (playbook steps 4 and 5), and again at each review. The record is `risk-register.csv`.

Clause references are to ISO/IEC 19770-1:2017 (paraphrased) and to the shared crosswalk (`XW-` rows). The standard's requirements on risk sit in clause 6.1. This guide does not give legal advice; where a risk turns on a contract term, have counsel review it.

**Owner:** ______________________  **Date:** ___________

## The five steps

### 1. Identify

List what could go wrong with an asset or a process in scope. Look at each source of trouble in turn. [[XW-024]]

- Records: missing proof of purchase, out-of-date inventory, no named owner.
- Contracts: renewals that pass unnoticed, terms nobody has read, transfer or reassignment limits.
- People: leavers who keep access, knowledge held by one person.
- Technology: software past its support date, installs no one authorized.
- Suppliers: an audit letter, a change of ownership at a publisher, a price increase.

For each risk, write one line that says what could happen, one line for the cause, and one for the consequence. Name the asset or process it touches.

### 2. Assess

Rate each risk on two scales, using the three words below. These are your own scales, not taken from a standard, so adjust the wording to what matters at your organization.

| Rating | Likelihood | Impact |
| --- | --- | --- |
| low | Not expected in the next year | A nuisance that staff can absorb |
| medium | Could happen in the next year | A cost, delay, or finding that needs a decision |
| high | Likely, or has happened before | A serious cost, a legal exposure, or harm to confidential data |

Rate on what you can show. If you have no evidence either way, say so in the action and rate it medium until you do. Work first on the risks that are high on both scales.

### 3. Treat

Pick one treatment for each risk. [[XW-024]]

| Treatment | Meaning |
| --- | --- |
| accept | Do nothing more now, and record why |
| reduce | Add a control or take an action that lowers the rating |
| transfer | Move part of the cost to another party, for example through a contract term. Have counsel review it. |
| avoid | Stop the activity or retire the asset that causes the risk |

Write the action in plain words, name who does it, and give a date.

### 4. Record

Enter each risk in `risk-register.csv`, one row per risk. Give each an id, an owner, a status (open, in progress, closed, or accepted), and a review date. The owner is the person who answers for the risk, not necessarily the person who does the work. Keep closed risks in the file so the history shows.

### 5. Review

Review the register at each quarterly check and after any event that changes the picture: an audit letter, a merger, a move to cloud, a vendor ending support. Re-rate each open risk. Close a risk only when its action is done and a check shows the rating has dropped. Record reviews that change nothing too. [[XW-025]]

## Who accepts what is left

After treatment, some risk remains. The owner of the risk accepts what remains, in writing, with a date. If the remaining risk is high on both scales, the sponsor accepts it or sends it back for more treatment. Do not accept a risk on someone else's behalf. **Decision needed:** the risk owner, and the sponsor for any risk that stays high.

## What to bring to a review

- `risk-register.csv`, with every open row rated and dated.
- The evidence behind each rating: a row from `proof-of-purchase-check.csv`, `documentation-gaps-log.csv`, or `internal-check-log.csv`.
- The risks that came up since the last review, and the ones that closed.

## Decision

| Decision | Owner | Approver | Date |
| --- | --- | --- | --- |
| Remaining risks accepted, with an owner for each | | | |

Source: ISO/IEC 19770-1:2017 clause 6.1, and the shared crosswalk. Paraphrased; this is not a substitute for the standard.
