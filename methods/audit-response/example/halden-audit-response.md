# Software Audit Response Check — Halden Logistics (checked_on 2026-09-01)

Inputs: `audit-letter.md`, `proofs-of-purchase.csv`, `audit-installs.csv`, and the expiry dates in `licenses.csv`. This is a readiness briefing for counsel. It is not legal advice, and nothing here has been sent to the publisher.

## Inputs confirmed

The letter is from Brightvale Software Group, dated 2026-08-24, reference BSG-AUD-2026-0417, with a 30-day reply window. Six proofs of purchase cover three products. Four product and version counts were supplied, each with raw installs and the count in the license metric. **Decision needed: counsel** — confirm the letter has reached Legal and set the reply date [[XW-004]].

**Unverified:** the audit clause, the license metrics, and the accepted forms of proof come from Halden's own notes on agreement HAL-MSW-2022, not the signed text. Counsel should check them against the contract before relying on them [[XW-013]].

**Decision needed: counsel** — the agreement was signed with Mosswood Software in 2022, and Brightvale bought the product lines in 2025. Was the agreement assigned to Brightvale, and does it give Brightvale an audit right? [[XW-013]]

## Reconciliation per product and version

Taskmoor and Shapewise are counted per named user, so they reconcile on assigned users, not installs. Cellmate is counted per device.

| product | version | metric | proof quantity | raw installs | count in metric | position | gap |
|---|---|---|---|---|---|---|---|
| Taskmoor Project management (LIC-019) | 5 | named user | 272 | 301 | 289 | short | 17 users without proof |
| Shapewise Diagramming (LIC-020) | 3 | named user | 285 | 297 | 285 | even on paper | 0, but all 285 rest on P-003 and P-004 |
| Cellmate Spreadsheet add-in (LIC-043) | 2 | device | 50 | 50 | 50 | even on paper | 0, but see P-005 |
| Cellmate Spreadsheet add-in (LIC-043) | 3 | device | 34 | 34 | 34 | even on paper | 0, but P-006 is unproven |

Taskmoor v5 is the only product short [[XW-007]]. Counting raw installs would have shown Shapewise short by 12 as well; that gap is users with the product on two devices, not missing licenses. No product is over.

The P-006 upgrade names Cellmate version 1 as its qualifying base, and Halden holds no version 1 proof. Using the 50 version 2 licenses as the base instead would not help: the upgrade uses up its base, so version 2 would fall to 16 licenses against 50 devices. **Decision needed: counsel** — whether downgrade rights let any version 3 license cover version 2 installs [[XW-007]].

All three products show an expiry of 2027-06-30 in `licenses.csv`. Each proof shows the current term (2026-07-01 to 2027-06-30) on a 2026 invoice: the subscription term for Taskmoor and Shapewise, the support term for the perpetual Cellmate licenses [[XW-008]].

## Proofs with problems

| proof | problem | what to fix or explain |
|---|---|---|
| P-003 | Buyer name blank | Find the invoice copy, or the publisher's licensing-portal record, that names the buyer; confirm it is Halden Logistics Inc [[XW-006]] |
| P-004 | No payment proof | Ask the finance contact for the payment record that matches the current-term invoice 6031; check whether the agreement requires one [[XW-006]] |
| P-005 | Proof dated after the install: first order 2022-05-04, first version 2 install 2022-03-01 | Confirm whether it is a true-up or a later purchase (trial use, or an earlier order not on file) before relying on it [[XW-026]] |
| P-006 | Upgrade whose qualifying base, Cellmate version 1, has no proof on file | Find the version 1 purchase, or treat the 34 version 3 devices as unproven [[XW-006]] |

If P-003, P-004, and P-006 cannot be rescued, Shapewise v3 and Cellmate v3 would both move from even to short. **Decision needed: counsel.**

P-003 (2023) and P-005 (2022) predate the 36 months the audit clause covers. On Halden's notes, the period limits the use reviewed, not the age of the proof, so these older proofs still back current use. Keep them in the evidence for counsel to offer. **Decision needed: counsel** — confirm that reading against the signed text.

## Scope questions for counsel

The letter asks for every Halden group company worldwide, every Brightvale product, installation records back to 2019, and a device-level list with user names. Halden's notes limit the review to Halden Logistics Inc, three products, use in the 36 months before the notice, and counts per product and version. The entities, products, period of use, and level of detail all look wider than the agreement. The request for proof of purchase is not a scope problem; proofs of any age help Halden. **Decision needed: counsel** — whether to push back, what to release, and when [[XW-013]] [[XW-007]].

## Do not

Do not contact the publisher. Do not remove Taskmoor installs or change configuration while the audit is open unless counsel agrees [[XW-029]]. Do not release a device list unless counsel decides to.

## Briefing for Legal and the executive sponsor

One product short by 17 named users, three proofs that need repair, one proof dated after its install that needs an explanation, a letter wider than the agreement, and an open question on whether Brightvale holds the audit right at all. The prepared response is within reach if the missing records turn up. **Decision needed:** the executive sponsor, with counsel, on any purchase to close the Taskmoor gap [[XW-027]].

```findings
[
  {"type": "install_shortfall", "id": "LIC-019"},
  {"type": "proof_missing_buyer", "id": "P-003"},
  {"type": "payment_proof_missing", "id": "P-004"},
  {"type": "proof_after_install", "id": "P-005"},
  {"type": "upgrade_without_original", "id": "P-006"},
  {"type": "letter_scope_overreach", "id": "letter-scope"}
]
```
