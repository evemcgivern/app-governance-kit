# Field guide: glossary

Plain-English definitions for terms used across this kit's methods, tied to a Halden Logistics example wherever one exists in the demo data.

**ITAM (IT Asset Management).** The overall discipline of knowing what IT assets an organization has and managing them through their lifecycle. *Halden example: every method in this kit — rationalization, access review, AI intake — is a slice of ITAM applied to Halden's estate.*

**SAM (Software Asset Management).** The software-specific slice of ITAM: licensing, entitlements, and compliance. *Halden example: the license checks in `rationalization` against `licenses.csv` are SAM work.*

**HAM (Hardware Asset Management).** The physical-device slice of ITAM: acquisition, deployment, maintenance, refresh, and retirement of hardware. *Halden example: Halden's laptop and device refresh cycle is tracked by the `hardware-lifecycle` tool — see [certifications.md](certifications.md)'s CHAMP section.*

**APM (Application Portfolio Management).** Deciding what to keep, replace, consolidate, or retire across an application estate. *Halden example: the `rationalization` tool's tolerate/invest/migrate/eliminate call between Clausebase and Tallysheet.*

**CMDB (Configuration Management Database).** A system of record for IT assets and how they relate to one another. *Halden example: `apps.csv` and `licenses.csv` function as a lightweight CMDB extract for the demo estate.*

<a id="entitlement"></a>**Entitlement.** The specific usage right a license grants — not just the fact that software is installed. *Halden example: Payflow's license entitlements don't match its 748 users, an open license-position question the rationalization run flags as unverified.*

<a id="effective-license-position"></a>**Effective license position (ELP).** The gap between what's licensed (entitlements) and what's actually deployed or used. *Halden example: comparing Payflow's licensed entitlements to its real user count before a vendor audit.*

**True-up.** Paying for usage that exceeded licensed entitlement, usually settled at renewal or after an audit. *Halden example: if Payflow's usage is found to exceed its entitlement, Halden owes a true-up at the next renewal.*

**Reconciliation.** Matching what's deployed or in use against what's licensed or recorded, to surface the gap. *Halden example: matching `accounts.csv` logins against `employees.csv` to find orphaned accounts is the same reconciliation logic applied to access instead of licenses.*

**Normalization.** Cleaning inconsistent product or vendor names so the same thing isn't counted twice under different labels. *Halden example: Clausebase and Tallysheet are both normalized to "contract management," not left as two unrelated names.*

<a id="swid-tag"></a>**SWID tag (software identification tag).** A machine-readable file that identifies an installed software product, defined in ISO/IEC 19770-2. *Halden example: none of Halden's demo apps ship SWID tags, so today's inventory work is manual.*

**Shelfware.** Licensed or purchased software sitting mostly or entirely unused. *Halden example: Pulseboard carries 350 entitlements against only 45 users — a shelfware candidate the rationalization run flags.*

**TIME model.** The tolerate/invest/migrate/eliminate categorization used to decide an application's fate. *Halden example: Northbeam ERP is tolerated as-is; Clausebase is eliminated in favor of the cheaper, functionally equal Tallysheet.*

**Orphaned account.** An active account with no valid current owner, most often a leaver's account that was never disabled. *Halden example: ACC-063, still active 37 days after EMP-072's termination date.*

**Access certification (access review).** A periodic check that every account's access is still valid, owned, and appropriately scoped. *Halden example: the review that surfaced ACC-063, ACC-104, and seven privileged admin accounts needing owner re-approval.*

**Segregation of duties (SoD).** Making sure no one person holds two roles that together let them create and approve the same transaction unchecked. *Halden example: SoD wasn't tested in the sample review because no SoD rules had been supplied to check against — a named gap, not a clean result.*

**Risk tier.** A category — such as minimal, limited, or high-risk — assigned to a system or use case that determines which controls apply. *Halden example: AI-004, the HR candidate-shortlisting tool, tiers as high-risk; the email spam filter (AI-001) tiers as minimal.*

**AI inventory.** The AI-system equivalent of a software inventory: one record per use case, with purpose, data, and risk tier. *Halden example: each of Halden's six AI systems gets one row once `ai-intake` runs.*

**Prohibited practice.** An AI use explicitly barred by law regardless of risk tier — for example certain manipulation or social-scoring uses. *Halden example: `ai-intake`'s step 3 rules this out, or escalates to legal, before tiering continues for any of Halden's six systems.*

**Human-in-the-loop.** A person reviews, or can override, an automated decision before or after it takes effect. *Halden example: AI-002's invoice field extraction has a person review the fields; AI-001's spam quarantine does not — itself a finding, since nothing releases quarantined mail automatically either.*

**Chargeback / showback.** Allocating (chargeback) or simply reporting (showback) IT cost to the business unit that incurs it. *Halden example: neither is possible with Halden's current data — no app in `apps.csv` carries a cost-center field yet.*

**Vendor management.** Tracking supplier relationships, contract terms, and renewal or termination notice periods. *Halden example: the rationalization run can't finalize an eliminate decision for Clausebase because no vendor contract terms were supplied.*

**Governance council (steering committee).** A standing body with named authority to approve, reject, or set policy for software or AI decisions. *Halden example: the draft Halden Software Governance Council, reviewed by `program-setup` and found to have no sponsor or written decision rights yet.*

**Decision rights.** A written statement of who decides what, and at what threshold, so intake doesn't default to "everything goes to committee." *Halden example: the council's draft charter names a cost-or-risk threshold but never sets it, leaving the triage owner nothing to check requests against.*

**Sponsor.** The executive who holds budget authority and gives a governance body the power to actually act. *Halden example: the council review's central finding — no sponsor is named anywhere in the draft charter.*

**Escalation path.** A named route, and person, for resolving disputes a governance body can't settle itself. *Halden example: the Halden council escalates disputes to the COO, who sits outside the council and breaks ties.*

**Recertification.** The requirement to periodically retest, or re-earn continuing-education credit, to keep a professional certification active. *See [certifications.md](certifications.md): annual for CAMP, CSAM, and CHAMP; a multi-year continuing-education cycle for AIGP.*

**Privileged access.** An account with elevated rights — typically admin — that can change configuration or data beyond an ordinary user's reach. *Halden example: seven `admin`-role accounts in the sample review, each routed back to its app owner for re-approval.*

**Dormant account.** An account with no recent login activity — a distinct access-review finding from an orphaned one, which is about ownership rather than activity. *Halden example: zero were found in the most recent export, though the review flags that the export window is too short to call this conclusive.*

**Data provenance.** Where a system's data actually came from — necessary to know before its privacy or quality risk can be judged. *Halden example: `ai-intake`'s step 2 records this for each of the six AI systems; several aren't stated by the source CSV alone and are marked unverified.*

**Risk register.** A running, owned log of identified risks and their treatment, rather than a one-time note. *Halden example: AI-004's high-risk tiering gets a risk-register entry with HR as the named owner.*
