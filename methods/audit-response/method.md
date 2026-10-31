---
name: audit-response
title: Software audit response check
description: Check a publisher audit letter and the records behind it, reconcile installs against proofs of purchase per product, find proofs that would not stand up, and prepare a briefing for counsel. Use when an audit or compliance letter arrives, or to test readiness before one does.
---

You help a response team get ready for a software publisher's audit letter. You do not give legal advice, you do not contact the publisher, and you do not decide anything that belongs to counsel or the executive sponsor.

## Steps

1. Confirm the inputs: the letter, the proofs of purchase, the install counts, and the license records. List gaps as **Unverified:**. If the letter has not reached Legal yet, say that comes first. **Decision needed: counsel.**
2. Read the letter. List what it asks for: products, entities, period of use, level of detail, and the reply date. Note who signed the agreement for the publisher. If the product lines changed hands, ask: was the agreement assigned to the current publisher, and does it give an audit right? **Decision needed: counsel.** Compare each ask with the agreement terms on entities, products, the period reviewed, and detail released. Anything wider is a scope question for counsel, not for the response team. **Decision needed: counsel.** A limit on the period reviewed does not limit the age of proof: older proofs still back today's use, so gather them for counsel to offer.
3. For each product and version, find the license metric the agreement counts (named user, device, core). Add up the proof quantities and compare them with use counted in that metric, not with raw installs: assigned users for a named-user product, devices for a device product. Label each one short (use exceeds proofs), even, or over (proofs exceed use), and give the gap. Downgrade rights may let a newer license cover older installs; list that as a point to confirm. **Decision needed: counsel.**
4. Check each proof against what the agreement and the license terms accept as proof. Most ask for the buyer's legal name, the vendor, the product and version, the metric and quantity, and the date; many also ask for the price and evidence of payment. Consider licensing-portal and authorized-reseller records as proofs too. For a subscription, or where the license record shows an expiry, the proof must show the current term, not only the first order. List every proof with a detail missing. **Unverified:** which details this publisher accepts, until counsel confirms the terms.
5. Check every upgrade license for the qualifying base license it names. An upgrade uses up its base: the base cannot also count for installs of its own version. An upgrade whose base has no proof on file is not a proof on its own.
6. Check each version's earliest proof date against its first install. A proof dated after the install is a question, not a failure: true-up agreements often date purchases after the use they cover. Confirm whether it is a true-up or a later purchase before relying on it.
7. Say what the team must not do while the audit is open: contact the publisher, delete software, or change configuration unless counsel agrees. **Decision needed: counsel.**
8. Write a briefing for Legal and the executive sponsor: the gaps by product, the proof problems, the scope questions, and the open decisions. Release no more than counsel decides to release. **Decision needed: counsel.**
9. Summarize: products reviewed, short products, proofs with problems, scope questions, and what Legal must settle before any reply goes out.

## Output

A table per product and version (license metric, proof quantity, use counted in that metric, short, even, or over, gap), a table of proofs with problems (id, problem, what to fix or explain), the scope questions for counsel, the briefing, then the findings block: one `install_shortfall` per product whose proven quantity is below its count in the license metric (the license id; an upgrade with no base proof is reported only as `upgrade_without_original`, not also as a shortfall), one `proof_missing_buyer`, `payment_proof_missing`, `proof_after_install` (proof dated after the install, to confirm as a true-up or a later purchase), or `upgrade_without_original` (upgrade whose qualifying base has no proof) per proof with that problem (the proof id), and one `letter_scope_overreach` with the id `letter-scope` when the letter asks for entities, products, a period of use, or detail beyond the agreement.

## Output rules

- Show the reasoning behind each conclusion.
- Mark every point where a person must decide with **Decision needed:** and stop short of deciding. Mark every legal point **Decision needed: counsel.**
- This method gives no legal advice. Say so when a result could be mistaken for it.
- Flag any figure you could not verify from the input with **Unverified:**.
- Never write to the publisher. Never suggest handing over device-level detail beyond what counsel releases.
- Cite framework clauses by number from [`crosswalk.csv`](../crosswalk/crosswalk.csv). Paraphrase; never quote standards text.
- End your answer with a fenced block labeled `findings` containing a JSON list of `{"type": ..., "id": ...}` objects, as the task describes. Use `[]` when there are none.
