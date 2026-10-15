# Certification study coach: sample CHAMP session (illustrative)

The learner's answers below are invented to show how the tool responds. The data is the Halden `devices.csv`, `checked_on` 2026-09-01.

## Setup

CHAMP, hardware lifecycle owner, 3 hours a week, no exam date. First drill: retire hardware with data-wipe evidence, then track refresh against budget.

## Drill 1: refresh and disposal

**Scenario:** Halden's device fleet is due its quarterly lifecycle check. Which devices need action, and why?

**Learner's answer (invented):** "DEV-008 is overdue for refresh. The retired devices are fine because they're retired."

**Comparison with the data:**

| Point | Result | Why it matters |
|---|---|---|
| DEV-008 overdue (due 2026-03-05) | Right | An old server past its refresh date is a failure risk [[XW-010]] |
| DEV-027 overdue (due 2026-03-05) | Missed | Mobile devices lose support quickly [[XW-010]] |
| DEV-045 overdue (due 2026-03-05) | Missed | About three years in service; budget needs the full list [[XW-012]] |
| DEV-011 retired 2023-02-19, no confirmed wipe | Missed | Disposal cannot close without wipe or destruction evidence [[XW-010]] |
| DEV-042 retired 2025-01-09, no confirmed wipe | Missed | Same, and the data is still on the device [[XW-010]] |

**Rating: gap.** The learner checked refresh dates for one device and did not check retired devices at all. Retirement is a risk step, not an end state.

## Summary

| Drill | Task | Rating | Gap |
|---|---|---|---|
| 1 | Retire hardware with wipe evidence | gap | Retired devices not checked for wipe confirmation |

**Next drills:** repeat the retirement drill with a different device, then track refresh against budget (cost as a range, not a quote). Practicum exercise 07 works the same data by hand.

For exam content, use IAITAM's own CHAMP outline and training. This is practice only and does not predict the result.

**Decision needed:** which gap to work first, and whether to book the exam.

```findings
[
  {"type": "knowledge_gap", "id": "retired-device-wipe-check"},
  {"type": "knowledge_gap", "id": "refresh-overdue-completeness"}
]
```
