I've run intake for all six systems in `ai-systems.csv`. The legal content behind this skill was last reviewed in 2026-09, so treat the EU AI Act points below as a starting point. **Legal review is required for AI-004**, which is tiered high-risk.

**Summary**

| id | Owner | Tier | Main driver |
|---|---|---|---|
| AI-001 | Email security | Minimal | Spam and phishing filtering, not a listed area |
| AI-002 | Finance | Minimal | Pulls fields from invoices, and a person reviews them |
| AI-003 | Operations | Minimal | Dispatchers approve every route; not a safety part of traffic infrastructure |
| **AI-004** | **HR** | **High-risk** | **Ranks and shortlists job applicants (employment is a listed high-risk area)** |
| AI-005 | Customer service | Limited | Chatbot that talks to the public, so people must be told it's AI |
| AI-006 | Planning | Minimal | Forecasts total volumes, with no decisions about people |

**Common gaps in the input:** The CSV gives only an id, an owner and one line of description. It doesn't give the supplier, the model provider, the data fields used, where the data came from, or who reviews the outputs beyond what the description says. Each record marks these gaps. Some systems may match vendors in `apps.csv`, but those links are guesses and are marked **Unverified:**.

**Controls every system needs (baseline):**
- **XW-021** (ISO/IEC 42001 6.1.4 and Annex A.5; COBIT APO12): a risk and impact assessment before deployment.
- **XW-022** (ISO/IEC 19770-1 8.3; COBIT BAI09.01): an entry in the AI inventory.
- **XW-023** (ISO/IEC 42001 A.10; ISO/IEC 27001 A.5.19; COBIT APO10): supplier and model-provider oversight.
- **XW-024** (ISO/IEC 42001 6.1.2 and 6.1.3; COBIT APO12): an entry in the risk register with an owner.
- **XW-028** (ISO/IEC 42001 A.7; ISO/IEC 27001 A.5.12 and A.5.13): data classification and handling.
- **XW-020** (ISO/IEC 42001 7.5; ISO/IEC 27001 A.5.33): keep the evidence of approval.

In NIST AI RMF terms: **Govern** covers ownership and approval, **Map** covers the restatement and tiering, **Measure** covers the assessment and accuracy monitoring, and **Manage** covers the risk-register treatment and re-review. The tier-specific controls below are added on top of this baseline.

---

## AI-001: Email spam and phishing classifier

**What it does:** It sorts inbound email into spam, phishing or legitimate, and quarantines emails automatically.
- **Who it affects:** Staff receiving email and external senders.
- **Decisions:** It makes the quarantine decision itself. No one reviews each output before it acts; quarantined mail can presumably be released, but **Unverified:** that a release process exists.
- **Data:** Email content, headers and sender addresses. **This is personal data.** It flows from Halden's mail stream. **Unverified:** whether the vendor also trains on Halden's email.

**Tier: Minimal-risk.**
- **Prohibited practices:** none apply. The system doesn't manipulate people, score them socially, use biometrics or read emotions.
- **High-risk areas:** it isn't used for employment, essential services, education, law enforcement or critical infrastructure. Screening email for security reasons doesn't decide anything about a person's rights or opportunities.
- **Transparency duty:** none, because it doesn't talk to people or generate content.
- **Remaining risks are operational:** legitimate mail being quarantined by mistake, and the vendor's handling of mail content.

**Controls beyond the baseline:**
- **XW-028:** confirm how email content is classified, and whether the vendor keeps it or trains on it.
- **XW-023:** get the vendor to disclose its subprocessors.
- **Measure:** track the false-positive rate and how often quarantined mail is released.
- **Manage:** have a documented release process for quarantined mail.

| Field | Value |
|---|---|
| id | AI-001 |
| name | Email spam/phishing classifier |
| owner | Email security |
| purpose | Classify inbound email as spam or phishing and quarantine it |
| affected people | Staff recipients; external senders |
| decisions made or supported | Makes the quarantine decision automatically |
| human review | No review of each output; quarantined mail can be released (**Unverified:**) |
| supplier | **Unverified:** possibly Mailguard (APP-057) |
| data used | Inbound email content and metadata |
| personal data (yes/no) | Yes |
| data provenance | Halden inbound mail stream; vendor training data unknown |
| risk tier | Minimal-risk |
| reasoning | Not prohibited and not in a listed high-risk area; no transparency duty |
| required controls | Baseline; XW-028 data handling; XW-023 subprocessor disclosure; tracking of false positives |
| approval | **Decision needed:** approval to proceed |
| approver | *(pending)* |
| date | 2026-09-24 |
| next review | 2027-09-24, or sooner if the use changes |

## AI-002: Supplier invoice extraction

**What it does:** It reads supplier invoices and extracts the totals, dates and PO numbers.
- **Who it affects:** Suppliers and Finance staff.
- **Decisions:** It supports payment processing. A person reviews each extraction ("for review").
- **Data:** Supplier invoices. **Personal data: likely a little.** Invoices can include named contacts, and sole traders' names and bank details. **Unverified.**
- **Where the data comes from:** invoices sent in by suppliers.

**Tier: Minimal-risk.**
- It pulls fields out of documents and a person checks them before anything happens.
- It's not in any listed high-risk area, and it doesn't talk to people.
- The risk is financial: a wrong figure or a duplicate payment. That belongs under finance controls, not AI Act controls.

**Controls beyond the baseline:**
- **XW-028:** decide how financial data is classified and handled.
- **Measure:** track extraction accuracy against the corrections people make.
- **Manage:** make sure a person still signs off before payment.
- **XW-023:** confirm whether invoices go to an outside OCR or model provider.

| Field | Value |
|---|---|
| id | AI-002 |
| name | Supplier invoice extraction |
| owner | Finance |
| purpose | Extract totals, dates and PO numbers from supplier invoices |
| affected people | Suppliers; Finance staff |
| decisions made or supported | Supports invoice processing and payment |
| human review | Yes, each extraction is reviewed |
| supplier | **Unverified:** possibly Scanwright Invoice OCR (APP-055) |
| data used | Supplier invoices |
| personal data (yes/no) | Likely yes, but limited (**Unverified:**) |
| data provenance | Invoices submitted by suppliers |
| risk tier | Minimal-risk |
| reasoning | Document extraction with a person reviewing; not in a listed area |
| required controls | Baseline; XW-028; accuracy monitoring; person signs off before payment |
| approval | **Decision needed:** approval to proceed |
| approver | *(pending)* |
| date | 2026-09-24 |
| next review | 2027-09-24, or sooner if the use changes |

## AI-003: Delivery route suggestions

**What it does:** It suggests delivery routes, and a dispatcher approves each plan.
- **Who it affects:** Dispatchers, drivers, and customers indirectly.
- **Decisions:** It supports route planning. A person reviews every plan.
- **Data:** Delivery addresses, orders and possibly vehicle or driver data. **Personal data: likely yes.** Customer addresses count, and driver location data may too. **Unverified.**
- **Where the data comes from:** Halden's order and transport data.

**Tier: Minimal-risk.**
- **Critical infrastructure:** I considered it, because the Act's list includes safety parts of road-traffic management. This system plans Halden's own delivery routes and doesn't manage road traffic, and a dispatcher approves every plan. So it doesn't meet that test.
- **Worker management:** if the routes were used to allocate work to drivers or to monitor and judge their performance, the system would move into the employment and worker-management high-risk area.

**Decision needed:** Operations must confirm the route output is **not** used to assign tasks to individual drivers or to monitor or judge their performance. If it is, re-run intake as a possible high-risk system.

**Controls beyond the baseline:**
- **XW-028:** handling of customer address and driver location data.
- **Map:** record the worker-management limit above in the intake record.
- **Measure:** track how often dispatchers override or reject plans.

| Field | Value |
|---|---|
| id | AI-003 |
| name | Delivery route suggestions |
| owner | Operations |
| purpose | Suggest delivery routes for dispatcher approval |
| affected people | Dispatchers; drivers; customers (indirectly) |
| decisions made or supported | Supports route planning |
| human review | Yes, a dispatcher approves each plan |
| supplier | **Unverified:** possibly Pathcraft (APP-031) or Routewise/Routesmith (APP-029/058) |
| data used | Orders, delivery addresses, possibly vehicle and driver data |
| personal data (yes/no) | Likely yes (**Unverified:**) |
| data provenance | Halden order and transport systems |
| risk tier | Minimal-risk, as long as it isn't used to manage workers |
| reasoning | A person approves each plan; not a safety part of traffic infrastructure |
| required controls | Baseline; XW-028; worker-use limit recorded; tracking of dispatcher overrides |
| approval | **Decision needed:** confirm it isn't used to manage workers, then approve |
| approver | *(pending)* |
| date | 2026-09-24 |
| next review | 2027-09-24, or at once if the route output starts being used to manage drivers |

## AI-004: CV ranking and applicant shortlisting ⚠ HIGH-RISK

**What it does:** It ranks job applicants' CVs and shortlists candidates for interview.
- **Who it affects:** Job applicants, meaning external people plus any internal candidates, and HR recruiters.
- **Decisions:** It directly shapes who gets an interview. Candidates it doesn't shortlist may never be seen by a person. The description doesn't say whether a person reviews every ranking; **Unverified:**.
- **Data:** CVs and application data. **This is personal data**, and it may include special-category data (health, ethnicity) or stand-ins for protected characteristics (age, gender, address).
- **Where the data comes from:** applicants. **Unverified:** what data the model was trained on.

**Prohibited practices:** none apply on this description. The ban on emotion recognition in the workplace would apply if the tool analysed video or voice interviews for emotion, and the ban on biometric categorisation would apply if it inferred protected traits from photos.

**Decision needed:** Legal must confirm that neither of these features exists in the product.

**Tier: High-risk.**
- The Act lists employment uses as high-risk, specifically recruiting and selecting people, and filtering or evaluating job applications (Annex III, point 4(a)). This system does exactly that.
- There's an exception for tools doing only a "narrow procedural task" (Art. 6(3)), but it doesn't apply. Ranking applicants is profiling of people, and profiling always stays high-risk.
- It's also a hiring decision with a real effect on people, which brings in GDPR automated decision-making rules (Art. 22) and a data protection impact assessment (DPIA, Art. 35).

**Unverified:** The Annex III high-risk obligations were due to apply from 2 August 2026, but EU "digital omnibus" proposals would push that date back. Legal should confirm the current date. Either way, implement the controls now.

**Required controls (on top of the baseline):**
- **Legal review before approval (XW-021):** confirm the tier, and whether Halden is only a *deployer* or also a *provider*. Halden becomes a provider if it built the system, substantially modified it, or put its own name on it.
- **Human oversight (Govern / Manage):** trained recruiters review the rankings, can override them, and see candidates the tool didn't shortlist. No one is rejected on the tool's output alone.
- **Informing people:** tell applicants that an AI system is used in assessing them. Tell workers' representatives and affected staff before it's put in use at work.
- **Input data quality (Map / XW-028):** make sure the data fed in is relevant and representative for the purpose. Don't feed in special-category data.
- **Bias and accuracy monitoring (Measure / XW-025):** compare selection rates across protected groups and track how accurate the rankings are.
- **Logs:** keep the system's automatic logs for at least six months (per Art. 26), and link them to the XW-020 evidence records.
- **Supplier (XW-023, ISO/IEC 42001 A.10):**
  - Get the provider's EU declaration of conformity, CE marking, instructions for use, and registration in the EU database.
  - Get disclosure of training data sources and subprocessors.
  - Add AI clauses to the contract covering model updates and incident reporting.
- **DPIA (XW-028):** complete one, run by Data protection.
- **Risk register (XW-024):** log the risks of discrimination, wrongful exclusion and non-compliance, owned by the Head of HR.
- **Incidents:** report serious incidents to the provider and the regulator, and be able to suspend use.

| Field | Value |
|---|---|
| id | AI-004 |
| name | CV ranking and applicant shortlisting |
| owner | HR |
| purpose | Rank applicant CVs and shortlist candidates for interview |
| affected people | Job applicants (external and internal); HR recruiters |
| decisions made or supported | Shortlisting, meaning who gets an interview |
| human review | **Unverified:** not stated; must be ensured before go-live |
| supplier | **Unverified:** possibly Hirewell Recruiting (APP-004) |
| data used | CVs and application data |
| personal data (yes/no) | Yes, possibly including special-category data or stand-ins for protected traits |
| data provenance | Submitted by applicants; model training data unknown |
| risk tier | **High-risk** (EU AI Act Annex III, point 4(a)) |
| reasoning | Filters and evaluates job applicants; profiling blocks the Art. 6(3) exception |
| required controls | Baseline + legal review, human oversight, notice to applicants and workers, bias monitoring, logs kept at least 6 months, provider conformity evidence, DPIA, risk register entry, incident process |
| approval | **Decision needed:** legal review, then approval (don't deploy before both) |
| approver | *(pending; legal sign-off required)* |
| date | 2026-09-24 |
| next review | **Decision needed:** suggest 6-monthly given the tier; at minimum 2027-09-24, and on any change of model or use |

## AI-005: Shipment-status chatbot

**What it does:** It answers customers' shipment-status questions in the website chat.
- **Who it affects:** Customers and members of the public.
- **Decisions:** It gives information only; it doesn't decide anything. The customer reads the answer directly, and there's no review of each reply.
- **Data:** Tracking numbers, shipment status, and possibly customer names and addresses. **Personal data: yes, likely.**
- **Where the data comes from:** Halden's shipment systems, plus whatever customers type in.

**Tier: Limited-risk.**
- It's not prohibited and not in a listed area. Shipment tracking is not an "essential service" in the Act's sense.
- It does talk directly to people, so the transparency duty for chatbots (Art. 50(1)) applies: customers must be told clearly that they are chatting with AI, unless that's obvious. That duty applies from 2 August 2026.
- Other risks: it could share someone's shipment details with the wrong person if identity isn't checked, and it could give wrong answers.

**Controls beyond the baseline:**
- **AI disclosure:** tell users they're talking to AI at the start of the chat.
- **Handover:** offer a route to a person.
- **XW-028:** check identity or match the tracking number before showing shipment details, and set rules for keeping chat logs.
- **XW-023:** confirm whether chats go to a third-party model provider, and whether that provider keeps or trains on them.
- **Measure:** track answer accuracy and how often chats are escalated to a person.

| Field | Value |
|---|---|
| id | AI-005 |
| name | Shipment-status chatbot |
| owner | Customer service |
| purpose | Answer shipment-status questions in website chat |
| affected people | Customers and members of the public |
| decisions made or supported | Information only |
| human review | No review of each reply; handover route required |
| supplier | **Unverified:** possibly Askbay Chatbot (APP-056) or Chattera (APP-012) |
| data used | Shipment records; customer chat input |
| personal data (yes/no) | Yes (likely) |
| data provenance | Halden shipment systems; customer-supplied |
| risk tier | Limited-risk |
| reasoning | Talks directly to people, so the Art. 50 disclosure applies; not in a listed high-risk area |
| required controls | Baseline; AI disclosure; handover to a person; identity/tracking check; chat-log retention rules; XW-023 provider terms |
| approval | **Decision needed:** approval to proceed |
| approver | *(pending)* |
| date | 2026-09-24 |
| next review | 2027-09-24, or sooner if the use changes (e.g. it starts handling refunds or complaints) |

## AI-006: Weekly warehouse volume forecast

**What it does:** It forecasts weekly warehouse volume from past shipments.
- **Who it affects:** Planning staff directly; warehouse staffing indirectly.
- **Decisions:** It supports capacity planning. Planners presumably use the forecast rather than acting on it automatically. **Unverified.**
- **Data:** Past shipment volumes. **Personal data: likely no** if the data is aggregated. **Unverified.**
- **Where the data comes from:** Halden's shipment history.

**Tier: Minimal-risk.**
- It forecasts total volumes and makes no decisions about any person.
- It's not in a listed area and doesn't talk to people.
- If the forecasts were later used to schedule or judge individual workers, re-run intake under the worker-management area.

**Controls beyond the baseline:**
- **Measure:** track forecast accuracy against actual volumes.
- **XW-028:** confirm the input is aggregated.

| Field | Value |
|---|---|
| id | AI-006 |
| name | Weekly warehouse volume forecast |
| owner | Planning |
| purpose | Forecast weekly warehouse volume |
| affected people | Planners; warehouse staff (indirectly) |
| decisions made or supported | Supports capacity planning |
| human review | Planners use the output (**Unverified:**) |
| supplier | **Unverified:** possibly Foresight Demand forecasting (APP-038) |
| data used | Historic shipment volumes |
| personal data (yes/no) | Likely no (**Unverified:**) |
| data provenance | Halden shipment history |
| risk tier | Minimal-risk |
| reasoning | Forecasts totals; no decisions about individuals; not in a listed area |
| required controls | Baseline; forecast accuracy tracking; confirm the data is aggregated |
| approval | **Decision needed:** approval to proceed |
| approver | *(pending)* |
| date | 2026-09-24 |
| next review | 2027-09-24, or sooner if forecasts are used to schedule individual staff |

---

**Decisions needed, in summary:**
1. **Legal review for AI-004** before anything else: confirm the tier, confirm whether Halden is a deployer or provider, confirm there's no emotion-recognition or biometric feature, and confirm when the obligations apply.
2. **AI-003:** Operations to confirm routes aren't used to manage drivers.
3. **All systems:** approve each one and name the approver.
4. **Suppliers:** each system's owner to confirm its supplier and model provider, which feeds the XW-023 assessment.

```findings
[{"type": "high_risk_ai", "id": "AI-004"}]
```
