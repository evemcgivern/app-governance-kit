# Tier self-assessment

A short check of how far your IT asset management has got, using the three tiers in ISO/IEC 19770-1:2017 Annex B. The tiers are cumulative: tier 2 expects tier 1, and tier 3 expects both. Use this as a starting point before the full ITAM maturity check.

**How to use it:** answer each question yes, partly, or no, and write down the evidence you could show an auditor. A tier counts as met when no question is a "no" and at most one is "partly". Your assumed tier is the highest tier you meet, along with every tier below it. The first tier you do not meet is your next piece of work.

The Annex B tier names and aims are summarized here. Which Annex A processes sit in which tier is shown in Figure B.2 of the standard. Check that figure in your copy before using this to scope a certification.

## Tier 1: Trustworthy data ("know what you have")

Aim: know what you have so you can manage it, with reasonable assurance of license compliance.

| # | Question | Yes / partly / no | Evidence |
| --- | --- | --- | --- |
| 1.1 | Is there a record for every software and hardware asset in scope, with an owner? (8.3, 7.6.2) **NOTE:** if owner is missing for any, choose Partly | | |
| 1.2 | Does each record say whether the asset is authorized? (8.3) | | |
| 1.3 | Are records verified against what is actually installed or in use, on a schedule? (8.3) | | |
| 1.4 | Do you hold entitlement records for the licenses you own, each backed by a proof of purchase kept as long as the records schedule requires? (8.4) | | |
| 1.5 | Do you compare entitlements with usage on a schedule, and act on the gaps? (8.4) | | |
| 1.6 | Is there a measurable target for data accuracy? (6.2.3) | | |
| 1.7 | Are changes to the asset record controlled? (8.2) | | |
| 1.8 | Are security and access controls applied to the asset data itself? (8.5) | | |

## Tier 2: Life cycle integration ("greater efficiency across the life cycle")

Aim: greater efficiency and cost-effectiveness across the asset life cycle.

| # | Question | Yes / partly / no | Evidence |
| --- | --- | --- | --- |
| 2.1 | Do requests go through a specification and approval step before purchase? | | |
| 2.2 | Is every acquisition recorded when it happens, not later? | | |
| 2.3 | Do release and deployment steps update the asset record? | | |
| 2.4 | Is use of assets monitored, including for cost-effectiveness? | | |
| 2.5 | Is retirement a defined step with disposal and record keeping? | | |
| 2.6 | Are authorizations and their execution logged (who, when, why)? (7.6.3) | | |

## Tier 3: Optimization ("focus on cross-cutting processes")

Aim: greater efficiency and effectiveness through the cross-cutting functional processes.

| # | Question | Yes / partly / no | Evidence |
| --- | --- | --- | --- |
| 3.1 | Are supplier relationships and contracts managed, including compliance with terms beyond licensing? (8.7) | | |
| 3.2 | Are asset costs and values tracked and tied to budgets? | | |
| 3.3 | Are the service levels that ITAM depends on defined and recorded? | | |
| 3.4 | Are risks not covered elsewhere managed, with the treatment checked? (6.1.2, 6.1.3) | | |
| 3.5 | Is ITAM performance measured and reported, financial and non-financial? (9.1) | | |

## Work out your tier

Count your answers for each tier, then check the last column. The web page and the Excel workbook do this for you; in Word, count by hand.

| Tier | Yes | Partly | No | Met? (no "no", at most one "partly") |
| --- | --- | --- | --- | --- |
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

Your assumed tier: the highest tier you met, where every tier below it is also met. If tier 1 is not met, you are below tier 1.

## Gap report

List every question you answered "no" or "partly", with the step that closes it. The web page builds this from your answers, and the Excel workbook has a Gap report sheet you can filter. In Word, write your answer in the third column and delete the rows you do not need.

| # | Question | Your answer | What closes the gap | Owner | Due date |
| --- | --- | --- | --- | --- | --- |
| 1.1 | A record for every asset, with an owner | | Build one record per asset in scope and name an owner for each. Start from the asset record template. | | |
| 1.2 | Each record says whether the asset is authorized | | Add an authorized yes/no field to every record and fill it from purchase and approval evidence. | | |
| 1.3 | Records verified against what is installed | | Set a schedule (at least quarterly) to compare records with discovery data, and log the differences found. | | |
| 1.4 | Entitlement records held | | Collect licenses, contracts, and proofs of purchase into one entitlement list per product. | | |
| 1.5 | Entitlements compared with usage | | Run the license position workbook on a schedule and give each shortfall or surplus an owner. | | |
| 1.6 | A measurable target for data accuracy | | Pick a measurable accuracy target, such as the share of records verified this quarter, and report against it. | | |
| 1.7 | Changes to the asset record controlled | | Require an authorization entry before any record changes, and log who changed what and when. | | |
| 1.8 | Security applied to the asset data | | Limit who can view and edit the asset data, and review that access on a schedule. | | |
| 2.1 | Specification and approval before purchase | | Add a request step that records the need and an approval before any purchase. | | |
| 2.2 | Acquisitions recorded when they happen | | Make creating the asset record a step of buying, not a later cleanup. | | |
| 2.3 | Release and deployment update the record | | Add a record-update step to the release and deployment checklists. | | |
| 2.4 | Use monitored, including cost-effectiveness | | Track usage for each major asset and review its cost against its value on a schedule. | | |
| 2.5 | Retirement is a defined step | | Write a retirement procedure that covers disposal, data removal, and closing the record. | | |
| 2.6 | Authorizations and their execution logged | | Use the authorization log template for approvals and for who carried them out. | | |
| 3.1 | Suppliers and contracts managed | | Keep a vendor and contract register, and check compliance with contract terms as well as licensing. | | |
| 3.2 | Costs and values tied to budgets | | Record the cost and value of each asset and tie them to budget lines. | | |
| 3.3 | Service levels defined | | List the services ITAM depends on and record the agreed service level for each. | | |
| 3.4 | Other risks managed | | Run an ITAM risk assessment, record the treatment for each risk, and check that it worked. | | |
| 3.5 | Performance measured and reported | | Define financial and non-financial ITAM measures and report them to management on a schedule. | | |

## Result

| Tier | Mostly yes? | Biggest gap | Owner | Next step | Date |
| --- | --- | --- | --- | --- | --- |
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

Source: ISO/IEC 19770-1:2017, Annex A (processes) and Annex B (tiers). Paraphrased; this is not a substitute for the standard.
