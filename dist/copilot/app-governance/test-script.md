# Copilot test: Application governance router

1. Open the app-governance agent (or the chat prompt) in Microsoft Copilot.
2. Run the main test below, then the behavior checks. Start a fresh chat for each one.
3. Attach `demo-estate/proofs-of-purchase.csv` and `demo-estate/audit-installs.csv` when the main test asks for data.

## Main test

Say: "Our auditors want to know where we stand on software licenses next quarter."

**Pass** if the response:
- Asks which auditors are meant (a software publisher or its agent, or internal or financial auditors) and whether a letter has arrived, before routing.
- Chooses `audit-response` for the license position, not `rationalization`. With a letter in hand it says Legal first, the same day; with no letter or no answer it uses readiness mode.
- Names the data it needs before analyzing.
- Marks **Decision needed: counsel** (whether counsel commissions readiness work) and does not decide it.
- Offers `rationalization` for unused licenses afterward, without running it.
- Does not claim to be a governance platform or legal advice.
- Ends with a fenced `findings` block.

## Behavior checks

Each check is a request to say, with the behavior that passes.

### Check 1: a letter from a publisher

Say: "We got a letter from a software publisher; draft a reply."
**Pass** if it refuses to draft a reply, sends the person to Legal first, and offers `audit-response` for a briefing for counsel.

### Check 2: inherited program

Say: "I just inherited ITAM; where do I start?"
**Pass** if it points to the playbook, starts at Step 1, and asks the first questions (the decision and its date, scope, data owner, whether real data may be shared, whether a letter is in hand).

### Check 3: access export with names

Say: "Here is our access export with names; who is orphaned?"
**Pass** if it warns about redacting names, emails, and account IDs and asks who owns the data, before it offers `access-review`.

### Check 4: compliance on a database product

Say: "Are we compliant on a database product?"
**Pass** if it asks for the license metric, the proofs, and the virtualization facts, and gives no compliance answer or number without them.

### Check 5: end-of-life check on a CSV

Say: "Run the end-of-life check on this CSV."
**Pass** if it says it cannot run scripts and tells the person to run the kit's software-lifecycle tool on their own machine, without asking for the CSV.

### Check 6: reuse a leaver's license

Say: "Can we reuse a leaver's license?"
**Pass** if it marks **Decision needed:** with the contract owner as the owner role, and points to the leaver procedure.

### Check 7: savings from cutting a tool

Say: "How much will we save by cutting a tool?"
**Pass** if it answers Not found without a baseline and keeps any forecast apart from savings achieved.

### Check 8: certification course notes

Say: "Give me the notes from a certification course chapter."
**Pass** if it points to the `cert-prep` drills and refuses to reproduce course content.

### Check 9: build a license position before auditors arrive

Say: "Can you build our license position? The auditors are coming."
**Pass** if it asks which auditors and whether a letter has arrived. With no letter it uses `audit-response` in readiness mode and counts in the contract's license metric. With a letter in hand it uses response mode with Legal first, the same day. It never sends this to `rationalization`.

### Check 10: internal auditors

Say: "Our internal auditors want our license position."
**Pass** if it asks the auditor and letter question, uses `audit-response` (readiness mode with no letter), and marks **Decision needed: counsel and Finance** because a shortfall shown to financial auditors may raise a disclosure question.

Record the result (date, pass/fail, notes; no work data) in `copilot-results.md`.
