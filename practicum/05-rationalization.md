# Exercise 05: Rationalization, Halden's application portfolio

**Level:** CSAM · **Time:** 45–60 minutes

## Scenario

Halden's finance team wants a savings estimate ahead of next year's budget cycle, and the CIO wants to know which applications are duplicating each other before that number goes to anyone. You've been handed the inventory and the license file and asked to find the duplicate applications and the expired licenses.

## Files

- [`demo-estate/apps.csv`](../demo-estate/apps.csv): 60 applications with category, cost, users, and data sensitivity
- [`demo-estate/licenses.csv`](../demo-estate/licenses.csv): one license row per application, with entitlements, expiry, and the date it was checked

## Work through

Use `methods/rationalization/checklist.md` by hand, without AI.

- Sort or group `apps.csv` by `category`. A duplicate pair doesn't need matching names; two apps can serve the same function under completely different vendor names, and the category column is a better signal than the name is.
- Compare every license's `expiry` date against its own `checked_on` date, not against today's date or a single date you assume for the whole file. An expiry that's already past its own checked-on date is the problem; there are exactly two.
- There are five duplicate pairs, so don't stop at the most obvious one; categories repeat in more places than a first skim catches.

## Hand in

A TIME table (app id, name, category, TIME call, one-line reason) covering all 60 apps, a duplicates section naming each pair and which side you'd keep and why, a license section listing the expired ones, and a savings range (not a single number) for what Eliminate/Migrate would free up. Then, on the interactive practicum page: tick the two apps in each duplicate pair and use "Mark selected as duplicates," and tick "expired" next to each license you found past its own checked-on date.

## Check yourself

Open the [interactive practicum page](../site/practicum.html#rationalization) and enter your findings there. "Passed" means every duplicate pair and every expired license in the key showed up in your findings, with at most one extra finding the key doesn't recognize; "missed" lists anything real you didn't flag; "extra" lists anything you flagged that isn't in the key. The key is `demo-estate/answer-key.json` in this repo; it's public, so check your own answer before you look at it.

## Reflect

1. For one duplicate pair, you had to pick which app to keep. What tipped the decision (cost, user count, category fit, something else) and would the losing app's users agree with that call?
2. Neither expired license belongs to a duplicate app. What would you have missed if you had trusted the duplicate scan to surface license problems?
3. Your savings range has a low end and a high end. Which fact (a notice period, a migration cost, a dependency nobody documented) would hold the actual number at the low end even after every retirement is approved?

## Certification link

This exercise practices the CSAM body of knowledge's license-compliance and portfolio-optimization ground: building an effective license position and finding consolidation candidates by function.
