# Labs and tests under tests/

Each lab variant is one folder under `tests/`: [Small](../../tests/small/README.md), [Small with a mobile host](../../tests/small/mobile/README.md), [Medium](../../tests/medium/README.md), [Medium with two pairs](../../tests/medium/two-pair/README.md), [two pairs with lacp-strict](../../tests/medium/two-pair-strict/README.md) and [Large](../../tests/large/README.md).
Networka runs the tests. This repository holds only the labs, the test files and their limits.

## Layout

| File | Job |
| --- | --- |
| `topology.clab.yml` | Containerlab topology. It sets the lab name, its own management subnet, the pinned CHR image, the Linux hosts and the `syslog` collector node. |
| `switch.rsc` or `routeros.rsc` | RouterOS startup config for every CHR, with per-node branches on `.ShortName`. It brings the lab into the state the tests need, including spanning tree off and remote logging to the collector. |
| `devices.yml` | Networka inventory: device types and the lab logins. Containerlab supplies the addresses. |
| `lab.yaml` | Streams, state checks run before and after every test, and the collector file `syslog/switches.log`. |
| `*.yaml` | One test each. The `lab` field names the lab file. |
| `start.sh` | Builds the host image, creates the collector folder and deploys the lab. |
| `host-setup.sh` or `client-setup.sh` | Bonds, addresses and fixed neighbours of the Linux hosts. |
| `.gitignore` | Ignores `/clab-<name>/` in nested folders. The root `.gitignore` covers only `tests/*/clab-*/`. |
| `README.md` | Topology, tests, limits with their source, and live verdicts. |

All labs build the host image `small-mlag-client:local` from [tests/small/client.Dockerfile](../../tests/small/client.Dockerfile) and use the collector config [tests/small/rsyslog.conf](../../tests/small/rsyslog.conf).

## Run a lab

Live tests run in the OrbStack VM `mlag-external` (`orb -m mlag-external`), where the repository has the same path, and only with spanning tree off.
The host needs Docker, sudo, tcpdump, tshark, ping, nsenter and `tc` from iproute2.
Use Containerlab with native CHR support from commit `06ac3ca4d442ce4f937b50bd7c04d5f32fb3173b`. On the VM this is the qualified ARM64 build with SHA-256 `feac9ffc57b34ccb8f6793eedf7c13f85fe86c56632cfe6809b0fd068d495929`.
The lockfile pins Networka 0.5.1 from PyPI, and the VM-local uv environment keeps each checkout separate.

At most three labs with tests may run in the VM at once, counting the labs of other sessions. Check first what is running and deployed, and touch no lab you did not start.

```sh
pgrep -af "nw test|mlag-lab|campaign.sh"
sudo containerlab inspect --all
```

Run from the repository root. Each lab README gives `LAB`, `NAME` and `CONFIG`, and any argument its `start.sh` takes.

```sh
export PATH=/var/tmp/pt1-tools:$PATH  # uv 0.13.10
CLAB=/mnt/mac/tmp/containerlab-chr-06ac3ca4d.YXKSaT/containerlab
lab_nw() {
  sudo env "PATH=/usr/sbin:/sbin:$PATH" "UV_PROJECT_ENVIRONMENT=/var/tmp/mlag-lab-venvs$PWD" \
    uv run --locked nw "$@"
}
LAB=tests/small NAME=small-mlag CONFIG=tests/small/devices.yml CASE=bond-member-loss
sudo env "CLAB=$CLAB" "$LAB/start.sh"
mkdir -p test-results
RUN=$(mktemp -d test-results/run.XXXXXX)
lab_nw test run "$LAB/$CASE.yaml" --lab "$LAB/clab-$NAME" --config "$CONFIG" --save "$RUN"
lab_nw test replay "$RUN/$CASE"
sudo "$CLAB" destroy -t "$LAB/topology.clab.yml" --cleanup
```

`nw test run` exits 0 on pass, 1 on fail and 2 when the result is not verified. `nw test replay` judges the saved evidence again and exits 2 when the result differs from the saved `result.json`.

## Add a test

1. Copy the nearest test of the same lab and change the steps.
2. Write the reason for each limit and hold next to the number in the test file.
3. Run the test live and replay it. The replay must give byte-identical `result.json` and `report.md`.
4. Add the test with its limits to the lab README, and record the verdict from the generated `report.md` with the date, RouterOS and Networka versions and the number of runs.
5. Commit the files by path with a body that says why, what changed, how it was verified and what is not covered. Push to `main` only what has run live.

## Add a lab

1. Choose a new lab name and an unused management subnet `172.30.x.0/24`, with the collector at `.10`. The labs in use take 100, 101, 110, 111, 112 and 120.
2. Write the startup config with `protocol-mode=none` on every bridge. Copy the remote logging and the `refresh-collector` scheduler from [tests/small/switch.rsc](../../tests/small/switch.rsc) and set the collector address.
3. Write the topology links, `devices.yml`, the host setup and `lab.yaml`. In `lab.yaml`, check `stp_mode: none` on every bridge and MLAG connected on every peer.
4. Copy `start.sh` from [tests/medium/start.sh](../../tests/medium/start.sh) and set the collector folder to `clab-<name>/syslog`.
5. Add a `.gitignore` when the folder is nested, and a README in the shape of the other labs.

## Reference

The [Networka lab test guide](https://github.com/narrowin/networka/blob/main/docs/lab-tests.md) describes every lab and test field, every action, the evidence and the replay. State checks use the [Networka intent check format](https://github.com/narrowin/networka/blob/main/docs/intent.md).
