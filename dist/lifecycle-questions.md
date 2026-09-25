# Application lifecycle questions

Questions to ask at each stage. Each names the crosswalk row it satisfies and the kit tool that handles it.

## Plan and request

A request is written up: the problem, the owner, and any AI risk.

Rules that apply:

- Nothing is bought or built above the council's threshold without an approved request. [[XW-027]]
- Every request names an accountable owner before it moves forward. [[XW-002]]
- A request that duplicates an application already owned is flagged first. [[XW-011]]
  - Blocks: Acquire — What license model applies, and how many entitlements do we need?
- Any AI component is flagged at intake for a risk-tier assessment. [[XW-021]]
  - May impact: Deploy — For AI systems: is the inventory record complete and the risk in the register?
- The data the application will hold, and its sensitivity, is recorded early. [[XW-028]]
  - Refers to: Deploy — Is the app in the inventory with owner, category, and data sensitivity?

Gate to move on: The council or its delegate approves the request and assigns an owner.
Hands off to: acquire. the approved request becomes the basis for a purchase.
Who decides: The application owner drafts it; the council or its delegate approves it.

Questions to ask:

- [ ] What problem does this solve, and do we own an app that does it? [[XW-011]] (tool: `rationalization`)
  - May be impacted by: Review and optimize — Is it still worth its cost: tolerate, invest, migrate, or eliminate?
- [ ] Who will own it, and who is the executive sponsor? [[XW-002]] (tool: `program-setup`)
- [ ] Does the request meet the council's threshold and come through the intake path? [[XW-027]] (tool: `program-setup`)
  - Referenced by: Review and optimize — Does the council's decision log show bottlenecks or rubber-stamping?
  - Referenced by: Acquire — Nothing is bought above the council's threshold without an approved request.
- [ ] Does it use AI? If so, what risk tier is it? [[XW-021]] (tool: `ai-intake`)
  - Referenced by: Acquire — Any AI supplier and model provider is assessed before the purchase closes.
- [ ] What data will it hold, and how sensitive is that data? [[XW-028]] (tool: `access-review`)
  - Referenced by: Retire — What data does it hold, and will we archive, migrate, or delete it?

## Acquire

The approved request becomes a purchase: license chosen, contract negotiated, supplier assessed.

Rules that apply:

- Nothing is bought above the council's threshold without an approved request. [[XW-027]]
  - Refers to: Plan and request — Does the request meet the council's threshold and come through the intake path?
- Every purchase records its entitlements before deployment starts. [[XW-006]]
  - Refers to: Operate — Do installs and users stay within entitlements?
- Contracts are checked for audit, renewal, and exit terms before signature. [[XW-013]]
  - May impact: Retire — Is the contract ended on time, without auto-renewal?
- Any AI supplier and model provider is assessed before the purchase closes. [[XW-023]]
  - Refers to: Plan and request — Does it use AI? If so, what risk tier is it?

Gate to move on: Contract signed with audit, renewal, and exit terms reviewed; entitlements recorded.
Hands off to: deploy. the entitlement record and contract travel with the application.
Who decides: Procurement with the application owner; the council above its cost threshold.

Questions to ask:

- [ ] What license model applies, and how many entitlements do we need? [[XW-006]] (tool: `rationalization`)
  - Blocked by: Plan and request — A request that duplicates an application already owned is flagged first.
- [ ] Does the contract give audit, renewal, and exit terms we can live with? [[XW-013]] (tool: `rationalization`)
- [ ] Have the supplier and any AI model provider been assessed? [[XW-023]] (tool: `ai-intake`)
  - Referenced by: Deploy — An AI system's inventory record and risk entry are complete before go-live.
- [ ] Is the purchase recorded against an owner and a cost center? [[XW-012]] (tool: `itam-maturity`)
  - May impact: Review and optimize — Is it still worth its cost: tolerate, invest, migrate, or eliminate?

## Deploy

The application is installed, added to the inventory, and given access roles.

Rules that apply:

- The application is recorded in the inventory with owner and data sensitivity. [[XW-001]]
  - Blocks: Operate — Is access reviewed on schedule, and are leavers removed?
  - Referenced by: Retire — The inventory record is formally closed, with evidence retained for audit.
- Access roles are defined, and new access only granted through an approved path. [[XW-015]]
  - May impact: Operate — Is access reviewed on schedule, and are leavers removed?
- Privileged and administrative accounts are limited and named individually. [[XW-018]]
  - May impact: Operate — Is access reviewed on schedule, and are leavers removed?
- An AI system's inventory record and risk entry are complete before go-live. [[XW-022]]
  - Refers to: Acquire — Have the supplier and any AI model provider been assessed?
  - Referenced by: Operate — Has the AI system's use changed since intake?

Gate to move on: The inventory record and access roles are complete before wider rollout.
Hands off to: operate. the live system and its access records carry forward.
Who decides: The application owner, with access approved through the named policy.

Questions to ask:

- [ ] Is the app in the inventory with owner, category, and data sensitivity? [[XW-001]] (tool: `itam-maturity`)
  - Referenced by: Plan and request — The data the application will hold, and its sensitivity, is recorded early.
- [ ] Are access roles defined, and who approves new access? [[XW-015]] (tool: `access-review`)
- [ ] Are privileged accounts limited and named? [[XW-018]] (tool: `access-review`)
- [ ] For AI systems: is the inventory record complete and the risk in the register? [[XW-022]] (tool: `ai-intake`)
  - May be impacted by: Plan and request — Any AI component is flagged at intake for a risk-tier assessment.

## Operate

The application runs day to day: usage tracked, access kept current, records reconciled.

Rules that apply:

- Installed copies and active users are kept within held entitlements. [[XW-007]]
- Access is reviewed on schedule, and leavers are removed promptly. [[XW-016]]
  - Refers to: Retire — Are all accounts removed and licenses cancelled or reclaimed?
- Asset records are reconciled against what is actually installed. [[XW-026]]
  - Referenced by: Review and optimize — Where is our asset management process weakest this year?
- A changed AI system's use is reassessed, not assumed unchanged. [[XW-021]]

Gate to move on: Installs stay within entitlements and access reviews happen on schedule.
Hands off to: optimize. the running history and asset record get reviewed.
Who decides: The application owner, checked periodically by whoever runs access reviews.

Questions to ask:

- [ ] Do installs and users stay within entitlements? [[XW-007]] (tool: `rationalization`)
  - Referenced by: Acquire — Every purchase records its entitlements before deployment starts.
- [ ] Is access reviewed on schedule, and are leavers removed? [[XW-016]] (tool: `access-review`)
  - Blocked by: Deploy — The application is recorded in the inventory with owner and data sensitivity.
  - May be impacted by: Deploy — Access roles are defined, and new access only granted through an approved path.
  - May be impacted by: Deploy — Privileged and administrative accounts are limited and named individually.
- [ ] Are asset records accurate and reconciled? [[XW-026]] (tool: `itam-maturity`)
- [ ] Has the AI system's use changed since intake? [[XW-021]] (tool: `ai-intake`)
  - Refers to: Deploy — An AI system's inventory record and risk entry are complete before go-live.

## Review and optimize

The portfolio is reviewed to decide whether each application still earns its cost.

Rules that apply:

- Every application is periodically assessed against tolerate, invest, migrate, or eliminate. [[XW-011]]
- Anything expiring within the review window is flagged before it lapses. [[XW-008]]
- The review checks where the organization's own asset process is weakest. [[XW-025]]
- The council's own decision log is checked for bottlenecks or rubber-stamping. [[XW-025]]

Gate to move on: The owner or council records a decision: keep, invest, migrate, or retire.
Hands off to: plan, retire. reinvest or replace starts a new request; otherwise retire begins.
Who decides: The application owner recommends; the council decides above its threshold.

Questions to ask:

- [ ] Is it still worth its cost: tolerate, invest, migrate, or eliminate? [[XW-011]] (tool: `rationalization`)
  - May impact: Plan and request — What problem does this solve, and do we own an app that does it?
  - May be impacted by: Acquire — Is the purchase recorded against an owner and a cost center?
- [ ] Is anything expiring or due for renewal in the next 90 days? [[XW-008]] (tool: `rationalization`)
  - May impact: Retire — Is the contract ended on time, without auto-renewal?
- [ ] Where is our asset management process weakest this year? [[XW-025]] (tool: `itam-maturity`)
  - Refers to: Operate — Asset records are reconciled against what is actually installed.
- [ ] Does the council's decision log show bottlenecks or rubber-stamping? [[XW-025]] (tool: `program-setup`)
  - Refers to: Plan and request — Does the request meet the council's threshold and come through the intake path?

## Retire

The application is decommissioned: data archived, migrated, or deleted; access and licenses unwound.

Rules that apply:

- What happens to the application's data is decided and recorded, not left implicit. [[XW-028]]
- All accounts tied to the application are removed and licenses reclaimed. [[XW-017]]
- The contract is ended on schedule, with any auto-renewal cancelled in time. [[XW-013]]
- The inventory record is formally closed, with evidence retained for audit. [[XW-020]]
  - Refers to: Deploy — The application is recorded in the inventory with owner and data sensitivity.
  - Blocked by: Retire — What data does it hold, and will we archive, migrate, or delete it?

Gate to move on: Accounts removed, licenses reclaimed, and the inventory record closed with evidence.
Hands off to: plan. the freed licenses, data capacity, and budget go to the next request.
Who decides: The application owner executes; the council confirms closure above its threshold.

Questions to ask:

- [ ] What data does it hold, and will we archive, migrate, or delete it? [[XW-028]] (tool: `rationalization`)
  - Refers to: Plan and request — What data will it hold, and how sensitive is that data?
  - Blocks: Retire — The inventory record is formally closed, with evidence retained for audit.
- [ ] Are all accounts removed and licenses cancelled or reclaimed? [[XW-017]] (tool: `access-review`)
  - Referenced by: Operate — Access is reviewed on schedule, and leavers are removed promptly.
- [ ] Is the contract ended on time, without auto-renewal? [[XW-013]] (tool: `rationalization`)
  - May be impacted by: Acquire — Contracts are checked for audit, renewal, and exit terms before signature.
  - May be impacted by: Review and optimize — Is anything expiring or due for renewal in the next 90 days?
- [ ] Is the inventory record closed, with evidence kept? [[XW-020]] (tool: `itam-maturity`)
