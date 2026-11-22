# Field guide: confusable pairs

Seven pairs of terms that learners mix up when they study for CAMP and CSAM. Each one has a short difference, a small Halden Logistics scenario, and an answer. Try the scenario before you read the answer.

This is practice on concepts, not exam questions, and it does not predict a result. Terms are explained in this kit's own words; for exam content use the certification body's materials ([certifications.md](certifications.md)). Halden is fictional, and its files are in `demo-estate/`.

Pairs 1 to 5 and 7 come up in CAMP. Pair 6 comes up in CSAM.

## 1. Program vs. project

**The difference.** A program is a standing effort with no end date. A project is a one-off effort with a start, a plan, and a calculated end. A project can sit inside a program.

**Try it.** Halden decides to replace its oldest laptops this quarter. After that, someone keeps watching device refresh dates for good (`refresh_due_date` in `devices.csv`). Which part is the project and which is the program?

**Check yourself.** The replacement drive is the project: it has a start, a plan, and an end. Watching refresh dates from then on is the program, because it never finishes.

## 2. Key process area vs. key performance indicator

**The difference.** A key process area names a broad kind of work. A key performance indicator is a number that shows how well that work is going. One names the work; the other measures it.

**Try it.** Halden's leadership asks how disposal is going. Name the process area, then give one number from `devices.csv` that would answer them.

**Check yourself.** Disposal is the process area. One good number is the share of retired devices that have a wipe confirmation (`data_wipe_confirmed`). Any measure tied to retirement records works, as long as it is a number tracked over time.

## 3. Policy vs. procedure

**The difference.** A policy says what is required and who is accountable. A procedure says the steps someone follows to meet it. Policies change rarely and need senior approval. Procedures change whenever the work does.

**Try it.** Two statements. (a) Retired software must have its data and access removed, and the retirement must be recorded. (b) Open the retirement ticket, export the account list, revoke each account, then mark the application retired in the inventory. Which is policy and which is procedure?

**Check yourself.** (a) is policy: a requirement. (b) is procedure: the steps to meet it. If the ticket system changes, (b) changes and (a) does not.

## 4. Role vs. job title

**The difference.** A role is a set of duties and decision rights someone holds in a process. A job title is the label on a person's position in the organization chart. Accountability is set by role, and each role has a current named holder.

**Try it.** Halden's draft council charter says the governance analyst keeps the register of decisions. The person who holds that job goes on leave for three months. What should the charter say so the register keeps being kept?

**Check yourself.** The duty belongs to the role, not the person. The charter should name the current holder and a backup, so a change of staff or a leave does not leave the register without a keeper.

## 5. Compliance management vs. legislation management

**The difference.** In IAITAM's course framing, compliance management looks inward: it checks your own estate against the rules and contracts you must follow, and acts on the result. Legislation management looks outward: it watches laws and standards set by others, works out what they mean, and tells the right people. One executes; the other interprets and communicates.

**Try it.** Two tasks at Halden. (a) Compare the installs in `audit-installs.csv` with the licenses its proofs of purchase cover, before a publisher's audit. (b) Suppose a new state privacy law could change how Halden stores customer data; someone reads it and briefs the owners of the affected systems. Which task is which?

**Check yourself.** (a) is compliance management: inward, executing against a contract. (b) is legislation management: outward, interpreting a new requirement and passing it on.

## 6. Entitlement vs. proof of purchase

**The difference.** An entitlement is the usage right a license grants. A proof of purchase is the evidence that the organization actually bought it. A number in a system is a claim; the proof is what supports the claim.

**Try it.** Halden's records say it holds a certain number of seats for a product (`licenses.csv`). A publisher asks Halden to show it. Which record states the right, and which record would you hand over to support it?

**Check yourself.** `licenses.csv` holds the entitlement: what Halden believes it may use. The documents behind it, such as those listed in `proofs-of-purchase.csv`, are the proof. If the proof is missing or does not show the product, version, quantity, or buyer, the entitlement is a claim you cannot support.

## 7. Asset record vs. CMDB record

**The difference.** An asset record says what you own and the facts that matter to money, contracts, and lifecycle: owner, cost, license, purchase, retirement. A CMDB record describes the configuration items that deliver a service and how they relate to each other. The two overlap, but they answer different questions. The CMDB holds the data; the system that manages it is the configuration management system.

**Try it.** Halden wants to know who owns Northbeam ERP and what it costs a year, and also which services stop if a server fails. Which question does the asset record answer, and which the CMDB?

**Check yourself.** Owner and annual cost belong in the asset record. Halden's `apps.csv` has `annual_cost_usd` but no owner column, which is itself a gap. Which services depend on a server is a relationship question, so the CMDB answers it. Good practice keeps one agreed identifier so the two records can be matched, and decides which one is authoritative for each fact.

## After the pairs

If a pair still feels shaky, run the matching `cert-prep` drill and the practicum exercise listed in the [study map](study-map.md).
