# Software lifecycle SOP

This SOP describes a practice. It does not replace the tool's own documents, which cover the quarterly review and its roles in full: see **Where the details live**.

## Purpose

Find installed software that is past or near end of life, and flag the rows whose vendor and product appear in the CISA Known Exploited Vulnerabilities catalog, so that a person decides what to replace, upgrade, retire, or accept. Do it without showing an agent a single software name.

## Scope

Applies to any software inventory export that can be saved as a CSV with a name column and a version column. It reports state per item from the tool's bundled data. It does not check licenses, duplicate apps, or device refresh dates, and it does not scan systems for vulnerabilities.

## Roles

- **IT or software asset manager** — runs the check, reads the report, and keeps the dated counts.
- **Asset owner** — for each past-end-of-life or ends-soon item, chooses replace, upgrade, retire, or request risk acceptance.
- **ITAM lead** — settles each item where the dates disagree.
- **A named person** — checks each review-urgently item's version against the KEV entries and sets the priority.
- **Budget holder** — takes the counts into an upgrade budget request.

## Frequency

Quarterly, and before an upgrade budget request. Check the data dates each run: a stale KEV snapshot or end-of-life snapshot is a decision, not a default.

## Steps

1. Export the software inventory as a CSV and confirm its header row with the agent, without sharing any data row [[XW-001]] [[XW-026]]
2. Name an owner for each row where one is known, so each finding has someone to decide [[XW-002]]
3. Keep the inventory and any golden-source, exception, tracking, or support-records files on the person's machine, out of prompts, issues, and commits [[XW-028]]
4. Make the tool copy at the pinned commit, only after the person agrees, and confirm `git rev-parse HEAD` matches the pin, and record the commit [[XW-020]]
5. Run `verify-data`, then read the data dates from the manifest and decide whether to use a newer data release **Decision needed:** the person running the check [[XW-026]]
6. Run `preflight` and fix every item on its "What to fix" list in the export [[XW-026]]
7. Run the check in counts-only mode into a new or empty folder the person names, as of a stated date [[XW-009]]
8. Relay only the summary count lines; the person reads names and IDs in the report themselves [[XW-028]]
9. Report counts by state, names to review, classification, and the data currency, with every limit stated [[XW-009]] [[XW-001]]
10. For each past-end-of-life or ends-soon item, the asset owner chooses replace, upgrade, retire, or request risk acceptance **Decision needed:** the asset owner [[XW-009]] [[XW-010]]
11. For each accepted risk, record it in the risk register with an owner and a review date **Decision needed:** the asset owner [[XW-024]]
12. For each review-urgently item, check the version against the KEV entries and set the priority **Decision needed:** IT security [[XW-024]]
13. Settle each dates-disagree item **Decision needed:** the person running the check [[XW-026]]
14. Pass the counts and owner decisions to the budget holder as inputs to a budget request [[XW-012]]
15. Keep the dated count line, data dates, and decisions, then rerun next quarter with the earlier report passed by path [[XW-020]] [[XW-025]]

## Rules

- The agent never opens the inventory, the optional input files, the tool's output folder, or any file in it.
- Only summary count lines are relayed. A line that lists item IDs is never relayed.
- A KEV match is a vendor and product match. It never means a version is affected.
- Unmatched means no date is claimed. It does not mean safe.
- The agent asks before it makes the tool copy and before it writes to the output folder the person names.
- If `git rev-parse HEAD` does not print the pinned commit, stop.
- Use only this line about security: "Runs locally with no network by default; not independently assessed."

## Questions to ask

- Which column holds the software name and which holds the version?
- Does the export carry an owner, a publisher, a parent, and an end-of-life date?
- Which date should the check run as of, and how many months ahead counts as ends soon?
- How old are the KEV and end-of-life snapshots in the data folder?
- Who owns each item that is past end of life or ends soon?
- Does the person hold support records, such as an extended-support contract, that belong beside the vendor's dates?

## Mistakes to avoid

- Pasting the inventory, or a report section the person did not choose to share, into a chat.
- Relaying a line with item IDs. They are a hash of publisher, name, and version, and someone holding a guess can confirm it.
- Reading Unmatched as safe, or a KEV match as exposure.
- Running the check into a folder that already holds files.
- Reporting a stale data snapshot as current.
- Treating a support record as a license position or as audit preparation.
- Reading the bundle-member count as the number of parts with a parent in the inventory. Those are different figures, and only the full report holds the second.

## Who decides

People decide. The agent relays counts. The asset owner decides replace, upgrade, retire, or accept. IT security sets priority on KEV items. The ITAM lead settles dates that disagree. The budget holder decides spend. No tool or agent makes any of these calls.

## Evidence to retain

- The dated count line the agent relayed, with the data dates.
- The tool release and commit used.
- The owner's decision for each past-end-of-life or ends-soon item, with the approver and date.
- The risk-register entry for each accepted risk.
- The report files, kept by the person outside the agent's reach and for as long as the records schedule requires. **Decision needed: records owner** for the exact period.

## Where the details live

The tool's own documents at the pinned commit hold the full usage, report schema, assistant setup, quarterly review, and checklist: `README.md`, `docs/usage.md`, `docs/report-schema.md`, `docs/assistant-setup.md`, `docs/sop.md`, and `docs/checklist.md` in the tool folder. They are not copied here.

## Related

- [Governance framework crosswalk](../crosswalk/) (`crosswalk`)
- [Hardware lifecycle check](../hardware-lifecycle/) (`hardware-lifecycle`)
- [Application rationalization](../rationalization/) (`rationalization`)
- [Software audit response check](../audit-response/) (`audit-response`)
- [ITAM maturity check](../itam-maturity/) (`itam-maturity`)
