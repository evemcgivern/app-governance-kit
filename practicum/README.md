# Halden practicum

Seven hands-on exercises built around one fictional company, Halden Logistics, and the same demo data this kit's tools already use. Each exercise asks you to work a real governance problem by hand, using only a checklist — no AI, no shortcuts — and then check your own answer against this kit's grader.

## Who it's for

Anyone studying toward CAMP, CSAM, or AIGP (see the [field guide](../site/field-guide.html) for what each certification actually covers), or anyone who wants practice reasoning through IT asset, framework-mapping, portfolio, access, or AI-governance problems before doing it for real. No prior use of this kit is required — each exercise names the files you need and the checklist to work from.

## How long each one takes

30 to 60 minutes, done by hand with the checklist open and nothing else. The rationalization and access-review exercises run toward the long end because their data files are larger; the rest are shorter.

## The seven exercises, in order

| # | Exercise | Level |
|---|---|---|
| 1 | [01-program-setup.md](01-program-setup.md) | CAMP |
| 2 | [02-itam-maturity.md](02-itam-maturity.md) | CAMP |
| 3 | [03-crosswalk.md](03-crosswalk.md) | CSAM |
| 4 | [04-rationalization.md](04-rationalization.md) | CSAM |
| 5 | [05-access-review.md](05-access-review.md) | CSAM |
| 6 | [06-ai-intake.md](06-ai-intake.md) | AIGP |
| 7 | [07-hardware-lifecycle.md](07-hardware-lifecycle.md) | CHAMP |

Work them in order if you're new to all three certifications — each one builds on ideas (crosswalk rows, the checklist habit) the earlier ones introduce. If you already hold one of the three, jump straight to its section.

## How self-checking works

Every exercise ends with what you found, entered directly into the [interactive practicum page](../site/practicum.html) — no installs, no command line, nothing to run. Pick your exercise, enter your answers in its checkboxes and selects, and hit Check. It reports three lists — **passed**, **missed**, and **extra** — comparing what you entered against a fixed answer key, so you get a pass/fail signal without anyone standing over your shoulder.

## A note on the answer key

The answer key each exercise is graded against, `demo-estate/answer-key.json`, sits in this same repository and is not access-controlled. That's a deliberate choice: this practicum is for self-study, not certification, and there's no exam integrity to protect. But reading the key before you've worked the exercise defeats the entire point — you'd be checking whether you can copy an answer, not whether you can find a problem in real data using only a checklist. Do the work first.
