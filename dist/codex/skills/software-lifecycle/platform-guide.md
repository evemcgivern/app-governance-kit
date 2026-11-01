# Platform guide: Software lifecycle check

This method runs a standalone tool on the person's own machine. No platform table or field is named here, because none was confirmed against a source for this method. Where a source would be needed, it says **Not found.**

## Where the inventory export comes from

The tool reads a CSV with a name column and a version column. For exports it knows, it offers `--profile flexera`, `--profile servicenow-mbs`, and `--profile rapid7`. **Unverified:** no one has run any of these profiles on a real export. For any other export, map the columns with `--columns FILE`; the tool ships `templates/columns.example.json` as a pattern. Which report or table in a given platform produces the right columns: **Not found.**

## Running the tool, by assistant

- **Claude Code and Codex:** run the commands on the person's machine, next to the inventory.
- **Microsoft Copilot:** cannot run local tools. The person runs each command themselves and pastes back only the summary count lines. Never paste the inventory, a report section, or a line that lists item IDs into Copilot.
- **Claude app and ChatGPT:** not supported by this method. Running it there would mean uploading the inventory to a remote sandbox.

## Optional counts-only server

The tool also ships an optional counts-only server for desktop chat apps, and a Claude Desktop package that is unsigned. See [docs/mcp-setup.md](https://github.com/evemcgivern/software-lifecycle/blob/main/docs/mcp-setup.md) at the pinned commit. The tool's docs say each was tested once on one Mac. **Unverified:** anything beyond that. This method runs the command line, not the server.

## What the tool does not replace

The tool reports state from its bundled data. It does not decide what to replace, what risk to accept, or whether a KEV match affects a version. Those are the owners' calls.

## Sources checked

Nothing was fetched for this guide. The tool facts come from the software-lifecycle tool's own documents at the pinned commit, v0.7.0, `1ebc996e52b728507a4113aee6c67ea0e208a9e7`, as summarized in the skill this method was adapted from.
