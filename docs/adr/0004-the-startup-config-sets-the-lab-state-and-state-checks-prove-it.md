# The startup config sets the lab state, and state checks prove it

Networka pushes no configuration to a lab.
Each lab boots into the state its tests need from its RouterOS startup config, for example `protocol-mode=none` and `lacp-strict` on the bridge and bond.
The lab file lists state checks that Networka runs before a test, at its end, and after a reboot or power loss before the hold continues.
A test whose starting state does not pass is not run, and its verdict is ERROR, not FAIL.

These state checks replace the old before and after "checkpoint" abstraction and the old suite's reset over management SSH before each test.
This reverses the management reset approved on 2026-11-24.

## Why

The old suite changed bridge settings over SSH for each test, then read them back.
On 2026-11-26 the operator decided that configuration belongs to the lab, not to the test engine: "it should not be living in [Networka] to actually push config".
What a test needs is evidence that the lab is in the known state when it starts, and that it came back to that state.
A reset by commands can leave the lab in a state nobody wrote down; replaying the startup `.rsc` with `import` duplicates its `add` entries.
A check that reads the state proves the starting point without changing it.

## Considered options

- **Config push as a Networka feature.** Rejected: it makes the engine responsible for every vendor's configuration.
- **One startup config, changed per test over SSH.** Rejected: the state a test ran in would depend on the order of earlier tests.
- **Ansible in this repository.** Rejected as more than the MikroTik labs need. A lab that needs a playbook, such as the planned Cumulus lab, runs it from its own repository between deploy and `nw test run`.

## Consequences

A lab with different settings is its own folder, with its own name and management subnet.
`tests/two-pair-strict/` exists only because `lacp-strict=yes` must be set at boot; it reuses the two-pair startup config through a topology variable and links to the two-pair tests.
A test that leaves the lab broken shows up as an ERROR in the next test's starting state checks.
