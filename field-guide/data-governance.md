# Field guide: application governance vs. data governance

These two disciplines get used interchangeably, but they ask different questions and are usually owned by different people.

Application governance manages the *software*: what applications exist, who owns each one, what they cost, how they're licensed, who has access to them, and when they get retired. It's the subject of this whole kit.

Data governance manages the *information inside those applications*: what each data element means, who's accountable for its quality and stewardship, how sensitive it is, how long it has to be kept, and what privacy law says about it. This kit doesn't build that discipline out — the comparison below exists so the boundary is clear, and so the four places the two disciplines meet don't get missed.

## Comparison

| | Application governance | Data governance |
|---|---|---|
| **What it asks** | What do we have, who owns it, what does it cost, is it licensed correctly, who can access it, when does it get retired? | What does this data mean, who's accountable for its quality, how sensitive is it, how long must it be kept, what does privacy law require? |
| **Who typically owns it** | An ITAM function, application owners, a software governance council | A data governance or data management function, data stewards, a chief data officer where one exists |
| **Main frameworks** | ISO/IEC 19770 family, COBIT (notably BAI09, Managed Assets), ISO/IEC 27001 | DAMA-DMBOK, ISO 8000 (data quality), applicable privacy law (e.g. GDPR, sector-specific statutes) |

## Where they meet

**Retiring an application is a data decision, not just a software one.** Before an app is eliminated, someone has to decide what happens to the data it holds — archive it, migrate it, or delete it — and that decision needs a data owner's sign-off, not just an IT one. *Halden example: the `rationalization` checklist's retirement step (step 10) requires exactly this before any eliminate decision is executed; it isn't optional cleanup.*

**Data sensitivity sets access-review priority.** Which accounts get reviewed first should follow how sensitive the underlying data is, not just an alphabetical or convenient order. *Halden example: the access review deliberately checked the 10 confidential apps before the 50 internal ones, and two of the three orphaned accounts it found were on confidential systems.*

**AI systems are only as trustworthy as the data behind them.** An AI system's risk tier and its controls both depend on what data it uses, where that data came from, and whether it includes personal data — you can't govern the AI system without governing its data. *Halden example: `ai-intake`'s step 2 records data used, personal-data status, and provenance for each of Halden's six systems before any tier is assigned.*

**Asset records are themselves data, and need the same quality discipline.** An inventory that's wrong — missing owners, mismatched user counts, stale entitlements — isn't just an ITAM problem; it's a data-quality problem inside the ITAM system. *Halden example: the crosswalk's XW-026 control theme, and the `itam-maturity` check's evidence-per-area step, both treat the accuracy of the asset data itself as something to verify, not assume.*

A full data classification and retention tool is planned for phase 2 of this kit; today, these four intersection points are handled inside the existing tools rather than by a dedicated one.
