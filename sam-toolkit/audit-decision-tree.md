# Audit decision tree

A printable outline for deciding what to do about software audits, and in what order. Each node asks one question, lists the answers, and says who acts, which kit file to open, and what to watch for. The answers link to the next node, so you can click through it on screen or follow the node ids on paper.

The tree covers the quiet case (nothing has happened), readiness work (someone is asking for a license position), and the live case (a letter has arrived). It follows the roles and records habits in clause 5.3 and clause 7.6.3, the license position work in clause 8.4, and the contract habits in clause 8.7. [[XW-004]] [[XW-007]] [[XW-013]] [[XW-020]]

The tree flags legal and contract points and leaves them with counsel and the contract owner. It gives no legal advice.

## How to use it

1. Start at [node 1](#node-1).
2. Answer the question in plain terms. If you are not sure, take the answer that mentions not being sure.
3. Follow the link for your answer. Each answer names the next node by id, so the path survives a printout.
4. At each node, check four things: who acts, which kit file to open, the label, and any flag.
5. Keep a dated note of each node you passed and the answer you gave. In a live case, that note goes in the case file.

## Legend

Each node carries one label.

- **Kit rule.** The kit takes a firm position and the position holds in every case.
- **Judgment.** A person weighs the facts. The kit offers a default.
- **Counsel decision.** Legal decides. The kit only asks the question.

A node can also carry a flag. A notice is open from a Yes at node 1 until counsel closes it at D5.

- **DN** means Decision needed. The names after it say who decides.
- **FREEZE** means nothing in scope is deleted, reconfigured, reassigned, or bought. Once a notice is open, keep every record as it stands: proofs, contracts, discovery output, emails and notes. Do not delete, edit or back-date any of them. Fix an error by adding a dated note, never by overwriting. **Decision needed: counsel**, for any exception.
- **ORIG** means originals stay in house. The team works from copies.

## Jump to a node

- Opening questions: [1](#node-1), [2](#node-2), [3](#node-3)
- Routine: [A1](#node-a1), [A2](#node-a2)
- Readiness: [B1](#node-b1), [B2](#node-b2), [B3](#node-b3), [B4](#node-b4), [B5](#node-b5)
- A notice is open: [C1](#node-c1), [C2](#node-c2), [C3](#node-c3), [C4](#node-c4), [C5](#node-c5), [C6](#node-c6), [C7](#node-c7), [C8](#node-c8), [C9](#node-c9), [C10](#node-c10), [C11](#node-c11)
- Findings and close: [D1](#node-d1), [D2](#node-d2), [D3](#node-d3), [D4](#node-d4), [D5](#node-d5), [E1](#node-e1)
- Internal or financial auditors: [F1](#node-f1)

## Opening questions

### Node 1

**Has a publisher, its agent, or a trade body sent anything about licenses?** Count a letter, an email, a license review, or a request for a self-declaration or self-audit.

- Yes, or not sure: go to [node C1](#node-c1).
- No: go to [node 2](#node-2).
- Who acts: anyone who receives mail or support requests passes it on; Legal takes it from there.
- Open: `audit-response-roles.csv`, to see who receives letters.
- Label: kit rule.

### Node 2

**Is someone asking you for a license position?**

- A publisher or its agent, even with no letter: go to [node C1](#node-c1).
- Your own leaders, or a self-check you planned: go to [node B1](#node-b1).
- Internal or financial auditors: go to [node F1](#node-f1).
- No one: go to [node 3](#node-3).
- If you cannot tell which kind of auditors are asking, ask them. If no answer comes and no publisher has been in touch, go to [node B1](#node-b1).
- Who acts: the asset manager asks; Legal hears the answer.
- Open: no kit file yet.
- Label: kit rule.

### Node 3

**Do you see any warning sign?** Examples: a merger or acquisition, a large renewal coming up, a licensing or ownership change at a publisher, a move to cloud or virtual machines, or mass hiring or layoffs.

- Yes: go to [node B1](#node-b1).
- No: go to [node A1](#node-a1).
- Who acts: the asset manager, with the executive sponsor.
- Open: `operating-calendar.md`, which lists the events that start extra work.
- Label: judgment.

## Routine

### Node A1

**Nothing is open. Keep the routine running.** Refresh license positions each quarter. Keep the renewal calendar and the gaps log current. Review the audit roster each year. Give staff an internal channel for raising license concerns.

- At a renewal: go to [node A2](#node-a2).
- Anything else happens (a letter, a request, a warning sign): go back to [node 1](#node-1).
- Who acts: the asset manager.
- Open: `license-position.csv`, `renewal-calendar.csv`, `documentation-gaps-log.csv`, `audit-response-roles.csv`, and `operating-calendar.md`.
- Label: kit rule.

### Node A2

**At renewal, what does the contract say about audits?** Look at who may audit and how often, whether third-party auditors are allowed, whether reviews are scheduled, and whether a true-up window exists. Decide what to ask for in the next term.

- Counsel and the contract owner settle what to ask for. Then go back to [node A1](#node-a1).
- Who acts: the contract owner and Procurement bring the terms; Legal decides what to negotiate.
- Open: `contract-terms-check.csv`.
- Label: counsel decision.
- Flag: DN (counsel, contract owner).

## Readiness

### Node B1

**Has counsel agreed to readiness work, and to who speaks to the publisher?**

- Yes: go to [node B2](#node-b2).
- No: stop and ask counsel. Do not start the work until the answer is yes.
- Who acts: the asset manager asks; Legal answers.
- Open: `audit-response-roles.csv`, and the `audit-response` method for readiness mode.
- Label: counsel decision.
- Flag: DN (counsel).

### Node B2

**Pick one publisher. What does its contract count?** The unit might be named users, devices, cores, or something else.

- The contract states it clearly: go to [node B3](#node-b3).
- It is unclear: log it in the gaps log and send the question to counsel. Wait for the answer, then go to [node B3](#node-b3).
- Who acts: the asset manager reads; the contract owner confirms.
- Open: `contract-terms-check.csv`.
- Label: judgment.
- Flag: DN (contract owner, counsel).

### Node B3

**Does each entitlement have proof the agreement accepts?** A certificate of authenticity or a product key alone is not proof. It shows a copy exists, not a right to use it.

- Log each gap with an owner, then go to [node B4](#node-b4).
- Who acts: Procurement and the asset manager.
- Open: `proof-of-purchase-check.csv` and `documentation-gaps-log.csv`.
- Label: kit rule.

### Node B4

**Counted in the contract's own unit, is the position short, even, or over?**

- You came from [node F1](#node-f1) (internal or financial auditors asked): send the result back to counsel and Finance, whatever it is. Do not go on to node B5.
- Otherwise, short: go to [node B5](#node-b5).
- Even: go to [node A1](#node-a1).
- Over: offer the `rationalization` method afterward for licenses nobody uses, then go to [node A1](#node-a1).
- Who acts: the asset manager.
- Open: `license-position.csv`.
- Label: kit rule.

### Node B5

**How will you close the gap?** Buy, reclaim (only where the contract allows reassignment), or retire the installs. Use normal change control.

- First answer [node 1](#node-1) again. If a notice has arrived, stop here and follow node 1; the freeze applies.
- If node 1 still says no: close the gap, then go to [node A1](#node-a1).
- Who acts: the asset manager proposes; Finance and the contract owner approve.
- Open: `acquisition-gate-checklist.md`, `retirement-signoff-checklist.md`, and `renewal-calendar.csv`.
- Label: judgment.
- Flag: DN (Finance, contract owner).

## A notice is open

### Node C1

**Does Legal have it today?**

- No: forward it to Legal now. Reply to no one. Note the reply deadline in the case file, then go to [node C2](#node-c2).
- Yes: note the reply deadline in the case file and go to [node C2](#node-c2).
- Who acts: whoever holds the letter; Legal receives it.
- Open: `audit-response-roles.csv`.
- Label: kit rule.

### Node C2

**Freeze.** Do not uninstall, reconfigure, reassign, retire, or buy in-scope licenses. Pause cleanup scripts. Counsel decides any exception, including a routine renewal.

Once a notice is open, keep every record as it stands: proofs, contracts, discovery output, emails and notes. Do not delete, edit or back-date any of them. Fix an error by adding a dated note, never by overwriting. **Decision needed: counsel**, for any exception.

- Go to [node C3](#node-c3).
- Who acts: the asset manager tells every team that touches the in-scope software; Legal sets any exception.
- Open: no kit file yet.
- Label: kit rule.
- Flags: FREEZE; DN (counsel).

### Node C3

**Name the single contact and open the case file.** Counsel is the only voice to the publisher. The asset manager opens a dated case file. Tell the executives who need to know.

- Go to [node C4](#node-c4).
- Who acts: Legal names itself; the asset manager opens the file; Legal and the asset manager brief the sponsor.
- Open: `audit-response-roles.csv`.
- Label: kit rule.

### Node C4

**Does this party hold an audit right, including by assignment? Is the letter's scope wider than the agreement?** Compare the entities, products, period reviewed, and level of detail the letter asks for with what the agreement allows.

- Counsel decides both questions. Write the answers and any scope counsel sets in the case file, then go to [node C5](#node-c5).
- Who acts: Legal, with the contract owner supplying the agreement.
- Open: `contract-terms-check.csv`.
- Label: counsel decision.
- Flag: DN (counsel; the contract owner supplies the terms).

### Node C5

**When is the reply due, and how will counsel answer?** Counsel may reply by the date, ask for more time, or ask to narrow the scope. All three go through counsel.

- Counsel picks one and records the date. Go to [node C6](#node-c6).
- Who acts: Legal.
- Open: no kit file yet.
- Label: counsel decision.
- Flag: DN (counsel).

### Node C6

**Build a quick first position for counsel, before anyone discusses details with the publisher.** A rough count in the contract's unit is enough to tell counsel how exposed you are.

- Go to [node C7](#node-c7).
- Who acts: the asset manager.
- Open: `license-position.csv`.
- Label: judgment.

### Node C7

**Does the auditor want to run its own tool or script in your environment?**

- Yes: IT security reviews the request and counsel decides. Nothing runs until counsel says so. Then go to [node C8](#node-c8).
- No: go to [node C8](#node-c8).
- Who acts: IT security reviews; Legal decides.
- Open: no kit file yet.
- Label: counsel decision.
- Flags: FREEZE; DN (counsel).

### Node C8

**Gather the evidence counsel scoped.** Collect proofs of any age (an old proof can still back current use), contracts, and payment records. Existing discovery reports are fine to use, and scheduled scans may continue. New agents or a wider scope need counsel first. The team works from copies.

- Go to [node C9](#node-c9).
- Who acts: Procurement and the asset manager find proofs; the technical lead supplies discovery output; the finance contact finds payment records.
- Open: `proof-of-purchase-check.csv` and `documentation-gaps-log.csv`.
- Label: kit rule.
- Flag: ORIG.

### Node C9

**Reconcile in the contract's unit, then brief Legal and the sponsor.** Say what is short, even, or over, which proofs have problems, and what is still open.

- Go to [node C10](#node-c10).
- Who acts: the asset manager reconciles; the asset manager and Legal brief the sponsor.
- Open: `license-position.csv` and `proof-of-purchase-check.csv`.
- Label: kit rule.

### Node C10

**What is released, and what is held back?** By default, hold back device lists, raw exports, and internal gap notes. Counsel decides what goes out.

- Counsel decides each release and records it. Go to [node C11](#node-c11).
- Who acts: Legal decides; IT security advises on what the data would expose.
- Open: no kit file yet.
- Label: counsel decision.
- Flag: DN (counsel).

### Node C11

**Meetings and site visits.** Counsel attends. While a notice is open, nobody calls the publisher about license wording.

- Go to [node D1](#node-d1).
- Who acts: Legal.
- Open: no kit file yet.
- Label: counsel decision.
- Flag: DN (counsel).

## Findings and close

### Node D1

**Have findings arrived?**

- Yes: go to [node D2](#node-d2).
- No: keep the freeze. All contact goes through counsel. Go back to [node D1](#node-d1) when counsel hears anything.
- Who acts: Legal receives; the asset manager keeps the case file current.
- Open: no kit file yet.
- Label: kit rule.

### Node D2

**Test each claim.** Ask for every claim itemized. Check the unit counted, downgrade rights, the proofs, and errors in the auditor's data. Give rebuttal evidence to counsel.

- Go to [node D3](#node-d3).
- Who acts: the asset manager tests; Legal decides what to send.
- Open: `proof-of-purchase-check.csv` and `contract-terms-check.csv`.
- Label: judgment.

### Node D3

**True-up, purchase, or settlement?** Ask counsel what a settlement or true-up covers and what it leaves open.

- Counsel, the contract owner, and Finance decide. Go to [node D4](#node-d4).
- Who acts: the executive sponsor with counsel.
- Open: no kit file yet.
- Label: counsel decision.
- Flag: DN (counsel, contract owner, Finance).

### Node D4

**Put any duties that follow a settlement on the calendar.** Examples: a later report to the publisher or a follow-up review. Counsel names them.

- Go to [node D5](#node-d5).
- Who acts: Legal names the duties; the asset manager calendars them.
- Open: `renewal-calendar.csv`, which holds dated obligations for contracts.
- Label: counsel decision.
- Flag: DN (counsel).

### Node D5

**Has counsel closed the audit and lifted the freeze, in writing?**

- Yes: go to [node E1](#node-e1).
- No: go back to [node D1](#node-d1). The freeze stays.
- Who acts: Legal.
- Open: no kit file yet.
- Label: counsel decision.
- Flag: DN (counsel).

### Node E1

**Learn from it.** Hold a lessons-learned review. Send fixes through change control. Update the roles, the renewal calendar, the gaps log, and the contract terms. Plan for a follow-up review.

- Then go to [node A1](#node-a1).
- Who acts: the asset manager, with the executive sponsor.
- Open: `audit-response-roles.csv`, `renewal-calendar.csv`, `documentation-gaps-log.csv`, `contract-terms-check.csv`, and `license-position.csv`.
- Label: kit rule.

## Internal or financial auditors

### Node F1

**Internal or financial auditors have asked for a license position.** Ask which auditors they are and whether the request is part of the financial audit. Tell counsel and Finance before sharing anything. Build the position through nodes B2 to B4. Release only what they approve.

- Counsel and Finance agree: go to [node B2](#node-b2).
- Counsel or Finance does not agree: stop and share nothing.
- Who acts: the asset manager asks; Legal and Finance approve.
- Open: `license-position.csv` and `audit-response-roles.csv`.
- Label: counsel decision.
- Flag: DN (counsel, Finance).

## Not in this tree

Penalty amounts, legal conclusions, and how long records must be kept are for counsel and the records owner. The tree does not answer them.

## Questions for counsel

While this notice is open, should routine disposal under our retention schedule pause for records tied to the audit? If so, which records, and who tells the records owner? **Decision needed: counsel.**

Source: ISO/IEC 19770-1:2017 clauses 5.3, 7.6.3, 8.4 and 8.7, and the shared crosswalk. Paraphrased; this is not a substitute for the standard.
