# A test is a YAML file, and every limit carries its reason next to it

A test is one file in `tests/<lab>/cases/`, a list of steps with an action, a hold and a limit for each stream.
The expected state, the limits and the timing live in that file and in the lab file, not in code.
Running a test needs no AI and no judgement by a person.

Every limit and every hold has a comment next to the number that says where it comes from.
Limits come from protocol timers, not from a target.
For example, a reboot allows 5 s per host stream: three fast LACP intervals of 1 s plus 2 s for forwarding.
A stream that the fault does not touch, such as `client2-to-client3` in the Small cable test, gets 0 s.

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
