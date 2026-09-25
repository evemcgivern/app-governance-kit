# Exercise 05: Access review — Halden's account export

**Level:** CSAM · **Time:** 45–60 minutes

## Scenario

Halden's auditor asked for a quarterly access review across the applications in scope. You have the account export, the HR roster, and the application list. Before anything else goes in the memo, every account has to be matched to a real, currently-employed person — and "the login worked recently" is not the same as "this person still works here."

## Files

- [`demo-estate/accounts.csv`](../demo-estate/accounts.csv) — one row per account, with the employee id, app, role, and last login
- [`demo-estate/employees.csv`](../demo-estate/employees.csv) — employee id, status, and termination date
- [`demo-estate/apps.csv`](../demo-estate/apps.csv) — application data sensitivity, to set review order

## Work through

Use `methods/access-review/checklist.md` by hand, without AI.

- Check the applications' `data_sensitivity` column first and review the `confidential` apps before the `internal` ones, as the checklist asks — it changes which accounts you'll look at first, not just the write-up order.
- For every account, look up its `employee_id` in `employees.csv` two ways: is that employee's status `terminated`, and does that employee id even *appear* in the roster at all. Those are two different reasons for the same finding, and one of them won't show up if you only check status.
- `last_login` alone won't tell you an account is orphaned — a recent login from a terminated employee's account is exactly the failure mode this checklist step exists to catch, not a reason to skip it.

## Hand in

An exceptions table (account id, employee id, app, issue, recommended action), a short evidence summary (scope, population reviewed, method), and a one-paragraph auditor memo. Then tick "orphaned" next to each account you found on the interactive practicum page.

## Check yourself

Open the [interactive practicum page](../site/practicum.html#access-review) and enter your findings there — no installs, no command line. "Passed" means every orphaned account in the key is in your findings, with at most one extra; "missed" lists any orphaned account you didn't catch; "extra" lists any account you flagged that the key doesn't. The key is `demo-estate/answer-key.json` in this repo — it's public, so check your own answer before you open it.

## Reflect

1. One orphaned account belongs to an employee id that isn't in `employees.csv` at all, rather than one marked terminated. What process failure would produce an account like that, and is it the same fix as a slow offboarding?
2. You reviewed confidential apps first. Did that change which orphaned accounts you found first, or only the order you wrote them up in?
3. If you could add one column to `accounts.csv` that would have made this review faster without changing what counts as orphaned, what would it be?

## Certification link

This exercise practices access-certification ground shared across the CSAM syllabus and ISO/IEC 27001's access-control controls: matching every account to a real, current person, prioritizing review by data sensitivity, and treating a missing HR record as seriously as an explicit termination date.
