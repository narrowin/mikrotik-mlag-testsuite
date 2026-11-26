# Small MLAG lab

The lab is two MikroTik CHR switches, `switch1` and `switch2`, joined by a peer link and running MLAG with spanning tree off.
Three Linux clients, `client1` to `client3`, each have one cable to each switch, bonded with LACP.
A collector node, `syslog`, receives the log of both switches.

## Commands

Run from the repository root on a Linux host with Docker, sudo, tcpdump, tshark, ping and nsenter. Put uv 0.13.10 on `PATH` (`export PATH=/var/tmp/pt1-tools:$PATH` on the lab VM).
This repository's lockfile pins Networka 0.5.0 from PyPI.

Use Containerlab with native CHR support from commit `06ac3ca4d442ce4f937b50bd7c04d5f32fb3173b`. Set `CLAB` to the absolute path of that binary. On the lab VM, use the qualified ARM64 build. Its SHA-256 is `feac9ffc57b34ccb8f6793eedf7c13f85fe86c56632cfe6809b0fd068d495929`.

```sh
CLAB=/mnt/mac/tmp/containerlab-chr-06ac3ca4d.YXKSaT/containerlab
sudo env "CLAB=$CLAB" tests/small/start.sh
```

In the same shell, use a VM-local uv environment for this checkout.

```sh
lab_nw() {
  sudo env "PATH=/usr/sbin:/sbin:$PATH" "UV_PROJECT_ENVIRONMENT=/var/tmp/mlag-lab-venvs$PWD" \
    uv run --locked nw "$@"
}
```

Choose the cable test or the reboot of switch1 in its current MLAG role. The two test files give the per-stream limits and their reasons. [Cable test](bond-member-loss.yaml) · [Reboot test](switch-reboot.yaml)

```sh
CASE=bond-member-loss
```

For a reboot run, use `CASE=switch-reboot`. Run this block for each attempt.

```sh
mkdir -p test-results/small
RUN=$(mktemp -d test-results/small/run.XXXXXX)
lab_nw test run "tests/small/$CASE.yaml" \
  --lab tests/small/clab-small-mlag --config tests/small/devices.yml --save "$RUN"
```

Replay the saved run, then remove the lab when finished.

```sh
lab_nw test replay "$RUN/$CASE"
sudo "$CLAB" destroy -t tests/small/topology.clab.yml --cleanup
```

The [Networka lab test guide](https://github.com/narrowin/networka/blob/main/docs/lab-tests.md) explains the evidence and replay.

## Additional Small cases

Cable delay and sustained one-way loss use the same topology and require `tc` from iproute2 on the host.
For these cases, use the source-checkout command in the mobile guide with the canonical YAML and lab path above.
The mobile setup adds an active-backup host and an independent bypass for the thirteen historical cases.

[Cable delay](cable-delay.yaml) · [Sustained cable loss](cable-packet-loss.yaml) · [Mobile Small guide](mobile/README.md)

## Measured cable return

On 26 November 2026, in the first committed native CHR cable run, client1 to client2 lost 24 pings at one ping every 100 ms when the cable to switch2 came back. The measured stop was 2.399 to 2.610 s, within its 4 s limit. [Walkthrough](../../docs/walkthrough-networka-tests.md)
