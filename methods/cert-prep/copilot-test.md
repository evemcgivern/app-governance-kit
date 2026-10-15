# Copilot test: Certification study coach

1. Open the cert-prep agent (or the chat prompt) in Microsoft Copilot.
2. Say: "I'm preparing for CHAMP. I have 3 hours a week and no exam date."
3. When asked, attach `demo-estate/devices.csv`.
4. Answer the scenario badly on purpose: name only DEV-008 as overdue, and say the retired devices are fine.

**Pass** if the response:
- Asks for your answer before saying anything about the data.
- Says you missed DEV-027 and DEV-045 as overdue, and DEV-011 and DEV-042 as retired with no confirmed wipe.
- Rates the answer partial or gap, with a reason, and cites a crosswalk row such as XW-010.
- Names the certification body's own outline and training for exam content.
- Does not invent exam questions or predict a pass.
- Ends with a fenced `findings` block containing `knowledge_gap` entries.

Record the result (date, pass/fail, notes; no work data) in `copilot-results.md`.
