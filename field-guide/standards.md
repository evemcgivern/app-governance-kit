# Field guide: standards and frameworks

This kit's [crosswalk explorer](../site/crosswalk.html) maps each of its 28 control themes to ISO/IEC 19770, COBIT 2019, ISO/IEC 27001, and ISO/IEC 42001. This page explains what each of those actually is, and how they relate to one another, in our own words — the explorer is where you see the exact clause-by-clause mapping.

## ISO/IEC 19770 — the IT asset management family

ISO/IEC 19770 isn't one document; it's a growing family of standards and technical specifications, each covering a different slice of IT asset management. As of this research pass, the following parts are published:

| Part | Title | Source |
|---|---|---|
| 19770-1:2017 | IT asset management systems — Requirements | [iso.org/standard/68531](https://www.iso.org/standard/68531.html) |
| 19770-2:2015 | Software identification tag | [iso.org/standard/65666](https://www.iso.org/standard/65666.html) |
| 19770-3:2016 | Entitlement schema | [iso.org/standard/52293](https://www.iso.org/standard/52293.html) |
| 19770-4:2017 | Resource utilization measurement | [iso.org/standard/68431](https://www.iso.org/standard/68431.html) |
| 19770-5:2015 | Overview and vocabulary | [iso.org/standard/68291](https://www.iso.org/standard/68291.html) |
| 19770-6:2024 | Hardware identification tag | [iso.org/standard/77642](https://www.iso.org/standard/77642.html) |
| 19770-8:2020 | Guidelines for mapping industry practices to/from the family | [iso.org/standard/72588](https://www.iso.org/standard/72588.html) |
| 19770-TS 10:2025 | Guidance for implementing ITAM | [iso.org/standard/86588](https://www.iso.org/standard/86588.html) |
| 19770-11:2021 | Requirements for bodies auditing and certifying an ITAMS | [iso.org/standard/77741](https://www.iso.org/standard/77741.html) |
| 19770-TS 13:2026 | IT asset management (title only confirmed; full scope not retrievable during this research pass) | [iso.org/standard/88836](https://www.iso.org/standard/88836.html) |

Part 1 is the management-system backbone: it sets scope, roles, IT asset risk assessment and treatment, license management, core data management, audit trails, and the review cycle that turns a one-off inventory into an ongoing system. This kit's crosswalk cites Part 1 clauses for most of its ISO/IEC 19770 rows, and adds Part 2's software-identification-tag clause, Part 3's entitlement-schema clause, or Part 4's resource-utilization clause on the handful of rows where the underlying data structure — not just the process — is the point (for example, a row about matching what's installed against what's licensed cites both Part 1's license-management clause and Part 3's entitlement schema). Parts 5, 6, 8, 10, 11, and 13 round out the family — vocabulary, a hardware equivalent of the software tag, mapping and implementation guidance, and auditor requirements — but this kit doesn't cite them directly today.

## COBIT 2019

COBIT is ISACA's framework for governing and managing enterprise IT — not an ISO standard, and broader than asset management alone. It organizes IT governance and management into objectives across five domains (evaluate-direct-monitor, align-plan-organize, build-acquire-implement, deliver-service-support, and monitor-evaluate-assess), each with its own goals and practices. Where ISO/IEC 19770-1 describes what an IT asset management system does, COBIT objectives like BAI09 (Managed Assets), APO01 (governance framework), APO10 (vendor management), APO12 (risk management), DSS05 (security services), and MEA02 (monitoring internal control) describe the broader governance and management structure that ITAM, AI governance, and access control all sit inside. The crosswalk cites specific COBIT objectives alongside the matching ISO clause for each control theme.

## ISO/IEC 27001

ISO/IEC 27001 is the information security management system (ISMS) standard — requirements for protecting the confidentiality, integrity, and availability of information, backed by an Annex A catalog of security controls. Where 19770-1 asks "do we know what we have and are we managing its lifecycle," 27001 asks "is access to it controlled and is its data protected." The two standards share several clause numbers (4.3, 5.1, 5.2, 5.3, 6.1, 7.5, 9.1, 9.3, 10) because both are built on ISO's common high-level management-system structure — the same reason the crosswalk can line up a single control theme against near-identical clause numbers in both frameworks.

## ISO/IEC 42001

ISO/IEC 42001 applies that same management-system structure to artificial intelligence specifically: an AI policy (clause 5.2), assigned roles and responsibilities (5.3), AI-specific risk assessment and treatment (6.1.2 through 6.1.4), and an Annex A of AI-specific controls covering areas like AI system impact assessment, supplier oversight, and data for AI systems. It relates to 19770 the way a specialized management-system standard relates to a general one: 42001 is to an AI system roughly what 19770-1 is to an IT asset generally, and the two overlap in practice wherever this kit treats an AI system as an entry in the same asset inventory an application would get.

## How they fit together

None of these four stands alone in the crosswalk: a single control theme is usually backed by an ISO/IEC 19770 clause for the asset-management process, a COBIT objective for the governance context, and either ISO/IEC 27001 or ISO/IEC 42001 (sometimes both) for the security or AI-specific control. The [crosswalk explorer](../site/crosswalk.html) is where that exact mapping lives, row by row, with the specific clause title and source for every cell.
