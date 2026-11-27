# The run writes its report, and nobody writes verdicts or numbers by hand

Networka writes the report of every run ([Networka ADR 0007](https://narrowin.github.io/networka/adr/0007-the-run-writes-its-report-and-nobody-writes-verdicts-or-numbers-by-hand/)).
In this repository a verdict or a number in a lab README, a ticket or a forum post is quoted from a generated `report.md` or `result.json`, with the run, date, RouterOS and Networka versions.

## Why

On 2026-11-25 a ticket sent to MikroTik and a forum post carried hand-counted numbers that were wrong, and the operator said that cost the suite its credibility.

## Consequences

Lab READMEs carry verdict tables taken from `report.md` ([docs/tests/README.md](../tests/README.md), "Add a test", step 4).
That table is a quote, not a count; how numbers are quoted in write-ups is a working rule in [AGENTS.md](../../AGENTS.md), "Numbers in write-ups".
A replay rebuilds `report.md` byte for byte ([Networka ADR 0006](https://narrowin.github.io/networka/adr/0006-replay-judges-saved-evidence-again-and-must-give-a-byte-identical-result/)).

See also [Networka ADR 0007](https://narrowin.github.io/networka/adr/0007-the-run-writes-its-report-and-nobody-writes-verdicts-or-numbers-by-hand/).
