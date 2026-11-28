# Labs and tests under tests/

Each lab is one folder under `tests/`: [Small](../../tests/small/README.md), [Small with a MAC-move host](../../tests/small-mac-move/README.md), [Medium](../../tests/medium/README.md), [Two-pair](../../tests/two-pair/README.md), [Two-pair strict](../../tests/two-pair-strict/README.md), [Small strict](../../tests/small-strict/README.md) and [Large](../../tests/large/README.md), each with spanning tree off. Three labs repeat a base lab with RSTP and the MLAG pair as root: [Small RSTP](../../tests/small-rstp/README.md), [Medium RSTP](../../tests/medium-rstp/README.md) and [Two-pair RSTP](../../tests/two-pair-rstp/README.md). [Medium RSTP with the access switch as root](../../tests/medium-rstp-access-root/README.md) repeats Medium with a switch outside the pair as root.
Networka runs the tests. This repository holds only the labs, the test files and their limits.

Numerical limits are local acceptance criteria with their reason beside them; a protocol detection interval is not automatically an end-to-end outage maximum. See [the limit rationale](../adr/0003-a-test-is-a-yaml-file-and-every-limit-carries-its-reason-next-to-it.md). MAC ageing and whole-site power loss deliberately interrupt hosts. The pinned Networka revision shows their combined interruption allowances separately from MAC relearning and power recovery, retaining every numerical limit and verdict check. Passing intentional interruptions do not compete with failover outages in the results summary; confirmed breaches remain visible.

## Layout

| File | Job |
| --- | --- |
| `README.md` | Topology, tests, limits with their source, and live verdicts. |
| `lab/topology.clab.yml` | Containerlab topology. It sets the lab name, its own management subnet, the pinned CHR image, the Linux hosts and the `syslog` collector node. |
| `lab/switch.rsc` or `lab/routeros.rsc` | RouterOS startup config for every CHR, with per-node branches on `.ShortName`. It brings the lab into the state the tests need, including the spanning tree mode and remote logging to the collector. |
| `lab/devices.yml` | Networka inventory: device types and the lab logins. Containerlab supplies the addresses. |
| `lab/host-setup.sh` | Bonds, addresses and fixed neighbours of the Linux hosts. Containerlab runs it once per host at deploy. Its last line, `touch /run/host-setup.done`, tells `start.sh` the setup finished. |
| `lab/lab.yaml` | Streams, state checks run before and after every test, and the collector file `syslog/switches.log`. The MAC-move lab has two lab files, `direct-lab.yaml` and `link-lab.yaml`. |
| `tests/*.yaml` | One test each. The `lab` field names the lab file relative to the test file, for example `../lab/lab.yaml`. |

Containerlab writes the running lab to `lab/clab-<name>/`, which the root `.gitignore` ignores.
Two-pair strict, Small strict and the MAC-move lab use some files of another lab, as their READMEs say.

Every lab uses the files in [tests/shared](../../tests/shared): the [Dockerfile](../../tests/shared/host.Dockerfile) of the host image, the collector config [rsyslog.conf](../../tests/shared/rsyslog.conf) and [start.sh](../../tests/shared/start.sh).
`tests/shared/start.sh <lab-folder> [age]` builds the host image `mlag-host:local`, creates the collector folder and deploys the lab. It returns once every Linux host has finished its host setup and its bond is up, or fails after 60 s and names the host. Only the MAC-move lab takes the `age` profile.

## Run a lab

Live tests run in the OrbStack VM `mlag-external` (`orb -m mlag-external`), where the repository has the same path.
The host needs Docker, sudo, tcpdump, tshark, ping, nsenter and `tc` from iproute2.
`tests/shared/containerlab` selects our published ARM64/AMD64 client, verifies its SHA-256 and caches it. Every topology uses the public CHR tc image pinned by digest. The installed containerlab is unchanged.
The lockfile pins the bundled Networka `0.5.2+chr.5` source artifact, which supports tc NIC discovery, delayed-queue cleanup and prompt impairment recovery checks. [Provenance and patch](../../vendor/README.md). Historical saved runs retain their original engine versions.

Check first what is running and deployed, and touch no lab you did not start.

```sh
pgrep -af "nw test"
sudo containerlab inspect --all
```

Run from the repository root. Each lab README gives `LAB`, `NAME` and `CONFIG`, and the start profile if the lab has one.

```sh
export PATH=/var/tmp/pt1-tools:$PATH  # uv 0.13.10
CLAB="$PWD/tests/shared/containerlab"
lab_nw() {
  sudo env "PATH=/usr/sbin:/sbin:$PATH" "UV_PROJECT_ENVIRONMENT=/var/tmp/mlag-lab-venvs$PWD" \
    uv run --locked nw "$@"
}
LAB=tests/small NAME=small-mlag CONFIG=tests/small/lab/devices.yml TEST=bond-member-loss
sudo tests/shared/start.sh "$LAB"
mkdir -p test-results
RUN=$(mktemp -d test-results/run.XXXXXX)
lab_nw test run "$LAB/tests/$TEST.yaml" --lab "$LAB/lab/clab-$NAME" --config "$CONFIG" --save "$RUN"
lab_nw test replay "$RUN/$TEST"
sudo "$CLAB" destroy -t "$LAB/lab/topology.clab.yml" --cleanup
```

`nw test run` exits 0 on pass, 1 on fail and 2 when the result is not verified. `nw test replay` judges the saved evidence again and exits 2 when the result differs from the saved `result.json`.

## Add a test

A test is a list of steps. This step from [tests/medium/tests/primary-reboot.yaml](../../tests/medium/tests/primary-reboot.yaml) reboots switch1, waits up to 60 s for the lab state checks to pass again, keeps measuring for 16 s and allows each host stream to stop for at most 5 s.

```yaml
  - name: Reboot switch1
    action:
      reboot: switch1
    # Allow boot and LACP recovery, plus the CHR SSH cooldown if it refuses an early login.
    recovery_deadline_s: 60
    # Continue through the post-boot observation, beyond five fast LACP timeouts.
    hold_s: 16
    max_outage_s:
      host1-to-host2: &reboot-limit 5  # Three fast LACP intervals plus two for forwarding.
      host2-to-host1: *reboot-limit
```

1. Copy the nearest test in the lab's `tests/` folder and change the steps.
2. Write the reason for each limit and hold next to the number in the test file.
3. Run the test live and replay it. The replay must give byte-identical `result.json` and `report.md`.
4. Add the test with its limits to the lab README, and record the verdict from the generated `report.md` with the date, RouterOS and Networka versions and the number of runs.
5. Commit the files by path with a body that says why, what changed, how it was verified and what is not covered. Push to `main` only what has run live.

## Add a lab

1. Choose a new lab name and an unused management subnet `172.30.x.0/24`, with the collector at `.10`. The labs in use take 100, 101, 102, 103, 110, 111, 112, 113, 114, 115 and 120.
2. Create the folder `tests/<lab>/` with the subfolders `lab/` and `tests/`.
3. Write the startup config in `lab/` with `protocol-mode=none` on every bridge. Copy the remote logging and the `refresh-collector` scheduler from [tests/small/lab/switch.rsc](../../tests/small/lab/switch.rsc) and set the collector address.
4. Write the topology, `devices.yml`, `host-setup.sh` and `lab.yaml` in `lab/`. The topology binds the collector config as `../../shared/rsyslog.conf`. In `lab.yaml`, check `stp_mode: none` on every bridge and MLAG connected on every peer.
5. Start the lab with `tests/shared/start.sh tests/<lab>`. The script reads the lab name from the topology.
6. Add a README in the shape of the other labs.

## Reference

The [Networka lab test guide](https://narrowin.github.io/networka/lab-tests/) describes every lab and test field, every action, the evidence and the replay. State checks use the [Networka intent check format](https://narrowin.github.io/networka/intent/).
