# Copilot test: Application governance router

1. Open the app-governance agent (or the chat prompt) in Microsoft Copilot.
2. Say: "Our auditors want to know where we stand on software licenses next quarter."
3. Attach `demo-estate/licenses.csv` and `demo-estate/apps.csv` when asked.

**Pass** if the response:
- Chooses `rationalization` (license position) and gives a reason.
- Names the data it needs before analyzing.
- Marks at least one **Decision needed:** and does not decide it.
- Offers `itam-maturity` or `access-review` as a follow-up without running it.
- Does not claim to be a governance platform or legal advice.
- Ends with a fenced `findings` block.

Record the result (date, pass/fail, notes; no work data) in `copilot-results.md`.
