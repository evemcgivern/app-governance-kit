# Lifecycle

## How it works together

The lifecycle is the spine every application travels, from a first request to retirement. The governance council owns the gate between each pair of stages, and delegates routine calls below its threshold. Each stage's questions and rules are handled by a specific kit tool. Every rule below names the crosswalk row it satisfies, so each decision traces back to a control. Review and optimize is where the loop branches: most applications feed back into Plan to be reinvested in or replaced, while the rest move forward into Retire, which closes the loop by freeing licenses, data, and budget for the next Plan.

## plan — Plan and request

- **What happens:** A request is written up: the problem, the owner, and any AI risk.
- **Gate to move on:** The council or its delegate approves the request and assigns an owner.
- **Hands off to:** acquire — the approved request becomes the basis for a purchase.
- **Who decides:** The application owner drafts it; the council or its delegate approves it.

### Rules that apply

- Nothing is bought or built above the council's threshold without an approved request. [[XW-027]]
- Every request names an accountable owner before it moves forward. [[XW-002]]
- A request that duplicates an application already owned is flagged first. [[XW-011]]
- Any AI component is flagged at intake for a risk-tier assessment. [[XW-021]]
- The data the application will hold, and its sensitivity, is recorded early. [[XW-028]]

## acquire — Acquire

- **What happens:** The approved request becomes a purchase: license chosen, contract negotiated, supplier assessed.
- **Gate to move on:** Contract signed with audit, renewal, and exit terms reviewed; entitlements recorded.
- **Hands off to:** deploy — the entitlement record and contract travel with the application.
- **Who decides:** Procurement with the application owner; the council above its cost threshold.

### Rules that apply

- Nothing is bought above the council's threshold without an approved request. [[XW-027]]
- Every purchase records its entitlements before deployment starts. [[XW-006]]
- Contracts are checked for audit, renewal, and exit terms before signature. [[XW-013]]
- Any AI supplier and model provider is assessed before the purchase closes. [[XW-023]]

## deploy — Deploy

- **What happens:** The application is installed, added to the inventory, and given access roles.
- **Gate to move on:** The inventory record and access roles are complete before wider rollout.
- **Hands off to:** operate — the live system and its access records carry forward.
- **Who decides:** The application owner, with access approved through the named policy.

### Rules that apply

- The application is recorded in the inventory with owner and data sensitivity. [[XW-001]]
- Access roles are defined, and new access only granted through an approved path. [[XW-015]]
- Privileged and administrative accounts are limited and named individually. [[XW-018]]
- An AI system's inventory record and risk entry are complete before go-live. [[XW-022]]

## operate — Operate

- **What happens:** The application runs day to day: usage tracked, access kept current, records reconciled.
- **Gate to move on:** Installs stay within entitlements and access reviews happen on schedule.
- **Hands off to:** optimize — the running history and asset record get reviewed.
- **Who decides:** The application owner, checked periodically by whoever runs access reviews.

### Rules that apply

- Installed copies and active users are kept within held entitlements. [[XW-007]]
- Access is reviewed on schedule, and leavers are removed promptly. [[XW-016]]
- Asset records are reconciled against what is actually installed. [[XW-026]]
- A changed AI system's use is reassessed, not assumed unchanged. [[XW-021]]

## optimize — Review and optimize

- **What happens:** The portfolio is reviewed to decide whether each application still earns its cost.
- **Gate to move on:** The owner or council records a decision: keep, invest, migrate, or retire.
- **Hands off to:** plan, retire — reinvest or replace starts a new request; otherwise retire begins.
- **Who decides:** The application owner recommends; the council decides above its threshold.

### Rules that apply

- Every application is periodically assessed against tolerate, invest, migrate, or eliminate. [[XW-011]]
- Anything expiring within the review window is flagged before it lapses. [[XW-008]]
- The review checks where the organization's own asset process is weakest. [[XW-025]]
- The council's own decision log is checked for bottlenecks or rubber-stamping. [[XW-025]]

## retire — Retire

- **What happens:** The application is decommissioned: data archived, migrated, or deleted; access and licenses unwound.
- **Gate to move on:** Accounts removed, licenses reclaimed, and the inventory record closed with evidence.
- **Hands off to:** plan — the freed licenses, data capacity, and budget go to the next request.
- **Who decides:** The application owner executes; the council confirms closure above its threshold.

### Rules that apply

- What happens to the application's data is decided and recorded, not left implicit. [[XW-028]]
- All accounts tied to the application are removed and licenses reclaimed. [[XW-017]]
- The contract is ended on schedule, with any auto-renewal cancelled in time. [[XW-013]]
- The inventory record is formally closed, with evidence retained for audit. [[XW-020]]
