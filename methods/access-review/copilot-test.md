# Copilot test: Access review pack

1. Open the access-review agent (or the chat prompt) in Microsoft Copilot.
2. Attach `demo-estate/accounts.csv`, `demo-estate/employees.csv`, and `demo-estate/apps.csv`.
3. Send it.

**Pass** if the response:
- Flags ACC-019, ACC-063, and ACC-104 as orphaned.
- Lists a recommended action for each exception found.
- Reviews the most sensitive applications first and says so.
- Ends with a fenced `findings` block.

Record the result (date, pass/fail, notes; no work data) in `copilot-results.md`.
