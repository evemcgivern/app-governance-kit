# Exercise 02: ITAM maturity — Halden's baseline scores

**Level:** CAMP · **Time:** 30–45 minutes

## Scenario

Halden's ITAM lead has already scored the organization against nine process areas, on a 1–5 scale, and handed you the raw answers. Your job isn't to re-score anything — it's to read the scores the way an assessor would: find the three areas that need attention first, and be ready to defend why those three and not some other three.

## Files

- [`demo-estate/maturity-answers.csv`](../demo-estate/maturity-answers.csv) — one score per process area
- [`methods/itam-maturity/checklist.md`](../methods/itam-maturity/checklist.md) — the assessment checklist

## Work through

Use the checklist by hand, without AI.

- Sort the nine areas by score, lowest first. The three lowest are your gaps — but check for ties before you commit to which three.
- The checklist calls for "tie-break reasoning," not just a sorted list. If two areas share the same low score, you need a reason to name both (or to break the tie) beyond "the CSV said so."
- The area column gives you a slug already (for example `data-quality`, not "Data quality and reconciliation"). That's the exact id the findings block expects — don't invent your own spelling of it.

## Hand in

A score table (area, score, one line of interpretation), the three gaps you've named with your tie-break reasoning, and a short 90-day-plan sketch for each gap (owner role, two or three actions, what evidence would show progress). Then tick your three gap areas on the interactive practicum page's score table.

## Check yourself

Open the [interactive practicum page](../site/practicum.html#itam-maturity) and enter your gap findings there — no installs, no command line. "Passed" means every gap in the key showed up in your findings and you didn't overshoot by more than one extra; "missed" lists any real gap you didn't flag; "extra" lists anything you flagged that the key doesn't recognize. The key sits in `demo-estate/answer-key.json` in this repo — it's public, so check your own answer before you open it.

## Reflect

1. Two areas tied at the same score. What made you name both as gaps (or pick one over the other), and would a different assessor reasonably disagree?
2. Vendor and cost management both scored highest. Does a high score there tell you anything is actually safe, or only that nobody's looked hard enough yet to find the problem?
3. If Halden could fund improvement work in only one of your three gap areas this year, which would you argue for, and what would you tell the sponsor they're accepting by not funding the other two?

## Certification link

This exercise practices the CAMP body of knowledge's process-maturity assessment work: scoring against defined criteria, naming gaps with reasoning rather than intuition, and turning a baseline into a funded 90-day plan instead of a filed report nobody acts on.
