# Platform guide: AI system intake and risk tiering

Where an AI inventory and AI risk assessments live in ServiceNow, and how Flexera One can surface AI software and SaaS usage, drawn only from sources I could reach. Where I could not confirm a named module, table, or field, I say so rather than guess.

## ServiceNow: AI governance and Integrated Risk Management (IRM)

ServiceNow's risk and compliance work sits in **Integrated Risk Management (IRM)**, its platform for unifying governance, risk, and compliance processes. On top of that, ServiceNow has named a specific governance layer for AI: **AI Control Tower**, which ServiceNow's own community documentation describes as a single system of record for AI governance, holding the policies, roles, and approvals that AI use cases pass through as they get registered, classified, assessed, approved, and then monitored. That registration-to-monitoring flow is the closest confirmed analog to this method's intake-to-inventory steps: a use case is registered (this method's restatement and inventory record), classified and assessed (this method's tiering), approved (this method's approval decision), and then monitored (this method's re-review date).

ServiceNow's own community writeup maps AI Control Tower's stages directly onto the NIST AI RMF's four functions this method also cites: intake and stakeholder mapping across domains such as IT, HR, Finance, and Security correspond to **Map**; assessment workflows and evidence collection correspond to **Measure**; centralizing policy, roles, and approvals corresponds to **Govern**; and linking identified risks to owners and remediation workflows in a closed loop corresponds to **Manage**.

Within IRM, AI-specific assessment work is increasingly handled by **ServiceNow Otto for IRM** (the current name for what earlier release material called "Now Assist for IRM" — I found the newer naming on a live docs page and I'm using it as the current one). Its documentation names two specific AI agents: a **"Report a GRC issue" AI agent**, which walks a user through reporting a governance, risk, or compliance issue and suggests relevant controls, entities, and policies before submission; and a **Control Objective Change Agent**, which lets a user review and update impacted control objectives against the latest citation details. Neither of these is an AI-intake-specific form, and I found no ServiceNow documentation naming a specific table or field that stores an AI use case's risk tier, its required controls, or its inventory record — so I'm not naming one. Treat AI Control Tower as the product surface this method's steps would run inside, and IRM's assessment and risk-register capabilities as the mechanism for this method's control list and risk-register entry, without a confirmed field-level mapping.

## Flexera One: surfacing AI software and SaaS usage

Flexera merged its own and Snow's SaaS management products into a single **Flexera One SaaS Management** offering, which Flexera's press material frames explicitly around **shadow AI**: unsanctioned or unlicensed AI tools in use without governance visibility. Discovery runs through what Flexera's press release calls a **Comprehensive Discovery Engine**, combining Browser and Financial Discovery, an installed Agent, API connectors, CASB integration, and SSO connections — the same multi-source approach Flexera documents for its general SaaS and hybrid IT discovery, extended here to flag AI-powered applications and employee AI tool usage alongside ordinary SaaS.

Flexera's own SaaS Management page describes this as helping an organization "take control of AI usage across your organization" by discovering where AI is used, assessing risk and cost, and checking usage against company policy — which is the discovery-and-risk-flagging step this method's supplier-and-provider identification step (checklist item 6) would draw on before intake proceeds. I found no confirmed Flexera field or table name for storing an AI system's risk tier or approval status; its documented capabilities support finding and costing AI usage, not recording an intake decision, so this method's inventory record (`template.md`) has no confirmed Flexera equivalent.

## What I could not confirm

- No named ServiceNow table or field for an AI use case's risk tier, required controls, or inventory record.
- No named Flexera table or field for an AI intake decision, approval, or risk tier.
- ServiceNow's own IRM product page (`servicenow.com/products/integrated-risk-management.html`) and its AI governance solution brief PDF both returned an error to automated fetches; the IRM name above comes from ServiceNow's own page title as indexed, not from a page I could read directly.

## Sources checked

- [Managing AI Risk Using NIST AI RMF and ServiceNow AI Control Tower — ServiceNow Community](https://www.servicenow.com/community/now-assist-articles/managing-ai-risk-using-nist-ai-rmf-and-servicenow-ai-control/ta-p/3466409) — AI Control Tower, the register/classify/assess/approve/monitor flow, and its mapping to NIST AI RMF's Govern/Map/Measure/Manage.
- [AI agents in Now Assist for IRM — ServiceNow Docs](https://www.servicenow.com/docs/r/governance-risk-compliance/grc-common-functions/standalone-ai-agents-in-risk-sustainability.html) — confirms the current name is ServiceNow Otto for IRM, and names the "Report a GRC issue" AI agent and the Control Objective Change Agent.
- [Integrated Risk Management (IRM) — ServiceNow](https://www.servicenow.com/products/integrated-risk-management.html) — product name and positioning, from the page's indexed title (the page itself returned an error to a direct fetch).
- [Flexera One SaaS Management](https://www.flexera.com/products/flexera-one/saas-management) — "take control of AI usage," AI usage discovery, and policy-alignment framing.
- [Flexera Launches New Unified SaaS Management Solution to Improve Visibility for Shadow AI — Flexera press release](https://www.flexera.com/about-us/press-center/flexera-launches-new-saas-management-solution) — the merged Flexera One SaaS Management product, the Comprehensive Discovery Engine, and its named discovery methods.

Two pages I would otherwise have cited returned an error to automated fetches rather than a page I could read: ServiceNow's own IRM product page and its AI governance solution brief PDF (both `servicenow.com/...`) returned 403. Everything named above with a confirmed source comes from a page that loaded.
