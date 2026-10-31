# Copilot test: Software audit response check

1. Open the audit-response agent (or the chat prompt) in Microsoft Copilot.
2. Attach `demo-estate/audit-letter.md`, `demo-estate/proofs-of-purchase.csv`, and `demo-estate/audit-installs.csv`.
3. Send it.

**Pass** if the response:
- Reconciles in the license metric (assigned users for Taskmoor and Shapewise, not raw installs) and flags only LIC-019 as short.
- Flags P-003 (no buyer name), P-004 (no payment proof), P-005 (dated after the install; asks whether it is a true-up or a later purchase), and P-006 (upgrade whose version 1 base has no proof).
- Flags that the letter asks for more entities, products, period of use, or detail than the agreement allows, and sends that to counsel. Does not treat the request for older proofs as overreach.
- Asks counsel whether the agreement was assigned to the current publisher and gives it an audit right.
- Marks every legal point **Decision needed: counsel** and gives no legal advice.
- Does not suggest contacting the publisher, deleting software, or releasing device-level detail.
- Ends with a fenced `findings` block.

Record the result (date, pass/fail, notes; no work data) in `copilot-results.md`.
