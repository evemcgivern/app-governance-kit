# Platform guide: Software audit response check

Where the records this tool uses live in ServiceNow Software Asset Management Professional (SAM Pro) and in Flexera One. Every table or field named below was confirmed on a source in the Sources list as of 2026-09-25 and has not been checked since; where no source names one, that is stated as a gap rather than guessed. Neither platform documents an audit-response workflow of its own, so what follows maps this method's inputs onto the records each platform holds.

## ServiceNow SAM Pro: entitlements, installs, and reconciliation

As of 2026-09-25: Purchase records are held as **Software Entitlements** (table `alm_license`). This is where the quantity bought for a product sits, the counterpart of the proof-of-purchase quantity in this method. SAM Pro's **Reconciliation** step matches entitlements against discovered installations with its licensing rules and produces a **License Compliance Position**, the counterpart of this method's short, even, or over label. The entitlement carries effective and expiry dates; the linked contract record (`ast_contract`) carries an end date.

No source reviewed names a field on the entitlement for the buyer's legal name, for proof of payment, or for the qualifying base license behind an upgrade. Treat those as attributes to keep in the governance record, with the invoice, order, and payment record stored together as attachments or in a linked repository. The platform will not check them for you.

SAM Pro's reconciliation works on installs the platform has discovered. Install counts narrowed to an agreed audit scope (entities, products, years) are a filtered view the team builds from that data; no source describes a built-in scope filter for an audit.

## Flexera One: discovery and license position

As of 2026-09-25: Flexera One's hybrid IT discovery feeds the install side of the reconciliation, and each discovered title is normalized against **Technopedia**, which matters when a publisher has renamed or acquired product lines. Its license position work compares what was found with what was bought, and reports unused and unassigned licenses.

Flexera's published pages reviewed do not name a field or record for proof of purchase, upgrade chains, or an audit case. That gap is stated here rather than guessed. Keep the proof register in the governance record and link each row to the entitlement it supports.

## What the platforms do not replace

Neither platform decides who speaks to a publisher, what is released, or whether a claim is valid. Those are counsel's calls. The platform supplies counts; the response team and Legal supply judgment.

## Sources checked

The platform facts above were fetched for the rationalization platform guide on 2026-09-25 and carried over here. They were not fetched again.

- [Review Software Entitlements — ServiceNow Community](https://www.servicenow.com/community/sam-blog/review-software-entitlements/ba-p/3304445) — Software Entitlements, Reconciliation, License Compliance Position.
- [Software Asset Management - Software Entitlement [alm_license] — ServiceNow Community](https://www.servicenow.com/community/sam-forum/software-asset-management-software-entitlement-alm-license-gt-br/m-p/3083406) — confirms the `alm_license` table name.
- [Guidance on SAM Pro license renewal process — ServiceNow Community](https://www.servicenow.com/community/sam-forum/guidance-on-sam-pro-license-renewal-process/m-p/3510712) — entitlement effective and expiry dates, and the contract end date.
- [Application Rationalization & Management — Flexera](https://www.flexera.com/flexera-one/it-visibility/application-rationalization) — hybrid IT discovery and Technopedia normalization.
- [Streamline Your SaaS Portfolio with Application Rationalization — Flexera](https://www.flexera.com/solutions/saas-spend/application-rationalization) — unused and unassigned license reporting.

Pages that do not return readable content to an automated fetch: Flexera's documentation site (`docs.flexera.com/...`, 403). Nothing above cites it.
