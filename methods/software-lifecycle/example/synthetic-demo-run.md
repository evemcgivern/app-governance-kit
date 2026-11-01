# Software Lifecycle Check — synthetic demo (checked_on 2026-10-24)

Inputs: the tool's synthetic demo inventory (`examples/software-inventory.csv` at the pinned commit, 60 rows) and its synthetic test data. Every product, publisher, and owner in it is fictional. The agent saw only the summary count lines. Nothing here comes from a real inventory.

## Data currency

Checked on 2026-10-24. KEV data current: yes (synthetic demo data). **Unverified:** the counts come from an earlier release of the tool and were not re-run on v0.7.0.

## Summary counts

| measure | count |
|---|---|
| items from rows | 50 items from 60 rows |
| past end of life | 8 |
| ends within 12 months | 5 |
| mainstream support ended | 1 |
| supported | 25 |
| unmatched | 11 |
| names to review | 1 (unmatched on purpose, not a finding) |

Classification: governable 40, component 0, bundle member 3, unknown 7 [[XW-001]] [[XW-009]].

Unmatched does not mean safe. No date is claimed for those items. Item IDs are not relayed; the person reads each list in `report.md` themselves [[XW-026]].

The vendor and product appear in CISA KEV. This does not mean your version is affected [[XW-024]].

## Open decisions

**Decision needed:** for each past-end-of-life or ends-soon item, the asset owner chooses replace, upgrade, retire, or request risk acceptance [[XW-009]] [[XW-010]].

**Decision needed:** a person checks each review-urgently version against the KEV entries and sets the priority [[XW-024]].

```findings
[]
```
