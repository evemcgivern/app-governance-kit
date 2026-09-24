All three controls have a match in `crosswalk.csv`: **C1 → XW-001, C2 → XW-016, C3 → XW-021**. The gaps are mostly in ISO 42001 (C1, C2) and in ISO 19770-1 and ISO 27001 (C3).

## C1: Maintain an accurate inventory of software and who owns each application

**In plain terms:** keep a complete list of your software, and name an owner for each application. This control makes two demands, so I mapped each one.

| Framework | Part (a): inventory, XW-001 | Part (b): ownership, XW-002 | What it asks for |
|---|---|---|---|
| ISO 19770-1 | 8.3 | 7.6.2 | A current record of all software assets; a named, accountable owner for each |
| COBIT 2019 | BAI09.01 | BAI09.01 | Identify and record assets, including who is responsible for them |
| ISO 27001 | A.5.9 | A.5.9 | An inventory of information assets, each with an owner |
| ISO 42001 | no direct equivalent | no direct equivalent | — |

**Why XW-001 is the best row:** "accurate inventory" is the main obligation. XW-002 only covers the ownership part, and it adds no framework that XW-001 lacks. XW-026 (data quality) supports the word "accurate" but also adds no framework.

**Gap:**
- **ISO 42001:** no equivalent, because 42001 governs AI systems, not software in general. A 42001 auditor would still ask whether the inventory marks which applications are AI systems. XW-022 (AI inventory) has no 42001 clause either, so this gap holds even for AI.

## C2: Review user access to applications on a schedule and remove access no longer needed

**In plain terms:** on a set schedule, check who has access to each application and remove access that is no longer justified.

| Framework | Clause (XW-016) | What it asks for |
|---|---|---|
| ISO 19770-1 | no direct equivalent | — |
| COBIT 2019 | DSS05.04 | Manage identities and access rights, including periodic re-checks |
| ISO 27001 | A.5.18 | Grant, review and remove access rights |
| ISO 42001 | no direct equivalent | — |

**Why XW-016 is the best row:** a periodic review is the core of this control, and removal is what the review leads to. XW-017 (removing access when people leave) adds 27001 A.6.5 but no new framework, so I did not use it.

**Gaps:**
- **ISO 19770-1:** it tracks assets and licenses, not user access. A 19770-1 auditor would instead ask whether removed accounts free up license entitlements (XW-007).
- **ISO 42001:** a 42001 auditor would ask whether the review covers access to AI systems and their training data.

## C3: Assess each AI system for risk before it is deployed

**In plain terms:** no AI system goes into production until its risk and impact have been assessed.

| Framework | XW-021 (best) | XW-024 (second) | What it asks for |
|---|---|---|---|
| ISO 19770-1 | no direct equivalent | 6.1.2, 6.1.3 | General risk assessment and treatment for the asset management system |
| COBIT 2019 | APO12 | APO12 | Manage risk |
| ISO 27001 | no direct equivalent | 6.1.3 | Treat information-security risks |
| ISO 42001 | 6.1.4, A.5 | 6.1.2, 6.1.3 | Assess an AI system's impact on people and society, plus general AI risk assessment |

**Why these two rows:** XW-021 matches both the "AI" and "before deployment" parts of the control. I named XW-024 as a second row because it adds 19770-1 and 27001, which XW-021 lacks. It is generic risk handling, though, not a check before deployment.

**Gaps:**
- **ISO 19770-1:** no clause specific to AI or to deployment. An auditor would ask whether AI systems appear in the asset inventory (XW-022, 8.3).
- **ISO 27001:** no step that blocks deployment. An auditor would expect security risks to be assessed for the AI system under clause 6.1.3.
- **Decision needed:** whether to rely on XW-024 for 19770-1 and 27001 coverage, or accept that they have no direct equivalent for C3.

## Notes
- No new rows are proposed, because every control had a match.
- **Decision needed:** `checklist.md` item 6 requires a second person to review and date this mapping.
- **Unverified:** every row shows a verified date of 2026-09-24, today. I did not check the clause numbers against the standards themselves.

```findings
[
  {"type": "crosswalk_match", "id": "C1:XW-001"},
  {"type": "crosswalk_match", "id": "C2:XW-016"},
  {"type": "crosswalk_match", "id": "C3:XW-021"}
]
```

🟢 All 3 controls mapped. Waiting on you: whether to use XW-024 for C3, and who does the second-person review.
