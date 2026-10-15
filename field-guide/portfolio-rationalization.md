# Field guide: deciding what to keep, merge, or retire

**Common practice, not a standard.** No ISO or COBIT text defines how to score applications for a keep, merge, or retire decision. ISO/IEC TS 19770-13:2026 advises retiring unused assets and keeping the application portfolio small (clause 6.1 Table 1 and 4.4.3), and COBIT BAI09.04 covers optimizing asset value. Neither gives a scoring method. The methods below are what practitioners and vendors use. Each is backed by at least two independent sources, fetched and read for this page on 2026-10-14. Vendors describe their own versions, so treat the sources as practice reports, not authority.

## TIME (Tolerate, Invest, Migrate, Eliminate)

The most widely cited approach, and the one this kit's `rationalization` tool uses. Each application lands in one of four groups:

| Group | Meaning |
| --- | --- |
| Tolerate | Keep running as is; little reason to spend more. |
| Invest | Fund and expand; the application is worth more investment. |
| Migrate | Move to a better platform or replace; the need is real but the technology is not. |
| Eliminate | Retire. |

Placement uses two axes. LeanIX names them technical fit and functional fit. GetInSync names them business fit and technical health. Sources credit the model to Gartner.

Where sources differ:

- GetInSync renames Migrate to Modernize, because migration is only one way to fix an application with high value on failing technology.
- Axis names vary by publisher.
- I could not retrieve a Gartner original, so the attribution rests on the vendor and consultancy pages.

Sources: [LeanIX](https://www.leanix.net/en/wiki/ea/gartner-time-model); [GetInSync](https://getinsync.ca/time-framework/); [IF4IT](https://if4it.org/best-practices/application-portfolio-management-apm/use-rationalization-postures-to-classify-applications-by-their-current-investment-and-action-direction/).

## Invest, sustain, migrate, retire (ServiceNow)

ServiceNow's Enterprise Architecture (formerly Application Portfolio Management) frames the same decision with four of its own labels. Its documentation says bubble charts place applications by their indicator scores, and that the placement guides the four decisions. A ServiceNow partner writes the same set as invest, sustain or maintain, replace, retire, and migrate. Rough mapping to TIME: sustain is Tolerate, retire is Eliminate, invest and migrate carry over. Neither source describes a scoring formula.

Sources: [ServiceNow documentation](https://www.servicenow.com/docs/r/application-portfolio-management/eaw-rationalize-business-applications.html); [Surety Systems](https://www.suretysystems.com/insights/servicenow-apm-application-portfolio-management-surety-systems/).

## The "R" families (rehost, replatform, retire, and so on)

These are cloud-migration strategies, not scoring methods. They say what to do with an application you have already decided to move: rehost, replatform, repurchase, refactor or re-architect, retire, or retain. They help after the keep-or-retire call, and only "retire" and "retain" speak to it. Both sources say the six build on an earlier set of five from Gartner; they disagree on the year (AWS says 2011, Cortex says 2010).

Sources: [AWS](https://aws.amazon.com/blogs/enterprise-strategy/6-strategies-for-migrating-applications-to-the-cloud/); [Cortex](https://www.cortex.io/post/the-6-rs-of-cloud-migration).

## Scoring on more than two axes

A two-axis grid is a start. Two sources argue for scoring on more factors:

- Netguru scores five: business criticality, cost to run, cost to change, technical risk, and blast radius (how many other systems depend on the application). It argues that a two-axis view can point to retiring a system that many others rely on.
- Apptio lists criteria including business function, usage, cost against value, redundancy with other tools, risk, and technical fit. Redundancy is the factor behind "merge".

Neither gives a numeric model. This kit's tool follows the same idea: it scores business value and technical fit, states the scoring it used each run, and leaves the final keep-or-retire call to a person.

Sources: [Netguru](https://www.netguru.com/blog/application-portfolio-rationalization-guide); [Apptio](https://www.apptio.com/topics/application-rationalization/).
