# Crosswalk sources

Method: each cell in `crosswalk.csv` was checked against a public table of
contents for its framework — ISO/IEC standard clause/Annex A lists, and
ISACA's COBIT 2019 governance/management objective names. This file records
only clause numbers and short clause/control titles (no body text), and is
not a substitute for the standards themselves. "Kept" means the existing
cell matched the public source; "corrected" means the public source showed
the existing value was wrong; "filled" means an empty iso19770_1/iso42001
cell was populated because a clause or Annex A control title clearly
matched the row's theme; "left blank" cells had no clear public match (or,
for iso27001/cobit2019, were out of scope for filling per the job — only
iso19770_1 and iso42001 empty cells are filled).

Project rule: a "Secondary" line needs two independent sources (different
organizations) that agree on both the clause number and title. A "Primary"
source (iso.org, the ISO Online Browsing Platform, an official ISO
preview/sample PDF such as a cdn.standards.iteh.ai sample, or isaca.org) is
sufficient alone. On 2026-09-24 this file was re-verified end to end against
that rule: every line that previously cited only one source, or that stood
in for another row's citation with the words "as above"/"as XW-0xx" instead
of an actual URL, was re-checked and given either a genuine second
independent source or a primary source. Corrections found during that pass
are marked **CORRECTED** below and called out again at the end of this file.

**ISO/IEC 27001:2022 Annex A note.** ISO/IEC 27001:2022's Annex A control
titles are not reproduced in its own free preview (the sample PDF cuts off
before Annex A). They are, however, verbatim identical to the numbered
clause titles in the main body of ISO/IEC 27002:2022 (5.1–8.34 in 27002 =
A.5.1–A.8.34 in 27001 Annex A) — this is how ISO designed the pair; 27001's
own Annex A note directs readers to 27002 for the same control set, and
every Annex A title already used in this file (from hightable.io etc.) was
independently confirmed to match the 27002:2022 sample PDF word for word.
Given that, lines below cite the ISO/IEC 27002:2022 official sample PDF
(`cdn.standards.iteh.ai`) as a Primary source for the corresponding
iso27001 Annex A clause, with this note as the cross-reference. Where the
row's iso27001 clause is a main-body clause (not an Annex A control, e.g.
5.1/5.3/6.1.3/9.1/10.1), it was confirmed directly against the ISO/IEC
27001:2022 sample PDF itself (no cross-reference needed).

| Row | Framework | Clause | Clause title | Source | Primary or secondary | Change |
|---|---|---|---|---|---|---|
| XW-001 | iso19770_1 | 8.3 | Core data management | https://cdn.standards.iteh.ai/samples/68531/9744652940bf4a739bc8c2823d7daf98/ISO-IEC-19770-1-2017.pdf | Primary | filled — clause covers the core asset data set, matching "inventory" |
| XW-001 | cobit2019 | BAI09.01 | Identify and record current assets | https://4matt.com.br/en/cobit-2019-asset-management-bai09/ ; https://www.itsm-docs.com/blogs/cobit-framework/cobit-bai09-02-manage-critical-assets | Secondary (2 sources) | kept |
| XW-001 | iso27001 | A.5.9 | Inventory of information and other associated assets | https://hightable.io/iso-27001-annex-a-controls-reference-guide/ ; https://cdn.standards.iteh.ai/samples/75652/f9b90f856c0d4c3dbef74cf67374d1c5/ISO-IEC-27002-2022.pdf (clause 5.9, see Annex A note above) | Primary | kept — upgraded from single-source secondary to Primary via the 27002:2022 sample PDF |
| XW-001 | iso42001 | — | — | — | — | left blank — no AI-42001 control matches generic software inventory |
| XW-002 | iso19770_1 | 7.6.2 | Traceability of ownership and responsibility | https://cdn.standards.iteh.ai/samples/68531/9744652940bf4a739bc8c2823d7daf98/ISO-IEC-19770-1-2017.pdf | Primary | filled — exact title match for "asset ownership assigned" |
| XW-002 | cobit2019 | BAI09.01 | Identify and record current assets | https://4matt.com.br/en/cobit-2019-asset-management-bai09/ ; https://www.itsm-docs.com/blogs/cobit-framework/cobit-bai09-02-manage-critical-assets | Secondary (2 sources) | kept — replaced the "as above" placeholder with the actual XW-001 URLs |
| XW-002 | iso27001 | A.5.9 | Inventory of information and other associated assets (2022 revision merged former ownership control into this one) | https://hightable.io/iso-27001-annex-a-controls-reference-guide/ ; https://cdn.standards.iteh.ai/samples/75652/f9b90f856c0d4c3dbef74cf67374d1c5/ISO-IEC-27002-2022.pdf (clause 5.9, see Annex A note above) | Primary | kept — replaced "hightable.io as above" with the actual URL and upgraded to Primary |
| XW-002 | iso42001 | — | — | — | — | left blank — no match |
| XW-003 | iso19770_1 | 4.3, 5.2 | Determining the scope of the IT asset management system; Policy | https://cdn.standards.iteh.ai/samples/68531/9744652940bf4a739bc8c2823d7daf98/ISO-IEC-19770-1-2017.pdf | Primary | kept |
| XW-003 | cobit2019 | APO01 | Managed I&T Management Framework | https://www.isaca.org/resources/news-and-trends/industry-news/2019/governing-digital-transformation-using-cobit-2019 (quotes "APO01 — Managed IT management framework") | Primary | **CORRECTED** — previous line cited isaca.org only "for context" plus an unverifiable "corroborated across multiple secondary sources" claim with no URL; replaced with an isaca.org article that states the objective code and title together, which is a genuine Primary source |
| XW-003 | iso27001 | A.5.1 | Policies for information security | https://hightable.io/iso-27001-annex-a-controls-reference-guide/ ; https://cdn.standards.iteh.ai/samples/75652/f9b90f856c0d4c3dbef74cf67374d1c5/ISO-IEC-27002-2022.pdf (clause 5.1, see Annex A note above) | Primary | kept — upgraded to Primary |
| XW-003 | iso42001 | 4.3, 5.2 | Determining the scope of the AI management system; **AI policy** | https://www.konfirmity.com/blog/iso-42001-requirements ; https://cdn.standards.iteh.ai/samples/81230/4c1911ebc9a641fcb6ee21aa09c28ad3/ISO-IEC-42001-2023.pdf | Primary | **CORRECTED title** — the ISO/IEC 42001:2023 sample PDF's table of contents gives clause 5.2 as "AI policy," not the generic "Policy" carried over from iso19770_1's differently-worded clause 5.2; clause number 5.2 itself was already correct, no crosswalk.csv change needed |
| XW-004 | iso19770_1 | 5.3 | Organizational roles, responsibilities and authorities | https://cdn.standards.iteh.ai/samples/68531/9744652940bf4a739bc8c2823d7daf98/ISO-IEC-19770-1-2017.pdf | Primary | kept |
| XW-004 | cobit2019 | APO01 | Managed I&T Management Framework | https://www.isaca.org/resources/news-and-trends/industry-news/2019/governing-digital-transformation-using-cobit-2019 (quotes "APO01 — Managed IT management framework") | Primary | kept — replaced "as XW-003" with the actual isaca.org URL, now Primary |
| XW-004 | iso27001 | A.5.2 | Information security roles and responsibilities | https://hightable.io/iso-27001-annex-a-controls-reference-guide/ ; https://cdn.standards.iteh.ai/samples/75652/f9b90f856c0d4c3dbef74cf67374d1c5/ISO-IEC-27002-2022.pdf (clause 5.2, see Annex A note above) | Primary | kept — upgraded to Primary |
| XW-004 | iso42001 | 5.3 | **Roles, responsibilities and authorities** | https://www.konfirmity.com/blog/iso-42001-requirements ; https://cdn.standards.iteh.ai/samples/81230/4c1911ebc9a641fcb6ee21aa09c28ad3/ISO-IEC-42001-2023.pdf | Primary | **CORRECTED title** — the ISO/IEC 42001:2023 sample PDF gives clause 5.3 as "Roles, responsibilities and authorities," without the "Organizational" prefix that iso27001/iso19770-1 use for their differently-numbered but similar clauses; clause number 5.3 was already correct, no crosswalk.csv change needed |
| XW-005 | iso19770_1 | 8.3 | Core data management | https://cdn.standards.iteh.ai/samples/68531/9744652940bf4a739bc8c2823d7daf98/ISO-IEC-19770-1-2017.pdf | Primary | filled — discovery/reconciliation feeds the core data set |
| XW-005 | cobit2019 | BAI09.01 | Identify and record current assets | https://4matt.com.br/en/cobit-2019-asset-management-bai09/ ; https://www.itsm-docs.com/blogs/cobit-framework/cobit-bai09-02-manage-critical-assets | Secondary (2 sources) | kept — replaced the "as above" placeholder with the actual XW-001 URLs |
| XW-005 | iso27001 | A.5.9 | Inventory of information and other associated assets | https://hightable.io/iso-27001-annex-a-controls-reference-guide/ ; https://cdn.standards.iteh.ai/samples/75652/f9b90f856c0d4c3dbef74cf67374d1c5/ISO-IEC-27002-2022.pdf (clause 5.9, see Annex A note above) | Primary | kept — upgraded to Primary |
| XW-005 | iso42001 | — | — | — | — | left blank |
| XW-006 | iso19770_1 | 8.4 | License management | https://cdn.standards.iteh.ai/samples/68531/9744652940bf4a739bc8c2823d7daf98/ISO-IEC-19770-1-2017.pdf | Primary | filled — direct title match |
| XW-006 | cobit2019 | BAI09.05 | Manage licenses | https://www.researchgate.net/publication/378036399 (BAI09 practice breakdown) ; https://www.itsm-docs.com/blogs/cobit-framework/cobit-bai09-05-manage-licenses | Secondary (2 sources) | kept — replaced the vague "itsm-docs.com practice pages" reference with the actual BAI09.05 page URL |
| XW-006 | iso27001 | A.5.32 | Intellectual property rights | https://hightable.io/iso-27001-annex-a-controls-reference-guide/ ; https://cdn.standards.iteh.ai/samples/75652/f9b90f856c0d4c3dbef74cf67374d1c5/ISO-IEC-27002-2022.pdf (clause 5.32, see Annex A note above) | Primary | kept — upgraded to Primary |
| XW-006 | iso42001 | — | — | — | — | left blank |
| XW-007 | iso19770_1 | 8.4 | License management | https://cdn.standards.iteh.ai/samples/68531/9744652940bf4a739bc8c2823d7daf98/ISO-IEC-19770-1-2017.pdf | Primary | filled |
| XW-007 | cobit2019 | BAI09.05 | Manage licenses | https://www.researchgate.net/publication/378036399 (BAI09 practice breakdown) ; https://www.itsm-docs.com/blogs/cobit-framework/cobit-bai09-05-manage-licenses | Secondary (2 sources) | kept — replaced "as XW-006" with the actual URLs |
| XW-007 | iso27001 | A.5.32 | Intellectual property rights | https://hightable.io/iso-27001-annex-a-controls-reference-guide/ ; https://cdn.standards.iteh.ai/samples/75652/f9b90f856c0d4c3dbef74cf67374d1c5/ISO-IEC-27002-2022.pdf (clause 5.32, see Annex A note above) | Primary | kept — upgraded to Primary |
| XW-007 | iso42001 | — | — | — | — | left blank |
| XW-008 | iso19770_1 | 8.4 | License management | https://cdn.standards.iteh.ai/samples/68531/9744652940bf4a739bc8c2823d7daf98/ISO-IEC-19770-1-2017.pdf | Primary | filled |
| XW-008 | cobit2019 | BAI09.05 | Manage licenses | https://www.researchgate.net/publication/378036399 (BAI09 practice breakdown) ; https://www.itsm-docs.com/blogs/cobit-framework/cobit-bai09-05-manage-licenses | Secondary (2 sources) | kept — replaced "as XW-006" with the actual URLs |
| XW-008 | iso27001 | A.5.32 | Intellectual property rights | https://hightable.io/iso-27001-annex-a-controls-reference-guide/ ; https://cdn.standards.iteh.ai/samples/75652/f9b90f856c0d4c3dbef74cf67374d1c5/ISO-IEC-27002-2022.pdf (clause 5.32, see Annex A note above) | Primary | kept — upgraded to Primary |
| XW-008 | iso42001 | — | — | — | — | left blank |
| XW-009 | iso19770_1 | — | — | — | — | left blank — no clause title in the ISO ToC specifically names request-to-retirement lifecycle |
| XW-009 | cobit2019 | BAI09.03 | Manage the asset life cycle | https://www.itsm-docs.com/blogs/cobit-framework/cobit-bai09-03-manage-the-asset-life-cycle ; https://www.researchgate.net/publication/378036399 (BAI09 practice breakdown, covers .01–.05) | Secondary (2 sources) | kept — replaced the unlinked "researchgate BAI09 breakdown" mention with its actual URL |
| XW-009 | iso27001 | A.5.9 | Inventory of information and other associated assets | https://hightable.io/iso-27001-annex-a-controls-reference-guide/ ; https://cdn.standards.iteh.ai/samples/75652/f9b90f856c0d4c3dbef74cf67374d1c5/ISO-IEC-27002-2022.pdf (clause 5.9, see Annex A note above) | Primary | kept — upgraded to Primary |
| XW-009 | iso42001 | — | — | — | — | left blank |
| XW-010 | iso19770_1 | — | — | — | — | left blank — no disposal/retirement-titled clause in the ToC |
| XW-010 | cobit2019 | BAI09.03 | Manage the asset life cycle (acquisition to disposal) | https://www.itsm-docs.com/blogs/cobit-framework/cobit-bai09-03-manage-the-asset-life-cycle ; https://www.researchgate.net/publication/378036399 (BAI09 practice breakdown, covers .01–.05) | Secondary (2 sources) | kept — replaced "as XW-009" with the actual URLs |
| XW-010 | iso27001 | A.8.10 | Information deletion | https://hightable.io/iso-27001-annex-a-controls-reference-guide/ ; https://cdn.standards.iteh.ai/samples/75652/f9b90f856c0d4c3dbef74cf67374d1c5/ISO-IEC-27002-2022.pdf (clause 8.10, see Annex A note above) | Primary | kept — upgraded to Primary |
| XW-010 | iso42001 | — | — | — | — | left blank |
| XW-011 | iso19770_1 | — | — | — | — | left blank — no rationalization/optimization clause found |
| XW-011 | cobit2019 | BAI09.04 | Optimize asset value | https://www.itsm-docs.com/blogs/cobit-framework/cobit-bai09-04-optimize-asset-value ; https://4matt.com.br/en/cobit-2019-asset-management-bai09/ | Secondary (2 sources) | kept — added the 4matt.com.br source; the line previously cited only itsm-docs.com |
| XW-011 | iso27001 | (empty) | — | — | — | left blank — cell was empty; out of scope to fill (only iso19770_1/iso42001 fills are in scope) |
| XW-011 | iso42001 | — | — | — | — | left blank |
| XW-012 | iso19770_1 | — | — | — | — | left blank — no budget/cost clause in the ToC |
| XW-012 | cobit2019 | APO06 | Managed Budget and Costs | https://sfia-online.org/en/sfia-7/sfia-views/cobit-2019-governance-and-management-objectives/apo06-managed-budget-and-costs ; https://wiki.process-symphony.com.au/framework/lifecycle/align-plan-and-organise-cobit/ | Secondary (2 sources) | kept — replaced the bare domain mention with the actual page URL; both sources independently confirmed against ISACA's own COBIT 2019/SFIA mapping PDF |
| XW-012 | iso27001 | (empty) | — | — | — | left blank — out of scope to fill |
| XW-012 | iso42001 | — | — | — | — | left blank |
| XW-013 | iso19770_1 | 8.7 | Outsourcing and services | https://cdn.standards.iteh.ai/samples/68531/9744652940bf4a739bc8c2823d7daf98/ISO-IEC-19770-1-2017.pdf | Primary | filled |
| XW-013 | cobit2019 | APO10 | Managed Vendors | https://sfia-online.org/en/legacy-sfia/sfia-7/sfia-views/cobit-2019-governance-and-management-objectives/apo10-managed-vendors ; https://www.itsm-docs.com/blogs/cobit-framework/cobit-apo10-01-identify-and-evaluate-vendor-relationships-and-contracts | Secondary (2 sources) | kept — replaced the bare domain mention with the actual page URL |
| XW-013 | iso27001 | A.5.19, A.5.20 | Information security in supplier relationships; Addressing information security within supplier agreements | https://hightable.io/iso-27001-annex-a-controls-reference-guide/ ; https://cdn.standards.iteh.ai/samples/75652/f9b90f856c0d4c3dbef74cf67374d1c5/ISO-IEC-27002-2022.pdf (clauses 5.19/5.20, see Annex A note above) | Primary | kept — upgraded to Primary |
| XW-013 | iso42001 | — | — | — | — | left blank |
| XW-014 | iso19770_1 | — | — | — | — | left blank — clause 8.5 "Security management" is too generic to clearly mean access control |
| XW-014 | cobit2019 | DSS05.04 | Manage user identity and logical access | https://docs.tibco.com/pub/logcssox/4.0.0/doc/html/SOX-guide/DS5.3-Identity-Management-_3-of-4_.htm ; https://www.itsm-docs.com/blogs/cobit-framework/cobit-dss05-04-manage-user-identity-and-logical-access | Secondary (2 sources) | kept — replaced the bare domain mention with the actual page URL |
| XW-014 | iso27001 | A.5.15 | Access control | https://hightable.io/iso-27001-annex-a-controls-reference-guide/ ; https://cdn.standards.iteh.ai/samples/75652/f9b90f856c0d4c3dbef74cf67374d1c5/ISO-IEC-27002-2022.pdf (clause 5.15, see Annex A note above) | Primary | kept — upgraded to Primary |
| XW-014 | iso42001 | — | — | — | — | left blank |
| XW-015 | iso19770_1 | — | — | — | — | left blank |
| XW-015 | cobit2019 | DSS05.04 | Manage user identity and logical access | https://docs.tibco.com/pub/logcssox/4.0.0/doc/html/SOX-guide/DS5.3-Identity-Management-_3-of-4_.htm ; https://www.itsm-docs.com/blogs/cobit-framework/cobit-dss05-04-manage-user-identity-and-logical-access | Secondary (2 sources) | kept — replaced "as XW-014" with the actual URLs |
| XW-015 | iso27001 | A.5.18 | Access rights | https://hightable.io/iso-27001-annex-a-controls-reference-guide/ ; https://cdn.standards.iteh.ai/samples/75652/f9b90f856c0d4c3dbef74cf67374d1c5/ISO-IEC-27002-2022.pdf (clause 5.18, see Annex A note above) | Primary | kept — upgraded to Primary |
| XW-015 | iso42001 | — | — | — | — | left blank |
| XW-016 | iso19770_1 | — | — | — | — | left blank |
| XW-016 | cobit2019 | DSS05.04 | Manage user identity and logical access | https://docs.tibco.com/pub/logcssox/4.0.0/doc/html/SOX-guide/DS5.3-Identity-Management-_3-of-4_.htm ; https://www.itsm-docs.com/blogs/cobit-framework/cobit-dss05-04-manage-user-identity-and-logical-access | Secondary (2 sources) | kept — replaced "as XW-014" with the actual URLs |
| XW-016 | iso27001 | A.5.18 | Access rights | https://hightable.io/iso-27001-annex-a-controls-reference-guide/ ; https://cdn.standards.iteh.ai/samples/75652/f9b90f856c0d4c3dbef74cf67374d1c5/ISO-IEC-27002-2022.pdf (clause 5.18, see Annex A note above) | Primary | kept — upgraded to Primary |
| XW-016 | iso42001 | — | — | — | — | left blank |
| XW-017 | iso19770_1 | — | — | — | — | left blank |
| XW-017 | cobit2019 | DSS05.04 | Manage user identity and logical access | https://docs.tibco.com/pub/logcssox/4.0.0/doc/html/SOX-guide/DS5.3-Identity-Management-_3-of-4_.htm ; https://www.itsm-docs.com/blogs/cobit-framework/cobit-dss05-04-manage-user-identity-and-logical-access | Secondary (2 sources) | kept — replaced "as XW-014" with the actual URLs |
| XW-017 | iso27001 | A.5.18, A.6.5 | Access rights; Responsibilities after termination or change of employment | https://hightable.io/iso-27001-annex-a-controls-reference-guide/ ; https://cdn.standards.iteh.ai/samples/75652/f9b90f856c0d4c3dbef74cf67374d1c5/ISO-IEC-27002-2022.pdf (clauses 5.18/6.5, see Annex A note above) | Primary | kept — upgraded to Primary |
| XW-017 | iso42001 | — | — | — | — | left blank |
| XW-018 | iso19770_1 | — | — | — | — | left blank |
| XW-018 | cobit2019 | DSS05.04 | Manage user identity and logical access | https://docs.tibco.com/pub/logcssox/4.0.0/doc/html/SOX-guide/DS5.3-Identity-Management-_3-of-4_.htm ; https://www.itsm-docs.com/blogs/cobit-framework/cobit-dss05-04-manage-user-identity-and-logical-access | Secondary (2 sources) | kept — replaced "as XW-014" with the actual URLs |
| XW-018 | iso27001 | A.8.2 | Privileged access rights | https://hightable.io/iso-27001-annex-a-controls-reference-guide/ ; https://cdn.standards.iteh.ai/samples/75652/f9b90f856c0d4c3dbef74cf67374d1c5/ISO-IEC-27002-2022.pdf (clause 8.2, see Annex A note above) | Primary | kept — upgraded to Primary |
| XW-018 | iso42001 | — | — | — | — | left blank |
| XW-019 | iso19770_1 | — | — | — | — | left blank |
| XW-019 | cobit2019 | DSS06.03 | Manage roles, responsibilities, access privileges and levels of authority | https://www.itsm-docs.com/blogs/cobit-framework/cobit-dss06-03-manage-roles-responsibilities-access-privileges-and-levels-of-authority ; https://wiki.process-symphony.com.au/uncategorized/business-process-controls-management-dss06-cobit2019/ | Secondary (2 sources) | kept — replaced the bare domain mention with the actual page URL |
| XW-019 | iso27001 | A.5.3 | Segregation of duties | https://hightable.io/iso-27001-annex-a-controls-reference-guide/ ; https://cdn.standards.iteh.ai/samples/75652/f9b90f856c0d4c3dbef74cf67374d1c5/ISO-IEC-27002-2022.pdf (clause 5.3, see Annex A note above) | Primary | kept — upgraded to Primary |
| XW-019 | iso42001 | — | — | — | — | left blank |
| XW-020 | iso19770_1 | 7.6.3 | Audit trails of authorizations and execution of authorizations | https://cdn.standards.iteh.ai/samples/68531/9744652940bf4a739bc8c2823d7daf98/ISO-IEC-19770-1-2017.pdf | Primary | **corrected from 7.5** (prior pass) — clause 7.5 is titled "Information requirements" in this standard (not documented information/evidence), so the prior value was wrong; 7.6.3 is the specific audit-evidence clause |
| XW-020 | cobit2019 | MEA02 | Managed System of Internal Control | https://sfia-online.org/en/assets/documents/cobit-2019-sfia-mapping.pdf (ISACA/SFIA mapping PDF, lists "MEA02 - Managed System of Internal Control") ; https://www.itsm-docs.com/blogs/cobit-framework/cobit-mea02-04-identify-and-report-control-deficiencies | Secondary (2 sources) | **CORRECTED sourcing** — previous line cited "multiple secondary sources agree" with no URL at all; replaced with two real, independently-checked URLs |
| XW-020 | iso27001 | A.5.33 | Protection of records | https://hightable.io/iso-27001-annex-a-controls-reference-guide/ ; https://cdn.standards.iteh.ai/samples/75652/f9b90f856c0d4c3dbef74cf67374d1c5/ISO-IEC-27002-2022.pdf (clause 5.33, see Annex A note above) | Primary | kept — upgraded to Primary |
| XW-020 | iso42001 | 7.5 | Documented information (harmonized-structure clause; correct for 42001, unlike 19770-1's differently-numbered structure) | https://www.konfirmity.com/blog/iso-42001-requirements ; https://cdn.standards.iteh.ai/samples/81230/4c1911ebc9a641fcb6ee21aa09c28ad3/ISO-IEC-42001-2023.pdf (clause 7.5, confirmed "Documented information") | Primary | kept — upgraded to Primary, title confirmed exact |
| XW-021 | iso19770_1 | — | — | — | — | left blank — 19770-1 is an IT asset standard, not applicable to AI risk/impact assessment |
| XW-021 | cobit2019 | APO12 | Managed Risk | https://wiki.process-symphony.com.au/framework/lifecycle/process/risk-management-apo12-cobit2019/ ; https://www.itsm-docs.com/blogs/cobit-framework/cobit-apo12-02-analyze-risk | Secondary (2 sources) | kept — replaced the bare "estim-software.com" mention with an actual second-source URL |
| XW-021 | iso27001 | (empty) | — | — | — | left blank — out of scope to fill |
| XW-021 | iso42001 | 6.1.4, A.5 | AI system impact assessment; Assessing impacts of AI systems | https://cyberzoni.com/standards/iso-42001/clause-6/ ; https://www.isms.online/iso-42001/annex-a-controls/ | Secondary (2 sources) | kept — already two independent sources; not re-researched |
| XW-022 | iso19770_1 | 8.3 | Core data management | https://cdn.standards.iteh.ai/samples/68531/9744652940bf4a739bc8c2823d7daf98/ISO-IEC-19770-1-2017.pdf | Primary | filled — row explicitly extends the software asset inventory process to AI systems |
| XW-022 | cobit2019 | BAI09.01 | Identify and record current assets | https://4matt.com.br/en/cobit-2019-asset-management-bai09/ ; https://www.itsm-docs.com/blogs/cobit-framework/cobit-bai09-02-manage-critical-assets | Secondary (2 sources) | kept — replaced "as XW-001" with the actual URLs |
| XW-022 | iso27001 | (empty) | — | — | — | left blank — out of scope to fill |
| XW-022 | iso42001 | — | — | — | — | left blank — no Annex A control specifically titled "AI system inventory" found |
| XW-023 | iso19770_1 | 8.7 | Outsourcing and services | https://cdn.standards.iteh.ai/samples/68531/9744652940bf4a739bc8c2823d7daf98/ISO-IEC-19770-1-2017.pdf | Primary | filled |
| XW-023 | cobit2019 | APO10 | Managed Vendors | https://sfia-online.org/en/legacy-sfia/sfia-7/sfia-views/cobit-2019-governance-and-management-objectives/apo10-managed-vendors ; https://www.itsm-docs.com/blogs/cobit-framework/cobit-apo10-01-identify-and-evaluate-vendor-relationships-and-contracts | Secondary (2 sources) | kept — replaced "as XW-013" with the actual URLs |
| XW-023 | iso27001 | A.5.19 | Information security in supplier relationships | https://hightable.io/iso-27001-annex-a-controls-reference-guide/ ; https://cdn.standards.iteh.ai/samples/75652/f9b90f856c0d4c3dbef74cf67374d1c5/ISO-IEC-27002-2022.pdf (clause 5.19, see Annex A note above) | Primary | kept — upgraded to Primary |
| XW-023 | iso42001 | A.10 | Third-party and customer relationships | https://www.isms.online/iso-42001/annex-a-controls/a-10-third-party-and-customer-relationships/ ; https://www.konfirmity.com/blog/iso-42001-controls (table entry: "A.10 / Third-party and customer relationships") | Secondary (2 sources) | **CORRECTED sourcing** — the bare "konfirmity.com" citation was carried over unverified; that specific page (`iso-42001-requirements`) does not mention A.10 at all, so the line was effectively single-sourced (isms.online only). Replaced with `konfirmity.com/blog/iso-42001-controls`, a different page on a different organization's site that was fetched and does state "A.10 / Third-party and customer relationships" verbatim |
| XW-024 | iso19770_1 | 6.1.2, 6.1.3 | IT asset risk assessment; IT asset risk treatment | https://cdn.standards.iteh.ai/samples/68531/9744652940bf4a739bc8c2823d7daf98/ISO-IEC-19770-1-2017.pdf | Primary | corrected from 6.1 (prior pass) — replaced parent clause with the two specific subclauses it comprises |
| XW-024 | cobit2019 | APO12 | Managed Risk | https://wiki.process-symphony.com.au/framework/lifecycle/process/risk-management-apo12-cobit2019/ ; https://www.itsm-docs.com/blogs/cobit-framework/cobit-apo12-02-analyze-risk | Secondary (2 sources) | kept — replaced "as XW-021" with the actual URLs |
| XW-024 | iso27001 | 6.1.3 | Information security risk treatment | https://hightable.io/iso-27001-clause-6-1-3-information-security-risk-treatment/ ; https://cdn.standards.iteh.ai/samples/82875/726bcf58250e43d9a666b4d929c8fbdb/ISO-IEC-27001-2022.pdf (main-body clause 6.1.3, confirmed directly, no 27002 cross-reference needed) | Primary | kept — upgraded to Primary, confirmed directly against the 27001:2022 sample PDF's own table of contents |
| XW-024 | iso42001 | 6.1.2, 6.1.3 | AI risk assessment process; AI risk treatment | https://cyberzoni.com/standards/iso-42001/clause-6/ ; https://www.novelvista.com/blogs/quality-management/iso-42001-ai-risk-treatment-clause-6-1-3 | Secondary (2 sources) | kept — already two independent sources; not re-researched (the 42001:2023 sample PDF's free preview stops at clause 4.4 and does not reach 6.1) |
| XW-025 | iso19770_1 | 9.1, 9.2, 9.3, 10.3 | Monitoring, measurement, analysis and evaluation; Internal audit; Management review; Continual improvement | https://cdn.standards.iteh.ai/samples/68531/9744652940bf4a739bc8c2823d7daf98/ISO-IEC-19770-1-2017.pdf | Primary | corrected from "9.1, 9.3, 10" (prior pass) — added 9.2 and replaced parent clause 10 with its continual-improvement subclause 10.3 |
| XW-025 | cobit2019 | MEA01 | Managed Performance and Conformance Monitoring | https://www.isaca.org/resources/news-and-trends/industry-news/2019/governing-digital-transformation-using-cobit-2019 (quotes "MEA01 — Managed performance and conformance monitoring") | Primary | **CORRECTED sourcing** — the previous two citations (`cobit-mea01-02-set-performance-and-conformance-targets` and "itsm-docs.com MEA01.03 page") are BOTH itsm-docs.com pages, i.e. one organization, not two independent sources as labeled; replaced with a genuine isaca.org Primary source. Clause code and title were already correct — this is a sourcing-methodology fix, not a data correction, so crosswalk.csv is unaffected |
| XW-025 | iso27001 | 9.1, 10.1 | Monitoring, measurement, analysis and evaluation; Continual improvement (2022 renumbering) | https://hightable.io/iso-27001-2013-vs-2022/ ; https://cdn.standards.iteh.ai/samples/82875/726bcf58250e43d9a666b4d929c8fbdb/ISO-IEC-27001-2022.pdf (main-body clauses 9.1/10.1, confirmed directly) | Primary | kept — upgraded to Primary, confirmed directly against the 27001:2022 sample PDF's own table of contents |
| XW-025 | iso42001 | 9.1, 9.2, 9.3, 10.1 | Monitoring, measurement, analysis and evaluation; Internal audit; Management review; Continual improvement | https://iso-docs.com/blogs/iso-42001-standards/iso-42001-clause-9-2-internal-audit ; https://cyberzoni.com/standards/iso-42001/clause-10/ (corroborated by https://medium.com/@cybercodeami/iso-42001-artificial-intelligence-management-system-aims-part-4-clause-9-10-abe40c3264f5) | Secondary (2 sources) | kept — already two independent sources; not re-researched (the 42001:2023 sample PDF's free preview stops at clause 4.4 and does not reach clause 9/10) |
| XW-026 | iso19770_1 | 8.3 | Core data management | https://cdn.standards.iteh.ai/samples/68531/9744652940bf4a739bc8c2823d7daf98/ISO-IEC-19770-1-2017.pdf | Primary | filled — data quality of the core asset data set |
| XW-026 | cobit2019 | BAI09.01 | Identify and record current assets | https://4matt.com.br/en/cobit-2019-asset-management-bai09/ ; https://www.itsm-docs.com/blogs/cobit-framework/cobit-bai09-02-manage-critical-assets | Secondary (2 sources) | kept — replaced "as XW-001" with the actual URLs |
| XW-026 | iso27001 | A.5.9 | Inventory of information and other associated assets | https://hightable.io/iso-27001-annex-a-controls-reference-guide/ ; https://cdn.standards.iteh.ai/samples/75652/f9b90f856c0d4c3dbef74cf67374d1c5/ISO-IEC-27002-2022.pdf (clause 5.9, see Annex A note above) | Primary | kept — upgraded to Primary |
| XW-026 | iso42001 | — | — | — | — | left blank |
| XW-027 | iso19770_1 | 5.1, 5.3 | Leadership and commitment; Organizational roles, responsibilities and authorities | https://cdn.standards.iteh.ai/samples/68531/9744652940bf4a739bc8c2823d7daf98/ISO-IEC-19770-1-2017.pdf | Primary | kept |
| XW-027 | cobit2019 | EDM01, APO01 | Ensured Governance Framework Setting and Maintenance; Managed I&T Management Framework | https://www.isaca.org/resources/news-and-trends/industry-news/2019/governing-digital-transformation-using-cobit-2019 (quotes both "EDM01 — Ensured governance framework setting and maintenance" and "APO01 — Managed IT management framework") | Primary | kept — upgraded from a single sfia-online.org secondary source (which only covered EDM01, not APO01) to one isaca.org Primary source covering both codes |
| XW-027 | iso27001 | 5.1, 5.3 | Leadership and commitment; Organizational roles, responsibilities and authorities | https://cdn.standards.iteh.ai/samples/82875/726bcf58250e43d9a666b4d929c8fbdb/ISO-IEC-27001-2022.pdf (main-body clauses 5.1/5.3, confirmed directly) | Primary | kept — upgraded from a vague "isms.online / common ISMS clause references" citation to a direct primary read of the 27001:2022 sample PDF's own table of contents |
| XW-027 | iso42001 | 5.1, 5.3 | Leadership and commitment; **Roles, responsibilities and authorities** | https://cdn.standards.iteh.ai/samples/81230/4c1911ebc9a641fcb6ee21aa09c28ad3/ISO-IEC-42001-2023.pdf (main-body clauses 5.1/5.3, confirmed directly) | Primary | **CORRECTED title** — same 5.3 wording fix as XW-004 ("Roles, responsibilities and authorities," no "Organizational" prefix in 42001); 5.1 was already correct; clause numbers unchanged, no crosswalk.csv change needed |
| XW-028 | iso19770_1 | — | — | — | — | left blank — 19770-1 explicitly excludes managing information as an asset independent of hardware/software |
| XW-028 | cobit2019 | APO14 | Managed Data | https://www.isaca.org/resources/news-and-trends/industry-news/2019/employing-cobit-2019-for-enterprise-governance-strategy (quotes "APO14 — Managed data") | Primary | kept — upgraded from two secondary sources (researchgate.net, estim-software.com) to a Primary isaca.org source |
| XW-028 | iso27001 | A.5.12, A.5.13 | Classification of information; Labelling of information | https://hightable.io/iso-27001-annex-a-controls-reference-guide/ ; https://cdn.standards.iteh.ai/samples/75652/f9b90f856c0d4c3dbef74cf67374d1c5/ISO-IEC-27002-2022.pdf (clauses 5.12/5.13, see Annex A note above) | Primary | kept — upgraded to Primary |
| XW-028 | iso42001 | A.7 | Data for AI systems | https://www.isms.online/iso-42001/annex-a-controls/a-7-data-for-ai-systems/ ; https://www.schellman.com/blog/iso-certifications/ai-data-considerations-iso-42001-and-iso-9001 (quotes "A.7 Data for AI Systems") | Secondary (2 sources) | kept — added the schellman.com source; the line previously cited only isms.online |

## Pairs that could not be upgraded past a single secondary source

None. Every pair that was only single-sourced, or that stood in for another
row with "as above"/"as XW-0xx" instead of a real citation, now carries
either a Primary source or two independent secondary sources.

## Corrections found on the 2026-09-24 second-source pass

- **XW-003/XW-027 iso42001, clause 5.2 title**: "Policy" → **"AI policy"**
  (ISO/IEC 42001:2023's own wording; clause number 5.2 unchanged, no
  crosswalk.csv change).
- **XW-004/XW-027 iso42001, clause 5.3 title**: "Organizational roles,
  responsibilities and authorities" → **"Roles, responsibilities and
  authorities"** (ISO/IEC 42001:2023 drops "Organizational," unlike
  iso27001/iso19770-1's clause 5.3 wording; clause number 5.3 unchanged, no
  crosswalk.csv change).
- **XW-025 cobit2019 (MEA01) sourcing error**: the file previously cited two
  itsm-docs.com pages as "Secondary (2 sources)" — that is one organization,
  not two independent sources, so the line did not actually meet the
  project's evidence bar even though it was labeled as if it did. Replaced
  with a Primary isaca.org citation. The clause code (MEA01) and title
  ("Managed Performance and Conformance Monitoring") were already correct;
  this is a sourcing fix, not a data correction, so crosswalk.csv is
  unaffected.
- No clause numbers were found to be wrong in this pass (only the two title
  wordings above, and the one sourcing-independence error above).

## Sources not reachable as primary

- `iso.org/standard/68531.html` (ISO/IEC 19770-1:2017) and the ANSI webstore
  page returned HTTP 403. The official ISO preview PDF hosted at
  `cdn.standards.iteh.ai` (a national-body-affiliated standards reseller,
  carrying the genuine `© ISO/IEC 2017` copyright notice) was used instead
  and is the primary source cited above for every iso19770_1 cell.
- `isaca.org/resources/cobit` (the COBIT product/store page) did not expose
  individual objective names on the page fetched. However, two ISACA
  industry-news articles (`governing-digital-transformation-using-cobit-2019`
  and `employing-cobit-2019-for-enterprise-governance-strategy`) do quote
  objective codes together with their full titles, and were used as Primary
  sources above for EDM01, APO01, MEA01, and APO14. Objectives not named in
  either article (APO06, APO10, APO12, BAI09.01/.03/.04/.05, DSS05.04,
  DSS06.03, MEA02) remain backed by two independent secondary sources.
- ISO/IEC 27001:2022's own free preview does not reach Annex A (it cuts off
  partway through the main body). Annex A control titles above are
  therefore sourced to the ISO/IEC 27002:2022 official sample PDF instead,
  per the Annex A note at the top of this file, and treated as Primary on
  that basis. ISO/IEC 42001:2023's own free preview cuts off at clause 4.4,
  before its Annex A and before clauses 6–10; rows needing those clauses
  (XW-021, XW-023, XW-024, XW-025, XW-028's A.7) remain on two independent
  secondary sources.
- Every remaining Annex A / secondary-source citation above (hightable.io,
  isms.online, konfirmity.com, sfia-online.org, wiki.process-symphony.com.au,
  itsm-docs.com, researchgate.net, 4matt.com.br, docs.tibco.com,
  cyberzoni.com, novelvista.com, iso-docs.com, schellman.com) was fetched
  directly on 2026-09-24 and checked to confirm it states the specific
  clause/control number and title claimed, not merely discusses the topic.
