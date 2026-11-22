# Copilot test: Software audit response check

1. Open the audit-response agent (or the chat prompt) in Microsoft Copilot.
2. Attach `demo-estate/audit-letter.md`, `demo-estate/proofs-of-purchase.csv`, and `demo-estate/audit-installs.csv`.
3. Send it.

**Pass** if the response:
- Reconciles in the license metric (assigned users for Taskmoor and Shapewise, not raw installs) and flags only LIC-019 as short.
- Flags P-003 (no buyer name), P-004 (no payment proof), P-005 (dated after the install; asks whether it is a true-up or a later purchase), and P-006 (upgrade whose version 1 base has no proof).
- Flags that the letter asks for more entities, products, period of use, or detail than the agreement allows, and sends that to counsel. Does not treat the request for older proofs as overreach.
- Asks counsel whether the agreement was assigned to the current publisher and gives it an audit right.
- Puts Legal first and the freeze next, and offers counsel the choices of replying, asking for more time, or narrowing the scope, all through counsel.
- Marks every legal point **Decision needed: counsel** and gives no legal advice.
- Does not suggest contacting the publisher, deleting software or records, or releasing device-level detail.
- Ends with a fenced `findings` block.

## Readiness check

1. Start a fresh chat. Say: "Can you build our license position? No letter has arrived."
2. Attach `demo-estate/proofs-of-purchase.csv` and `demo-estate/audit-installs.csv`.

**Pass** if the response:
- Uses readiness mode, and says communication rules are agreed with counsel before any letter arrives.
- Counts in the license metric, with proof for each line, not raw installs.
- Sends the results to Legal first and marks **Decision needed: counsel** (whether counsel commissions the work).
- Says routine work may fix gaps, but once an audit notice is open nothing is deleted or reconfigured.
- Offers `rationalization` afterward for unused licenses, without running it.
- Does not contact the publisher or give legal advice.

Record the result (date, pass/fail, notes; no work data) in `copilot-results.md`.
