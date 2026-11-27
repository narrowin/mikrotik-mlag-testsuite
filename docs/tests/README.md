# Labs and tests under tests/

Each lab is one folder under `tests/`: [Small](../../tests/small/README.md), [Small with a mobile host](../../tests/small-mobile/README.md), [Medium](../../tests/medium/README.md), [Medium with two pairs](../../tests/medium-two-pair/README.md), [two pairs with lacp-strict](../../tests/medium-two-pair-strict/README.md) and [Large](../../tests/large/README.md), each with spanning tree off. Three labs repeat a base lab with RSTP and the MLAG pair as root: [Small RSTP](../../tests/small-rstp/README.md), [Medium RSTP](../../tests/medium-rstp/README.md) and [two pairs RSTP](../../tests/medium-two-pair-rstp/README.md).
Networka runs the tests. This repository holds only the labs, the test files and their limits.

## Layout

| File | Job |
| --- | --- |
| `README.md` | Topology, tests, limits with their source, and live verdicts. |
| `lab/topology.clab.yml` | Containerlab topology. It sets the lab name, its own management subnet, the pinned CHR image, the Linux hosts and the `syslog` collector node. |
| `lab/switch.rsc` or `lab/routeros.rsc` | RouterOS startup config for every CHR, with per-node branches on `.ShortName`. It brings the lab into the state the tests need, including the spanning tree mode and remote logging to the collector. |
| `lab/devices.yml` | Networka inventory: device types and the lab logins. Containerlab supplies the addresses. |
| `lab/host-setup.sh` | Bonds, addresses and fixed neighbours of the Linux hosts. Containerlab runs it once per host at deploy. Its last line, `touch /run/host-setup.done`, tells `start.sh` the setup finished. |
| `lab/lab.yaml` | Streams, state checks run before and after every test, and the collector file `syslog/switches.log`. Small-mobile has two lab files, `direct-lab.yaml` and `link-lab.yaml`. |
| `cases/*.yaml` | One test each. The `lab` field names the lab file relative to the test file, for example `../lab/lab.yaml`. |

Containerlab writes the running lab to `lab/clab-<name>/`, which the root `.gitignore` ignores.
Medium-two-pair-strict and small-mobile use some files of another lab, as their READMEs say.

Every lab uses the files in [tests/shared](../../tests/shared): the [Dockerfile](../../tests/shared/client.Dockerfile) of the host image, the collector config [rsyslog.conf](../../tests/shared/rsyslog.conf) and [start.sh](../../tests/shared/start.sh).
`tests/shared/start.sh <lab-folder> [age]` builds the host image `small-mlag-client:local`, creates the collector folder and deploys the lab. It returns once every Linux host has finished its host setup and its bond is up, or fails after 60 s and names the host. Only small-mobile takes the `age` profile.

## Run a lab

Live tests run in the OrbStack VM `mlag-external` (`orb -m mlag-external`), where the repository has the same path.
The host needs Docker, sudo, tcpdump, tshark, ping, nsenter and `tc` from iproute2.
Use Containerlab with native CHR support from commit `06ac3ca4d442ce4f937b50bd7c04d5f32fb3173b`. On the VM this is the qualified ARM64 build with SHA-256 `feac9ffc57b34ccb8f6793eedf7c13f85fe86c56632cfe6809b0fd068d495929`.
The lockfile pins Networka 0.5.2 from PyPI, and the VM-local uv environment keeps each checkout separate. The release wheel and source archive are also kept in the Networka checkout's `dist/` folder.

At most three labs with tests may run in the VM at once, counting the labs of other sessions. Check first what is running and deployed, and touch no lab you did not start.

```sh
pgrep -af "nw test"
sudo containerlab inspect --all
```

Run from the repository root. Each lab README gives `LAB`, `NAME` and `CONFIG`, and the start profile if the lab has one.

```sh
export PATH=/var/tmp/pt1-tools:$PATH  # uv 0.13.10
CLAB=/mnt/mac/tmp/containerlab-chr-06ac3ca4d.YXKSaT/containerlab
lab_nw() {
  sudo env "PATH=/usr/sbin:/sbin:$PATH" "UV_PROJECT_ENVIRONMENT=/var/tmp/mlag-lab-venvs$PWD" \
    uv run --locked nw "$@"
}
LAB=tests/small NAME=small-mlag CONFIG=tests/small/lab/devices.yml CASE=bond-member-loss
sudo env "CLAB=$CLAB" tests/shared/start.sh "$LAB"
mkdir -p test-results
RUN=$(mktemp -d test-results/run.XXXXXX)
lab_nw test run "$LAB/cases/$CASE.yaml" --lab "$LAB/lab/clab-$NAME" --config "$CONFIG" --save "$RUN"
lab_nw test replay "$RUN/$CASE"
sudo "$CLAB" destroy -t "$LAB/lab/topology.clab.yml" --cleanup
```

`nw test run` exits 0 on pass, 1 on fail and 2 when the result is not verified. `nw test replay` judges the saved evidence again and exits 2 when the result differs from the saved `result.json`.

## Add a test

A test is a list of steps. This step from [tests/medium/cases/primary-reboot.yaml](../../tests/medium/cases/primary-reboot.yaml) reboots switch1, waits up to 60 s for the lab state checks to pass again, keeps measuring for 16 s and allows each host stream to stop for at most 5 s.

```yaml
  - name: Reboot switch1
    action:
      reboot: switch1
    # Allow boot and LACP recovery, plus the CHR SSH cooldown if it refuses an early login.
    wait_healthy_s: 60
    # Continue through the post-boot observation, beyond five fast LACP timeouts.
    hold_s: 16
    max_outage_s:
      host1-to-host2: &reboot-limit 5  # Three fast LACP intervals plus two for forwarding.
      host2-to-host1: *reboot-limit
```

1. Copy the nearest test in the lab's `cases/` folder and change the steps.
2. Write the reason for each limit and hold next to the number in the test file.
3. Run the test live and replay it. The replay must give byte-identical `result.json` and `report.md`.
4. Add the test with its limits to the lab README, and record the verdict from the generated `report.md` with the date, RouterOS and Networka versions and the number of runs.
5. Commit the files by path with a body that says why, what changed, how it was verified and what is not covered. Push to `main` only what has run live.

## Add a lab

1. Choose a new lab name and an unused management subnet `172.30.x.0/24`, with the collector at `.10`. The labs in use take 100, 101, 102, 110, 111, 112, 113, 114 and 120.
2. Create the folder `tests/<lab>/` with the subfolders `lab/` and `cases/`.
3. Write the startup config in `lab/` with `protocol-mode=none` on every bridge. Copy the remote logging and the `refresh-collector` scheduler from [tests/small/lab/switch.rsc](../../tests/small/lab/switch.rsc) and set the collector address.
4. Write the topology, `devices.yml`, `host-setup.sh` and `lab.yaml` in `lab/`. The topology binds the collector config as `../../shared/rsyslog.conf`. In `lab.yaml`, check `stp_mode: none` on every bridge and MLAG connected on every peer.
5. Start the lab with `tests/shared/start.sh tests/<lab>`. The script reads the lab name from the topology.
6. Add a README in the shape of the other labs.

## Reference

The [Networka lab test guide](https://github.com/narrowin/networka/blob/main/docs/lab-tests.md) describes every lab and test field, every action, the evidence and the replay. State checks use the [Networka intent check format](https://github.com/narrowin/networka/blob/main/docs/intent.md).
