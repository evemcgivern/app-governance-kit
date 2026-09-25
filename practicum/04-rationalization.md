# Exercise 04: Rationalization — Halden's application portfolio

**Level:** CSAM · **Time:** 45–60 minutes

## Scenario

Halden's finance team wants a savings estimate ahead of next year's budget cycle, and the CIO wants to know which applications are quietly duplicating each other before that number goes to anyone. You've been handed the inventory and the license file and asked to find both problems in one pass.

## Files

- [`demo-estate/apps.csv`](../demo-estate/apps.csv) — 60 applications with category, cost, users, and data sensitivity
- [`demo-estate/licenses.csv`](../demo-estate/licenses.csv) — one license row per application, with entitlements, expiry, and the date it was checked

## Work through

Use `methods/rationalization/checklist.md` by hand, without AI.

- Sort or group `apps.csv` by `category`. A duplicate pair doesn't need matching names — two apps can serve the same function under completely different vendor names, and the category column is a better signal than the name is.
- Compare every license's `expiry` date against its own `checked_on` date, not against today's date or a single date you assume for the whole file. An expiry that's already past its own checked-on date is the problem; there are exactly two.
- There are five duplicate pairs, not one or two — don't stop once you've found the most obvious pair. Categories repeat in more places in this file than a first skim usually catches.

## Hand in

A TIME table (app id, name, category, TIME call, one-line reason) covering all 60 apps, a duplicates section naming each pair and which side you'd keep and why, a license section listing the expired ones, and a savings range (not a single number) for what Eliminate/Migrate would free up. Then, on the interactive practicum page: tick the two apps in each duplicate pair and use "Mark selected as duplicates," and tick "expired" next to each license you found past its own checked-on date.

## Check yourself

Open the [interactive practicum page](../site/practicum.html#rationalization) and enter your findings there — no installs, no command line. "Passed" means every duplicate pair and every expired license in the key showed up in your findings, with at most one extra finding the key doesn't recognize; "missed" lists anything real you didn't flag; "extra" lists anything you flagged that isn't in the key. The key is `demo-estate/answer-key.json` in this repo — it's public, so check your own answer before you look at it.

## Reflect

1. For one duplicate pair, you had to pick which app to keep. What tipped the decision — cost, user count, category fit, something else — and would the losing app's users agree with that call?
2. Neither expired license belongs to a duplicate app. What does that tell you about treating "license problem" and "duplicate problem" as two separate scans rather than assuming one flags the other?
3. Your savings range has a low end and a high end. What real-world fact (notice period, migration cost, a dependency nobody documented) would push the actual number toward the low end even after every retirement is approved?

## Certification link

This exercise practices the CSAM body of knowledge's license-compliance and portfolio-optimization ground: building an effective license position instead of trusting entitlement counts at face value, and finding consolidation candidates by function rather than by name.
