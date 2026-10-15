# Application governance router: sample request on the Halden estate

**Request:** "Our auditors want to know where we stand on software licenses next quarter."

## Routing note

The decision is an audit-readiness position by next quarter, so the closest skill is `rationalization` (it checks license state and duplicates). The ITAM maturity check is the second candidate, because an auditor will also ask how the process is run [[XW-025]]. I'll run the first and offer the second.

**Data needed:** `licenses.csv` and `apps.csv`. Both are Halden demo files.

## Result from `rationalization` (summary)

- Two licenses have expired while the apps are still in use: LIC-044 (Payflow, expired 2025-12-31) and LIC-017 (Meetrix, expired 2026-03-31) [[XW-008]].
- **Unverified:** a user count is not the same as licensed seats or installs, so recorded users above entitlements point to a problem without proving a shortfall [[XW-007]].

**Decision needed:** whether to renew or shut down LIC-017 and LIC-044, and who owns that call.

## Follow-up offered

Run `itam-maturity` next to score the license and renewal process. Not run without your agreement.

This kit gives methods and reasoning support. It is not a governance platform, a certification, or legal advice.

```findings
[
  {"type": "routing", "id": "rationalization"}
]
```
