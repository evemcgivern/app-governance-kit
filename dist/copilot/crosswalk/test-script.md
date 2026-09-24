# Copilot test: Crosswalk

1. Open the Crosswalk agent (or the chat prompt) in Microsoft Copilot.
2. Paste in control **C2** from `demo-estate/controls.md`:

   > Review user access to applications on a schedule and remove access no longer needed.

3. Send it.

**Pass** if the response:
- Names crosswalk row `XW-016` as the match.
- Cites COBIT `DSS05.04` and ISO 27001 `A.5.18`.
- Ends with a fenced `findings` block.

Record the result (date, pass/fail, notes; no work data) in `copilot-results.md`.
