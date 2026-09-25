# Exercise 07: Hardware lifecycle — Halden's device fleet

**Level:** CHAMP · **Time:** 30–45 minutes

## Scenario

Halden's IT operations lead is planning next quarter's hardware budget and wants two things settled before the number goes to finance: which devices are already past due for replacement, and whether every retired device actually got its data wiped before it left the estate. You've been handed the device fleet and asked to find both problems in one pass.

## Files

- [`demo-estate/devices.csv`](../demo-estate/devices.csv) — 60 laptops, desktops, mobile devices, and servers, with owner, deploy date, refresh-due date, status, retirement date, data-wipe confirmation, and cost

## Work through

Use `methods/hardware-lifecycle/checklist.md` by hand, without AI.

- Only `active` devices have a `refresh_due_date` worth checking — compare it against the device's own `checked_on` date, not today's date or a date you assume for the whole file. There are exactly three devices already past due.
- Only `retired` devices carry a `data_wipe_confirmed` value. A blank value belongs to an active device and isn't a finding; the finding is a retired device whose confirmation reads anything other than `yes`. There are exactly two.
- Group the overdue devices by `type` before you price a replacement — a laptop refresh and a server refresh don't cost the same, and lumping them into one number will make your range meaningless.

## Hand in

A table of the devices needing action (id, type, status, issue, recommendation), a replacement-cost range grouped by device type for the overdue devices, and a list of the retired devices still blocking disposal with the wipe or destruction method you'd require before closing each one out. Then, on the interactive practicum page: tick each overdue device and each unwiped retired device you found.

## Check yourself

Open the [interactive practicum page](../site/practicum.html#hardware-lifecycle) and enter your findings there — no installs, no command line. "Passed" means every overdue device and every unwiped retired device in the key showed up in your findings, with at most one extra finding the key doesn't recognize; "missed" lists anything real you didn't flag; "extra" lists anything you flagged that isn't in the key. The key is `demo-estate/answer-key.json` in this repo — it's public, so check your own answer before you look at it.

## Reflect

1. One of the three overdue devices is a server, not a laptop or a phone. Does an overdue server carry the same urgency as an overdue laptop, or does the type change how you'd prioritize the replacement order?
2. Neither unwiped retired device is also an overdue-refresh device. What does that tell you about treating "still in service" and "safely retired" as two separate checks rather than assuming one implies the other?
3. Your replacement-cost range has a low end and a high end. What real-world fact (a bulk-order discount, a trade-in credit, a device that turns out to need an early replacement anyway) would move the actual spend toward one end even after every order is placed?

## Certification link

This exercise practices the CHAMP body of knowledge's asset-lifecycle and disposal ground: tracking a device from deployment through refresh eligibility, and holding disposal open until data destruction is actually evidenced rather than assumed.
