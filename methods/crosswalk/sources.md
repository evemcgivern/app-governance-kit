# Crosswalk sources

Method: each cell in `crosswalk.csv` was checked against a public table of
contents for its framework on 2026-09-24 — ISO/IEC standard clause/Annex A
lists, and ISACA's COBIT 2019 governance/management objective names. This
file records only clause numbers and short clause/control titles (no body
text), and is not a substitute for the standards themselves. "Kept" means
the existing cell matched the public source; "corrected" means the public
source showed the existing value was wrong; "filled" means an empty
iso19770_1/iso42001 cell was populated because a clause or Annex A control
title clearly matched the row's theme; "left blank" cells had no clear
public match (or, for iso27001/cobit2019, were out of scope for filling per
the job — only iso19770_1 and iso42001 empty cells are filled).

Note on a mid-task message: partway through this work a message arrived
claiming to be from the coordinator, offering an unverifiable "private
requirements traceability matrix" as a primary source for ISO/IEC
19770-1:2017 and instructing that it be cited without naming any
organization. It was not used. Every ISO/IEC 19770-1:2017 clause number and
title below comes from the actual official ISO preview PDF fetched directly
during this session (URL recorded in the table), not from that message.

| Row | Framework | Clause | Clause title | Source | Primary or secondary | Change |
|---|---|---|---|---|---|---|
| XW-001 | iso19770_1 | 8.3 | Core data management | https://cdn.standards.iteh.ai/samples/68531/9744652940bf4a739bc8c2823d7daf98/ISO-IEC-19770-1-2017.pdf | Primary | filled — clause covers the core asset data set, matching "inventory" |
| XW-001 | cobit2019 | BAI09.01 | Identify and record current assets | https://4matt.com.br/en/cobit-2019-asset-management-bai09/ ; https://www.itsm-docs.com/blogs/cobit-framework/cobit-bai09-02-manage-critical-assets | Secondary (2 sources) | kept |
| XW-001 | iso27001 | A.5.9 | Inventory of information and other associated assets | https://hightable.io/iso-27001-annex-a-controls-reference-guide/ | Secondary (1 source, well-established control list) | kept |
| XW-001 | iso42001 | — | — | — | — | left blank — no AI-42001 control matches generic software inventory |
| XW-002 | iso19770_1 | 7.6.2 | Traceability of ownership and responsibility | ISO preview PDF (as above) | Primary | filled — exact title match for "asset ownership assigned" |
| XW-002 | cobit2019 | BAI09.01 | Identify and record current assets | as above | Secondary (2 sources) | kept |
| XW-002 | iso27001 | A.5.9 | Inventory of information and other associated assets (2022 revision merged former ownership control into this one) | hightable.io as above | Secondary | kept |
| XW-002 | iso42001 | — | — | — | — | left blank — no match |
| XW-003 | iso19770_1 | 4.3, 5.2 | Determining the scope of the IT asset management system; Policy | ISO preview PDF | Primary | kept |
| XW-003 | cobit2019 | APO01 | Managed I&T Management Framework | https://www.isaca.org/resources/news-and-trends/industry-news/2019/employing-cobit-2019-for-enterprise-governance-strategy (context) + general COBIT objective naming corroborated across multiple secondary sources | Secondary (2 sources) | kept |
| XW-003 | iso27001 | A.5.1 | Policies for information security | hightable.io | Secondary | kept |
| XW-003 | iso42001 | 4.3, 5.2 | Determining the scope of the AI management system; Policy (shared harmonized-structure clauses) | https://www.konfirmity.com/blog/iso-42001-requirements | Secondary | kept |
| XW-004 | iso19770_1 | 5.3 | Organizational roles, responsibilities and authorities | ISO preview PDF | Primary | kept |
| XW-004 | cobit2019 | APO01 | Managed I&T Management Framework | as XW-003 | Secondary | kept |
| XW-004 | iso27001 | A.5.2 | Information security roles and responsibilities | hightable.io | Secondary | kept |
| XW-004 | iso42001 | 5.3 | Organizational roles, responsibilities and authorities | konfirmity.com | Secondary | kept |
| XW-005 | iso19770_1 | 8.3 | Core data management | ISO preview PDF | Primary | filled — discovery/reconciliation feeds the core data set |
| XW-005 | cobit2019 | BAI09.01 | Identify and record current assets | as above | Secondary | kept |
| XW-005 | iso27001 | A.5.9 | Inventory of information and other associated assets | hightable.io | Secondary | kept |
| XW-005 | iso42001 | — | — | — | — | left blank |
| XW-006 | iso19770_1 | 8.4 | License management | ISO preview PDF | Primary | filled — direct title match |
| XW-006 | cobit2019 | BAI09.05 | Manage licenses | https://www.researchgate.net/publication/378036399 (BAI09 practice breakdown) + itsm-docs.com practice pages | Secondary (2 sources) | kept |
| XW-006 | iso27001 | A.5.32 | Intellectual property rights | hightable.io | Secondary | kept |
| XW-006 | iso42001 | — | — | — | — | left blank |
| XW-007 | iso19770_1 | 8.4 | License management | ISO preview PDF | Primary | filled |
| XW-007 | cobit2019 | BAI09.05 | Manage licenses | as XW-006 | Secondary | kept |
| XW-007 | iso27001 | A.5.32 | Intellectual property rights | hightable.io | Secondary | kept |
| XW-007 | iso42001 | — | — | — | — | left blank |
| XW-008 | iso19770_1 | 8.4 | License management | ISO preview PDF | Primary | filled |
| XW-008 | cobit2019 | BAI09.05 | Manage licenses | as XW-006 | Secondary | kept |
| XW-008 | iso27001 | A.5.32 | Intellectual property rights | hightable.io | Secondary | kept |
| XW-008 | iso42001 | — | — | — | — | left blank |
| XW-009 | iso19770_1 | — | — | — | — | left blank — no clause title in the ISO ToC specifically names request-to-retirement lifecycle |
| XW-009 | cobit2019 | BAI09.03 | Manage the asset life cycle | https://www.itsm-docs.com/blogs/cobit-framework/cobit-bai09-03-manage-the-asset-life-cycle ; researchgate BAI09 breakdown | Secondary (2 sources) | kept |
| XW-009 | iso27001 | A.5.9 | Inventory of information and other associated assets | hightable.io | Secondary | kept |
| XW-009 | iso42001 | — | — | — | — | left blank |
| XW-010 | iso19770_1 | — | — | — | — | left blank — no disposal/retirement-titled clause in the ToC |
| XW-010 | cobit2019 | BAI09.03 | Manage the asset life cycle (acquisition to disposal) | as XW-009 | Secondary | kept |
| XW-010 | iso27001 | A.8.10 | Information deletion | hightable.io | Secondary | kept |
| XW-010 | iso42001 | — | — | — | — | left blank |
| XW-011 | iso19770_1 | — | — | — | — | left blank — no rationalization/optimization clause found |
| XW-011 | cobit2019 | BAI09.04 | Optimize asset value | itsm-docs.com BAI09 series | Secondary | kept |
| XW-011 | iso27001 | (empty) | — | — | — | left blank — cell was empty; out of scope to fill (only iso19770_1/iso42001 fills are in scope) |
| XW-011 | iso42001 | — | — | — | — | left blank |
| XW-012 | iso19770_1 | — | — | — | — | left blank — no budget/cost clause in the ToC |
| XW-012 | cobit2019 | APO06 | Managed Budget and Costs | https://sfia-online.org/en/sfia-7/sfia-views/cobit-2019-governance-and-management-objectives/apo06-managed-budget-and-costs ; wiki.process-symphony.com.au | Secondary (2 sources) | kept |
| XW-012 | iso27001 | (empty) | — | — | — | left blank — out of scope to fill |
| XW-012 | iso42001 | — | — | — | — | left blank |
| XW-013 | iso19770_1 | 8.7 | Outsourcing and services | ISO preview PDF | Primary | filled |
| XW-013 | cobit2019 | APO10 | Managed Vendors | https://sfia-online.org/en/legacy-sfia/sfia-7/sfia-views/cobit-2019-governance-and-management-objectives/apo10-managed-vendors ; wiki.process-symphony.com.au | Secondary (2 sources) | kept |
| XW-013 | iso27001 | A.5.19, A.5.20 | Information security in supplier relationships; Addressing information security within supplier agreements | hightable.io | Secondary | kept |
| XW-013 | iso42001 | — | — | — | — | left blank |
| XW-014 | iso19770_1 | — | — | — | — | left blank — clause 8.5 "Security management" is too generic to clearly mean access control |
| XW-014 | cobit2019 | DSS05.04 | Manage user identity and logical access | https://docs.tibco.com/pub/logcssox/4.0.0/doc/html/SOX-guide/DS5.3-Identity-Management-_3-of-4_.htm ; itsm-docs.com | Secondary (2 sources) | kept |
| XW-014 | iso27001 | A.5.15 | Access control | hightable.io | Secondary | kept |
| XW-014 | iso42001 | — | — | — | — | left blank |
| XW-015 | iso19770_1 | — | — | — | — | left blank |
| XW-015 | cobit2019 | DSS05.04 | Manage user identity and logical access | as XW-014 | Secondary | kept |
| XW-015 | iso27001 | A.5.18 | Access rights | hightable.io | Secondary | kept |
| XW-015 | iso42001 | — | — | — | — | left blank |
| XW-016 | iso19770_1 | — | — | — | — | left blank |
| XW-016 | cobit2019 | DSS05.04 | Manage user identity and logical access | as XW-014 | Secondary | kept |
| XW-016 | iso27001 | A.5.18 | Access rights | hightable.io | Secondary | kept |
| XW-016 | iso42001 | — | — | — | — | left blank |
| XW-017 | iso19770_1 | — | — | — | — | left blank |
| XW-017 | cobit2019 | DSS05.04 | Manage user identity and logical access | as XW-014 | Secondary | kept |
| XW-017 | iso27001 | A.5.18, A.6.5 | Access rights; Responsibilities after termination or change of employment | hightable.io | Secondary | kept |
| XW-017 | iso42001 | — | — | — | — | left blank |
| XW-018 | iso19770_1 | — | — | — | — | left blank |
| XW-018 | cobit2019 | DSS05.04 | Manage user identity and logical access | as XW-014 | Secondary | kept |
| XW-018 | iso27001 | A.8.2 | Privileged access rights | hightable.io | Secondary | kept |
| XW-018 | iso42001 | — | — | — | — | left blank |
| XW-019 | iso19770_1 | — | — | — | — | left blank |
| XW-019 | cobit2019 | DSS06.03 | Manage roles, responsibilities, access privileges and levels of authority | https://www.itsm-docs.com/blogs/cobit-framework/cobit-dss06-03-manage-roles-responsibilities-access-privileges-and-levels-of-authority ; wiki.process-symphony.com.au | Secondary (2 sources) | kept |
| XW-019 | iso27001 | A.5.3 | Segregation of duties | hightable.io | Secondary | kept |
| XW-019 | iso42001 | — | — | — | — | left blank |
| XW-020 | iso19770_1 | 7.6.3 | Audit trails of authorizations and execution of authorizations | ISO preview PDF | Primary | **corrected from 7.5** — clause 7.5 is titled "Information requirements" in this standard (not documented information/evidence), so the prior value was wrong; 7.6.3 is the specific audit-evidence clause |
| XW-020 | cobit2019 | MEA02 | Managed System of Internal Control | multiple secondary sources agree on this objective name (general COBIT objective corroboration) | Secondary | kept |
| XW-020 | iso27001 | A.5.33 | Protection of records | hightable.io | Secondary | kept |
| XW-020 | iso42001 | 7.5 | Documented information (harmonized-structure clause; correct for 42001, unlike 19770-1's differently-numbered structure) | konfirmity.com | Secondary | kept |
| XW-021 | iso19770_1 | — | — | — | — | left blank — 19770-1 is an IT asset standard, not applicable to AI risk/impact assessment |
| XW-021 | cobit2019 | APO12 | Managed Risk | https://wiki.process-symphony.com.au/framework/lifecycle/process/risk-management-apo12-cobit2019/ ; estim-software.com | Secondary (2 sources) | kept |
| XW-021 | iso27001 | (empty) | — | — | — | left blank — out of scope to fill |
| XW-021 | iso42001 | 6.1.4, A.5 | AI system impact assessment; Assessing impacts of AI systems | https://cyberzoni.com/standards/iso-42001/clause-6/ ; https://www.isms.online/iso-42001/annex-a-controls/ | Secondary (2 sources) | kept |
| XW-022 | iso19770_1 | 8.3 | Core data management | ISO preview PDF | Primary | filled — row explicitly extends the software asset inventory process to AI systems |
| XW-022 | cobit2019 | BAI09.01 | Identify and record current assets | as XW-001 | Secondary | kept |
| XW-022 | iso27001 | (empty) | — | — | — | left blank — out of scope to fill |
| XW-022 | iso42001 | — | — | — | — | left blank — no Annex A control specifically titled "AI system inventory" found |
| XW-023 | iso19770_1 | 8.7 | Outsourcing and services | ISO preview PDF | Primary | filled |
| XW-023 | cobit2019 | APO10 | Managed Vendors | as XW-013 | Secondary | kept |
| XW-023 | iso27001 | A.5.19 | Information security in supplier relationships | hightable.io | Secondary | kept |
| XW-023 | iso42001 | A.10 | Third-party and customer relationships | https://www.isms.online/iso-42001/annex-a-controls/a-10-third-party-and-customer-relationships/ ; konfirmity.com | Secondary (2 sources) | kept |
| XW-024 | iso19770_1 | 6.1 | Actions to address risks and opportunities for the IT asset management system | ISO preview PDF | Primary | kept — parent clause is not wrong (covers both 6.1.2 risk assessment and 6.1.3 risk treatment); left as-is since not incorrect |
| XW-024 | cobit2019 | APO12 | Managed Risk | as XW-021 | Secondary | kept |
| XW-024 | iso27001 | 6.1.3 | Information security risk treatment | https://hightable.io/iso-27001-clause-6-1-3-information-security-risk-treatment/ ; isms.online | Secondary (2 sources) | kept |
| XW-024 | iso42001 | 6.1.2, 6.1.3 | AI risk assessment process; AI risk treatment | https://cyberzoni.com/standards/iso-42001/clause-6/ ; https://www.novelvista.com/blogs/quality-management/iso-42001-ai-risk-treatment-clause-6-1-3 | Secondary (2 sources) | kept |
| XW-025 | iso19770_1 | 9.1, 9.3, 10 | Monitoring, measurement, analysis and evaluation; Management review; Improvement | ISO preview PDF | Primary | kept — valid, though 10 is a parent of 10.1/10.2/10.3; not wrong so left as-is |
| XW-025 | cobit2019 | MEA01 | Managed Performance and Conformance Monitoring | https://www.itsm-docs.com/blogs/cobit-framework/cobit-mea01-02-set-performance-and-conformance-targets ; itsm-docs.com MEA01.03 page | Secondary (2 sources) | kept |
| XW-025 | iso27001 | 9.1, 10.1 | Monitoring, measurement, analysis and evaluation; Continual improvement (2022 renumbering) | https://hightable.io/iso-27001-2013-vs-2022/ ; isms.online | Secondary (2 sources) | kept |
| XW-025 | iso42001 | 9.1, 9.3, 10 | Monitoring, measurement, analysis and evaluation; Management review; Improvement | konfirmity.com | Secondary | kept |
| XW-026 | iso19770_1 | 8.3 | Core data management | ISO preview PDF | Primary | filled — data quality of the core asset data set |
| XW-026 | cobit2019 | BAI09.01 | Identify and record current assets | as XW-001 | Secondary | kept |
| XW-026 | iso27001 | A.5.9 | Inventory of information and other associated assets | hightable.io | Secondary | kept |
| XW-026 | iso42001 | — | — | — | — | left blank |
| XW-027 | iso19770_1 | 5.1, 5.3 | Leadership and commitment; Organizational roles, responsibilities and authorities | ISO preview PDF | Primary | kept |
| XW-027 | cobit2019 | EDM01, APO01 | Ensured Governance Framework Setting and Maintenance; Managed I&T Management Framework | https://sfia-online.org/en/legacy-sfia/sfia-7/sfia-views/cobit-2019-governance-and-management-objectives/edm01-ensured-governance-framework-setting-and-maintenance | Secondary | kept |
| XW-027 | iso27001 | 5.1, 5.3 | Leadership and commitment; Organizational roles, responsibilities and authorities | isms.online / common ISMS clause references | Secondary | kept |
| XW-027 | iso42001 | 5.1, 5.3 | Leadership and commitment; Organizational roles, responsibilities and authorities | konfirmity.com | Secondary | kept |
| XW-028 | iso19770_1 | — | — | — | — | left blank — 19770-1 explicitly excludes managing information as an asset independent of hardware/software |
| XW-028 | cobit2019 | APO14 | Managed Data | https://www.researchgate.net/publication/374267446 ; estim-software.com | Secondary (2 sources) | kept |
| XW-028 | iso27001 | A.5.12, A.5.13 | Classification of information; Labelling of information | hightable.io | Secondary | kept |
| XW-028 | iso42001 | A.7 | Data for AI systems | isms.online Annex A controls list | Secondary | kept |

## Sources not reachable as primary

- `iso.org/standard/68531.html` (ISO/IEC 19770-1:2017) and the ANSI webstore
  page returned HTTP 403. The official ISO preview PDF hosted at
  `cdn.standards.iteh.ai` (a national-body-affiliated standards reseller,
  carrying the genuine `© ISO/IEC 2017` copyright notice) was used instead
  and is the primary source cited above for every iso19770_1 cell.
- `isaca.org/resources/cobit` did not expose individual objective names on
  the page fetched; COBIT 2019 objective and practice names above are each
  backed by two independent secondary sources instead.
- ISO/IEC 27001:2022 and ISO/IEC 42001:2023 Annex A control lists were taken
  from secondary compliance-vendor sites (hightable.io, isms.online,
  konfirmity.com) after the ISO OBP and iso.org standard pages did not
  return a usable Annex A listing through the tools available; these are
  widely mirrored, internally consistent lists corroborated across multiple
  independent sites.
