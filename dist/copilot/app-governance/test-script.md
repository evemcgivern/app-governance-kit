# Copilot test: Application governance router

1. Open the app-governance agent (or the chat prompt) in Microsoft Copilot.
2. Run the main test below, then the behavior checks. Start a fresh chat for each one.
3. Attach `demo-estate/licenses.csv` and `demo-estate/apps.csv` when the main test asks for data.

## Main test

Say: "Our auditors want to know where we stand on software licenses next quarter."

**Pass** if the response:
- Asks whether "auditors" means an internal audit or a software publisher's audit, before routing.
- For an internal audit, chooses `rationalization` (license position) and gives a reason. For a publisher's audit, says Legal comes first and offers `audit-response`.
- Names the data it needs before analyzing.
- Marks at least one **Decision needed:** and does not decide it.
- Offers `itam-maturity` or `access-review` as a follow-up without running it.
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

Record the result (date, pass/fail, notes; no work data) in `copilot-results.md`.
