# Application governance router: sample request on the Halden estate

**Request:** "Our auditors want to know where we stand on software licenses next quarter."

## Routing note

A license position goes to `audit-response`, so I will not start with `rationalization`. First I need two answers: which auditors (a software publisher or its agent, or your internal or financial auditors), and whether a letter has arrived.

**Answer given:** a publisher's agent has asked for a review next quarter. No letter has arrived.

With no letter, I run `audit-response` in readiness mode. Legal hears about this first, because a publisher is involved. Count in the contract's license metric, not raw installs [[XW-025]]. I'll offer `rationalization` afterward for unused licenses and `itam-maturity` for the process [[XW-027]].

**Data needed:** `proofs-of-purchase.csv` and `audit-installs.csv`. Both are Halden demo files.

**Decision needed: counsel** on whether counsel commissions the readiness work. If the answer had been internal or financial auditors, **Decision needed: counsel and Finance**, since a shortfall shown to financial auditors may raise a disclosure question.

## Follow-up offered

Run `rationalization` for unused licenses and `itam-maturity` for the process. Neither is run without your agreement.

This kit gives methods and reasoning support. It is not a governance platform, a certification, or legal advice.

```findings
[
  {"type": "routing", "id": "audit-response"}
]
```
