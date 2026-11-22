# SAM toolkit guide

Forty working files, including this guide, to support a software and IT asset management (SAM/ITAM) practice. They are blank templates and checklists. Open the CSV files in Excel, Google Sheets, or any spreadsheet; they are plain text, so nothing is locked. The documents are Markdown in the repository and download as Word files from the site. All data in the examples is fictional (the Halden Logistics demo estate).

The files are informed by ISO/IEC 19770-1:2017. Most files trace to a clause of the standard; the purchasing, savings, and practice files trace to crosswalk rows instead. The text is paraphrased and does not replace the standard. No affiliation with or endorsement by ISO or IEC.

## Where to start

Start with `itam-program-playbook.md`. It is the one order to follow: ten steps, each with the files to use, the matching setup prompt, and what done looks like. This guide is the reference for what each file is and how to fill it in; it does not set an order. Read the plain-language [glossary](../field-guide/glossary.md) for the terms, and the `program-setup` method (`methods/program-setup/method.md`) for the charter in step 2.

Two files support the playbook rather than sit in it: `operating-calendar.md` lists the routines and maps its weeks to the playbook's steps, and `setup-prompts.md` holds the thirteen prompts for an AI assistant. For one place to assess, plan, and measure, use `application-management-workbook.xlsx`.

## The files

**One key.** Every file that refers to an application, device, or service uses `asset_id`, the same value as in `asset-record.csv`. `license-position.csv`, `proof-of-purchase-check.csv`, and `renewal-calendar.csv` use `asset_id` for the item they cover. `contract_ref` is the key for a contract: it is the same value as `contract_ref` in `vendor-contract-register.csv`, `contract_id` in `contract-terms-check.csv`, and `governing_agreement` in `invoice-verification.csv`. The Halden demo estate files `licenses.csv` and `accounts.csv` call the same value `app_id`, and `apps.csv` calls it `id` (for example APP-001). They are source data for the practicum, so they keep their own column names; map them to `asset_id` when you copy a row into a toolkit file.

### license-position.csv (clause 8.4)

One row per product. Reconcile what you own against what is in use.

- `asset_id`: the asset this row covers, as in `asset-record.csv`.
- `entitlements_owned`: the count of licenses you hold, in the vendor's license metric (`license_metric`: user, device, core, and so on).
- `in_use_count`: installs, users or cores in use, in the same metric. Do not mix metrics in one row.
- `position`: `entitlements_owned` minus `in_use_count`. Negative is a shortfall.
- `status`: shortfall, surplus or balanced.
- `evidence_source`, `checked_on`, `reviewer`: where the numbers came from, when, and who checked.

A user count is not always the licensed quantity. Confirm the vendor's metric before acting on a shortfall. See `examples/license-position-example.csv`.

### proof-of-purchase-check.csv (clause 8.4, crosswalk XW-006, XW-007, XW-020)

One row per product (per publisher, product and version). This is the evidence behind `entitlements_owned` in `license-position.csv`.

A count of installs is not a position. A license counts only when acceptable proof of purchase backs it. Keep proofs for as long as the license and any upgrade rights depend on them, and as long as your records schedule requires. **Decision needed: records owner or counsel** for the period. A later upgrade is only as good as the original purchase behind it. A certificate of authenticity or a license key alone shows a copy exists, not that you have the right to use it.

- `asset_id`: the asset the proofs cover, as in `asset-record.csv`.
- `installs_found`, `count_in_metric`, `proofs_located`, `quantity_proven`: what discovery found, the count in the license metric (assigned users for named-user licenses, devices for device licenses), how many proofs you located, and the quantity those proofs add up to. `term_start`, `term_end`: the current subscription or support term the proof shows.
- `proof_ref`: invoice or purchase order numbers. Separate several with a semicolon.
- `result`: short if `quantity_proven` is below `count_in_metric`, even if equal, over if above.
- `shows_purchase_date`, `shows_full_product_description`, `shows_version`, `shows_quantity`, `shows_vendor`, `shows_buyer_entity`, `shows_price`, `payment_proof_on_file`: yes or no. Answer yes only if every proof you counted shows that item. A "no" means the proof may not count; ask the vendor for a reissue.
- `license_metric`: the unit the contract counts (named users, devices, cores). Reconcile in that metric, not in a raw install count.
- `license_type`: full, upgrade or competitive upgrade. For an upgrade or a competitive upgrade, `upgrade_chain_complete` is yes only when the original qualifying purchase is also on file. Use "not applicable" for a full license.
- `evidence_location`, `checked_on`, `reviewer`: where an auditor can find the proofs, when you checked, and who checked.

Downgrade rights may let a newer license cover older installs; confirm with counsel. For a subscription, the proof must show the current term. The agreement defines what counts as acceptable proof; licensing-portal and reseller records can count. If `quantity_proven` differs from `entitlements_owned`, use the proven number until the gap is explained. See `examples/proof-of-purchase-check-example.csv`.

### contract-terms-check.csv (clause 8.4, crosswalk XW-013)

One row per contract term or definition you checked. Link each row to its contract through `contract_id`, which matches `contract_ref` in `vendor-contract-register.csv` and in `renewal-calendar.csv`, and copy `notice_deadline` from `renewal-calendar.csv` into `renewal_notice_deadline` so a term that changes the renewal is not missed.

Read license terms as permissions: anything not clearly granted is treated as not permitted until counsel or the vendor confirms. This file does not interpret contracts or give legal advice. It finds what to ask counsel.

- `term_or_definition`, `clause_ref`: what you read and where, for example the definition of "device" or the transfer clause.
- `clear`: yes, no or maybe. Put what is unclear in `what_is_unclear`.
- `which_document_governs`: record which document claims precedence and where it says so. Send any conflict between documents to counsel. **Decision needed: counsel**.
- `counsel_needed`: yes or no. `owner` and `checked_on` say who is following it up and when.

### acquisition-gate-checklist.md (crosswalk XW-009, XW-011, XW-013, XW-021)

A checklist every software request passes before any purchase. It asks whether you already own it, whether it is installed and unused, which path it takes, whether it duplicates an existing product (see the rationalization method), and whether it uses AI or handles organizational data (see the AI intake method). It ends with a check of spend outside procurement, such as expense cards and department budgets. The rule is: no purchase outside this path.

### invoice-verification.csv (crosswalk XW-012, XW-013)

One row per invoice line check. Compare the invoice to the contract and purchase order before payment, not after, when a correction is cheaper.

- Begin the back-review with your biggest suppliers and the invoices that are hardest to read.
- `payment_terms_match_contract`, `quantity_invoiced` against `quantity_agreed`, and `unit_price` against `negotiated_unit_price`: the common places where an invoice drifts from the agreement.
- `line_math_ok`, `subtotal_ok`, `tax`, `shipping`, `total`: check the arithmetic and the add-ons.
- `matched`: yes or no. If no, say why in `discrepancy` and record `amount_at_issue` and `resolved_on`.

Chart discrepancy categories over time. The pattern is what supports a change in practice to management.

### savings-report.csv (crosswalk XW-012)

One row per savings type per period: invoice errors recovered, purchases avoided by redeploying, contract terms, negotiation, maintenance cancelled and unused licenses reclaimed.

- `baseline_cost`, `amount_saved`, `percent_saved`: the cost before and what you saved. Leave `percent_saved` blank if there is no baseline.
- `evidence_ref`: the record that supports the number, such as a row in `invoice-verification.csv`.
- `adverse_trend_note`: report bad news too, such as rising error rates or reclaimed licenses being requested again. A report with only wins is not trusted.
- `reported_to`, `reported_on`: who saw it and when.

### renewal-calendar.csv (clause 8.4, crosswalk XW-008)

One row per license or contract.

- `asset_id` and `contract_ref`: the asset the contract covers, and the contract. `contract_ref` matches `contract_id` in `contract-terms-check.csv`, so you can look up the clauses that change the renewal.
- `notice_deadline`: `contract_end` minus `notice_days`. This is the date that matters, not the end date.
- `auto_renews`: yes or no.
- `in_use_last_90_days`: usage before you decide, so you do not renew shelfware.
- `decision`: renew, reduce or cancel. Record `reason`, `decision_owner`, `approver` and `decided_on`.

See `examples/renewal-calendar-example.csv` for three Halden rows. Each `contract_ref` has a matching row in `contract-terms-check-example.csv`.

### asset-record.csv (clause 8.3, 7.6.2)

The core data record. One row per asset (software, hardware, or an IT service).

- `asset_id`: the one key for the asset. Other files copy it.
- `owner`: the named person accountable. `custodian`: who looks after it day to day.
- `authorized`: yes or no, with `authorization_ref` pointing to the entry in the authorization log.
- `status`: for example requested, in use, retiring, retired. Add `retired_on` when it leaves use.
- `source_system` and `last_verified_on`: where the data came from and when it was last checked.

The standard requires accurate data for every core asset through its life and a record of whether each asset is authorized.

### authorization-log.csv (clause 7.6.3)

Record who made each authorization, when, and why. Record who carried it out, when, and against which authorization.

- `authorization_type`: financial, security, operational or managerial.
- `scope`: the organization, a unit, a group of people, one asset or a class of assets.
- `valid_until`: leave blank if there is no end date.
- An example of an execution is installing authorized software; put the ticket or change reference in `execution_ref`.

### statement-of-applicability.csv (clause 6.2.2)

Pre-filled with the 15 processes in Annex A. For each, say whether it is in scope and why. The standard asks for a justification for every inclusion and exclusion.

- Change, core data, license and security management are marked "always included". The standard says their objectives are already part of clause 8.
- `tier`: fill in from Annex B, Figure B.2 of your copy of the standard.
- `evidence_location`: where an auditor can see the process working.

### vendor-contract-register.csv (clause 8.7, crosswalk XW-013)

One row per supplier contract that affects ITAM.

- `activities_outsourced`: the scope and boundaries of what the supplier does.
- `mixed_responsibilities`: where you and the supplier share ownership of devices, servers, software or data, say so. This is where the risk sits.
- `risk_assessed_on`, `risk_rating`, `risk_owner`: the standard requires you to assess the risk of outsourcing.
- `knowledge_sharing_arrangement`: how information is shared with the supplier.
- `performance_reviewed_on` and `contract_terms_verified_on`: monitor performance, and check compliance with terms beyond licensing.

### tier-self-assessment.md (Annex A and B)

A yes/partly/no check across three tiers, with a place for evidence.

### audit-and-review-checklist.md (clauses 9.2, 9.3, 10.1)

A plan-and-record checklist for the internal audit, and a pack list for the management review.

### benefits-tracker.csv (crosswalk XW-012, XW-025)

One row per benefit you expect from a practice. It is how you prove the practice paid off, instead of asserting it.

- `metric`, `unit`, `baseline_value`, `baseline_date`: what you measure, and its value before the practice. Measure the baseline from your own records on a named date.
- `target_value` and `target_date`: where you want it to be, and when.
- `current_value`, `measured_on`, `evidence_ref`: the value when you measured again, the date, and where the proof is filed. Leave `current_value` blank until you have re-measured.
- `status`: baseline only, forecast, achieved, or not achieved. A forecast is an estimate, not a benefit. Mark a row achieved only when the evidence is filed.
- `effect_type` and `effect_amount`: cost saved, cost avoided, risk reduced, or time saved, and the amount if you can back it. Write Not found where you cannot. Net out any cost the change added.

See `examples/benefits-tracker-example.csv` for six rows on the Halden demo estate. Their baselines come from the demo files; the current values stay blank because no change has been made. Feed the achieved rows into `savings-report.csv` and `leadership-report.md`.

### application-management-workbook.xlsx (crosswalk XW-003, XW-025)

One workbook that carries a program from the As-Is assessment to measurement. It replaces filling in the self-assessment, the gap plan, and the benefits tracker as separate files, and adds a scorecard and a history. Open it in Excel, Google Sheets, or LibreOffice; it uses formulas only, with no macros, and nothing is locked.

- **Start:** your program name, scope and sponsor, the six steps, the scale, the status words, and four settings you can change.
- **Assess:** score each dimension 0 to 3 with evidence, then set the To-Be level. The gap and a check are calculated. Level and date cells reject anything invalid.
- **Plan:** choose the gaps to fund (no more than three at a time), with an owner, a first action, and a date.
- **Measures:** the benefits tracker. Row one is the program's own gap-points measure, tied to Assess. A measure counts as achieved only with a latest value, a date, and evidence; forecasts are never added to achieved results.
- **Scorecard:** headlines, a table by dimension, the six leadership questions, and checks. It is all calculated. Blank means not entered, never zero, and every status is a word.
- **Re-score:** one column per later assessment, so history is kept and nothing is overwritten.
- **Ideas:** credible measures that are hard to fake, and how people game each.

There is a blank copy and a Halden example, `application-management-workbook-example.xlsx`. The example's current values are blank because no change has been made. Previewers that do not calculate formulas, such as some phone and email previews, may show blanks; open it in a spreadsheet program.

### policy-template.md (clause 5.2, crosswalk XW-003, XW-004, XW-027)

A fill-in template for one ITAM policy: control block, purpose, scope and exclusions, definitions, policy statements, roles, related standards, exceptions, enforcement, communication, measures, consistency with other policies, review history, and approval. Use it for each policy in a small set: the umbrella policy, software acquisition and exceptions, vendor management, and records and evidence. The examples are fictional (Halden). Retirement follows `retirement-signoff-checklist.md` and, for devices, the `hardware-lifecycle` method; AI tool intake follows the `ai-intake` method.

Exceptions are logged in `authorization-log.csv`, with the end date in `valid_until`. Penalty wording is a **Decision needed: counsel**, and so are retention periods in the records policy. The template sets neither.

### policy-standard-template.md (clause 7.6.5, crosswalk XW-009, XW-020)

A fill-in template for one software standard: a catalog of approved titles by role or device class, including software delivered as a service. It adds acceptance and rejection criteria with reason codes, security requirements, the non-standard path, a pilot-first rollout, a feedback channel, and where it is published. The standard says what is on the list; the policy says people must use it.

### policy-checklist.md (clauses 5.2, 7.3, 7.4, 7.6.5, crosswalk XW-003, XW-004, XW-020, XW-025, XW-027, XW-030)

Sixteen questions to test a draft policy before approval and at each review: owner and approver, sponsor approval, bounded scope, defined terms, commitments, license compliance and acceptable use, rules that can be met and tested, roles, exceptions, penalties, consistency, controlled publication, communication, awareness with acknowledgment, review triggers, and change history.

### policy-lifecycle-sop.md (clauses 5.2, 7.3, 7.4, 7.6.5, crosswalk XW-003, XW-020, XW-025, XW-030)

A short procedure for the life of a policy: draft, consult, counsel review, sponsor approval, publish with a version, communicate and record acknowledgment, log and expire exceptions, review yearly or on a trigger, and withdraw superseded versions. It ends with questions to take to counsel and the contract owner on penalty wording, retention periods, and license reassignment. The questions have no answers; those come from counsel and the contract owner.

### itam-program-playbook.md (crosswalk XW-003, XW-025, XW-027)

The one order to follow. Ten steps from reading the map to measuring and reviewing, each with a one-line reason, the files to use, the matching setup prompt, tickable done-when boxes, and a rough planning time. A marker after step 5 says where a small program can stop. It also has a box for people with no sponsor, no inventory, or an audit letter already in hand, what must exist first, why programs stall in the first year, the routines that keep a program alive, and how to tell a healthy program from a busy one.

### data-sources-guide.md (clauses 8.3, 8.4, crosswalk XW-005, XW-006, XW-012, XW-026)

How to get the data that playbook steps 7 and 8 need. Five sources: discovery or inventory output, sign-in logs for cloud apps, expense and accounts-payable data, purchasing and contract records, and HR joiner and leaver lists. For each it gives how to get it, what it can and cannot tell you, and who to ask. It then shows how to clean product and publisher names so counts match, and ends with a good-enough-to-start test.

### risk-assessment-guide.md and risk-register.csv (clause 6.1, crosswalk XW-024, XW-025)

A five-step method (identify, assess, treat, record, review) and the register it fills. The guide defines a plain low, medium, and high scale for likelihood and impact, and four treatments: accept, reduce, transfer, avoid. The CSV has six fictional Halden rows to replace with your own.

- `id`, `risk`, `asset_or_process`, `cause`, `consequence`: what could go wrong, where, why, and what it would cost.
- `likelihood`, `impact`: low, medium, or high, by the guide's scale. Rate on evidence.
- `owner`: the person who answers for the risk, and who accepts what remains after treatment.
- `treatment`: accept, reduce, transfer, or avoid. Have counsel review any transfer that rests on contract wording.
- `action`, `due`, `status`: what will be done, by when, and whether it is open, in progress, closed, or accepted.
- `review_date`: when you re-rate it. Keep closed rows so the history shows.

### resources-and-training-plan.md (clauses 7.1, 7.2, 7.3, crosswalk XW-004, XW-025, XW-027, XW-030)

What to budget in people, data sources, training, and tools, a table to size it with your own figures (write Not found where you have none), who needs which training, and what evidence shows competence. It sets no price and no head count.

### joiner-mover-leaver-procedure.md (clauses 7.6.3, 8.3, 8.4, crosswalk XW-008, XW-009, XW-012, XW-015, XW-017)

What HR tells ITAM, what happens to software and licenses when a person joins, changes role, or leaves, and the steps to reclaim a license. Check the contract's reassignment rights first: device-tied or named-user terms may not allow reuse, so have the contract owner confirm. It lines up with items R6, R9, and R10 of `retirement-signoff-checklist.md`.

### customer-expectations.csv (crosswalk XW-004, XW-027)

One row per customer of asset management information: the people and teams whose decisions depend on your data. Pre-filled with eleven common customers and a typical starting point for each; confirm or change it with them.

- `what_they_need_from_itam`, `level_of_detail`, `how_often`: what they need, in how much detail, and how often. Ask them; do not guess.
- `what_we_need_from_them`: what you need back, such as leaver triggers from HR or contract terms from Legal.
- `how_we_deliver` and `measure_of_success`: how they get it, and how you would know you served them well.
- `owner` and `last_confirmed_on`: who looks after this customer, and when you last checked the need is still right.

Use it in the first month, and again when a new team starts to rely on your data. It tells you what to collect and what you can stop collecting.

### what-good-looks-like.md (crosswalk XW-025, XW-027)

A worksheet for deciding how far your program needs to go. Eight yes-or-no questions about regulation, audit exposure, spend, subscriptions, change, data, capacity, and sponsorship suggest which dimensions need a higher target. Then write a one-line good-enough statement, pick up to five measures, and list what you will not do yet. Full conformance to a standard is optional and the standard's tiers are informative, so this is how you aim for what is right for you. Use it before you set the To-Be levels.

### rolling-internal-check.md and internal-check-log.csv (crosswalk XW-020, XW-025)

A small, regular test of how the program really works, so an external audit holds no surprises. Test two or three areas each quarter: take a sample, test each record against a rule, log each failure, fix it, and retest. The document lists seven areas with a simple test, a suggested sample size, and a pass rule, and a four-quarter rotation. The CSV is the findings log.

- `quarter`, `area`, `test`, `sample_size`, `records_failed`: what you tested and what failed.
- `finding` and `severity`: what was wrong, and your own rating of how serious it is. Define the scale the first time you use it.
- `owner`, `due_on`, `retested_on`, `result`, `evidence_ref`: who fixes it, by when, and the retest that closes it. A finding is closed only when a retest passes.

See `examples/internal-check-log-example.csv` for two Halden findings.

### setup-prompts.md (crosswalk XW-025)

Thirteen copy-and-paste prompts that walk you through setting up with an AI assistant: set the scene, baseline the program, map a process, choose where data lives, back licenses with proof, control renewals, prepare for an audit, draft governance and policy, turn the plan into reminders, report to leaders, map your customers, decide what good looks like, and plan rolling internal checks. Each prompt names the file to attach, the decision you keep, and what a good result looks like. They work in plain chat, and use the kit's skills where those are installed. Practice on the Halden demo estate first, and keep real inventories off public tools.

### operating-calendar.md (crosswalk XW-002, XW-004, XW-008, XW-025)

A schedule and a starter plan. It lists the monthly, quarterly, and yearly routines for the other files, the events that start an extra task (a purchase request, an invoice, a retirement, an audit letter), and a table that places the first 90 days against the playbook's steps. Give each routine a named owner and a calendar date. The frequencies are suggestions; adjust them to your size and risk.

### application-management-self-assessment.md and application-management-gap-plan.csv (crosswalk XW-003, XW-025)

A self-assessment for the application management program as a whole, with an As-Is state and a To-Be state for each of eleven dimensions: policy, roles and ownership, inventory, intake, lifecycle review, licenses and renewals, cost and rationalization, risk, retirement, measures, and communication. The document defines a four-level scale (0 to 3) and what levels 1, 2, and 3 look like for each dimension. The CSV is where you record the result.

- `as_is_level_0_to_3` and `as_is_evidence`: where you are now, and the evidence you could show. If you cannot show it, score one level lower.
- `to_be_level_0_to_3` and `to_be_reason_and_date`: where you need to be, why, and by when. Not every dimension needs level 3.
- `gap`: To-Be minus As-Is. Rank by the risk or cost of leaving it.
- `priority`, `owner`, `first_action`, `due_on`: the plan. Close no more than three gaps at a time.
- `reviewed_on`: the date you last re-scored the row. Repeat the assessment at least yearly.

See `examples/application-management-gap-plan-example.csv` for a worked example on the Halden demo estate. It complements the tier self-assessment (a standard's tiers) and the `itam-maturity` method (nine areas scored with evidence). Neither records a target state, so this is the one that produces a plan.

### source-of-truth-map.csv (crosswalk XW-001, XW-005, XW-026)

One row per kind of data. Pre-filled with ten common kinds; add your own.

- `authoritative_system`: the one system that wins when two disagree. Name it once; "both" is not an answer.
- `data_owner`: the role accountable for that data being right.
- `other_systems_holding_copies` and `how_copies_are_kept_in_step`: where the same data also lives, and whether it is synced automatically, by import, or by hand.
- `reconcile_every`, `last_reconciled_on`, `mismatches_found`, `mismatch_owner`: how often you compare the copies, when you last did, what differed, and who fixes it.

Keep the register of record where the decisions are made, and link to specialist systems rather than copying their data into it.

### documentation-gaps-log.csv (crosswalk XW-006, XW-007, XW-020, XW-026)

One row per missing or weak record. Compliance is judged on what you can show. A missing proof of purchase is a gap to log and close.

- `record_type`: proof of purchase, contract, certificate, license agreement, retirement record, and so on.
- `related_asset_or_contract`: the application, license id, or contract the record belongs to.
- `what_is_missing` and `why_it_matters`: say what you cannot show, and what that stops you doing.
- `blocks`: audit, renewal, retirement, or true-up. This sets the priority.
- `owner`, `found_on`, `due_on`, `status`, `closed_on`, `evidence_ref`: who closes it, when it was found, the target date, its state, and where the closing evidence is filed.

Review the log with the audit-readiness check. A gap with no owner and no date is a finding in itself.

### vendor-scorecard.csv (crosswalk XW-013)

One row per strategic supplier per review period. It sits beside `vendor-contract-register.csv`: the register says what the contract is; the scorecard says how the supplier is performing.

- `vendor_id`: matches the same id in the contract register.
- `issue_meetings_to_resolve`: how many meetings it took to settle problems this period.
- `response_within_agreed_time`: yes or no, against the response time the contract sets.
- `contact_list_current_on`: the date you last checked the supplier's contact details were right.
- `contract_obligations_met`: yes, no, or partly, and say which obligation in `notes`.
- `rating_1_to_5`: your own scale, defined in `notes` the first time you use it. It is not taken from a standard.

Hold supplier reviews on a schedule, and keep a library of significant interactions so the next negotiator has the history.

### retirement-signoff-checklist.md (crosswalk XW-010, XW-012, XW-020)

A checklist completed before an application or device is closed out as retired. It asks IT, Finance, HR, Procurement, and Legal to confirm their own part, then checks the evidence: license released or reclaimed, data wiped or archived, asset record updated, final cost recorded.

### process-map-worksheet.md (crosswalk XW-004, XW-025)

A worksheet for one process at a time. Describe the Is map first, then the Should map, then list the gaps. The gaps are your scope of work. It also asks you to put scope-expanding requests through a change log, so a small fix does not quietly grow.

### leadership-report.md (crosswalk XW-012, XW-025, XW-027)

A one-page report that links each control to a KPI, the KPI to a decision, and the decision to an outcome in money or risk. It also answers six questions leaders ask. Keep the KPI set to five or fewer, each with a target and an action when it is missed.

### audit-response-roles.csv (crosswalk XW-004, XW-020)

Pre-filled with twelve audit-response tasks that match the `audit-response` method. For each, name the role, the primary holder, and a backup.

- `backup_holder` and `backup_ready`: a backup who has not been briefed does not count. Fill `backup_ready` with yes, no, or the date they were last walked through the task.
- `single_person_risk`: yes where there is no backup, or the backup is the same person. Aim for no.
- `decision_authority` and `escalates_to`: who decides, and where a dispute goes.

Keep two versions of the roster: one with roles only, which survives staff changes, and one with names and phone numbers, which is the one you use in a hurry.

## Limits

These are templates, not a platform. They do not discover installs, read vendor license terms, or tell you what a license permits. They do not interpret contracts or give legal advice; verify license terms against the contract and ask counsel where a term is unclear. A proof-of-purchase check shows what you can document, not what a vendor will accept in an audit. A governance decision still needs a person to make it.
