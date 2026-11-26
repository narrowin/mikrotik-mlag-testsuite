# Small MLAG lab

The lab is two MikroTik CHR switches, `switch1` and `switch2`, joined by a peer link and running MLAG with spanning tree off.
Three Linux clients, `client1` to `client3`, each have one cable to each switch, bonded with LACP.
A collector node, `syslog`, receives the log of both switches.

## Commands

Run from the repository root on a Linux host with Docker, containerlab and sudo. Set `NETWORKA` to the absolute path of the Networka checkout. Put uv 0.13.10 on `PATH` (`export PATH=/var/tmp/pt1-tools:$PATH` on the lab VM).

```sh
sudo tests/small/start.sh
```

In the same shell, use a VM-local uv environment for this checkout.

```sh
lab_nw() {
  sudo env "PATH=$PATH" "UV_PROJECT_ENVIRONMENT=/var/tmp/networka-venvs$PWD" \
    uv run --locked --project "$NETWORKA" nw "$@"
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
sudo containerlab destroy -t tests/small/topology.clab.yml --cleanup
```

The [Networka lab test guide](https://github.com/narrowin/networka/blob/main/docs/lab-tests.md) explains the evidence and replay.
