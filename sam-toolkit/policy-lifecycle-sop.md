# Policy lifecycle SOP

## Purpose

Keep each ITAM policy written, approved, published, understood, and current, so that people can follow it and an auditor can see how it was made and changed.

## Scope

Applies to the smallest useful ITAM policy set and the standards beneath it:

- The IT asset management umbrella policy, owned by the ITAM manager and approved by the sponsor. It covers license compliance, acceptable use, and penalties.
- The software acquisition and exceptions policy, with a standard path, a non-standard path, and approval that escalates with cost and risk.
- The software standards, which are a catalog of approved titles by role, versions, and SaaS. A selection committee owns them.
- The vendor management policy, one policy with a section for each topic.
- The records and evidence policy: proofs, authorizations, and retention. The company's own records schedule sets the retention rules. **Decision needed:** records owner or counsel.

Retirement follows `retirement-signoff-checklist.md` and, for devices, the `hardware-lifecycle` method. AI tool intake follows the `ai-intake` method. Both link to this process for their policy text. Use `policy-template.md` and `policy-standard-template.md` to draft, and `policy-checklist.md` to test the draft.

## Roles

- **Policy owner**: drafts the policy, keeps it current, and answers for it. A named role such as the ITAM manager.
- **Approver**: the sponsor, who approves the policy and any change to its scope.
- **Reviewers**: Legal, Security, Procurement, Finance, HR, and business leads, each consulted on their own part.
- **Counsel**: reviews enforcement wording and any retention period before approval.

## Frequency

Each policy is reviewed at least yearly, and sooner when a trigger occurs: a vendor audit, a merger, a move to cloud, a change of sponsor, a finding from an internal check, or a new or changed law, regulation, or contract rule that touches how software is bought, used, or kept.

## Steps

1. Before drafting, find the company's records retention schedule. If you cannot find it, ask the records owner or legal where it is written. For each record type below, note the rule, where it is written, who owns it, and how a legal hold is applied. Also name where the backup copy of these records is kept and who can restore it. Do not choose a period yourself. [[XW-020]]
   - Proofs of entitlement, with the contracts and terms that grant them.
   - Orders and invoices.
   - Audit correspondence and records gathered for an audit.
   - Discovery and usage reports, kept as they stood on the day they ran.
   - Disposal and wipe certificates.
   - Approval records.
   - Renewal notices.
2. The owner drafts from `policy-template.md`, or from `policy-standard-template.md` for a standard [[XW-003]]
3. The owner consults Legal, Security, Procurement, Finance, HR, and the business leads, and records what each changed [[XW-004]]
4. The owner compares the draft with other policies and records any conflict and who resolves it [[XW-003]]
5. The owner tests the draft with `policy-checklist.md` and fixes each failed item, so counsel sees a draft that already meets the checklist [[XW-025]]
6. Counsel reviews the enforcement wording and any retention period. **Decision needed:** counsel [[XW-020]]
7. The sponsor approves, and the approval is dated and filed. **Decision needed:** sponsor [[XW-027]]
8. The owner publishes the approved version, with its version number, in one controlled location [[XW-020]] [[XW-030]]
9. The owner communicates it, trains the people it binds, records each acknowledgment, and checks that people understood it, for example with a short quiz, a question in a team meeting, or a spot check of a few people, and records the result [[XW-004]] [[XW-030]]
10. Exceptions are logged in `authorization-log.csv` with an approver and an end date, and each is reviewed at expiry [[XW-009]] [[XW-019]]
11. The owner reviews the policy yearly or on a trigger, and records the result even when nothing changes [[XW-025]]
12. When a version is replaced, the owner withdraws the old one and keeps it in the archive with its dates [[XW-020]]

## Evidence to retain

- Each approved version, with its dated sponsor approval.
- The consultation record and the conflict record.
- Counsel's review of the enforcement wording and any retention period.
- The completed policy checklist.
- The communication plan and the acknowledgment records.
- The exceptions in `authorization-log.csv`, each with its end date and review.
- The review record and change history, including reviews that changed nothing.

Keep these records as you go.

## Questions to take to counsel and the contract owner

These are questions only. The answers belong to counsel and the contract owner, and the owner records each answer with a date in the review record.

Penalties and enforcement
- Which consequences may the policy state for a breach, and for which kinds of breach?
- Does any local law or employment agreement limit how the policy may be enforced?
- Who may apply a consequence, and what must be recorded before they do?
- Does the wording for contractors and temporary staff need to differ from the wording for employees?

Retention
- Who owns the retention rule: the records owner or counsel? **Decision needed:** records owner or counsel.
- How does a legal hold or an audit notice stop normal disposal, and who lifts it?
- Is the rule long enough to cover each publisher's audit look-back and the life of each license? Licenses bought long ago still need proof. **Decision needed:** counsel.
- Who approves disposal of expired records, and where is the approval recorded?
- Do personal data in HR lists and sign-in logs have a shorter limit than the other records?

License reassignment
- For each strategic contract, may a license be moved from a leaver or mover to another person or device?
- If so, is there a waiting period, a notice, or a fee?
- Do device-tied or named-user terms limit reuse, and which clause says so?
- Does a transfer to an acquired company or an affiliate need the supplier's consent?

## Related

- The `program-setup` method, which sets up the body that approves policy.
- `policy-template.md`, `policy-standard-template.md`, and `policy-checklist.md` in this toolkit.
- `acquisition-gate-checklist.md` and `retirement-signoff-checklist.md`, which carry the policies into daily work.
- The `hardware-lifecycle` and `ai-intake` methods, which hold retirement and AI use rules.

Source: ISO/IEC 19770-1:2017 clauses 5.2, 7.3, 7.4 and 7.6.5, and the shared crosswalk. Paraphrased; this is not a substitute for the standard.
