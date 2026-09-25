# Exercise 01: Program setup — Halden's council charter

**Level:** CAMP · **Time:** 30–45 minutes

## Scenario

Halden Logistics' CIO wants a software governance council and asked a working group to draft a charter first. The draft is done and the CIO wants an honest read before it goes to the executive team: does this charter actually let the council function, or does it just look like one on paper?

## Files

- [`demo-estate/council-draft.md`](../demo-estate/council-draft.md) — the draft charter
- [`methods/program-setup/checklist.md`](../methods/program-setup/checklist.md) — the 11-point launch checklist

## Work through

Read the draft charter once straight through, then go line by line against the checklist. Don't stop at the first thing that looks wrong — the checklist has 11 items and the draft doesn't fail all of them.

- Count the "Members (voting)" list by hand. The checklist gives a range; the draft doesn't state a number, so you have to count it yourself.
- Read the "Intake" section next to the "Escalation" section. One of them names a threshold in words ("above a cost or risk threshold") without ever saying what that threshold *is* — that's a different problem from not having an intake process at all.
- Look for a heading, or even a sentence, that names one single executive who controls budget for this council. There isn't a "Members" role that automatically counts.

## Hand in

A short gap table: checklist item, what the draft has or lacks, why it matters. Then tick the gaps you found on the interactive practicum page — it lists the same seven possible gaps this checklist covers (decision rights, sponsor, membership size, intake path, cadence, success measures, escalation), so tick only the ones you actually found.

## Check yourself

Open the [interactive practicum page](../site/practicum.html#program-setup) and enter your gap findings there — no installs, no command line. It reports three lists: **passed** (you found it), **missed** (it's real and you didn't flag it), and **extra** (you flagged something the key doesn't recognize — one extra is tolerated, more than that fails the run). The key behind it, `demo-estate/answer-key.json`, is public in this repo, so open it only after you've checked your own answer — looking first defeats the point of the exercise.

## Reflect

1. The charter's escalation and cadence sections have no gaps at all. What would you tell the CIO those sections got right, so the rewrite doesn't accidentally break them while fixing the rest?
2. If you were the sponsor being asked to sign this charter, what one number would you insist on seeing added before you'd put your name on it?
3. A 14-person voting body and an unset threshold are different failure modes — one makes decisions slow, the other makes them arbitrary. Which would you fix first if you could only fix one before the next council meeting?

## Certification link

This exercise practices the CAMP body of knowledge's program-management ground: standing up a governance body with a named sponsor, written decision rights, and a workable membership size, rather than treating "we held a meeting" as the same thing as "we have a functioning council."
