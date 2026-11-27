# Networka holds all test logic, and this repo holds only labs, tests and limits

On 2026-11-26 the operator decided that running a test, judging included, is one function of Networka (`nw test run` and `nw test replay`).
This repository holds only what describes the MLAG labs: the containerlab topology, the RouterOS startup config, the Networka inventory, the host script `host-setup.sh`, the lab file, the test files and their limits.
There is no Python test code in this repository for the labs under `tests/`.

## Why

The MLAG lab is one of several labs that need the same engine: a Cumulus lab for a colleague, the OT lab and others.
On 2026-11-26 the operator said: "The MLAG lab is one incarnation of many labs".
A new lab should need only a description of itself, not a copy of a runner.
The first port to Networka split the work: device state checks moved into Networka, while the judge, the pings and the captures stayed in this repository.
The operator rejected that split because half the logic lived in each repository.
Using Networka as a library from a local runner was dropped for the same reason.

## Considered options

- **The judge stays in this repository, Networka reads device state.** Rejected: it kept two places for one test.
- **Move the MLAG lab into Networka.** Rejected: the lab is one user of the engine, not part of it.
- **A large framework such as pyATS, Genie or NUTS.** Rejected as far more than needed. Networka keeps a fixed set of actions and checks (ping streams, state checks, captures, cable, reboot and power actions) and grows only when a test needs more.

## Consequences

A change to how a test is judged is a change in the Networka repository, released and then pinned here.
The lockfile pins Networka 0.5.1 from PyPI.
