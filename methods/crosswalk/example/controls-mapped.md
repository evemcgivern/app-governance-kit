## Crosswalk mapping: controls.md (C1–C3)

Source: `crosswalk.csv`. Every row used has a verified date of 2026-09-24. I took clause numbers straight from that file and didn't check them against the standards themselves.

---

### C1: Software inventory and application ownership

**Restated:** Keep a correct list of the software in use and name an owner for each application.

This control contains two obligations, so I split it:
- **C1a, inventory:** matches **XW-001** (Application and software inventory). This is the best match because it covers the core of the control.
- **C1b, ownership:** matches **XW-002** (Asset ownership assigned). I haven't added XW-002 as a second row because it covers the same three frameworks as XW-001 and adds none. The only difference is that it points to a different ISO 19770-1 clause (7.6.2).

| Framework | Clause (XW-001) | What it asks for |
|---|---|---|
| ISO/IEC 19770-1 | 8.3 | A maintained record of software assets |
| COBIT 2019 | BAI09.01 | Identify and record current assets |
| ISO/IEC 27001 | A.5.9 | An inventory of information and associated assets, including their owners |
| ISO/IEC 42001 | No direct equivalent | — |

**Gaps**
- **ISO/IEC 42001:** No clause matches. The crosswalk's AI inventory row (XW-022) also has no 42001 clause. A 42001 auditor would still want to see which AI systems are in scope of the management system (the scope clause is 4.3, in XW-003), and that they appear in the inventory. At the moment this list covers only software, not AI systems.
- **Wording:** The control says "accurate". XW-026 (data quality of asset records) uses the same clauses as XW-001, so it adds no coverage. An auditor would still ask how you show the list is accurate, for example by comparing it against discovered installs (XW-005).

**Decision needed:** Should the mapping sheet record XW-002 as well, so the ownership part is traced separately (ISO 19770-1 7.6.2)? Or is XW-001 enough?

---

### C2: Periodic access review and removal

**Restated:** Check on a schedule who can use each application, and remove access that's no longer needed.

- Best match: **XW-016** (Periodic access review). Removing access that is no longer needed is what a review leads to, so it falls within this row.
- **XW-017** (Leaver access removal) is related, but it covers removal when someone leaves or changes role, not removal after a review. It also adds no framework, so I haven't used it.

| Framework | Clause (XW-016) | What it asks for |
|---|---|---|
| ISO/IEC 19770-1 | No direct equivalent | — |
| COBIT 2019 | DSS05.04 | Manage user identities and logical access, including periodic review |
| ISO/IEC 27001 | A.5.18 | Grant, review, change and remove access rights |
| ISO/IEC 42001 | No direct equivalent | — |

**Gaps**
- **ISO/IEC 19770-1:** This standard doesn't frame access as a security control. Its auditor would instead ask whether removed access leads to licences being reclaimed and entitlement records being updated (8.4, via XW-006 and XW-007).
- **ISO/IEC 42001:** No row in the crosswalk links access review to 42001. An auditor would probably ask who can use, change or retrain AI systems, but the crosswalk has no clause for that, so I can't cite one.

**Decision needed:** Should C2 set a review frequency? "On a schedule" is not specific, and ISO 27001 and COBIT auditors will ask to see the defined interval.

---

### C3: AI risk assessment before deployment

**Restated:** Assess each AI system's risks before it goes live.

- Best match: **XW-021** (AI system risk and impact assessment before deployment). It matches both the theme and the timing.
- **XW-024** (Risk register and treatment) adds ISO 19770-1 and ISO 27001 clauses that XW-021 lacks, so it qualifies as a second row. It only partly fits, though: it covers logging risks and treating them, not an impact assessment done before deployment.

| Framework | Clause (XW-021) | What it asks for |
|---|---|---|
| ISO/IEC 19770-1 | No direct equivalent (XW-024 gives 6.1.2, 6.1.3) | General risk identification and treatment for the asset management system |
| COBIT 2019 | APO12 | Manage IT-related risk |
| ISO/IEC 27001 | No direct equivalent (XW-024 gives 6.1.3) | Information security risk treatment |
| ISO/IEC 42001 | 6.1.4, A.5 | Assess the effects of an AI system on people and society, and control those assessments |

**Gaps**
- **ISO/IEC 27001:** It has no AI-specific requirement. Its auditor would expect AI systems to go through the normal information security risk process, with results logged and treated (6.1.3 via XW-024). A separate AI assessment on its own wouldn't satisfy them.
- **ISO/IEC 19770-1:** It has no deployment gate for AI. Its auditor would ask whether the AI system is recorded as an asset before it goes live (XW-022, 8.3).
- **Scope:** "Each AI system" needs a complete AI inventory before you can show coverage, which links back to the C1 gap.

**Decision needed:** Should the mapping sheet record XW-024 as a partial second row for C3, to get the ISO 19770-1 and ISO 27001 coverage?

---

### Overall
- All three controls matched an existing row, so I'm not proposing any new rows.
- **Decision needed:** Checklist item 6 requires a second person to review the mapping and date it. Who should that reviewer be?

```findings
[
  {"type": "crosswalk_match", "id": "C1:XW-001"},
  {"type": "crosswalk_match", "id": "C2:XW-016"},
  {"type": "crosswalk_match", "id": "C3:XW-021"}
]
```
