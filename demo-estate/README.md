# Halden Logistics Demo Estate

Halden Logistics is a fictional logistics and transportation company created for testing and demonstration purposes. The demo estate contains twelve generated data files representing a complete software and AI governance scenario with deliberately planted problems for tools to discover and correct.

**Generated files:**
- `apps.csv`: id, name, vendor, category, annual_cost_usd, users, data_sensitivity — 60 applications with confidential and internal sensitivity levels
- `licenses.csv`: id, app_id, entitlements, expiry, checked_on — licensing records (checked_on: 2026-09-01)
- `employees.csv`: id, status, termination_date — 80 employee records with active and terminated statuses
- `accounts.csv`: id, employee_id, app_id, role, last_login — 120 user accounts linking employees to applications
- `ai-systems.csv`: id, owner, description — 6 AI systems in use across the organization
- `maturity-answers.csv`: area, label, score — ITAM maturity assessment scores across 9 governance areas
- `devices.csv`: device_id, type, vendor, owner, deploy_date, refresh_due_date, status, retirement_date, data_wipe_confirmed, cost_usd, checked_on — 60 devices
- `proofs-of-purchase.csv`: proof_id, license_id, product, version, quantity, license_metric, license_model, vendor, buyer_entity, purchase_date, term_start, term_end, price_usd, payment_proof, license_type, upgrade_base, upgrade_chain_complete, evidence_location — six proofs for the audit scenario. `purchase_date` and `price_usd` are from the first order. For a subscription, the term is the current subscription term; for a perpetual license, it is the current support term. Both end on the expiry in `licenses.csv`. `upgrade_base` names the qualifying license an upgrade uses up.
- `audit-installs.csv`: license_id, product, version, license_metric, installs_counted, count_in_metric, first_install_date, checked_on — discovery for the audit scenario. `count_in_metric` is the number to reconcile: assigned users for a named-user product, devices for a device product.
- `audit-letter.md`: a fictional publisher audit letter with Halden's notes on its agreement
- `controls.md`: 3 sample controls for mapping to external frameworks
- `council-draft.md`: A draft software governance council charter with intentional gaps

The `answer-key.json` file contains the authoritative list of planted problems (duplicates, expired licenses, orphaned accounts, high-risk AI systems, overdue devices, audit-response proof problems, maturity gaps, control mappings, and charter flaws) organized by tool and problem type. This file is for grading tool outputs only and must never be given to a tool under test.
