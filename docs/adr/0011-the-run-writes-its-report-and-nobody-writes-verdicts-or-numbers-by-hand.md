# The run writes its report, and nobody writes verdicts or numbers by hand

Every run writes `report.md` itself.
It starts with the verdict.
For every step and stream it shows the limit against the measured outage, the lost pings with the ping interval and the time they stand for, the log rules with the matching syslog line, and a timeline in words.
Machine data stays in `result.json`, `events.jsonl` and `syslog.log`.
A verdict or a number in a lab README, a ticket or a forum post is quoted from a generated `report.md` or `result.json`, with the run, date, RouterOS and Networka versions.

## Why

On 2026-11-24 reports were written by hand after the runs.
They drifted from MikroTik's terms and lacked the expected behaviour, so a reader could not tell a PASS from a FAIL.
On 2026-11-25 a ticket sent to MikroTik and a forum post carried hand-counted numbers that were wrong, and the operator said that cost the suite its credibility.
He said: "the tooling should actually write all those numbers. They should be measured during a test."
On 2026-11-26 the old `timeline.tsv` was replaced by the report, because it was not readable by a person.

## Considered options

- **A hand-written README per campaign.** Rejected: the numbers in it are not traceable to a run.
- **`timeline.tsv` as the human view.** Rejected as unreadable.

## Consequences

The report wording lives in Networka, so a change to it is a Networka release.
A replay rebuilds `report.md` byte for byte ([ADR 0010](0010-replay-judges-a-saved-run-again-and-must-give-a-byte-identical-result.md)).
Lab READMEs still carry verdict tables, copied from `report.md` by the author ([docs/tests/README.md](../tests/README.md), "Add a test", step 4).
That copy is a quote, not a count; how numbers are quoted in write-ups is a working rule in [AGENTS.md](../../AGENTS.md), "Numbers in write-ups".
