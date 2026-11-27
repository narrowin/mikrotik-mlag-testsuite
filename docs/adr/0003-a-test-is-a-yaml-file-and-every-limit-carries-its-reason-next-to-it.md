# A test is a YAML file, and every limit carries its reason next to it

A test is one file in `tests/<lab>/tests/`, a list of steps with an action, a hold and a limit for each stream.
The expected state, the limits and the timing live in that file and in the lab file, not in code.
Running a test needs no AI and no judgement by a person.

Every limit and every hold has a comment next to the number that says where it comes from.
Limits are local acceptance criteria, informed by configured protocol timers where those timers apply.
For example, the retained 5 s reboot limit is a local availability requirement. Its original rationale was three fast LACP intervals of 1 s plus 2 s for forwarding; neither IEEE LACP nor MikroTik documents that sum as a universal MLAG outage maximum.
A stream that the fault does not touch, such as `host2-to-host3` in the Small cable test, gets 0 s.

The documentation audit of 27 November 2026 distinguished detection, attachment, deliberate downtime and measured interruption. The [MikroTik bridge reference](https://manual.mikrotik.com/docs/cli-reference/interface/bridge/) documents a warning after three missed MLAG heartbeat intervals; saved lab state shows an interval of 5 s. That warning is not a forwarding deadline. The [MLAG guide](https://manual.mikrotik.com/docs/high-availability-solutions/multi-chassis-link-aggregation-group/) also describes LACP system-ID changes and renegotiation on rejoin without promising a numerical outage maximum. The audit corrects the rationale without changing any numerical outage limit.

The 4 s VRRP failover limit is informed by the actual 1 s advertisement interval and backup priority 100: the down interval is 3.609375 s under [RFC 9568, section 6.1](https://www.rfc-editor.org/rfc/rfc9568.html#section-6.1), rounded up with a local margin. Keeping 4 s for return/preemption is a separate local acceptance criterion; the abrupt-failover calculation does not establish a return outage bound.

MAC ageing's 26 s and site power loss's 216 s include intentional downtime. Reports retain these combined interruption limits and show the existing 1 s MAC relearning limit and 180 s power recovery deadline separately. An intentional interruption within its allowance does not compete with failover outages in the results summary; a breach remains visible.

## Why

On 2026-11-25 the expected state was spread over Python runners and several files, and the operator asked why it was not in one place.
A proposal to keep YAML optional was rejected; the operator answered that YAML is how the intent is described.
He added: "running the tests shouldn't need AI, right?"
Earlier, on 2026-11-24, limits of 1 s had appeared with no source.
The operator asked: "Where did you actually get these timers?"
He set the bounds: under 3 s is acceptable, sub-second is better, 10 or 30 s is not, and limits must not be so strict that they fail on normal protocol behaviour.
A number without its reason looks arbitrary, and the next reader tightens or loosens it without knowing what it protects.

## Consequences

A limit set from a timer can hide a regression below it.
An earlier 3 s limit for a bond member losing carrier would have passed a loss 14 times the 0.217 s the old runs measured, so the Small cable test now allows 1 s for carrier loss and keeps LACP timing for the return.
Whether the cable return limit stays at 4 s, against the 2.399 to 2.610 s measured on 2026-11-26, is still open.

See also [Networka ADR 0002](https://narrowin.github.io/networka/adr/0002-a-test-is-a-yaml-file-of-exact-values-and-running-it-needs-no-ai/).
