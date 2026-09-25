# Copilot test: Hardware lifecycle check

1. Open the hardware-lifecycle agent (or the chat prompt) in Microsoft Copilot.
2. Attach `demo-estate/devices.csv`.
3. Send it.

**Pass** if the response:
- Flags DEV-008, DEV-027, and DEV-045 as overdue for refresh.
- Flags DEV-011 and DEV-042 as retired with no confirmed data wipe.
- Recommends a replacement, upgrade, or extension for each overdue device, and a wipe or destruction method for each unwiped one.
- States a total replacement cost as a range, not a promise.
- Ends with a fenced `findings` block.

Record the result (date, pass/fail, notes; no work data) in `copilot-results.md`.
