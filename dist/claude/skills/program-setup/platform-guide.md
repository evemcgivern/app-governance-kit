# Platform guide: Stand up a governance program

Where this method's intake, approval, and meeting-input steps map onto ServiceNow and Flexera One, drawn only from sources I could reach. Where I could not confirm a named module, table, or field, I say so rather than guess.

## ServiceNow: intake through a catalog item, decisions through an approval workflow

A governance intake form (this method's step 5) maps onto a **Service Catalog** item: a catalog item carries a request form and a **Workflow** field that defines its fulfilment process, including any approval step. Submitting the item creates a **Request**, which in turn creates one or more **Requested Items (RITM)**; the request-level approval covers everything in the cart, and once that clears, each requested item's own workflow starts running.

Approval logic is built either in the classic **Workflow Editor** or in **Flow Designer**, using activities such as **Approval - User**, **Approval - Group**, or **Approval - Action**, evaluated against a **Condition** — the mechanism a cost or risk threshold (this method's step 3) would be built on, for example routing to the council only when a requested item's cost exceeds a set figure. Approval records live against the request or requested item and move through states such as Requested, Approved, Rejected, and Cancelled, which is the natural place to attach this method's decision log, alongside workflow activity logs and notifications for each decision.

I could not load ServiceNow's own Service Catalog Management documentation (`docs.servicenow.com`) or its Service Catalog Management product page (`servicenow.com/products/service-catalog-management.html`); the first redirected to a generic docs landing page and the second returned a 403 to automated fetches. The Workflow / Flow Designer / Approval - User / Approval - Group / RITM / Request terminology above comes from a ServiceNow Community how-to thread that did load; I found no ServiceNow documentation naming a specific table (such as `sysapproval_approver`) as the authoritative store for a council's decision log, so I have not named one here.

## Flexera One: usage, spend, and shadow IT discovery as meeting inputs

Flexera One's SaaS Management product is built to feed exactly the kind of item this method's intake and meeting inputs need: it combines **application usage, license data, and spend insights** to surface waste, and its discovery draws on multiple sources at once — Flexera names financial and expense data, API connectors, a browser extension, and connections to single sign-on (SSO) and Cloud Access Security Broker (CASB) systems — to build a fuller picture than any one source alone, including applications nobody sanctioned. That combined view of usage, spend, and contract data is what Flexera positions as the basis for governance and license-optimization decisions, which is the natural agenda input for this method's cadence step (rather than convening the body with no live item to decide on).

I found no confirmed Flexera One field, table, or dashboard name for a per-application "last reviewed" or "last decided" date that this method's decision log could cite directly; Flexera's documented capability is usage-and-spend-based discovery and optimization recommendations, not a named governance-decision object. Flexera's own documentation site (`docs.flexera.com`) was not tested against every page for this guide; the claims above come from Flexera's product and solution marketing pages, which loaded and which I have cited directly.

## Sources checked

- [Understanding Approval Workflows in ServiceNow: A Practical Guide — ServiceNow Community](https://www.servicenow.com/community/servicenow-ai-platform-forum/understanding-approval-workflows-in-servicenow-a-practical-guide/td-p/3129602) — Flow Designer, Workflow Editor, Approval - User/Group/Action activities, condition-based triggers, RITM/Request objects, approval states, and workflow activity logs.
- [Optimize SaaS spend and utilization with Flexera One SaaS Management — Flexera](https://www.flexera.com/products/flexera-one/saas-management) — combined usage, license, and spend insights; multi-source discovery (financial data, API connectors, browser extension, SSO/CASB); license right-sizing and unused-application elimination.
- [Mitigate Risks with Shadow IT Discovery and Management — Flexera](https://www.flexera.com/solutions/saas-spend/shadow-it) — shadow IT discovery methods (usage metering, CASB, browser extension, financial records, SSO) and the case for combining multiple sources over relying on one.

Two pages I would otherwise have cited did not return a readable page to automated fetches: ServiceNow's Service Catalog Management documentation under `docs.servicenow.com` (redirected to a generic docs landing page with no article content) and its Service Catalog Management product page (`403 Forbidden`). Everything above comes from a page that loaded.
