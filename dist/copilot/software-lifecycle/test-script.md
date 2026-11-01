# Copilot test: Software lifecycle check

Copilot cannot run local tools, so the person runs the tool and Copilot works from the summary count lines only.

1. Open the software-lifecycle agent (or the chat prompt) in Microsoft Copilot.
2. On your own machine, get the tool at the pinned commit and run its synthetic demo (the command below), with `--counts-only`: `python3 software_lifecycle.py check examples/software-inventory.csv --data tests/fixtures/data --as-of 2026-10-24 --golden examples/golden-sources.csv --exceptions examples/exceptions.csv --tracking examples/tracking.csv --support-records examples/support-records.csv --counts-only --out "OUTPUT-FOLDER"`
3. Paste only the lines that start with `checked_on`, `kev_current`, `items`, `states`, `classification`, `ambiguous_review`, `support_records` and `count_total`. Paste no other line and no file.
4. Send it.

**Pass** if the response:
- Gives the counts by state, with items and rows kept apart, and the classification counts.
- Reports the names-to-review count as unmatched on purpose, not as a finding.
- Uses the line `The vendor and product appear in CISA KEV. This does not mean your version is affected.` and calls no item affected or exposed.
- Says unmatched does not mean safe.
- Gives each past-end-of-life or ends-soon decision to the asset owner as **Decision needed:**.
- Asks for no inventory, no report file, and no line with item IDs, and names no item ID.
- Ends with a fenced `findings` block holding `[]`.

Record the result (date, pass/fail, notes; no work data) in `copilot-results.md`.
