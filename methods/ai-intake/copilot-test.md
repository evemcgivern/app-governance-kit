# Copilot test: AI system intake and risk tiering

1. Open the AI intake agent (or the chat prompt) in Microsoft Copilot.
2. Attach `demo-estate/ai-systems.csv`.
3. Send it.

**Pass** if the response:
- Tiers AI-004 (HR: ranks and shortlists job applicants) as high-risk, naming employment as the reason.
- Does not tier the other systems high-risk.
- Names Legal content last reviewed: 2026-09 and recommends legal review for the high-risk result.
- Ends with a fenced `findings` block.

Record the result (date, pass/fail, notes; no work data) in `copilot-results.md`.
