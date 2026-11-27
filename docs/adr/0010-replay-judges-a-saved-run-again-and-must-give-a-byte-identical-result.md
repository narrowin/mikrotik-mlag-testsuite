---
status: superseded by Networka ADR 0006, https://github.com/narrowin/networka/blob/main/docs/adr/0006-replay-judges-saved-evidence-again-and-must-give-a-byte-identical-result.md
---

# Replay judges a saved run again and must give a byte-identical result

Every run saves the evidence needed to judge it again with the lab offline: the test and lab files as run, the device replies of every state check, the capture slices the judge kept, `events.jsonl` and the device syslog.
Today Networka still keeps the full captures, not only slices ([ADR 0012](0012-a-run-keeps-only-the-capture-slices-that-prove-its-verdict-and-captures-are-never-published.md)).
`nw test replay` judges that evidence again, writes `report.md` again and compares the new `result.json` byte for byte with the saved one.
It exits 2 on any difference, even when the verdict word is the same.

## Why

A verdict is only as good as the evidence behind it, and nobody can rerun a past lab state.
Replay shows which expectation decided a verdict, and it lets a change to the judge be checked against every saved run without a lab.
During the port to Networka, replay showed that the old and new judges agree on the same evidence, and it ran negative checks such as forcing `forwarding: false` in a saved reply.

## Consequences

The judge must be deterministic: no timestamps of its own in `result.json` or `report.md`, and a fixed order everywhere.
Whatever a run keeps must be enough for replay to reach the same result.
How a change is shown to work with a live run and its replay is in [docs/tests/README.md](../tests/README.md), "Add a test".
