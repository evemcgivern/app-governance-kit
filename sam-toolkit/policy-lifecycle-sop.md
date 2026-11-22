# Policy lifecycle SOP

## Purpose

Keep each ITAM policy written, approved, published, understood, and current, so that people can follow it and an auditor can see how it was made and changed.

## Scope

Applies to the smallest useful ITAM policy set and the standards beneath it:

- The IT asset management umbrella policy, owned by the ITAM manager and approved by the sponsor. It covers license compliance, acceptable use, and penalties.
- The software acquisition and exceptions policy, with a standard path, a non-standard path, and approval that escalates with cost and risk.
- The software standards, which are a catalog and not a policy: approved titles by role, versions, and SaaS. A selection committee owns them.
- The vendor management policy, one policy with a section for each topic.
- The records and evidence policy: proofs, authorizations, and retention. Counsel sets the retention periods. **Decision needed:** counsel.

Retirement follows `retirement-signoff-checklist.md` and, for devices, the `hardware-lifecycle` method. AI tool intake follows the `ai-intake` method. Both link to this process for their policy text. Use `policy-template.md` and `policy-standard-template.md` to draft, and `policy-checklist.md` to test the draft.

## Roles

- **Policy owner**: drafts the policy, keeps it current, and answers for it. A named role such as the ITAM manager.
- **Approver**: the sponsor, who approves the policy and any change to its scope.
- **Reviewers**: Legal, Security, Procurement, Finance, HR, and business leads, each consulted on their own part.
- **Counsel**: reviews enforcement wording and any retention period before approval.

## Frequency

Each policy is reviewed at least yearly, and sooner when a trigger occurs: a vendor audit, a merger, a move to cloud, a change of sponsor, or a finding from an internal check.

## Steps

1. The owner drafts from `policy-template.md`, or from `policy-standard-template.md` for a standard [[XW-003]]
2. The owner consults Legal, Security, Procurement, Finance, HR, and the business leads, and records what each changed [[XW-004]]
3. The owner compares the draft with other policies and records any conflict and who resolves it [[XW-003]]
4. The owner tests the draft with `policy-checklist.md` and fixes each failed item, so counsel sees a draft that already meets the checklist [[XW-025]]
5. Counsel reviews the enforcement wording and any retention period. **Decision needed:** counsel [[XW-020]]
6. The sponsor approves, and the approval is dated and filed. **Decision needed:** sponsor [[XW-027]]
7. The owner publishes the approved version, with its version number, in one controlled location [[XW-020]] [[XW-030]]
8. The owner communicates it, trains the people it binds, and records each acknowledgment [[XW-004]] [[XW-030]]
9. Exceptions are logged in `authorization-log.csv` with an approver and an end date, and each is reviewed at expiry [[XW-009]] [[XW-019]]
10. The owner reviews the policy yearly or on a trigger, and records the result even when nothing changes [[XW-025]]
11. When a version is replaced, the owner withdraws the old one and keeps it in the archive with its dates [[XW-020]]

## Evidence to retain

- Each approved version, with its dated sponsor approval.
- The consultation record and the conflict record.
- Counsel's review of the enforcement wording and any retention period.
- The completed policy checklist.
- The communication plan and the acknowledgment records.
- The exceptions in `authorization-log.csv`, each with its end date and review.
- The review record and change history, including reviews that changed nothing.

Design these records as a by-product of the steps, not something rebuilt when an auditor asks.

## Questions to take to counsel and the contract owner

These are questions only. The answers belong to counsel and the contract owner, and the owner records each answer with a date in the review record.

Penalties and enforcement
- Which consequences may the policy state for a breach, and for which kinds of breach?
- Does any local law or employment agreement limit how the policy may be enforced?
- Who may apply a consequence, and what must be recorded before they do?
- Does the wording for contractors and temporary staff need to differ from the wording for employees?

Retention
- What period applies to each record type: proofs of purchase, contracts, authorizations, wipe certificates, acknowledgments, and consultation records?
- Does any legal hold, open audit, or dispute change a period?
- Who may destroy a record when its period ends, and how is the destruction recorded?
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
