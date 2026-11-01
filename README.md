# app-governance-kit

Version 0.4.0 <!-- x-release-please-version -->

Nine governance methods — portfolio, AI, and access — packaged as skills for
Claude, Codex, and Microsoft Copilot, plus a public reference site and a set
of hands-on practicum exercises for learning the underlying certifications
(CAMP, CSAM, CHAMP, AIGP) by hand before using the tools.

Each method maps to real standards (ISO/IEC 19770, COBIT 2019, ISO/IEC 27001,
ISO/IEC 42001) via a 29-row crosswalk, so every recommendation traces back to
a clause, not just a rule of thumb.

## The nine tools

| Tool | Does |
|---|---|
| `program-setup` | Stand up or review a software/AI governance council — charter, decision rights, intake path. |
| `itam-maturity` | Score IT asset management maturity across nine process areas, with evidence, not self-ratings. |
| `crosswalk` | Map a control or policy statement to ISO/IEC 19770, COBIT 2019, ISO/IEC 27001, and ISO/IEC 42001. |
| `rationalization` | Recommend tolerate/invest/migrate/eliminate per application; find duplicates and license risk. |
| `access-review` | Review user access against HR records; find orphaned, excessive, and privileged accounts. |
| `ai-intake` | Tier a new AI use case for risk (EU AI Act, NIST AI RMF, ISO/IEC 42001) and produce an inventory record. |
| `hardware-lifecycle` | Check a device fleet for overdue refreshes and retired devices missing a confirmed data wipe. |
| `audit-response` | Answer a publisher audit letter: reconcile installs against proofs of purchase, find weak proofs, and brief counsel. |
| `software-lifecycle` | Find installed software past or near end of life, with a CISA KEV needs-review flag, by running an offline tool on your own machine; counts only. |

Each ships to `dist/claude/skills/`, `dist/codex/skills/`, and
`dist/copilot/` in the platform-native shape those tools expect, built from
one shared source under `methods/`.

## Install

Pick your platform, then open its section. Downloads are on the [Tools page](https://evemcgivern.github.io/app-governance-kit/tools.html#install) (one ZIP per platform, or one per tool), or copy from `dist/` after a `git clone`.

| Platform | How | Format |
|---|---|---|
| Claude Code, terminal | Plugin, or copy skills | Plugin, or `claude-skills.zip` / `dist/claude/skills/` |
| Claude Code, desktop app | Plugin | Same plugin as the terminal |
| Claude app (claude.ai, Desktop chat, Cowork) | Upload a skill | One `<tool>-claude.zip` per tool |
| Codex (CLI, IDE extension, desktop app) | Copy skills | `codex-skills.zip` / `dist/codex/skills/` |
| ChatGPT | Upload a skill (work plans), or a project | `<tool>-codex.zip`, or `dist/copilot/<tool>/` files |
| Microsoft 365 Copilot, Copilot Studio | Build an agent | `copilot-agents.zip` / `dist/copilot/<tool>/` |
| Other assistants | Paste a prompt | `dist/copilot/<tool>/chat-prompt.md` |

<details>
<summary><b>Claude Code, terminal</b></summary>

1. Install it: `curl -fsSL https://claude.ai/install.sh | bash` on macOS, Linux, or WSL; `irm https://claude.ai/install.ps1 | iex` in Windows PowerShell; or `brew install --cask claude-code`. Run `claude` once to sign in (needs a Pro, Max, Team, Enterprise, or Console account). [Docs](https://code.claude.com/docs/en/setup).
2. Add the marketplace: `claude plugin marketplace add evemcgivern/agent-skills`.
3. Install the plugin: `claude plugin install app-governance-kit@evemcgivern-skills`. Inside a session, the same steps are `/plugin marketplace add evemcgivern/agent-skills` and `/plugin install app-governance-kit@evemcgivern-skills`.
4. Type `/app-governance-kit:access-review`, or ask for a tool by name.

<details>
<summary>More</summary>

- **What you get:** the nine tools, the `app-governance` router, the `cert-prep` study coach, and `app-governance-agent`. Plugin skills appear as `/app-governance-kit:<skill>`.
- **Without the plugin:** `cp -R dist/claude/skills/* ~/.claude/skills/`, or unzip `claude-skills.zip` into `~/.claude/skills`. For one project only, use that project's `.claude/skills/`. Skills then appear as `/access-review`. For the agent, save [`app-governance-agent.md`](agents/app-governance-agent.md) to `~/.claude/agents`.
- **Update:** `claude plugin update app-governance-kit@evemcgivern-skills`. Auto-update is off by default for marketplaces other than Anthropic's, so run it after each release. For copied skills, copy them again.
- **Check it worked:** `claude plugin list` shows `app-governance-kit@evemcgivern-skills`, and typing `/` lists its skills.
- **Safe trial:** in a clone of this repo, ask for an access review of `demo-estate/accounts.csv`, `demo-estate/employees.csv`, and `demo-estate/apps.csv`. It should flag ACC-019, ACC-063, and ACC-104 as orphaned.
- [Plugin docs](https://code.claude.com/docs/en/discover-plugins).

</details>
</details>

<details>
<summary><b>Claude Code, desktop app</b></summary>

1. Install the Claude desktop app for [macOS, Windows, or Linux](https://code.claude.com/docs/en/desktop), sign in, and open the **Code** tab.
2. Start a **Local** session (not Cloud).
3. Click **+** next to the prompt box, then **Plugins**, then **Add plugin**. The browser lists plugins from marketplaces you have added, so add `evemcgivern/agent-skills` first from the terminal (`claude plugin marketplace add evemcgivern/agent-skills`).
4. Select `app-governance-kit` and choose your user account as the scope.

<details>
<summary>More</summary>

- **What you get:** the same plugin as the terminal. The terminal, the desktop app's local sessions, and the VS Code extension read the same settings, so a user-scope install in one shows up in the others. Local sessions also load skills copied to `~/.claude/skills/`.
- **Cloud sessions:** they don't load plugins installed on your computer.
- **Update:** `claude plugin update app-governance-kit@evemcgivern-skills` in a terminal. **+**, then **Plugins**, then **Manage plugins** enables, disables, or uninstalls it.
- **Check it worked:** type `/` in a local session and look for `/app-governance-kit:access-review`.
- **Safe trial:** open a local session on a clone of this repo and run the access review on the `demo-estate/` files listed under the terminal steps.
- [Desktop docs](https://code.claude.com/docs/en/desktop).

</details>
</details>

<details>
<summary><b>Claude app (claude.ai, Desktop chat, Cowork)</b></summary>

1. Turn on **Code execution and file creation** in Settings, then Capabilities. On Enterprise, an owner first turns on code execution and skills in Organization settings, then Plugins & skills.
2. Download one tool's Claude ZIP, such as `access-review-claude.zip`, from its card on the [Tools page](https://evemcgivern.github.io/app-governance-kit/tools.html). The app takes one skill per ZIP.
3. Go to **Customize**, then **Skills**. Click **+**, then **Create skill**, then **Upload a skill**, and choose the ZIP.
4. In a chat, ask for the tool by name: "Use the access review skill on these files."

<details>
<summary>More</summary>

- **What you get:** one tool per upload. Repeat for each tool you want.
- **Cowork:** the Desktop app's Cowork tab loads the skills turned on for your claude.ai account, so an upload here covers it.
- **Update:** delete the skill (open it, turn it off, then **...**, **Delete**) and upload the new ZIP.
- **Check it worked:** the skill shows in **Customize**, then **Skills**, with its toggle on.
- **Safe trial:** attach `accounts.csv`, `employees.csv`, and `apps.csv` from [`demo-estate/`](demo-estate/) and ask for an access review. It should flag ACC-019, ACC-063, and ACC-104 as orphaned.
- [Help article](https://support.claude.com/en/articles/12512180-using-skills-in-claude).

</details>
</details>

<details>
<summary><b>Codex (CLI, IDE extension, desktop app)</b></summary>

1. Install it: `curl -fsSL https://chatgpt.com/codex/install.sh | sh`, then run `codex` and sign in with ChatGPT. [Docs](https://developers.openai.com/codex/cli). For VS Code, Cursor, or Windsurf, install the [Codex extension](https://developers.openai.com/codex/ide).
2. Add the skills: `cp -R dist/codex/skills/* ~/.agents/skills/`, or unzip `codex-skills.zip` into `~/.agents/skills`. For one repo only, use that repo's `.agents/skills/`.
3. Type `$access-review`, or describe the task and let Codex pick the skill.

<details>
<summary>More</summary>

- **What you get:** the nine tools, the `app-governance` router, and the `cert-prep` study coach.
- **Where they work:** standalone skills work in the Codex CLI, the IDE extension, and the ChatGPT desktop app, where Codex runs. In the desktop app, open **Skills** in the sidebar to see them. [Skills docs](https://developers.openai.com/codex/skills).
- **Update:** copy the new folders over the old ones. Codex picks up changes; if one doesn't appear, restart Codex.
- **Check it worked:** run `/skills` in the CLI or IDE extension and look for `access-review`.
- **Safe trial:** in a clone of this repo, ask for an access review of the three `demo-estate/` files above. It should flag ACC-019, ACC-063, and ACC-104 as orphaned.

</details>
</details>

<details>
<summary><b>ChatGPT</b></summary>

Skills upload only on ChatGPT Business, Enterprise, Healthcare, and Edu, when the workspace allows it. On Free, Go, Plus, and Pro, use a project (steps under More).

1. In the sidebar, select **Plugins**, then the **Skills** tab in the Plugin Directory.
2. Select **Create**, then **Upload from your computer**, and choose one tool's Codex ZIP, such as `access-review-codex.zip`.
3. Wait for ChatGPT's scan. A skill marked **Needs Review** asks you to check it first.
4. In a chat, type `@` to pick the skill, or ask for the tool by name.

<details>
<summary>More</summary>

- **What you get:** one tool per upload. ChatGPT and Codex use the same skill format, but OpenAI doesn't list which upload file types it accepts, and this kit hasn't been tested there. If the upload is refused, use a project.
- **Admins:** Enterprise and Edu admins control **Enable skills** and **Enable skill uploading** in Permissions & roles.
- **Project instead (any plan):** select **New project** in the sidebar. In **...**, then **Project settings**, paste the tool's `dist/copilot/<tool>/agent-instructions.md`. Add the files from its `knowledge/` folder, plus your data. Free plans allow 5 project files, so add the data and `checklist.md` first.
- **Not supported:** skill folders on your computer work only in the ChatGPT desktop app's Codex, not in ChatGPT chat on the web (see Codex above). Personal plans can't create new custom GPTs.
- **Update:** upload the new ZIP, or replace the project's instructions and files.
- **Check it worked:** the skill shows on the Skills page, and `@` lists it in a chat.
- **Safe trial:** attach `accounts.csv`, `employees.csv`, and `apps.csv` from [`demo-estate/`](demo-estate/). It should flag ACC-019, ACC-063, and ACC-104 as orphaned.
- Sources: [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt), [Projects](https://help.openai.com/en/articles/10169521-projects-in-chatgpt), [GPTs](https://help.openai.com/en/articles/8554397-creating-a-gpt).

</details>
</details>

<details>
<summary><b>Microsoft 365 Copilot and Copilot Studio</b></summary>

Create an agent in [Agent Builder](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agent-builder-build-agents) or Copilot Studio. Each tool is a folder under `dist/copilot/<tool>/`, or in `copilot-agents.zip`.

1. Paste `agent-instructions.md` into the agent's instructions (the limit is 8,000 characters; ours are all under it).
2. Upload the files in `knowledge/` as knowledge sources. If an upload rejects `.md` files, rename them to `.txt`.
3. Run `test-script.md` against the demo estate to check it works.

<details>
<summary>More</summary>

- **What you get:** one agent per tool. Build one for each tool you need, including `app-governance` for routing.
- **Copilot chat (no agent):** paste `chat-prompt.md` into a chat, then attach your data files.
- **Skills (preview):** organizations in Microsoft's Frontier Program can add a skill package on the agent's **Configure** tab, under **Skills**. Microsoft's example ZIP has `SKILL.md` at the top, while our ZIPs hold a folder, so zip the folder's contents. Not tested with this kit. [Docs](https://learn.microsoft.com/en-us/microsoft-365-copilot/extensibility/agent-builder-add-skills).
- **Update:** replace the instructions and knowledge files with the new release's.
- **Check it worked:** `test-script.md` lists the pass checks. For access review, it should flag ACC-019, ACC-063, and ACC-104 as orphaned.
- **Safe trial:** the test scripts use the files in [`demo-estate/`](demo-estate/).

</details>
</details>

<details>
<summary><b>Other assistants</b></summary>

1. Open the tool's `dist/copilot/<tool>/chat-prompt.md`.
2. Paste it into a new chat.
3. Attach your data files, or the [`demo-estate/`](demo-estate/) files for a trial.

<details>
<summary>More</summary>

- **Agent Skills support:** if your assistant reads `SKILL.md` folders, use the folders in `dist/codex/skills/` or `dist/claude/skills/`. Check its docs for the folder it reads.
- **Update:** paste the prompt from the new release.
- **Check it worked:** the access review on the demo estate should flag ACC-019, ACC-063, and ACC-104 as orphaned.

</details>
</details>

<details>
<summary><b>Troubleshooting</b></summary>

- **Plugin skill not found in Claude Code:** check `claude plugin list`. If you installed from your shell during a session, run `/reload-plugins`. Plugin skills carry a prefix: `/app-governance-kit:access-review`.
- **Copied skill not found in Claude Code:** each skill needs its own folder with `SKILL.md`, such as `~/.claude/skills/access-review/SKILL.md`. If you created `~/.claude/skills` during the session, run `/reload-skills`.
- **Skill not found in Codex:** check the folder is `~/.agents/skills/access-review/SKILL.md`, then restart Codex.
- **ZIP rejected by the Claude app:** upload one tool's ZIP, not `claude-skills.zip`, and check code execution is on.
- **Old version still running:** run `claude plugin update app-governance-kit@evemcgivern-skills`, then run `/reload-plugins` or start a new session. For uploaded skills, delete and upload again.

</details>

## Try it

- **Read a method directly**: `methods/<tool>/method.md` for the full workflow, `checklist.md` for the a la carte version, `platform-guide.md` for where each field lives in ServiceNow/Flexera/etc.
- **Let an agent pick the tool**: the `app-governance` skill routes a plain request ("review our software estate") to the right skill and hands every decision back to you. In Claude Code, `app-governance-agent` loads it for you.
- **Practice for a certification**: ask the `cert-prep` study coach for scenario drills on the demo estate (CAMP, CSAM, CHAMP, AIGP, ITIL 4 Foundation, IAM Certificate). Practice only, not exam content.
- **Run a SAM practice by hand**: the templates and checklists in `sam-toolkit/` (license position, proof of purchase, renewals, asset record, authorizations, scope, tiers, audit, vendors, contract terms, acquisition gate, invoice verification, savings report), with a guide in `sam-toolkit/guide.md`.
- **Work an exercise by hand**: `practicum/01-program-setup.md` through `practicum/08-audit-response.md`, then self-check on the site's interactive practicum page — no installs, no AI shortcuts.
- **Use it with an agent**: point Claude, Codex, or Copilot at the relevant `dist/<platform>/...` skill and a real dataset (or the demo one under `demo-estate/`).

## Repo layout

```
methods/       One folder per tool: method.md, checklist.md, sop.md, template.csv, platform-guide.md, example/
sam-toolkit/   Thirteen templates and checklists for a software asset management practice, downloadable from the site
demo-estate/   A fictional company (Halden Logistics) with planted, findable problems, used by every practicum exercise
practicum/     Eight hands-on exercises, worked by hand against demo-estate before checking the answer key
field-guide/   Certifications, standards, glossary — the reference material behind the tools
site/          The public site (built, not hand-maintained — see below)
dist/          Generated per-platform skill packages (do not hand-edit; regenerated by `make build`)
build/         The Python build system that generates dist/ and site/ from the sources above
tests/         Full test suite for the build system
```

## Building

```
make test    # run the test suite
make build   # regenerate dist/ and the data-driven parts of site/ from methods/, demo-estate/, field-guide/
make scan    # check for copyright-risk long quotes and any private terms leaking into public output
```

Everything under `dist/` and the generated parts of `site/` is build output.
Edit the sources under `methods/`, `demo-estate/`, `field-guide/`, and
`practicum/` instead, then run `make build`.

## License

MIT — see [LICENSE](LICENSE). Names of third-party frameworks and standards
(ISO, COBIT, NIST, IAITAM, IAPP, PeopleCert, IAM) are used for reference only;
no affiliation with or endorsement by any of them.
