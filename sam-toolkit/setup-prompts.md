# Setup prompts

Thirteen prompts that walk you through setting up an application management practice with an AI assistant. The playbook gives the order. They're written to work in plain chat in Microsoft Copilot, ChatGPT, and Claude. Each one carries its own rules and scale, so the assistant doesn't need the kit installed. Copy one prompt at a time and replace each [BRACKET] with your own details.

## Pick your prompt

Start with the playbook, then choose the prompt for your step. Read the safety notes under Before you start first. Each prompt opens with when to use it and why.

Use each prompt at the step of `itam-program-playbook.md` shown here.

| Playbook step | Prompts |
| --- | --- |
| 1 Read the map | 1 |
| 2 Sponsor, problem statement, light charter | 8 (charter), 11 |
| 3 Stop the bleeding | 6, 7 |
| 4 Set the scope | No prompt. The scope is a decision for you and your sponsor, so write it from the files named in that step. |
| 5 Baseline and targets | 12, then 2 |
| 6 The policy set | 8 (policy) |
| 7 Build one inventory | 4, 3 |
| 8 Proof, then the position | 5 |
| 9 Put controls in place | 3 |
| 10 Measure and review | 10, 13, 9 |

After the first pass, repeat on a schedule:

- **Every month:** prompt 6, for renewals due in 180 days.
- **Every quarter:** prompt 5 for your most important products, prompt 7 to confirm each audit role still has a ready backup, prompts 10 and 13, and prompt 9 when the plan changes.
- **Every year, and after a big change:** prompt 2 again, after a merger or a change of sponsor.
- **Before an event:** prompts 5 and 6 before a renewal or an audit. If an audit letter has already arrived, give it to Legal first, then use prompt 7.

Pick the one that matches what's in front of you:

1. [Set the scene and plan the ten playbook steps (playbook step 1)](#prompt-1-set-the-scene)
2. [Score my program as it is and as it should be](#prompt-2-baseline-your-program)
3. [Map how a process really works](#prompt-3-map-a-process-before-you-change-it)
4. [Decide where each kind of data lives](#prompt-4-decide-where-each-kind-of-data-lives)
5. [Check my licenses against proof of purchase](#prompt-5-back-your-licenses-with-proof)
6. [Find renewals and notice deadlines](#prompt-6-get-your-renewals-under-control)
7. [Get ready for a publisher audit](#prompt-7-prepare-for-an-audit-before-a-letter-arrives)
8. [Review my governance charter and policy](#prompt-8-set-up-governance-and-a-policy)
9. [Turn my plan into calendar reminders](#prompt-9-turn-the-plan-into-reminders)
10. [Write a report for leaders](#prompt-10-report-to-leaders-and-plan-the-next-round)
11. [Map my customers and what they expect](#prompt-11-map-your-customers-and-what-they-expect)
12. [Decide what good looks like for my organization](#prompt-12-decide-what-good-looks-like)
13. [Plan quarterly internal checks](#prompt-13-plan-your-rolling-internal-checks)

## How to use them

- **Start a new chat for each prompt**, or paste the next prompt into the same chat. Each prompt repeats the short rules, so it works even in a fresh chat.
- **Attach the named file, or paste it.** In ChatGPT and Claude, use the attach button. In Microsoft Copilot, attach where your version allows it; if your organization blocks uploads, paste the column headings or the text. Every prompt also works if you attach nothing: the assistant asks you for the facts instead.
- **Replace the brackets.** Replace everything in [square brackets] and delete any option you don't use. On a phone, paste the prompt first, then edit the brackets inside the chat.
- **Ask for text you can copy.** The prompts ask for results as plain text, a table, or CSV. Copy that into the matching toolkit file. Do not rely on the assistant to hand back a finished file.
- **If your tool has custom instructions or projects,** paste the rules from Prompt 1 there once.
- **If the assistant drifts,** reply: Stay in the coach role, ask one question at a time, and don't invent figures.

## Before you start

**Privacy rule for every prompt:** Use only an assistant your organization has approved for confidential data; otherwise use the Halden data, column headings only, or redacted rows; never paste passwords, license keys, or employee names and emails; and once an audit letter exists, nothing about it goes to any assistant unless Legal agrees.

- **Practice on fictional data.** The Halden Logistics demo estate in `demo-estate/` is built for this. Start there if you're unsure.
- **Keep real inventories safe.** Real inventories, contracts, and invoices are confidential. Use them only where your organization allows, and check your account's data settings first. When in doubt, share column headings, not rows, or redact names, prices, and account numbers.
- **You decide.** Every prompt tells the assistant to mark the points that need a person's decision and to stop there.
- **Check dates and sums yourself.** Assistants make arithmetic and date mistakes, and they don't reliably know today's date, so the date prompts ask you to state it. Treat every figure as unverified until you've checked it.
- **Different assistants answer differently.** Compare the result with the Good looks like line under each prompt, not with another assistant's wording.

## Prompt 1: Set the scene

**When to use it:** At playbook step 1, when you don't know where to begin, or when you take over an existing program.

**Why:** It fits the plan to your time and your biggest worry, instead of handing you every template at once.

**Paste this:** Rules: act as a read-only application governance coach, ask one question at a time, never decide for me, mark each point needing a person's decision as Decision needed, mark anything you cannot verify as Unverified, write Not found where I give no figure and never invent one, show the arithmetic for every date and sum, and do not browse the web. I work at [ORGANIZATION TYPE AND SIZE] as [YOUR ROLE]. We keep our inventory in [WHERE], our contracts in [WHERE], and our spend data in [WHERE]. My main worry is [AUDIT, RENEWALS, DUPLICATE SPEND, OWNERSHIP, OR OTHER]. I can give this [HOURS] hours a week. Ask me up to five questions you need. Then take me through the ten steps of the playbook in this order: 1 read the map; 2 get a sponsor, a problem statement, and a light charter; 3 stop the bleeding on renewals and the audit contact; 4 set the scope; 5 baseline and targets; 6 the policy set; 7 build one inventory; 8 proof first, then the position; 9 put controls in place; 10 measure and review. If I have no sponsor, say that comes first. For each step, say what I should do first given my worry and my hours, and which steps can wait. Finish with a plan that places the steps against my hours, and mark the point where a program with steps 1 to 5 done is complete enough to stop.

**Attach (optional):** `operating-calendar.md`.

**Good looks like:** a plan that follows the ten playbook steps and starts with a sponsor. It fits your hours and invents nothing about your organization.

## Prompt 2: Baseline your program

**When to use it:** At playbook step 5, before you buy a tool or write a policy. Repeat it every year, and after a merger or a change of sponsor.

**Why:** It shows where you are and where you need to be, with evidence, so you fund the gaps that matter and can show progress later.

**Paste this:** Rules: read-only coach, one question at a time, never decide for me, mark Decision needed and Unverified, write Not found for missing figures, show arithmetic, no web. Walk me through a self-assessment of my application management program, one dimension at a time. Dimensions: policy and decision rights; roles and ownership; inventory and data quality; intake and acquisition; lifecycle and periodic review; licenses, contracts, and renewals; cost, value, and rationalization; risk, security, and AI use; retirement and data disposition; measures and leadership reporting; communication and education. Scale: 0 not done; 1 ad hoc, done sometimes and not written down; 2 defined, written down, owned, followed, with a recent example; 3 measured, a number shows how well it works and has led to a change. For each dimension ask what we do today and what evidence I could show a leader or auditor. If I cannot show evidence, score it one level lower and say why. Then ask where we need to be, by when, and why; do not set every target to 3. At the end, give a CSV with these columns: dimension, as_is_level, as_is_evidence, to_be_level, to_be_reason_and_date, gap, priority, owner, first_action, due_on. Rank by gap and recommend the three gaps to fund first. Decision needed: the sponsor chooses.

**Attach (optional):** `application-management-self-assessment.md` for the level descriptions, and `application-management-gap-plan.csv`. When the assistant gives you the rows, type them into the Assess sheet of `application-management-workbook.xlsx`. See `examples/application-management-gap-plan-example.csv` for a finished one.

**Good looks like:** each score has evidence, and targets differ by dimension. Owners are roles, not names.

## Prompt 3: Map a process before you change it

**When to use it:** At playbook steps 7 and 9, before you change a process such as intake, renewals, or retirement, or when a process keeps going wrong.

**Why:** A tool or policy built on a process nobody has described only writes down guesses. The gaps between the two maps become your work list.

**Paste this:** Rules: read-only coach, one question at a time, never decide for me, mark Decision needed and Unverified, write Not found for missing figures, no web. Help me map how [PROCESS, FOR EXAMPLE NEW SOFTWARE REQUESTS] works today. Ask me, one step at a time, what triggers the step, who does it, what they do, what record it produces, and where the record is kept. Then help me describe how it should work, using roles instead of names. List every gap between the two maps in a table with these columns: gap, type (missing step, no owner, no record, wrong order, or manual work that could be reliable), risk of leaving it, fix, owner role, due date. Rank by risk. Do not suggest a software tool yet.

**Attach (optional):** `process-map-worksheet.md`.

**Good looks like:** the first map shows what really happens, even where it's messy.

## Prompt 4: Decide where each kind of data lives

**When to use it:** When the same fact, such as an owner, a count, or a date, differs between systems, or before you consolidate data or buy a tool.

**Why:** When two systems disagree, nobody knows which to trust, so name one authoritative system per kind of data.

**Paste this:** Rules: read-only coach, one question at a time, never decide for me, mark Decision needed and Unverified, write Not found for missing figures, no web. I will name the systems we use and give you no data. For each of these kinds of data, help me choose one authoritative system, a data owner role, how the copies are kept in step, and how often to compare them: application inventory, hardware inventory, entitlements and license position, proofs of purchase, contracts and renewal dates, invoices and spend, discovery and usage data, configuration and service relationships, application owners, retirement records. Point out any row where I name two systems as the source or none. List the options and the cost of each; do not choose for me. Give the result as CSV with columns data_domain, authoritative_system, data_owner, other_systems_holding_copies, how_copies_are_kept_in_step, reconcile_every.

**Attach (optional):** `source-of-truth-map.csv`.

**Good looks like:** one authoritative system per row, and an owner for each.

## Prompt 5: Back your licenses with proof

**When to use it:** At playbook step 8, before a renewal, a true-up, or an audit, and every quarter for your most important products.

**Why:** An audit works from the proofs you can show. This prompt finds the missing ones now, while you can still chase them.

**Paste this:** Rules: read-only coach, one question at a time, never decide for me, mark Decision needed and Unverified, write Not found for missing figures, never guess a quantity, show arithmetic, no web. I will give you, for [A FEW PRODUCTS], the quantity I report as owned, the quantity in use, the license metric the agreement counts, and the proofs of purchase I hold. For each product, compare the quantity I can prove with the quantity I report, in that metric. Label each product short, even, or over. Do not count a proof that lacks the buyer, vendor, product, version, metric, quantity, or date. List every missing record as a row for a documentation gaps log with columns gap, record type, related product, what is missing, why it matters, what it blocks, owner role, due date. Never tell me what the agreement permits; ask me to check the contract or counsel.

**Attach (optional):** `license-position.csv`, `proof-of-purchase-check.csv`, and `documentation-gaps-log.csv`, filled in for a few products, or the Halden files in `demo-estate/` to practice.

**Good looks like:** each shortfall points to a missing proof or a real gap, with an owner and a date.

## Prompt 6: Get your renewals under control

**When to use it:** At playbook step 3, then every month, and at least 180 days before any large contract ends.

**Why:** The notice deadline comes before the end date. Miss it and the contract can renew without anyone deciding.

**Paste this:** Rules: read-only coach, never decide for me, mark Decision needed and Unverified, write Not found for missing figures, show the arithmetic for every date, no web. Today's date is [TODAY'S DATE, YYYY-MM-DD]. From the renewal data I give you, list every renewal in the next 180 days. Work out each notice deadline as the contract end date minus the notice days. If notice days are missing, say so and do not guess them. Group renewals by the window each is in: 120 to 180 days, 90 to 120, 60 to 90, 30 to 60, and past due. Flag every auto-renewing contract and every renewal with no named owner. Do not decide any renewal. For each, say which decision is needed from whom: renew, reduce, or cancel. Give the result as a table with columns product, contract end, notice days, notice deadline, days left, window, auto-renews, owner, decision needed.

**Attach (optional):** `renewal-calendar.csv` with redacted or fictional rows. To check your assistant, give it `demo-estate/licenses.csv` and a date of 2026-09-01: it should say notice days are missing and note that 2 licenses were already expired.

**Good looks like:** every date has its arithmetic shown, and no renewal is left without an owner.

## Prompt 7: Prepare for an audit before a letter arrives

**When to use it:** At playbook step 3, before a publisher audit letter arrives, and every quarter to confirm each role has a ready backup. If a letter has already arrived, give it to Legal first and use this to organize the team.

**Why:** Under audit pressure people improvise. Knowing who does each task, and who covers for them, prevents single points of failure and missteps.

**Paste this:** Rules: read-only coach, one question at a time, never decide for me, mark Decision needed and Unverified, write Not found for missing figures, no web. Help me fill in a roster of audit-response tasks. The tasks are: receive the letter and pass it to Legal; own all contact with the publisher; open and keep the dated case file; gather proofs of purchase; run discovery and keep the dated output; run the hardware audit; reconcile use against proofs; advise on what may be released; find payment records; brief the executive sponsor; decide spend and settlement; hold the post-audit review. For each task ask who would do it today and who the backup is. If there is no backup, or the backup has never been briefed, mark it a single-person risk. Give a CSV with columns task, role, primary_holder, backup_holder, backup_ready, single_person_risk. Then name the three roles to fix first and why. Remind me that only counsel talks to the publisher. Do not draft any message to a publisher.

**Attach (optional):** `audit-response-roles.csv`.

**Good looks like:** every task has a role and a holder, and each holder has a ready backup, or the task carries a clear flag saying there isn't one.

## Prompt 8: Set up governance and a policy

**When to use it:** At playbook step 2 for the charter and step 6 for the policy set, or when nobody is sure who decides.

**Why:** Without a sponsor, a scope, and written decision rights, requests stall and exceptions pile up.

**Paste this:** Rules: read-only coach, never decide for me, mark Decision needed and Unverified, write Not found for missing figures, no web. I will paste my draft governance charter and my draft policy. Check the charter for a named sponsor, decision rights with a threshold, an escalation path, and measures. Check the policy for a clear scope, an accountable role, defined terms, enforcement, a review cycle, and any rule nobody could actually meet. List what is missing in order of importance, tie each gap to the section it belongs in, and propose plain-language wording I can edit. Mark the points where leaders must decide. If I have no drafts yet, ask me five questions and then outline both.

**Attach (optional):** your drafts, or `demo-estate/council-draft.md` and `demo-estate/policy-draft.md` to practice. To draft from a blank page, use `policy-template.md` and `policy-standard-template.md`, then test the draft with `policy-checklist.md`; `policy-lifecycle-sop.md` covers approval and review.

**Good looks like:** each gap is tied to a section of your draft, and the proposed wording is yours to edit.

## Prompt 9: Turn the plan into reminders

**When to use it:** After you have a gap plan or a renewal list, to turn decisions into dates.

**Why:** Notice deadlines and gap fixes need dates in a calendar before anyone can be reminded of them.

**Paste this:** Rules: read-only coach, never decide for me, mark Unverified, show the arithmetic for every date, no web. Today's date is [TODAY'S DATE, YYYY-MM-DD]. From the gap plan and renewal data I give you, list the dates I should be reminded of in a table with columns date, task, dimension, file to use, owner role. Label each task by its dimension name, never by a row number, and take file names only from what I give you, writing Not found if there is none. Ask me how many days ahead I want a reminder. Then give the same dates as the text of an iCalendar file, with an alarm that many days before each date, in one plain text block that I can copy, save with the ending .ics, and import. Do not say you have attached or created a file. I will check each date before I import it.

**Attach (optional):** `application-management-gap-plan.csv` and `renewal-calendar.csv`.

**Good looks like:** every reminder has a date you've checked, and the calendar text imports without errors.

## Prompt 10: Report to leaders and plan the next round

**When to use it:** At playbook step 10, every quarter before leaders meet, and any time you need funding or a decision.

**Why:** The report ties your work to money saved or risk reduced, and lists the decisions you need from leaders.

**Paste this:** Rules: read-only coach, never decide for me, mark Decision needed and Unverified, write Not found where I give no figure and never invent one, no web. Draft a one-page leadership report from the gap plan and notes I give you. For each control, link a measure to a decision and the decision to an outcome in money or risk. Count only savings I can back with evidence, and put adverse trends beside the savings. Answer these six questions, writing Not found where you have no evidence: do applications have accountable owners; how much renewal spend is undecided; what spend could be reduced or retired; which license gaps could become audit exposure; which gaps need escalation; what did we save and what is the proof. End with the decisions leaders must make and the three gaps to close next quarter.

**Attach (optional):** `leadership-report.md` and `application-management-gap-plan.csv`.

**Good looks like:** no figure without a source, and the decisions are clear enough to approve or reject.

## Prompt 11: Map your customers and what they expect

**When to use it:** At playbook step 2, in the first month, and again when a new team starts to rely on your data.

**Why:** Asset data is only worth keeping if it answers someone's question. Knowing who needs what, in how much detail, and how often tells you what to collect and what you can stop collecting.

**Paste this:** Rules: read-only coach, one question at a time, never decide for me, mark Decision needed and Unverified, write Not found for missing figures, never invent a need, no web. Help me map the people who rely on asset management information. For each of these customers, ask me one question at a time: IT security, service desk, procurement, finance, legal and compliance, HR, application owners, IT operations and change, executives and the sponsor, internal audit and risk. Ask what decision or task of theirs depends on asset data, what data and what level of detail they need, how often, what we need from them in return, and how we could tell we served them well. Skip any customer I say does not exist. Then give a CSV with columns customer, what_they_need, level_of_detail, how_often, what_we_need_from_them, how_we_deliver, measure_of_success. Finally name the two customers whose needs I can meet cheapest and fastest, and the one whose unmet need is the biggest risk.

**Attach (optional):** `customer-expectations.csv`.

**Good looks like:** each customer has a need you could check, a way to deliver it, and a measure. You've chosen where to start.

## Prompt 12: Decide what good looks like

**When to use it:** At playbook step 5, before you set To-Be targets in Prompt 2, and each year when you review them.

**Why:** Full conformance to a standard is optional. Targets should match your risk, your size, and the time you have. The sponsor settles them with you, so you fund what matters.

**Paste this:** Rules: read-only coach, one question at a time, never decide for me, mark Decision needed and Unverified, write Not found for missing figures, no web. Help me decide how far my asset management program needs to go. Ask me these eight questions one at a time and ask for a yes or no and one line of why: do laws or contracts require us to prove control of software or data; have publishers audited us in the last three years or do our contracts allow audits; is software spend large enough that savings matter to the budget; do teams buy subscriptions without IT; do mergers, sales of units, or fast growth keep changing our estate; do our applications hold sensitive or regulated data; can people give at least five hours a week; does a sponsor with budget back this. Scale: 0 not done, 1 ad hoc, 2 defined (written, owned, followed, with a recent example), 3 measured (a number shows it works and led to a change). Then suggest a target level for each of these dimensions: policy, roles, inventory, intake, lifecycle review, licenses and renewals, cost, risk, retirement, measures, communication. Use level 2 unless my answers justify 3, and do not set every target to 3. Give a reason for each target, three things I should deliberately not do yet, a one-line good-enough statement for the next 12 months, and up to five measures that cannot be met by paperwork alone. If I have no sponsor, tell me to get one before setting targets. Decision needed: the sponsor settles the targets.

**Attach (optional):** `what-good-looks-like.md`.

**Good looks like:** targets that differ by dimension, each with a reason. It also has a short list of what you won't do yet and a good-enough statement you could say to the sponsor.

## Prompt 13: Plan your rolling internal checks

**When to use it:** Every quarter, to choose what to test next, and before an external audit.

**Why:** Practicing the audit on your own records finds problems while you can still fix them quietly.

**Paste this:** Rules: read-only coach, one question at a time, never decide for me, mark Decision needed and Unverified, write Not found for missing figures, no web. Help me plan rolling internal checks of my asset management program. Ask which areas worry me most. The areas are ownership, inventory accuracy, renewals, proof of purchase, retirement, the purchase gate, and leavers. Then propose a four-quarter rotation so every area is tested once a year, with the riskiest first. For the next quarter, give for each chosen area the test to run, a suggested sample size, what counts as a pass, and a row for a findings log with columns check_id, quarter, area, test, sample_size, records_failed, finding, severity, owner, due_on. Remind me that findings are for fixing and not for blame, and that a finding is closed only when a retest passes. Do not make up results.

**Attach (optional):** `rolling-internal-check.md` and `internal-check-log.csv`.

**Good looks like:** a rotation that fits your risks and a clear test for the next quarter, plus a log you can start filling in.

## Keep going

Run Prompt 2 again each year, and after a merger or a change of sponsor. Run Prompts 5 and 7 each quarter and Prompt 6 each month. Keep the results with the files, and record what you decided and who approved it.

If you have the kit's skills installed, you can instead ask Claude Code for the `app-governance` skill, or type `$app-governance` in Codex. The prompts above don't need them.

The kit gives methods and reasoning support. It's not a governance platform, a certification, or legal advice. Ask counsel where a contract term or audit step is unclear.
