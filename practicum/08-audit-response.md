# Exercise 08: Audit response — Halden's publisher letter

**Level:** CSAM · **Time:** 45–60 minutes

## Scenario

A software publisher, Brightvale Software Group, has written to Halden Logistics about three product lines it bought in 2025. Halden's general counsel has the letter and has asked the asset manager to find out, before anyone replies, what the records can and cannot prove. You've been handed the letter, the proofs of purchase, and Halden's install counts. Counsel will decide what is said and released. Your job is to find the weak spots.

## Files

- [`demo-estate/audit-letter.md`](../demo-estate/audit-letter.md) — the publisher's letter, with Halden's own notes on its agreement
- [`demo-estate/proofs-of-purchase.csv`](../demo-estate/proofs-of-purchase.csv) — six proofs of purchase for three products, with license metric, current term, and upgrade base, linked to license records
- [`demo-estate/licenses.csv`](../demo-estate/licenses.csv) — the license records and expiry dates the proofs link to
- [`demo-estate/audit-installs.csv`](../demo-estate/audit-installs.csv) — raw installs and the count in the license metric per license and version, with the first install date

## Work through

Use `methods/audit-response/checklist.md` by hand, without AI.

- Reconcile per product and version, not for the estate as a whole, and in the license metric the agreement counts: assigned users for a named-user product, devices for a device product, not raw installs. Add up the proof quantities for each license and version and compare them with `count_in_metric`. Exactly one is short.
- Read every proof for the details it must show. Exactly one has no buyer name and exactly one has no evidence of payment.
- An upgrade uses up the qualifying base license it names, so the base cannot also count for its own version. Exactly one upgrade names a base Halden holds no proof of.
- Compare each version's earliest proof date with its first install date. Exactly one proof is dated after the install; note it as a question to confirm (a true-up or a later purchase), not as a failure.
- Check that each proof shows the current term where `licenses.csv` shows an expiry date. Keep proofs older than the audit period: they still back current use.
- Read the letter against Halden's notes on its agreement: entities, products, period of use, and level of detail. Decide whether the letter asks for more than the agreement allows. Also note who signed the agreement: was it assigned to the current publisher, and does it give an audit right? Both questions go to counsel; you only flag them.

## Hand in

A table per product and version (license metric, proof quantity, count in that metric, short, even, or over), a list of the proofs with problems and what you would do about each, and the scope and audit-right questions for counsel, with no legal conclusion of your own. Then, on the interactive practicum page: mark each product short of proofs, each problem proof, and whether the letter asks for too much.

## Check yourself

Open the [interactive practicum page](../site/practicum.html#audit-response) and enter your findings there — no installs, no command line. "Passed" means every planted problem in the key showed up in your findings, with at most one extra finding the key doesn't recognize; "missed" lists anything real you didn't flag; "extra" lists anything you flagged that isn't in the key. The key is `demo-estate/answer-key.json` in this repo — it's public, so check your own answer before you look at it.

## Reflect

1. Two of the three products show an even count, yet both have proof problems. Why is "the numbers match" not the same as "the proofs hold"?
2. The letter asks for a device-level list. What would you want counsel to decide before anyone prepares one?
3. Removing Taskmoor from the 17 users without proof would make the count look clean. Why does the method say not to, and who can approve it?

## Certification link

This exercise practices responding to a publisher audit with prepared evidence: reconciling use against proofs of purchase in the contract's license metric, and keeping legal decisions with counsel.
