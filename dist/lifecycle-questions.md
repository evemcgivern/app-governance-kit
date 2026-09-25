# Application lifecycle questions

Questions to ask at each stage. Each names the crosswalk row it satisfies and the kit tool that handles it.

## Plan and request

- [ ] What problem does this solve, and do we own an app that does it? [[XW-011]] (tool: `rationalization`)
- [ ] Who will own it, and who is the executive sponsor? [[XW-002]] (tool: `program-setup`)
- [ ] Does the request meet the council's threshold and come through the intake path? [[XW-027]] (tool: `program-setup`)
- [ ] Does it use AI? If so, what risk tier is it? [[XW-021]] (tool: `ai-intake`)
- [ ] What data will it hold, and how sensitive is that data? [[XW-028]] (tool: `access-review`)

## Acquire

- [ ] What license model applies, and how many entitlements do we need? [[XW-006]] (tool: `rationalization`)
- [ ] Does the contract give audit, renewal, and exit terms we can live with? [[XW-013]] (tool: `rationalization`)
- [ ] Have the supplier and any AI model provider been assessed? [[XW-023]] (tool: `ai-intake`)
- [ ] Is the purchase recorded against an owner and a cost center? [[XW-012]] (tool: `itam-maturity`)

## Deploy

- [ ] Is the app in the inventory with owner, category, and data sensitivity? [[XW-001]] (tool: `itam-maturity`)
- [ ] Are access roles defined, and who approves new access? [[XW-015]] (tool: `access-review`)
- [ ] Are privileged accounts limited and named? [[XW-018]] (tool: `access-review`)
- [ ] For AI systems: is the inventory record complete and the risk in the register? [[XW-022]] (tool: `ai-intake`)

## Operate

- [ ] Do installs and users stay within entitlements? [[XW-007]] (tool: `rationalization`)
- [ ] Is access reviewed on schedule, and are leavers removed? [[XW-016]] (tool: `access-review`)
- [ ] Are asset records accurate and reconciled? [[XW-026]] (tool: `itam-maturity`)
- [ ] Has the AI system's use changed since intake? [[XW-021]] (tool: `ai-intake`)

## Review and optimize

- [ ] Is it still worth its cost: tolerate, invest, migrate, or eliminate? [[XW-011]] (tool: `rationalization`)
- [ ] Is anything expiring or due for renewal in the next 90 days? [[XW-008]] (tool: `rationalization`)
- [ ] Where is our asset management process weakest this year? [[XW-025]] (tool: `itam-maturity`)
- [ ] Does the council's decision log show bottlenecks or rubber-stamping? [[XW-025]] (tool: `program-setup`)

## Retire

- [ ] What data does it hold, and will we archive, migrate, or delete it? [[XW-028]] (tool: `rationalization`)
- [ ] Are all accounts removed and licenses cancelled or reclaimed? [[XW-017]] (tool: `access-review`)
- [ ] Is the contract ended on time, without auto-renewal? [[XW-013]] (tool: `rationalization`)
- [ ] Is the inventory record closed, with evidence kept? [[XW-020]] (tool: `itam-maturity`)
