# Exercise 06: AI intake — Halden's six AI systems

**Level:** AIGP · **Time:** 30–45 minutes

## Scenario

Halden has quietly accumulated six AI systems across different departments, and nobody has ever tiered any of them for risk. Before the AI governance board's first meeting, someone needs to go through the list and flag which system, if any, needs to stop and get legal review before anything else happens to it.

## Files

- [`demo-estate/ai-systems.csv`](../demo-estate/ai-systems.csv) — six systems, each with an owner and a one-line description

## Work through

Use `methods/ai-intake/checklist.md` by hand, without AI.

- For each system, ask who it affects and what decision it makes or supports about a real person, not just what department owns it. A system that only ranks or scores things (routes, forecasts, spam) is a different case from one that ranks *people*.
- Check whether a person reviews the output before it takes effect on someone. Two systems in this file already have a human in the loop by description; the rest don't, and that absence matters more for some systems than others.
- Employment-related uses — screening, ranking, or shortlisting people for a job — are treated as high-risk regardless of how small or well-intentioned the tool sounds. Look for that pattern specifically before you tier anything as merely limited or minimal.

## Hand in

One short section per system: the use case restated, the risk tier with your reasoning, and the controls you'd require for that tier (tie each control back to a crosswalk row if you can). Then set each system's tier (prohibited, high, limited, minimal) on the interactive practicum page.

## Check yourself

Open the [interactive practicum page](../site/practicum.html#ai-intake) and enter your findings there — no installs, no command line. "Passed" means the high-risk system(s) in the key are in your findings, with at most one extra; "missed" names any high-risk system you didn't tier that way; "extra" names any system you tiered high-risk that the key doesn't. The key is `demo-estate/answer-key.json` in this repo — it's public, so check yourself before you open it.

## Reflect

1. Two systems in this file involve a human reviewing the output before it affects anyone. Does that change the risk tier you'd assign, or only the controls you'd require at that tier?
2. The high-risk system here is a small internal tool, not a flagship product. What made you tier it that way regardless of its size or how routine it sounded to its owner?
3. If Halden's forecasting system started being used to schedule individual warehouse shifts instead of just planning volume, would that change its tier — and what would trigger the re-review that catches a change like that?

## Certification link

This exercise practices the AIGP body of knowledge's risk-tiering and lifecycle ground: recognizing a high-risk use case by its effect on real people rather than its size or department, checking for prohibited practices before tiering, and setting controls and a re-review trigger tied to the tier rather than to a calendar alone.
