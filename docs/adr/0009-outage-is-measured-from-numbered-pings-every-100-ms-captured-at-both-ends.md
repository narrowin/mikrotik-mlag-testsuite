---
status: superseded by Networka ADR 0005, https://github.com/narrowin/networka/blob/main/docs/adr/0005-outage-is-measured-from-numbered-pings-every-100-ms-captured-at-both-ends.md
---

# Outage is measured from numbered pings every 100 ms, captured at both ends

Every stream in a lab file sends one numbered ICMP ping every 100 ms, and Networka captures it at both ends.
Every limit in the test files is written for this cadence.
Missing evidence is never PASS: a step whose outage cannot be decided from the captures is ERROR.
How Networka bounds an outage and when it rejects a measurement are Networka's design, described in its [lab test guide](https://github.com/narrowin/networka/blob/main/docs/lab-tests.md).

## Why

A short ping summary, such as five pings before and after a fault, misses an outage that ends between them, and it misses a failure on only one hash path.
A 100 ms interval resolves outages well under one second, which the limits in [ADR 0003](0003-a-test-is-a-yaml-file-and-every-limit-carries-its-reason-next-to-it.md) need.
Capturing at both ends tells which direction lost the ping.

## Considered options

- **IRTT or another sequenced UDP stream.** Not used: numbered ICMP captured at both ends already gives the direction and the timing, and it also reaches a switch or VRRP address that cannot run a server for it.
- **mtr or traceroute for timing.** Rejected: they show the path, not when forwarding stopped.

## Consequences

Changing the interval means recalibrating every limit.
A report gives lost pings together with the interval and the time they stand for.
