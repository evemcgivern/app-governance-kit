# Data sources guide

How to get the data that playbook steps 7 and 8 need: a record of what you run, and a count of who uses it. You will pull from five places and then clean the names so the counts match. No single source is complete; use all five to start.

Clause references are to ISO/IEC 19770-1:2017 (paraphrased) and to the shared crosswalk (`XW-` rows). This guide does not name or recommend any tool. Use whatever your organization already has.

**Owner:** ______________________  **Date:** ___________

## Before you ask anyone

Write down the question first. A request for "the list of installed software on laptops, as a spreadsheet, once" gets an answer.

| Question | Best first source | Feeds |
| --- | --- | --- |
| What is installed or running? | Discovery or inventory tool output | `asset-record.csv`, `proof-of-purchase-check.csv` [[XW-005]] |
| Who signs in to a cloud app? | Sign-in or single sign-on logs | `license-position.csv` [[XW-007]] |
| What do we pay for? | Expense and accounts-payable data | `renewal-calendar.csv`, `source-of-truth-map.csv` [[XW-012]] |
| What did we buy, and on what terms? | Purchasing and contract records | `proof-of-purchase-check.csv`, `contract-terms-check.csv` [[XW-006]] |
| Who joined, moved, or left? | HR joiner and leaver lists | `joiner-mover-leaver-procedure.md` [[XW-017]] |

## The five sources

### 1. Discovery or inventory tool output

- **How to get it:** Ask the team that runs the tool for an export of installed software by device, as a CSV file. Ask for the date it was taken and the devices it covers.
- **What it tells you:** What is installed, on which device, and often the version and the last time it ran.
- **What it cannot tell you:** What you are licensed for. Devices that never checked in. Software that runs only in a browser or as a service. Whether an install is authorized.
- **Who to ask:** The endpoint or infrastructure team.
- **Check before you use it:** How many devices are in the export, and how many devices IT thinks exist. A gap means part of the estate is missing. Note the gap in `documentation-gaps-log.csv`.

### 2. Sign-in or single-sign-on logs for cloud apps

- **How to get it:** Ask the identity team for a report, per app, of each user and the date of their last sign-in, for the last 90 days. Ask for user names, not only counts, so you can match them to HR lists.
- **What it tells you:** Who has used a cloud app recently, and who has an account but has not signed in.
- **What it cannot tell you:** Use that happens outside single sign-on, such as a personal login or a shared account. What the person did in the app. Whether the account type matches what you pay for.
- **Who to ask:** The identity or access management owner.
- **Check before you use it:** Is the app set up to use single sign-on at all? If not, the log is empty and says nothing about use.

### 3. Expense and accounts-payable data

- **How to get it:** Ask Finance for twelve months of payments to suppliers, with supplier name, amount, date, and cost center. Ask separately for expense-card spend. Software bought on a card may not appear in the contract files.
- **What it tells you:** What you pay for and to whom, including products no one in IT knows about. Which suppliers are your largest by spend.
- **What it cannot tell you:** What you bought, how many licenses, or what term. A payment line often names only a supplier.
- **Who to ask:** Finance or accounts payable.
- **Check before you use it:** Sort by supplier and look at the long tail of small payments. These are the ones most likely to be missing from every other source. [[XW-012]]

### 4. Purchasing and contract records

- **How to get it:** Ask Procurement for purchase orders and the contract register. Ask Legal where signed contracts are filed. Pull the invoice behind each large payment.
- **What it tells you:** The quantity, metric, term, and price you agreed. The notice period and whether the contract renews on its own. These are the proofs behind a license position. [[XW-006]]
- **What it cannot tell you:** What is in use. A contract on file does not show that anyone installed the product.
- **Who to ask:** Procurement, then Legal. Have the contract owner confirm what a term means. Do not decide it from the invoice. [[XW-013]]
- **Check before you use it:** Does each large payment from source 3 have a matching order or contract? List the ones that do not in `documentation-gaps-log.csv`.

### 5. HR joiner and leaver lists

- **How to get it:** Ask HR for a list of current employees with a start date and, for leavers, an end date. Ask what each person's job role and department is. Ask how often the list can be refreshed.
- **What it tells you:** Who should have an account today, and who should not. It is how you find accounts that belong to people who left.
- **What it cannot tell you:** Contractors, temporary staff, and service accounts, which are often not on an HR list. Which apps a person needs.
- **Who to ask:** HR. Treat the list as personal data. Ask only for the fields you need, keep it in a restricted place, and agree with HR how long you may hold it. **Decision needed:** HR and counsel for the retention period.
- **Check before you use it:** Does the list use the same person identifier as the sign-in logs, such as a work email address? If not, settle on a way to match them before you start.

## Clean the names so the counts match

The same product shows up under several names. Discovery may say `Northbeam ERP 2024`, the invoice may say `NORTHBEAM INC - ERP SUBSCRIPTION`, and the contract may say `Northbeam Enterprise Resource Planning`. Counts only match when all three resolve to one publisher and one product. [[XW-026]]

1. Export every source to a spreadsheet, one tab each, with the raw name as it came.
2. Make one new tab called the name map, with columns for raw name, clean publisher, clean product, version, and `asset_id`.
3. Start with your five largest publishers by spend from source 3. Do not try to clean everything. [[XW-005]]
4. Clean the publisher first. Ignore case and punctuation, and drop company-form words such as Inc or Ltd. Then clean the product: drop edition and marketing words that do not change the license, and keep the version.
5. For each raw name, find or create its clean publisher, clean product, and version, and write them in the name map. Give each clean product an `asset_id` from `asset-record.csv`. Use the same `asset_id` in `license-position.csv`, `proof-of-purchase-check.csv`, and `renewal-calendar.csv`.
6. List every raw name you could not match. Leave them on the list; do not guess. Ask the owner of the source what the name refers to.
7. Keep the name map. Next quarter you add only the new names.

A worked line for Halden Logistics:

| Raw name | Source | Clean publisher | Clean product | Version | asset_id |
| --- | --- | --- | --- | --- | --- |
| Northbeam ERP 2024 | Discovery | Northbeam | Northbeam ERP | 2024 | APP-001 |
| NORTHBEAM INC - ERP SUBSCRIPTION | Accounts payable | Northbeam | Northbeam ERP | Not found | APP-001 |

A version number matters. Two versions of one product can fall under different license terms, so do not merge them until you have checked.

## Good enough to start

You are ready to build the inventory and a first license position when all of these are true:

- [ ] You have at least one export from each of the five sources, each with a date on it.
- [ ] The five largest publishers by spend each have a clean name and an `asset_id` for each product.
- [ ] You know how many devices the discovery export covers and how many devices IT believes exist, and you have written the gap down.
- [ ] Each leaver on the HR list has been compared with the sign-in logs, and the matches and misses are noted.
- [ ] Every raw name you could not match is on a list with an owner.
- [ ] You have written down what each source cannot tell you, so no one reads more into the numbers than they hold.

If one source is out of reach, start without it, record the gap in `documentation-gaps-log.csv` with an owner and a date, and say in the position which numbers rest on it.

## Decision

| Decision | Owner | Approver | Date |
| --- | --- | --- | --- |
| Data accepted as good enough to build the first position | | | |

Source: ISO/IEC 19770-1:2017 clauses 8.3 and 8.4, and the shared crosswalk. Paraphrased; this is not a substitute for the standard.
