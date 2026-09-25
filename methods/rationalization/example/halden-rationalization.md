# Application rationalization: Halden Logistics (2026-09-24)

**Main caveat:** `apps.csv` has no `owner` field. Every one of the 60 apps is **Unverified:** for ownership; this rationalization uses category, cost, and users only, and ownership should be filled in before any Eliminate decision is executed [[XW-002]]. `apps.csv` and `licenses.csv` supply id, category, cost, users, data sensitivity, entitlements, expiry, and `checked_on` (2026-09-01); no vendor contract terms or termination-notice data were supplied [[XW-013]].

## Scoring used

- **Business value:** read from `users` (higher usage = higher value) and whether the category is core to a logistics/transportation operation (e.g. Transport management, Customs brokerage, Freight audit) versus a general back-office function.
- **Technical fit:** Poor if the app is one side of a functional duplicate, or its license has expired; Good otherwise. No installation or dependency data was supplied, so technical fit is scored on those two signals only — **Unverified:** beyond that.

## Duplicates

Five category pairs share a function. Within each pair, technical fit is Poor for both, so the tie-break is cost per user — the cheaper app per user becomes the consolidation target [[XW-011]].

| Pair | Category | Cost/user (higher) | Cost/user (lower) | Keep | Retire |
|---|---|---|---|---|---|
| APP-008 (Clausebase) + APP-041 (Tallysheet) | Contract management | $216.46 (APP-008) | $93.72 (APP-041) | APP-041 | APP-008 |
| APP-014 (Signwell) + APP-052 (Quickink) | E-signature | $394.44 (APP-052) | $48.14 (APP-014) | APP-014 | APP-052 |
| APP-022 (Fleetdesk) + APP-037 (Linkup) | Endpoint management | $106.95 (APP-022) | $57.26 (APP-037) | APP-037 | APP-022 |
| APP-029 (Routewise) + APP-058 (Routesmith) | Transport management | $283.42 (APP-029) | $39.07 (APP-058) | APP-058 | APP-029 |
| APP-033 (Borderline) + APP-046 (Clearport) | Customs brokerage | $253.08 (APP-033) | $11.31 (APP-046) | APP-046 | APP-033 |

**Decision needed:** these are the recommended keep/retire calls; the app owners and architecture still have to confirm neither retired app has a dependency the cheaper one can't cover before consolidation starts [[XW-011]].

## Licenses

Checked against `checked_on` (2026-09-01):

- **LIC-017** (APP-017, Meetrix Video conferencing) expired 2026-03-31 — 5 months lapsed. 649 users.
- **LIC-044** (APP-044, Payflow Accounts payable automation) expired 2025-12-31 — 8 months lapsed. 748 users, confidential data.

No license expires within 90 days of `checked_on` beyond these two. **Unverified:** on paper, entitlements are far below `users` for most apps and far above `users` for a smaller group (e.g. APP-025 Pulseboard: 350 entitlements against 45 users). `users` in this file isn't documented as licensed seats or installs, so I'm treating this pattern as a licence-position question to investigate, not as a proven over- or under-buy [[XW-007]].

Both expired licenses sit on high-usage apps, not duplicates, so the fix is renewal, not elimination — see the TIME table.

## TIME table

| App | Name | Category | TIME | Reason |
|---|---|---|---|---|
| APP-001 | Northbeam ERP | ERP | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-002 | Paylane Payroll | Payroll | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-003 | Staffhub HR information system | HR information system | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-004 | Hirewell Recruiting | Recruiting | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-005 | Coursefield Learning management | Learning management | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-006 | Receiptly Expense management | Expense management | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-007 | Buyline Procurement | Procurement | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-008 | Clausebase Contract management | Contract management | Eliminate | Functional duplicate of APP-041 in Contract management; higher cost per user, retire and consolidate onto APP-041. |
| APP-009 | Relato CRM | CRM | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-010 | Campaignly Marketing automation | Marketing automation | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-011 | Helpwise Customer support desk | Customer support desk | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-012 | Chattera Live chat | Live chat | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-013 | Pollform Survey | Survey | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-014 | Signwell E-signature | E-signature | Tolerate | Keep: lower cost per user than duplicate APP-052 in E-signature; becomes the consolidation target. |
| APP-015 | Docuvault Document management | Document management | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-016 | Hallway Intranet | Intranet | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-017 | Meetrix Video conferencing | Video conferencing | Invest | License LIC-017 expired but app is high-usage (649 users); renew, don't lose the app over a lapsed contract. |
| APP-018 | Threadly Team chat | Team chat | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-019 | Taskmoor Project management | Project management | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-020 | Shapewise Diagramming | Diagramming | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-021 | Keyfort Password manager | Password manager | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-022 | Fleetdesk Endpoint management | Endpoint management | Eliminate | Functional duplicate of APP-037 in Endpoint management; higher cost per user, retire and consolidate onto APP-037. |
| APP-023 | Shieldline Antivirus | Antivirus | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-024 | Vaultline Backup | Backup | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-025 | Pulseboard Monitoring | Monitoring | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-026 | Servicely IT service management | IT service management | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-027 | Gatekey Identity provider | Identity provider | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-028 | Stackyard Warehouse management | Warehouse management | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-029 | Routewise Transport management | Transport management | Eliminate | Functional duplicate of APP-058 in Transport management; higher cost per user, retire and consolidate onto APP-058. |
| APP-030 | Trackmile Fleet telematics | Fleet telematics | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-031 | Pathcraft Route optimization | Route optimization | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-032 | Dockside Yard management | Yard management | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-033 | Borderline Customs brokerage | Customs brokerage | Eliminate | Functional duplicate of APP-046 in Customs brokerage; higher cost per user, retire and consolidate onto APP-046. |
| APP-034 | Ratecheck Freight audit | Freight audit | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-035 | Tradelink EDI gateway | EDI gateway | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-036 | Loadboard Carrier portal | Carrier portal | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-037 | Linkup Endpoint management | Endpoint management | Tolerate | Keep: lower cost per user than duplicate APP-022 in Endpoint management; becomes the consolidation target. |
| APP-038 | Foresight Demand forecasting | Demand forecasting | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-039 | Chartwell Business intelligence | Business intelligence | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-040 | Lakeshore Data warehouse | Data warehouse | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-041 | Tallysheet Contract management | Contract management | Tolerate | Keep: lower cost per user than duplicate APP-008 in Contract management; becomes the consolidation target. |
| APP-042 | Pipewright ETL | ETL | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-043 | Cellmate Spreadsheet add-in | Spreadsheet add-in | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-044 | Payflow Accounts payable automation | Accounts payable automation | Invest | License LIC-044 expired but app is high-usage (748 users); renew, don't lose the app over a lapsed contract. |
| APP-045 | Cashmere Treasury | Treasury | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-046 | Clearport Customs brokerage | Customs brokerage | Tolerate | Keep: lower cost per user than duplicate APP-033 in Customs brokerage; becomes the consolidation target. |
| APP-047 | Levywise Tax compliance | Tax compliance | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-048 | Trailmark Audit management | Audit management | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-049 | Controlroom GRC | GRC | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-050 | Rulebook Policy management | Policy management | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-051 | Safeyard Health and safety | Health and safety | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-052 | Quickink E-signature | E-signature | Eliminate | Functional duplicate of APP-014 in E-signature; higher cost per user, retire and consolidate onto APP-014. |
| APP-053 | Frontdesk Visitor management | Visitor management | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-054 | Roomly Facilities booking | Facilities booking | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-055 | Scanwright Invoice OCR | Invoice OCR | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-056 | Askbay Chatbot | Chatbot | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-057 | Mailguard Email security | Email security | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-058 | Routesmith Transport management | Transport management | Tolerate | Keep: lower cost per user than duplicate APP-029 in Transport management; becomes the consolidation target. |
| APP-059 | Clickpath Web analytics | Web analytics | Tolerate | No duplicate, license, or usage problem found; keep as-is. |
| APP-060 | Commitly Code repository | Code repository | Tolerate | No duplicate, license, or usage problem found; keep as-is. |

## Savings and risk summary

- **Eliminate:** APP-008, APP-022, APP-029, APP-033, APP-052 — combined annual cost **$355,400**.
- **Migrate:** none. No app showed a technical-replatform need that stopped short of full elimination; every duplicate resolves by retiring one side outright.
- **Potential savings:** **$250,000–$355,400 a year**, not a promise. The low end assumes vendor notice periods and a wind-down period eat into year-one savings; the high end assumes clean, immediate termination. **Unverified:** actual contract terms, since none were supplied [[XW-013]] [[XW-012]].

**Top risks of acting:**
1. Retiring the wrong side of a pair without checking for an undocumented dependency (no CMDB or integration data was supplied) [[XW-011]].
2. Executing a retirement before ownership is confirmed — every app is currently Unverified for owner, so there's no one accountable to sign off the retirement or the data disposition [[XW-002]] [[XW-010]].
3. Losing LIC-017 or LIC-044's app entirely by treating an expired license as a retirement trigger instead of a renewal one — both apps are high-usage and neither is a duplicate [[XW-008]].
4. Vendor contracts for the five Eliminate apps may carry termination penalties or notice periods that shrink the savings range; none of that data was supplied [[XW-013]].

## Data held by Eliminate apps

**Decision needed:** the data owner's disposition call for each of the following. All five retiring apps carry `internal`, not `confidential`, data sensitivity, which supports archiving over an immediate delete, but the owner still has to set the retention period [[XW-028]] [[XW-010]]:

| App | Category | Data sensitivity | Recommended disposition |
|---|---|---|---|
| APP-008 Clausebase | Contract management | internal | Archive contract records for the standard retention period, then delete; confirm no live contract still references Clausebase before archiving. |
| APP-022 Fleetdesk | Endpoint management | internal | Migrate managed-device records into APP-037 (Linkup) before decommissioning; archive anything Linkup doesn't import. |
| APP-029 Routewise | Transport management | internal | Migrate open routes and shipment records into APP-058 (Routesmith); archive historical records after cutover. |
| APP-033 Borderline | Customs brokerage | internal | Migrate open customs filings into APP-046 (Clearport) before cutover; archive closed filings for the regulatory retention period. |
| APP-052 Quickink | E-signature | internal | Archive completed signature records for the standard retention period; confirm no signature request is still in flight before shutdown. |

```findings
[
  {"type": "duplicate_app", "id": "APP-008+APP-041"},
  {"type": "duplicate_app", "id": "APP-014+APP-052"},
  {"type": "duplicate_app", "id": "APP-022+APP-037"},
  {"type": "duplicate_app", "id": "APP-029+APP-058"},
  {"type": "duplicate_app", "id": "APP-033+APP-046"},
  {"type": "expired_license", "id": "LIC-017"},
  {"type": "expired_license", "id": "LIC-044"}
]
```
