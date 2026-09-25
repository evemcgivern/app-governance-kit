# Copilot test: Application rationalization

1. Open the rationalization agent (or the chat prompt) in Microsoft Copilot.
2. Attach `demo-estate/apps.csv` and `demo-estate/licenses.csv`.
3. Send it.

**Pass** if the response:
- Reports all 5 duplicate pairs.
- Reports both expired licenses, LIC-017 and LIC-044.
- Assigns a TIME decision to every app with a one-line reason.
- Ends with a fenced `findings` block.

Record the result (date, pass/fail, notes; no work data) in `copilot-results.md`.
