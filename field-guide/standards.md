# Field guide: standards and frameworks

This kit's [crosswalk explorer](../site/crosswalk.html) maps each of its 30 control themes to ISO/IEC 19770, COBIT 2019, ISO/IEC 27001, and ISO/IEC 42001. This page explains what each of those is and how they relate to one another, in our own words. A theme is usually backed by an ISO/IEC 19770 clause for the asset-management process, a COBIT objective for the governance context, and either ISO/IEC 27001 or ISO/IEC 42001 (sometimes both) for the security or AI-specific control. The explorer has the exact mapping, row by row, with the clause title and source for every cell.

## ISO/IEC 19770: the IT asset management family

ISO/IEC 19770 is a growing family of standards and technical specifications, each covering a different slice of IT asset management. At the last check, these parts are published:

| Part | Title | Source |
|---|---|---|
| 19770-1:2017 (Amd 1:2024) | IT asset management systems — Requirements | [iso.org/standard/68531](https://www.iso.org/standard/68531.html) |
| 19770-2:2015 | Software identification tag | [iso.org/standard/65666](https://www.iso.org/standard/65666.html) |
| 19770-3:2016 | Entitlement schema | [iso.org/standard/52293](https://www.iso.org/standard/52293.html) |
| 19770-4:2017 | Resource utilization measurement | [iso.org/standard/68431](https://www.iso.org/standard/68431.html) |
| 19770-5:2015 | Overview and vocabulary | [iso.org/standard/68291](https://www.iso.org/standard/68291.html) |
| 19770-6:2024 | Hardware identification tag | [iso.org/standard/77642](https://www.iso.org/standard/77642.html) |
| 19770-8:2020 | Guidelines for mapping industry practices to/from the family | [iso.org/standard/72588](https://www.iso.org/standard/72588.html) |
| 19770-TS 10:2025 | Guidance for implementing ITAM | [iso.org/standard/86588](https://www.iso.org/standard/86588.html) |
| 19770-11:2021 | Requirements for bodies auditing and certifying an ITAMS | [iso.org/standard/77741](https://www.iso.org/standard/77741.html) |
| 19770-TS 13:2026 | Guidance on the incorporation of sustainability aspects in an IT asset management system | [iso.org/standard/88836](https://www.iso.org/standard/88836.html) |

Part 1 is the management-system backbone: it sets scope, roles, IT asset risk assessment and treatment, license management, core data management, audit trails, and the review cycle that turns a one-off inventory into an ongoing system. This kit's crosswalk cites Part 1 clauses for most of its ISO/IEC 19770 rows, and adds Part 2's software-identification-tag clause, Part 3's entitlement-schema clause, or Part 4's resource-utilization clause on the handful of rows where the underlying data structure, not just the process, is the point (for example, a row about matching what's installed against what's licensed cites both Part 1's license-management clause and Part 3's entitlement schema).

Parts 5, 6, 8, 10, 11, and 13 round out the family: vocabulary, a hardware equivalent of the software tag, mapping and implementation guidance, auditor requirements, and sustainability guidance, but this kit cites only Part 13 among them, on the portfolio-rationalization row (§6.1 Table 1, §4.4.3). Part 13 is guidance on adding sustainability aspects to an ITAM system, and Amendment 1:2024 to Part 1 adds a climate-change check to clauses 4.1 and 4.2; neither changes a crosswalk row.

## COBIT 2019

COBIT is ISACA's framework for governing and managing enterprise IT, not an ISO standard. It organizes IT governance and management into objectives across five domains (evaluate-direct-monitor, align-plan-organize, build-acquire-implement, deliver-service-support, and monitor-evaluate-assess), each with its own goals and practices. Where ISO/IEC 19770-1 describes what an IT asset management system does, COBIT objectives like BAI09 (Managed Assets), APO01 (governance framework), APO10 (vendor management), APO12 (risk management), DSS05 (security services), and MEA02 (monitoring internal control) describe the broader governance and management structure that ITAM, AI governance, and access control all sit inside. The crosswalk cites specific COBIT objectives alongside the matching ISO clause for each control theme.

## ISO/IEC 27001

ISO/IEC 27001 is the information security management system (ISMS) standard: requirements for protecting the confidentiality, integrity, and availability of information, backed by an Annex A catalog of security controls. 19770-1 covers whether you know what you have and manage its lifecycle; 27001 covers whether access to it is controlled and its data protected. The two standards share several clause numbers (4.3, 5.1, 5.2, 5.3, 6.1.2, 6.1.3, 9.1, 9.2, 9.3) because both follow ISO's common management-system structure. 19770-1 gets there by building on ISO 55001 (asset management), and its risk clauses follow 27001 6.1.2 and 6.1.3. The numbering drifts in places: documented information is 7.5 in 27001 but 7.6 in 19770-1, and continual improvement is 10.1 in 27001 but 10.3 in 19770-1. The crosswalk therefore lists each standard's own numbers instead of assuming they match. The Annex A control numbers (A.5.9 and so on) use the 27001:2022 edition.

## ISO/IEC 42001

ISO/IEC 42001 applies that same management-system structure to artificial intelligence specifically: an AI policy (clause 5.2), assigned roles and responsibilities (5.3), AI-specific risk assessment and treatment (6.1.2 through 6.1.4), and an Annex A of AI-specific controls covering areas like AI system impact assessment, supplier oversight, and data for AI systems. It relates to 19770 the way a specialized management-system standard relates to a general one: the two overlap in practice wherever this kit treats an AI system as an entry in the same asset inventory an application would get.
