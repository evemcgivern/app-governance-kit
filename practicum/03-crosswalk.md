# Exercise 03: Crosswalk — mapping Halden's three controls

**Level:** CSAM · **Time:** 30–45 minutes

## Scenario

Halden's internal auditor wrote three plain-English controls she wants tied back to recognized frameworks before the next audit cycle, so a control review doesn't come down to "trust us." Your job is to find where each control already lives in the kit's framework mapping, not to write new framework text.

## Files

- [`demo-estate/controls.md`](../demo-estate/controls.md) — the three controls to map
- [`methods/crosswalk/crosswalk.csv`](../methods/crosswalk/crosswalk.csv) — the 28-row crosswalk table

## Work through

Use `methods/crosswalk/checklist.md` by hand, without AI.

- Restate each control in one sentence before you go looking. C1 actually bundles two obligations together — notice that before you pick a row, even though only one of the two obligations is what the exercise grades.
- Skim the `theme` and `summary` columns in `crosswalk.csv` for words that echo the control's verb, not just its noun. "Review... on a schedule" and "Assess... before it is deployed" are both actions a theme name should mirror.
- Don't stop at the first row that seems plausible for a given control — at least one control has a second row nearby that only covers part of it. Pick the row that's the *best* match, not just *a* match.

## Hand in

A table per control: control label, matched theme, the clause number from each of the four framework columns (or "no direct equivalent"), and one sentence on what that clause asks for in your own words. Then a short gaps note — which framework(s) have no equivalent for a given control, and what that framework's auditor would ask for instead. Then pick your matching crosswalk row for each control from the dropdown on the interactive practicum page.

## Check yourself

Open the [interactive practicum page](../site/practicum.html#crosswalk) and enter your matches there — no installs, no command line. "Passed" means all three controls matched the row the key expects and you didn't add more than one wrong match; "missed" names any control whose expected row you didn't record; "extra" names any match you recorded that the key doesn't expect. The key is `demo-estate/answer-key.json` in this repo, and it's public — check your own work first.

## Reflect

1. C1 bundles inventory and ownership into one sentence. If Halden's auditor insists on a second row for the ownership half, what would that do to how the finding is scored versus how the control is actually satisfied in practice?
2. Pick one control where a framework has no direct equivalent. Is that framework actually silent on the topic, or does it just not use the vocabulary this control does?
3. The crosswalk only has 28 rows. What's a control you can imagine Halden needing that wouldn't map cleanly to any of them — and what would you propose as the new row's one-sentence summary?

## Certification link

This exercise practices the CSAM body of knowledge's compliance-mapping ground: tying a plain-language control to the specific standard clause that backs it, and being able to name — rather than guess at — where a framework's coverage actually stops.
