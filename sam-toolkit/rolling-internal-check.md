# Rolling internal check

A small, regular test of how your program really works, so an external audit finds nothing you haven't already fixed. Instead of one large audit a year, test two or three areas each quarter, fix what you find, and test again. The yearly internal audit and management review in `audit-and-review-checklist.md` then becomes a summary of work already done.

Findings are for fixing; they're not a rating of anyone. Clause references are to the shared crosswalk (`XW-` rows).

## The five steps

1. Choose this quarter's areas. Pick two or three from the table below. Start with the one you worry about most. [[XW-025]]
2. Take a sample. Pull the records the test needs, not the ones you already know are good. Write the sample size down.
3. Test each record against the rule. A record either passes or fails. Do not average.
4. Log every failure in `internal-check-log.csv`, with a severity, an owner, and a date. [[XW-020]]
5. Fix, then test again next quarter. A finding is closed only when a retest passes.

## Areas to test, and how

The sample sizes are suggestions. Use a larger sample for a risky area.

| Area | Simple test | Suggested sample | Passes when |
| --- | --- | --- | --- |
| Ownership | Is the named owner an active employee who knows they own it? | 20 applications | Every sampled application has a valid owner |
| Inventory accuracy | Do sampled discovered items appear in the record, and sampled records appear in discovery? | 20 each way | Every sampled item matches |
| Renewals | Does each renewal in the next 180 days have an owner and a decision date? | All of them | None is missing either |
| Proof | Can you show proof for each product of your three largest publishers, in the contract's metric? | 3 publishers | Every product has proof, or a logged gap |
| Retirement | Does each recently retired asset have a wipe or destruction record and a closed license? | Last 10 retirements | Every one is complete |
| Intake gate | Did each recent purchase pass the gate before it was paid? | Last 20 purchases | Every one has a gate result on file |
| Leavers | Were licenses and access reclaimed for recent leavers? | Last 10 leavers | Every one is reclaimed |

## A four-quarter rotation

A simple plan so every area is tested at least once a year. Change it to fit your risks.

| Quarter | Areas |
| --- | --- |
| First | Retirement, renewals |
| Second | Proof, intake gate |
| Third | Ownership, leavers |
| Fourth | Inventory accuracy, plus the areas that failed earlier |

## Keep it useful

- Test what you can fix.
- Report the trend, not only the count. Fewer repeat findings means fixes are holding.
- Share the log with your sponsor each quarter. Use it in the leadership report.
- Before an external audit, run the same tests on the products the publisher named.

## Decision

| Decision | Owner | Approver | Date |
| --- | --- | --- | --- |
| This quarter's areas and sample sizes agreed | | | |
