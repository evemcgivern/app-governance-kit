# Platform guide: Access review pack

Where the fields this tool uses live in ServiceNow's GRC attestation capability, and in Flexera One. Where no source names a module, table, or field, the guide says so instead of guessing.

## ServiceNow: access certification through Policy and Compliance Management attestations

ServiceNow's own access-certification capability sits inside **Policy and Compliance Management**, part of its Integrated Risk Management (IRM) product line, and runs on **control attestations**; there is no standalone "access review" object. ServiceNow's documentation defines the pieces. The Control Objectives module is the main hub of the application. A **Control** is a specific implementation of a control objective. An **Entity** is a person, process, department, application, or object whose risk exposure must be managed and monitored. **Attestation** assesses the control to continuously monitor its compliance. No backing table name is given for any of these records.

A ServiceNow Community thread describes the setup for a user access review. Create a **Control Objective** and link it to the **Entity Type** being reviewed (for example, users holding access to a given system). That generates one **Control** per entity, and each control routes an **Attestation** to its named **Control Owner**, who confirms the access is still needed and attaches their decision as evidence.

Evidence collection runs one of two ways. A **Manual Indicator** gathers the control owner's response as evidence by hand. Where ServiceNow is connected to an identity and access management (IAM) solution, an **Automated Indicator** can monitor the control continuously. That is the mechanism this method's account-to-person matching maps onto. The account and person data behind an automated indicator's check is expected to come from the connected IAM system, not from a table inside ServiceNow.

No ServiceNow documentation names a field or table that stores the account-to-person match from this method's step 3. The Attestation and Control Owner objects carry the *decision*. Where the account export sits isn't named.

ServiceNow does not natively ship a standalone identity-governance or access-certification module beyond Policy and Compliance Management's attestations; full identity-governance workflows (for example, certification campaigns run against an identity warehouse) are delivered by third-party apps such as Saviynt's ServiceNow Store integration, not by ServiceNow itself.

The Control Objective / Entity Type / Control / Control Owner / Attestation / Manual Indicator / Automated Indicator terminology above comes from a ServiceNow Community discussion, cross-checked against ServiceNow's own structural-overview and entity-definition documentation.

## Flexera One: application usage data for dormant access

Flexera One's SaaS Management surfaces the usage evidence this method's dormant-access check (no login in 90 days) would draw on. Flexera states it can **identify underused licenses** and find downgrade opportunities from bundled subscriptions, built on **detailed usage insights** drawn from multiple discovery methods (financial data, API connectors including a Universal Connector, a browser extension, and connections to SSO and CASB technologies), covering both sanctioned and unsanctioned (shadow) applications. The product combines application usage, spend, and contract information to recommend right-sizing licenses and eliminating unused applications.

Flexera One's SaaS Management Users Tab has a named column, **Days Since Last Activity**, which reports "Never Active" for accounts with no recorded login (the threshold is 60 days without login, or 30 days when an application is first integrated). That is the closest named equivalent to this method's `last_login` column. Flexera's documentation site (`docs.flexera.com/...`) wouldn't load, so the column name comes from a search-engine excerpt of the Flexera-authored page. The rest of this section comes from Flexera's marketing page.

## Sources checked

- [Access Reviews in P&C, ServiceNow Community](https://www.servicenow.com/community/grc-forum/access-reviews-in-p-amp-c/m-p/2342369): Control Objective, Entity Type, Control, Control Owner, Attestation, Manual Indicator, Automated Indicator, and the connected-IAM-solution route to continuous monitoring.
- [Policy and Compliance Management structural overview, ServiceNow Docs, Xanadu](https://www.servicenow.com/docs/r/xanadu/governance-risk-compliance/policy-and-compliance-management/pc-structural-overview-policy-comp.html): Control Objectives module, Control, and Attestation definitions.
- [What is an Entity?, ServiceNow Docs (GRC common functions), Washington DC](https://www.servicenow.com/docs/r/washingtondc/governance-risk-compliance/grc-common-functions/what-is-an-entity.html): Entity and Entity Type definitions.
- [Identity governance on ServiceNow, Saviynt blog](https://saviynt.com/blog/identity-governance-servicenow) (search-confirmed; not independently fetched): the third-party, partner-built route to full access-certification workflows.
- [Optimize SaaS spend and utilization with Flexera One SaaS Management, Flexera](https://www.flexera.com/products/flexera-one/saas-management): underused-license identification, multi-source discovery (financial data, API connectors, browser extension, SSO/CASB), usage-and-spend-based optimization recommendations.
- [SaaS Management Users Tab reference, Flexera Docs](https://docs.flexera.com/flexera-one/saas/saas-manager/saas-management-user-interface-reference/saas-application-details/users-tab) (search-indexed excerpt only; the page returns 403): the "Days Since Last Activity" column.
- [Tracking user activity, Flexera Docs](https://docs.flexera.com/flexera-one/saas/saas-manager/managing-saas-applications/tracking-user-activity) (search-indexed excerpt only; the page returns 403): the 60-day ("Never Active") / 30-day (first integration) thresholds.

ServiceNow's IRM product page (`servicenow.com/products/integrated-risk-management.html`) wouldn't load, and nothing here rests on it. No Flexera documentation page loaded either, including the Users Tab and activity-tracking pages cited above by search excerpt.
