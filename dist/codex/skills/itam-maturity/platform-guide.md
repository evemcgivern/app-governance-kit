# Platform guide: ITAM maturity check

For each of the nine process areas, the ServiceNow and Flexera One capability that supports it, drawn only from sources I could reach. Where I could not confirm a named module for a platform in a given area, I say so rather than guess.

## Governance and policy

**ServiceNow.** Asset management policy lives in the same **Policy and Compliance Management** capability, inside ServiceNow's Integrated Risk Management (IRM) product, that the crosswalk tool's platform guide describes: policies at the top, **Control Objectives** as the measurable targets, and **Controls** as the activities and evidence underneath them. There is no capability specific to SAM Pro, HAM Pro, or APM for holding the organization's own asset management policy document; it belongs in this shared IRM workspace.

**Flexera One.** I found no Flexera One feature for authoring or holding an organization's own asset management policy document; its capabilities (below) act on the estate the policy describes rather than storing the policy itself.

## Inventory and discovery

**ServiceNow.** SAM Pro gathers installation data automatically from integrations such as Discovery and normalizes what it finds through the **Content Library and Content Service**, then runs **Reconciliation** to compare discovered installs against records. HAM Pro's **Hardware Asset Manager Workspace** and **Asset Inventory Audit** capability do the equivalent for hardware, including barcode/QR scanning through the Agent Mobile app. Application Portfolio Management (APM) builds its own application inventory from the **CMDB**, tracking the dependencies between applications and the technology they run on.

**Flexera One.** Flexera One's **asset discovery and inventory** capability builds a unified inventory across on-prem, cloud, SaaS, and containers, and normalizes what it finds against **Technopedia**, which Flexera states recognizes and normalizes titles at over 98%.

## Entitlement and license management

**ServiceNow.** SAM Pro's core license workflow is **Reconciliation | Remediation | Compliance**: matching entitlements to deployed installs, and surfacing over- or under-licensed positions. Its **Reclamation Rules and Removal Candidates** identify licenses to recover from unused installs.

**Flexera One.** Flexera One applies **Use Rights Analysis** against publisher-specific entitlement terms and uses **AI contract & entitlement ingestion** to read purchase orders, invoices, and contracts. It calculates an **Effective License Position (ELP)** to state the compliance position for top-tier vendors automatically.

## Lifecycle, request to retirement

**ServiceNow.** HAM Pro automates the hardware lifecycle with Flow Designer flows covering the **Hardware Asset Order flow** (procurement through deployment), **Asset Onboarding and Offboarding flows**, and six asset task types — Deploy, Swap, Retire, Refresh, Loaner, and Leased Return — ending in **Hardware Disposal flows** with certificate tracking. APM runs **Application Portfolio Rationalisation** through classify, measure, analyse, and plan phases to decide whether an application is migrated, sustained, or divested.

**Flexera One.** Flexera One's **Hardware Lifecycle Management** tracks hardware "from the time they're requested until they're disposed," with **Lifecycle Automation** integrating vendors, procurement, and disposal systems, and **Lifecycle Alerts** for events such as end of life, warranty expiry, or lease termination. I found no equivalent named lifecycle-orchestration capability for software or application lifecycle in Flexera One; its lifecycle tracking, as documented, is scoped to hardware.

## Vendor and contract management

**ServiceNow.** **Vendor Risk Management (VRM)**, part of the GRC portfolio, covers vendor relationships through named functional areas: **Vendor Portfolio**, **Vendor Tiering**, **Assessment Management**, **Vendor Portal**, and **Issues and Remediation**.

**Flexera One.** Flexera One's **AI contract & entitlement ingestion** extracts vendor contract data automatically from invoices and purchase orders. I found no broader named Flexera One capability for vendor risk tiering or relationship management beyond contract data extraction.

## Data quality and reconciliation

**ServiceNow.** Both SAM Pro and HAM Pro normalize records through the shared **Content Library and Content Service**, and SAM Pro's reconciliation step is where mismatches between discovered and recorded data surface for correction.

**Flexera One.** Flexera One's **Technopedia** enrichment is the named data-quality capability: Flexera states it standardizes software titles and versions and adds details such as end-of-life and end-of-support dates, with over 98% recognition and normalization rates.

## Risk and security integration

**ServiceNow.** I could not confirm, from a source I could reach, a specific named integration between SAM Pro, HAM Pro, or APM and a ServiceNow security product for enforcing access control policy on new applications. I did not find a reachable page naming that link, so I'm not naming one.

**Flexera One.** I found no Flexera One capability for enforcing or checking an access control policy against new applications; its confirmed capabilities are scoped to inventory, licensing, and cost rather than access security.

## Cost and financial management

**ServiceNow.** **Cloud Cost Management** is a named ServiceNow capability offered alongside SAM, with a **Cloud Cost Simulator** available to SAM Enterprise customers for modeling the cost of moving workloads to the cloud.

**Flexera One.** Flexera One's **renewal & true-up optimization** right-sizes renewals from usage and entitlement data, and its **automated license reclamation** identifies unused software to cut spend.

## Reporting and improvement

**ServiceNow.** HAM Pro's **Hardware Asset Manager Workspace** includes configurable KPI tiles for assets due for refresh, unassigned assets, and expiring contracts. APM's **Assessment Dashboard** visualizes application indicators — cost, quality, technical risk, investment, user satisfaction, and business value — for portfolio decisions.

**Flexera One.** Flexera One's **always-on audit readiness** is the named capability for maintaining a defensible, reportable license position on an ongoing basis rather than only at audit time.

## Sources checked

- [Policy Lifecycle Management in IRM: Closing the gap on a single, governed policy workflow](https://www.servicenow.com/community/grc-articles/policy-lifecycle-management-in-irm-closing-the-gap-on-a-single/ta-p/3566226) — Policies, Control Objectives, Controls terminology (also used by the crosswalk platform guide).
- [Software Asset Management Professional (SAM Pro) — ServiceNow Community](https://www.servicenow.com/community/developer-blog/software-asset-management-professional-sam-pro/ba-p/3025704) — Content Library and Content Service, Reconciliation | Remediation | Compliance, Reclamation Rules and Removal Candidates.
- [Core Asset Management vs HAM Pro — ServiceNow Community](https://www.servicenow.com/community/ham-blog/core-asset-management-vs-ham-pro-what-you-actually-get-and-when/ba-p/3518013) — Hardware Asset Manager Workspace, Asset Onboarding and Offboarding flows, Hardware Asset Order flow, asset task types, Hardware Disposal flows, Asset Inventory Audit.
- [Application Portfolio Management on ServiceNow — ServiceNow Community](https://www.servicenow.com/community/enterprise-architecture-articles/application-portfolio-management-on-servicenow/ta-p/2297172) — CMDB-based application inventory, Application Portfolio Rationalisation phases, Assessment Dashboard and indicators.
- [ServiceNow Vendor Risk Management notes and videos — ServiceNow Community](https://www.servicenow.com/community/grc-blog/servicenow-vendor-risk-management-notes-and-videos/ba-p/2274288) — Vendor Portfolio, Vendor Tiering, Assessment Management, Vendor Portal, Issues and Remediation.
- [Cloud Cost Management Path to Value — ServiceNow Community](https://www.servicenow.com/community/cloud-cost-management-articles/cloud-cost-management-path-to-value/ta-p/3060830) — Cloud Cost Management, Cloud Cost Simulator availability for SAM Enterprise.
- [Reporting & Dashboards: SAM — ServiceNow Community](https://www.servicenow.com/community/sam-forum/reporting-amp-dashboards-sam/td-p/3241900) — checked for a named SAM dashboard; confirms only reconciliation grouping/consumption rules, no named dashboard, so none is claimed above.
- [IT Asset Management (ITAM) Software — Flexera](https://www.flexera.com/products/flexera-one/it-asset-management) — asset discovery and inventory, Use Rights Analysis, AI contract & entitlement ingestion, renewal & true-up optimization, automated license reclamation, Technopedia.
- [Software Asset Management (SAM) Tools — Flexera](https://www.flexera.com/solutions/software-usage-costs/software-asset-management) — Effective License Position (ELP), always-on audit readiness, Technopedia recognition/normalization rate.
- [IT Hardware Asset Management Solutions — Flexera](https://www.flexera.com/solutions/it-asset-lifecycle/hardware-asset-management) — Hardware Lifecycle Management, Lifecycle Automation, Lifecycle Alerts.

Two pages I would otherwise have cited returned an error to automated fetches rather than a page I could read: ServiceNow's own product pages (`servicenow.com/products/...`, `servicenow.com/uk/products/...`) returned 403, and Flexera's documentation site (`docs.flexera.com/...`) also returned 403. Everything above comes from a page that loaded.
