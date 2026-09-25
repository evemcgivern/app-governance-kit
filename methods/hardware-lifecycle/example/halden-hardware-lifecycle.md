# Hardware Lifecycle Check — devices.csv (checked_on 2026-09-01)

## Inputs confirmed

All 60 devices have an id, type, owner, and status. All 50 active devices carry a refresh-due date; all 10 retired devices carry a retirement date and a data-wipe-confirmed value (yes/no). No missing owners, statuses, or dates found — no gaps to chase for step 1–2 [[XW-001]].

**Unverified:** `devices.csv` has no vendor-contract or warranty-terms field (the `template.csv` output schema has a `vendor_contract_checked` column, but the input doesn't), so the vendor/warranty check called for before any replacement decision [[XW-013]] has not been done here — it needs a separate pull from procurement.

**Unverified:** `cost_usd` in the input isn't labeled as original deployment cost vs. a current replacement quote. I've treated it as original cost and estimated a replacement range from it; the range is not a vendor quote.

## Devices needing action

| id | type | status | issue | recommendation |
|---|---|---|---|---|
| DEV-008 | server | active | Refresh overdue — due 2026-03-05, ~6 months past checked_on (2022-10-22 deploy → long-service server) | Like-for-like replacement likely warranted given server age and cost; short extension only if vendor support is confirmed still active. **Decision needed:** asset owner |
| DEV-027 | mobile | active | Refresh overdue — due 2026-03-05 | Mobile devices depreciate and lose support fastest; recommend replacement over extension. **Decision needed:** asset owner |
| DEV-045 | laptop | active | Refresh overdue — due 2026-03-05 (2023-03-21 deploy, ~3 years in service) | Replacement or upgrade reasonable; extension only if condition/warranty support it. **Decision needed:** asset owner |
| DEV-011 | mobile | retired | Retired 2023-02-19, data wipe **not** confirmed | Certified mobile wipe (remote wipe/factory reset with verification) or destruction certificate from ITAD vendor. Disposal cannot be closed out without evidence. **Decision needed:** disposal accountable owner |
| DEV-042 | desktop | retired | Retired 2025-01-09, data wipe **not** confirmed | Certified drive wipe (e.g., NIST 800-88 clear/purge) or physical destruction with certificate of destruction. Disposal cannot be closed out without evidence. **Decision needed:** disposal accountable owner |

Reasoning: refresh-due dates were compared against `checked_on` (2026-09-01) for all 50 active devices [[XW-001]] [[XW-010]]; only these three fall before that date. All 10 retired devices' `data_wipe_confirmed` values were checked [[XW-010]]; only these two are not "yes."

## Refresh cost summary (grouped by type)

| type | overdue devices | recorded cost | estimated replacement range |
|---|---|---|---|
| server | 1 (DEV-008) | $7,384 | **Unverified:** ~$7,000–$9,000 |
| laptop | 1 (DEV-045) | $1,785 | **Unverified:** ~$1,700–$2,100 |
| mobile | 1 (DEV-027) | $1,071 | **Unverified:** ~$950–$1,200 |
| **Total** | **3** | **$10,240** | **Unverified: roughly $9,650–$12,300** |

This is a range, not a commitment [[XW-012]] — actual quotes need procurement's current vendor pricing and any warranty/trade-in terms before a purchase order is placed [[XW-013]]. **Decision needed:** budget owner to confirm this range against available budget before any order.

## Disposal-blocking list

Two retired devices cannot be marked disposed until wipe or destruction evidence is attached [[XW-010]]:

- **DEV-011** (mobile, retired 2023-02-19)
- **DEV-042** (desktop, retired 2025-01-09)

The other 8 retired devices (DEV-005, DEV-018, DEV-024, DEV-029, DEV-035, DEV-048, DEV-053, DEV-059) show a confirmed "yes" wipe and are not blocking disposal.

## Summary

- **60 devices reviewed** — 50 active, 10 retired.
- **3 overdue-refresh devices** (1 server, 1 laptop, 1 mobile), estimated replacement cost range **~$9,650–$12,300** (unverified against current vendor pricing).
- **2 retired devices blocking disposal** for lack of confirmed data wipe (DEV-011, DEV-042).
- **Decision needed** from the asset owner on replace/upgrade/extend for each overdue device, and from whoever is accountable for disposal on wipe/destruction method for each unwiped device — see table above.

```findings
[
  {"type": "overdue_refresh", "id": "DEV-008"},
  {"type": "overdue_refresh", "id": "DEV-027"},
  {"type": "overdue_refresh", "id": "DEV-045"},
  {"type": "unwiped_retired_device", "id": "DEV-011"},
  {"type": "unwiped_retired_device", "id": "DEV-042"}
]
```
