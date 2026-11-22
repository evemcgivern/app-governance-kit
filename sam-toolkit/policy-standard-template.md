# Standard template

A fill-in template for one software standard. A standard is a catalog, not a policy: it lists what is approved for a role or device class, in what version and setup, and how to ask for something else. Replace each prompt in brackets with your own text. Every example is fictional and comes from Halden Logistics, the demo estate.

Clause references are to ISO/IEC 19770-1:2017 (paraphrased) and to the shared crosswalk (`XW-` rows). Verify license terms against the contract; this template does not interpret them.

## Control block

| Field | Entry |
| --- | --- |
| Standard ID | [Your numbering scheme, for example ITAM-STD-001] |
| Title | [Role or device class, for example Warehouse handheld devices] |
| Version | [Version number and one line on what changed] |
| Owner | [A selection committee, named by role] [[XW-004]] |
| Approver | [Role with authority over the parent policy] [[XW-027]] |
| Effective date | [Date] |
| Next review | [Date, and the events that bring it forward] [[XW-025]] |

## 1. Parent policy

Name the policy this standard serves, and the section that requires people to follow it. [[XW-003]]

| Parent policy | Section | Version |
| --- | --- | --- |
| [Software acquisition and exceptions policy] | [Section number] | [Version] |

## 2. Scope

State the role or device class this standard covers. Include software delivered as a service, not only installed titles. [[XW-001]]

| Item | Entry |
| --- | --- |
| Role or device class | [For example, dispatch coordinators] |
| Installed software included | [Yes or no] |
| Subscription and SaaS included | [Yes or no] |
| Out of scope | [What is left out, with the reason] |

Example (fictional): Halden dispatch coordinators, on Halden-managed laptops, including the routing subscription they use in a browser.

## 3. The standard

| Title | Version or plan | Configuration | Approved vendor | Linked hardware | Owner |
| --- | --- | --- | --- | --- | --- |
| [Product name] | [Approved versions] | [Required settings or image] | [Vendor] | [Device model or class, if the software depends on it] | [Role] |

Example (fictional): Northbeam ERP client, current supported release only, standard image, Northbeam, any Halden laptop model on the current list, ERP product owner.

For each row, confirm the license metric, the number of licenses held, and where the proof of purchase is filed (`license-position.csv`, `proof-of-purchase-check.csv`). [[XW-006]] [[XW-007]]

## 4. Acceptance and rejection criteria

A title joins the catalog when it meets the criteria below, and each decision carries a reason code so patterns can be counted later. [[XW-009]]

| Criterion | Accept when | Reject code | Reason in words |
| --- | --- | --- | --- |
| Business need | [A named need that no catalog title meets] | [R1] | [No unmet need] |
| License fit | [Metric and terms confirmed against the contract] | [R2] | [License terms cannot be met or confirmed] |
| Security | [The security requirements below are met] | [R3] | [Fails a security requirement] |
| Support | [Vendor supports the version in use] | [R4] | [Out of support or near end of support] |
| Overlap | [Does not duplicate a catalog title; see the `rationalization` method] [[XW-011]] | [R5] | [Duplicates an existing title] |
| Data and AI | [AI features and data handling cleared by the `ai-intake` method] [[XW-021]] [[XW-028]] | [R6] | [Not cleared for data or AI use] |

Change the codes and wording to fit your organization. Record each decision, with its code, where the committee keeps its decisions.

## 5. Security requirements

List the requirements a standard title must meet, stated so each can be checked. [[XW-028]]

| Requirement | How it is checked | Owner |
| --- | --- | --- |
| [Supported version that receives security fixes] | [Vendor support date on file] | [Role] |
| [Sign-in through the organization's identity system] | [Configuration review] | [Role] |
| [Data handling matches the classification of the data it holds] | [Review at approval] | [Role] |

## 6. Non-standard path

A request for something not on the catalog is allowed. It follows the exception path in the parent policy: a written request with the reason and risk, an approver who is not the requester, escalation by cost and risk, an end date, and an entry in `authorization-log.csv`. [[XW-009]] [[XW-019]]

| Question | Entry |
| --- | --- |
| Where the request is made | [Form or queue] |
| Who decides | [Role, and the next role up for higher cost or risk] |
| Longest time an exception runs before review | [Your limit] |
| What happens at the end | [Add to the catalog, or stop and remove] |

## 7. Rollout approach

Start with a small pilot group before everyone. Say who is in it, how long it runs, and what result moves it to full rollout. Plan for support, training, and rollback.

| Step | Detail |
| --- | --- |
| Pilot group | [Who, and how many] |
| Pilot length | [Dates] |
| Pass condition | [What you will check before going wider] |
| Full rollout | [Dates and method] |
| Rollback | [How a title is withdrawn if it fails] |

## 8. Feedback channel

Say where users report problems, ask for changes, or propose a title, and who answers within what time. [[XW-025]]

| Item | Entry |
| --- | --- |
| Channel | [Mailbox, form, or queue] |
| Answered by | [Role] |
| Answered within | [Your target] |

## 9. Review date

Review at least yearly, and when a listed title reaches end of support, a vendor changes its license terms, or a security advisory names a listed title. [[XW-025]]

| Last reviewed | Next review | Reviewed by |
| --- | --- | --- |
| [Date] | [Date] | [Role] |

## 10. Where published

Publish the current version where staff and buyers look, and withdraw older versions so they cannot be found by mistake. [[XW-020]] (7.6.5)

| Item | Entry |
| --- | --- |
| Location | [Link] |
| Versions kept | [Where older versions are archived] |
| Told when it changes | [Who is notified, and how] |

## Decision

| Decision | Owner | Approver | Date |
| --- | --- | --- | --- |
| Approve this standard as written | [Owner role] | [Approver role] | |

Source: ISO/IEC 19770-1:2017 clause 7.6.5, and the shared crosswalk. Paraphrased; this is not a substitute for the standard.
