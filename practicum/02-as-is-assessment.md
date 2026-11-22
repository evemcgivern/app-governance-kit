# Exercise 02: As-is assessment, score Halden's application management

**Level:** CAMP · **Time:** 30–45 minutes

## Scenario

Halden's CIO has asked the interim asset manager for a baseline of how application management runs today, and she has one afternoon. She starts the way the playbook says to: a five-minute gut check, a rough 0 to 3 for each of the eleven dimensions in the self-assessment, from memory and with no files open. That's playbook step 1, and it's a guess. Then she gathers what she can actually show and scores each dimension again from evidence, which is playbook step 5. She found ten pieces of evidence and wrote each one into a table, with a note on its quality. Your job is to do both passes, then name the three dimensions Halden should start with.

You won't find a single right answer to this in a real organization, because two assessors can read the same shelf of documents differently. This version has one, because the Halden evidence table was written so that each score follows from a rule. Apply the rule as written, the way you would apply the kit's evidence rule to your own records.

## Files

- [`demo-estate/as-is-evidence.csv`](../demo-estate/as-is-evidence.csv): ten evidence rows, each with a dimension, what was found, and how good the evidence is
- [`sam-toolkit/application-management-self-assessment.md`](../sam-toolkit/application-management-self-assessment.md): the eleven dimensions and the 0 to 3 scale
- [`sam-toolkit/itam-program-playbook.md`](../sam-toolkit/itam-program-playbook.md): step 1 (the gut check) and step 5 (the evidence-based baseline)

## Work through

Use the self-assessment by hand, without AI. Do the gut check first and write it down before you open the evidence table.

- Gut check (playbook step 1): give each of the eleven dimensions a 0 to 3 in five minutes, from memory. The practicum page doesn't grade this pass. Keep it so you can compare it with your evidence scores afterward.
- Score from evidence (playbook step 5): take each dimension's evidence row and turn its quality into a score. None means 0. Spoken means 1: it happens, but nothing is written down. Written but not followed or used means 1, the "one level lower" the evidence rule asks for. Written and followed, with a recent example, means 2. A measure that nobody has acted on means 2. A measure that has led to a change means 3.
- Cite your evidence: for every score, write the evidence ID (for example EV-02) that supports it.
- No evidence is an answer. If a dimension has no row in the table, nobody showed Halden anything for it, so it scores 0 and you write "no evidence." That's different from a row that says someone looked and found nothing, though both score 0.
- Check the dimension names against the self-assessment. The page uses a short id for each one (for example `roles`), and the page shows both.
- Choose the three weakest dimensions as the starting gaps. Check for ties before you commit: if a fourth dimension shares the third-lowest score, you'd need a tie-break reason.

## Hand in

Two score tables. The first is your gut check: dimension and a guess. The second is your evidence-based as-is score: dimension, score, the evidence ID you cite (or "no evidence"), and one line on why that score and not one level higher. Then name the three starting gaps. Enter your scores and tick the three weakest dimensions on the interactive practicum page.

## Check yourself

Open the [interactive practicum page](../site/practicum.html#as-is-assessment) and enter your scores and your three gaps there. No installs, no command line. "Passed" means every score and gap in the key showed up in your findings and you didn't overshoot by more than one extra; "missed" lists any score or gap you didn't enter correctly; "extra" lists anything you entered that the key doesn't recognize. The key sits in `demo-estate/answer-key.json` in this repo; it's public, so check your own answer before you open it.

## Reflect

1. Where did your gut check and your evidence score differ most? Which one would you show the CIO, and why?
2. Roles and ownership had no evidence row at all, while intake and communication had rows that said someone looked and found nothing. Is "nobody showed me anything" the same finding as "I checked and there's nothing"? What would you do differently about each?
3. A written policy that nobody follows scores 1, not 2. Where would a reader be tempted to give Halden credit for intent, and what would that cost the CIO later?
4. The three gaps all score 0. If Halden could fund one of them this quarter, which would you argue for, and what would you tell the sponsor they're accepting by leaving the other two?

## Certification link

This exercise practices the CAMP body of knowledge's baseline assessment work: separating what people believe from what they can show, scoring against a stated rule, treating missing evidence as a finding, and choosing a small set of gaps to fund first.

For a follow-on, repeat the assessment on your own program with `application-management-gap-plan.csv`, then set a To-Be level for each of your three gaps.
