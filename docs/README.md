# Documentation

Pick the page by what you need to do. New here? Start with the [quick start](../README.md#quick-start).

## Run and review tests

| Page | Answers |
| --- | --- |
| [Operator guide](operator-guide.md) | How do I deploy each lab, run its cases and collect a Networka checkpoint? |
| [Test framework](test-framework.md) | What does each case assert, what does a run write, how do I replay it or run it in CI? |
| [Small lab walkthrough](walkthrough-small-lab.md) | How does one Small lab run go from wiring to verdict, step by step with links into the code? |
| [Syslog](syslog/README.md) | How does RouterOS logging reach the collector, and how do I check it? |
| [Diagrams](diagrams/README.md) | How do I edit the lab drawings and where is each scenario's evidence? |

## Test cases

| Page | Answers |
| --- | --- |
| [Case index](cases/README.md) | Which cases exist, in what order, and which CLI selector runs each one? |
| [Case catalogue](case-catalog.md) | Which protocol and field-report scenarios are covered, and where do they come from? |
| [Lab naming](lab-naming.md) | What do the lab, device and case names mean? |

## Plans and status

| Page | Answers |
| --- | --- |
| [Validation plan](validation-plan.md) | What must each lab prove, and on which RouterOS version? |
| [Status report](status-report.md) | Where is the campaign now, and what comes next? |
| [Two-site design](plans/two-site-design.md) | How should the two sites be wired and tested? |
| [Primary reboot plan](plans/primary-reboot-plan.md) | Why does losing the MLAG primary stop traffic longer while the pair is the STP root? |
| [Member failure diagnosis](plans/member-failure-diagnosis.md) | What else is needed to explain the client-link loss result? |
| [Report generation plan](plans/report-generation-plan.md) | How do runs write their own reports? |
| [RouterOS 7.26beta7 MLAG faults](plans/routeros-failures-report.md) | Which two RouterOS faults do the live runs show, and how do you reproduce them? |

## Reference

| Page | Answers |
| --- | --- |
| [Measurement](reference/measurement.md) | How is an outage measured, and when does it pass? |
| [Protocol cases](reference/protocol-cases.md) | Which forwarding, mobility, STP and LACP tests apply? |
| [Site cases](reference/site-cases.md) | Which site, hardware and optional-service tests apply? |
| [Topologies](reference/topologies.md) | Why these lab topologies, in this order? |
| [Research](reference/research.md) | Which sources and test methods back the plan? |
| [MLAG fixes](reference/mlag-fixes.md) | Which MikroTik changelog fixes does each test check, and which have no test? |

Results live in [results/](../results/), one dated folder per campaign. [Report template](../results/REPORT-TEMPLATE.md)
