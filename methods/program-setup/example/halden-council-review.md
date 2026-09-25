# Review: Halden Software Governance Council draft charter

I checked `council-draft.md` against the 10 program-setup steps, `checklist.md` and `template.md`. The draft is four short sections: Purpose, Members, Meetings and Scope. It has a meeting cadence and a scope list, and nothing else the template requires. **Three of the gaps are fundamentals that only Halden can close: there is no sponsor, no decision rights, and 14 voting members.** Until those are settled, the council can't enforce anything, and all 14 members would vote on every request.

## Gap table

| Step | What's missing | Why it matters | Fix |
|---|---|---|---|
| 1. Purpose [XW-003] | "Oversees software and applications" describes an activity. It doesn't say what goes wrong today. | Without a stated problem, you can't tell whether the council is working, and meetings drift toward status updates. | Write one sentence naming the current failure — for example, that software is bought and renewed outside any review, so cost, security risk and AI use go unchecked. **Decision needed:** Halden must state the actual problem; the draft gives none. |
| 2. Sponsor [XW-027] | No sponsor is named. The CIO is a voting member, but nothing says the CIO sponsors the council or controls the budget. | Without a sponsor who controls budget, nobody can stop a purchase the council rejects. The charter would have no enforcement. | Name an executive who controls the software budget. The CIO or CFO are the likely candidates. **Decision needed:** who sponsors, and which budget they control. |
| 3. Decision rights [XW-027] | Scope lists four item types: new requests, renewals, retirements and AI tools. It doesn't say what the council decides versus advises on, and it sets no threshold. | With no threshold, every request goes to a monthly meeting. At roughly 30-day intervals that is a built-in bottleneck, and teams will learn to go around it. | Fill in the template's decision-rights table (sketch below). **Decision needed:** the cost, risk and AI thresholds, and which role decides items below them. |
| 4. Membership [XW-004] | There are 14 voting members: CIO, CISO, procurement, finance, legal, architecture, HR, operations, warehousing, transport, customer service, sales, marketing and the service desk lead. The limit is 5–9. | Above 9 voters, decisions get slower and quorum gets harder to reach. Five of the 14 are business functions with no specific software accountability. | Keep 7–9 voters: CIO, CISO, procurement, finance, legal, architecture, plus one or two business leads (for example operations and transport). Make HR, warehousing, customer service, sales and marketing consulted members. Move the service desk lead to non-voting secretary and triage owner. **Decision needed:** which business leads keep a vote. |
| 5. Intake path [XW-027] | No request form, no triage owner, no filter on what reaches the meeting. | Without a filter, the full request volume lands on the agenda. | *Draft:* all software, renewal, retirement and AI-tool requests go through one intake form. The service desk lead triages within 5 working days. Items below threshold are decided by the delegated role at intake. Only exceptions, above-threshold items and high-risk items (including AI tools) reach the council agenda. |
| 6. Enforcement [XW-027] | Procurement's role isn't stated, and overlaps with other boards (architecture review, change advisory) aren't settled. | If procurement isn't bound by council decisions, those decisions are advisory at best. With architecture voting here and possibly running its own board, the same item can be reviewed twice or not at all. | *Draft:* procurement will not raise a PO or sign a renewal above threshold without a logged council approval. Add the template's adjacent-body table with rows for architecture review (technical standards), change advisory (deployment) and security risk. The sponsor settles who owns what. |
| 7. Cadence [XW-025] | Only "monthly, 90 minutes" and minutes are stated. There's no standing agenda, no decision log and no out-of-cycle path. | Minutes record what was said; a decision log records what was decided and why, which is the evidence auditors ask for [XW-020]. Without an urgent-item path, an expiring renewal can wait up to a month. | *Draft:* standing agenda — (1) actions from last meeting, (2) above-threshold requests, (3) exceptions, (4) renewals due in the next 90 days, (5) AI-tool items, (6) metrics (quarterly). The service desk lead keeps a dated decision log, published to a shared location. Urgent items go to the chair plus two voting members by email or ad hoc call within 5 working days and are ratified at the next meeting. Seed the first meeting with real, pending items. |
| 8. Escalation [XW-027] | No dispute or tie-break path. | Deadlocks have nowhere to go. With 14 voters, an even split is possible. | *Draft:* the chair breaks ties. If the chair can't resolve a dispute, it goes to the sponsor, whose decision is final and logged. |
| 9. Success measures [XW-025] | None. | You can't tell whether the council is a bottleneck or a rubber stamp, and the 90-day review has nothing to review. | *Draft:* median days from request to decision (target ≤ 10 working days); share of software spend through intake (target ≥ 90% by month 6); savings from denied or consolidated renewals; number of exceptions granted. **Unverified:** the targets are suggestions. The draft has no baseline data, so capture a baseline in the first 30 days. |
| 10. Approval, review and launch [XW-020] | No sponsor sign-off line, no charter review date, no 90-day plan. | An unapproved charter carries no authority. | Add a sponsor approval block and a review date no more than 12 months after approval. 90-day plan: sponsor approval and members named by day 15, intake live by day 30, three meetings in days 30–90, first metrics review at day 90. **Decision needed:** sponsor sign-off. |

## Decision-rights sketch for step 3

Thresholds are left blank because they are Halden's call.

| Decision | Council decides | Council advises | Delegated to (below threshold) | Threshold |
|---|---|---|---|---|
| New software purchase | Above threshold | — | Procurement + IT | **Decision needed:** $ per year |
| Renewal | Above threshold, or when usage has dropped | — | App owner + procurement | **Decision needed** |
| Retirement | Business-critical apps | Others | App owner | — |
| AI tools | High-risk AI tools | Low-risk AI tools | CISO + legal | Any high-risk use |
| Exceptions to policy | All | — | — | — |

I didn't use the other data files (such as `apps.csv`) because they aren't needed for a charter review.

I reported only the three fundamentals as findings: sponsor, decision rights and membership size. You listed intake-path, cadence, metrics and escalation as available slugs "where they apply". The skill's rule is to draft those gaps directly rather than raise them as findings, so the drafts are in the Fix column above.

```findings
[
  {"type": "charter_gap", "id": "sponsor"},
  {"type": "charter_gap", "id": "decision-rights"},
  {"type": "charter_gap", "id": "membership-size"}
]
```
