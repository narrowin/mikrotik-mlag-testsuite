# Operator guide

## How one fault turns into a report

1. On the selected topology, verify MLAG roles, active bond members and ordinary service. Start numbered probes in both directions at 100 ms and keep a separate client-to-client bypass running.
2. Change one thing. Mark the fault and its restoration on the host clock. Keep packet captures and management polling running on the surviving devices. RouterOS sends bridge, STP and interface logs to a management-side UDP receiver on port 1514.
3. Follow a missed sequence from source to destination and back. Packet captures show where the frame went. LACP flags, spanning-tree port state and the MAC table explain which ports were eligible at that time.
4. Read each direction and phase separately. The first and last missed sends bound the minimum outage. The surrounding successful sends bound the maximum. If the interval straddles the target, the measurement cannot decide that threshold.

| Open in the run directory | What it answers |
| --- | --- |
| `suite.json` or `junit.xml` | Which attempts passed, failed, or have insufficient evidence? |
| `01-CASE/result.json` | Which client lost traffic, for how long, and which assertion failed? |
| `01-CASE/timeline.tsv` | What changed just before the first packet was lost or delivered again? |
| `01-CASE/proof.tar.gz` (failed runs), `state-*.jsonl`, `syslog.jsonl` | Can I verify that sequence against the packets and device observations? |

[Timing and acceptance rules](reference/measurement.md#provisional-pass-criteria) · [Worked packet reconstruction](../results/2026-11-24-small-lab/postmortem.md) · [Syslog configuration](syslog/README.md) · [Run in CI](test-framework.md#run-in-ci)

## Reboot the root pair

[Root-pair reboot wiring and fault target](cases/medium-core-reboot.md)

Use a dedicated ARM64 OrbStack VM with a local Docker daemon. Install Containerlab, uv, OpenSSH client, iproute2 including `tc`, iputils, tcpdump and TShark. The root topology uses three CHRs, two Linux clients, and a separate syslog receiver on `172.30.216.20:1514` (instance N adds 10·N to the third octet). A reboot is issued inside the selected RouterOS guest. The Linux veths, TAPs, captures and other guests stay up to observe it.

From the repository root in that VM, use the shared image from `labs/campaign-image.txt`. The example uses **7.26beta7**, the latest on 24 November 2026. Deploy once by digest and use that image for the full campaign. [MikroTik development releases](https://mikrotik.com/download/changelogs?channelFilter=development) · [Version policy](validation-plan.md#routeros-version-for-live-tests) · [Root topology](../labs/medium/medium-pair-root.clab.yml)

These commands deploy instance 0 from the checkout. To run beside other labs or sessions in the same VM, use [Run suites in parallel](#run-suites-in-parallel).

```sh
chr=$(cat labs/campaign-image.txt)
sudo docker pull "$chr"
sudo docker pull rsyslog/rsyslog:latest
sudo docker build --pull --no-cache -f labs/shared/client.Dockerfile -t mlag-lab-endpoint:local labs/shared
syslog=$(sudo docker image inspect --format '{{index .RepoDigests 0}}' rsyslog/rsyslog:latest)
sudo env MLAG_CHR_IMAGE="$chr" MLAG_SYSLOG_IMAGE="$syslog" containerlab deploy -t labs/medium/medium-pair-root.clab.yml
```

Export `MLAG_SSH_PASSWORD` for the deployment credentials. For a checkout shared between macOS and Linux, set `UV_PROJECT_ENVIRONMENT` to a Linux-only path. Ensure sudo can resolve `uv` and the system administrative binary directories.

```sh
export UV_PROJECT_ENVIRONMENT=/var/tmp/mlag-validation-venv
sudo env "PATH=$PATH:/usr/sbin:/sbin" "UV_PROJECT_ENVIRONMENT=$UV_PROJECT_ENVIRONMENT" uv sync --locked
sudo --preserve-env=MLAG_SSH_PASSWORD env "PATH=$PATH:/usr/sbin:/sbin" \
  "UV_PROJECT_ENVIRONMENT=$UV_PROJECT_ENVIRONMENT" uv run --locked mlag-lab run \
  --case root-calibrate --case reboot-secondary --case reboot-primary --repeat 2 \
  --output "test-results/root-$(date -u +%Y%m%dT%H%M%SZ)"
```

On the first build, run `root-calibrate` and `reboot-secondary` in that order. Review the control before adding `reboot-primary`. The runner checks the shared root, expected roles, forwarding access-switch uplink, both LACP bonds and stable baseline delivery before applying a fault. It records the boot from uptime reset, management ICMP, and independent state and carrier on the surviving nodes. Replay a copied suite or attempt using `uv run --locked mlag-lab evaluate PATH`.

After scoring each attempt, the runner keeps only the proof. A failed run gets `01-CASE/proof.tar.gz`: every capture cut to 1 s around each piece of evidence behind a failed check, such as a loss gap over its limit, a frame looped back to its sender or the start of the failed phase. In the archive, `proof.json` lists each window with its reasons in seconds from the baseline and in UTC, `pcap.sha256` checks the cut captures and `source.sha256` lists the full captures. Attach the archive to a ticket or bug report as it is. The runner then deletes `captures/`, `probes/` and `links/` of every run, whether it passed, failed or errored. `result.json`, `timeline.tsv`, the configs, state, syslog and events stay. `uv run --locked mlag-lab prune PATH` does the same for saved runs that still have captures.

A pruned run cannot be replayed: `mlag-lab evaluate` and `mlag-lab verify` keep its saved verdict. To check an evaluator change against a pruned run, rerun the case. `uv run --locked mlag-lab verify results` replays every run that still has packet captures, lists each run whose verdict or checks changed against its `result.json`, and exits 1 if any changed. It rewrites the result files in place, so run it on a copy of `results/`. `--jobs` defaults to 4 so that live labs on the same host keep their pacing.

Open `result.json` for the missed sequence ranges, per-phase lower and upper bounds, and the count of successful probes during confirmed guest absence. `timeline.tsv` aligns the root BPDUs, per-port RouterOS state, LACP, ICCP, FDB transitions, timed carrier snapshots and UDP syslog with the missing traffic. The role attached to each reboot comes from the verified election. The 5 s service target applies separately to the loss and return phases. [CI verdicts and artifacts](test-framework.md#run-in-ci)

The independent routers must deliver both UDP markers. If the rebooted guest misses its ending marker, the result records the gap and the runner tries to rebind that guest's logging action after the observation closes. A late marker proves only that collection recovered at that point. Use guest uptime and the TAP captures to bound the reboot itself.

The clients pin their two VLAN 110 neighbor entries so they keep emitting unicast probes when ARP cannot traverse the failed path. The two-port Linux data bridges forward the virtual cables with MAC learning disabled. RouterOS still learns client MACs in VLAN 110. [Measured ARP, spanning-tree and virtual cable findings](../results/2026-11-24-medium-lab-pair-root/README.md)

Use `--case primary-sustained-stop` when a guest reboot ends before you can observe recovery on the absent-primary path. QMP stops and resumes guest execution while the veths and TAPs stay up. Use `--case reboot-primary-no-fallback` for the paired `mlag-lacp-fallback=no` experiment. That case records and restores the original setting.

## Deploy the three-CHR Medium lab

Use the `mlag-external` OrbStack VM and [Medium lab inventory](../labs/medium/README.md). Deploy from the repository root using the pinned CHR image, the local endpoint image and the syslog image used in the pair-root procedure. An existing five-CHR deployment must be replaced before running the revised cases.

```sh
chr=$(cat labs/campaign-image.txt)
sudo docker pull "$chr"
sudo docker pull rsyslog/rsyslog:latest
sudo docker build -f labs/shared/client.Dockerfile -t mlag-lab-endpoint:local labs/shared
syslog=$(sudo docker image inspect --format '{{index .RepoDigests 0}}' rsyslog/rsyslog:latest)
sudo env MLAG_CHR_IMAGE="$chr" MLAG_SYSLOG_IMAGE="$syslog" containerlab deploy -t labs/medium/medium.clab.yml
```

## Introduce RSTP after the all-bridges-off run

From the repository root, run the three modes on the same wiring. The access switch remains on both cores throughout. Each attempt checks guest uptime, bridge configuration and a loss-free packet baseline through the normal data path. A failed baseline withholds the faults for that mode.

```sh
launch_mlag() {
  sudo --preserve-env=MLAG_SSH_PASSWORD env "PATH=$PATH:/usr/sbin:/sbin" \
    "UV_PROJECT_ENVIRONMENT=$UV_PROJECT_ENVIRONMENT" uv run --locked mlag-lab run "$@"
}

run_dir="/var/tmp/mlag-medium-$(date -u +%Y%m%dT%H%M%SZ)"
for mode in stp-off pair-root access-root; do
  if launch_mlag --case "medium-${mode}-baseline" --output "$run_dir/${mode}-baseline"; then
    launch_mlag --case "medium-${mode}-calibrate" \
      --case "medium-${mode}-reboot-secondary" --case "medium-${mode}-reboot-primary" \
      --repeat 2 --output "$run_dir/${mode}-faults"
  fi
done
```

[Preflight assertions and scoring](test-framework.md#compare-forwarding-with-and-without-spanning-tree) · [Whole-pair restart plan](validation-plan.md#both-dc1-cores-down-and-return) · [Archived five-CHR results](cases/medium-spanning-tree.md#archived-diagnostics)

## Reboot the direct-client pair

Deploy [`small.clab.yml`](../labs/small/small.clab.yml) with the pinned campaign image. Both client LAGs terminate on Linux hosts, the core client ports are configured as edge ports, and the mobile endpoint is active-backup. There is no downstream switch in the scored client path. From the lab VM, use transparent virtual cables and pin the two scored neighbors.

```sh
for node in dc1-core-mlag1 dc1-core-mlag2; do
  sudo docker exec "clab-mlag-small-$node" /bin/sh /lab/forward-control.sh --wire
done
sudo docker exec clab-mlag-small-dc1-traffic-host1 ip neigh replace 10.110.0.12 \
  lladdr 02:00:00:11:00:12 nud permanent dev bond0
sudo docker exec clab-mlag-small-dc1-traffic-host2 ip neigh replace 10.110.0.11 \
  lladdr 02:00:00:11:00:11 nud permanent dev bond0

sudo --preserve-env=MLAG_SSH_PASSWORD env "PATH=$PATH:/usr/sbin:/sbin" \
  "UV_PROJECT_ENVIRONMENT=$UV_PROJECT_ENVIRONMENT" uv run --locked mlag-lab run \
  --case direct-calibrate --case direct-reboot-secondary --case direct-reboot-primary \
  --repeat 2 --output /var/tmp/mlag-direct-reboots
```

The container names are those of instance 0. For instance N, use `clab-mlag-small-i<N>-` and run the runner with `MLAG_INSTANCE=<N>` and `--lab-dir` set to that instance's copy.

The runner sets RSTP on both CHRs before each direct-client case. It selects the reboot target from the observed MLAG election, verifies both client bonds are forwarding edge ports, and scores VLAN 110 and the bypass in both directions. The matching Small lab STP-off run is pending. Validate routed gateway ownership and service separately for BASE-05. [Small lab bridge-mode plan](validation-plan.md#small-lab-bridge-mode-comparison)

Use `--case direct-baseline` immediately before each original Small lab case. It performs the management reset and verifies the direct-client state and packet paths. Run the original selector only after the gate passes. Save each gate and fault under its own evidence directory.

## Run suites in parallel

Independent suites run at the same time in one OrbStack VM, each on its own lab instance. [`labs/parallel.sh`](../labs/parallel.sh) starts one [`labs/campaign.sh`](../labs/campaign.sh) campaign per instance, waits for all of them and prints one verdict per campaign. Run suites one after another only when they need the same lab instance.

### Lab instances

`MLAG_INSTANCE` selects the instance, 0 to 3, default 0. Instance 0 is the lab as named in its topology. Instance N differs from it in four places:

- Name: the Containerlab name is `<deployment>-i<N>`, for example `mlag-small-i2`, and Docker names start with `clab-mlag-small-i2-`.
- Subnet: the third octet of the management subnet is the base octet plus 10·N, so Small instance 2 is `172.30.235.0/27`.
- Lab copy: the lab runs from `<MLAG_LABS_COPY>-i<N>`, by default `/var/tmp/mlag-labs-i<N>`. Instance 0 runs from `/var/tmp/mlag-labs`.
- Syslog: the instance has its own collector at `.20` in its subnet. In the copy, the RouterOS startup configs send syslog to that collector; the Medium and Large configs also use the instance addresses as source.

| Lab | `campaign.sh` lab | Deployment | Third octet, instances 0 to 3 |
| --- | --- | --- | --- |
| Small | `small` | `mlag-small` | 215, 225, 235, 245 |
| Medium, pair-root variant | `medium-pair-root` | `mlag-medium-pair-root` | 216, 226, 236, 246 |
| Medium | `medium` | `mlag-medium` | 218, 228, 238, 248 |
| Medium, two-pair variant | `medium-two-pair` | `mlag-medium-two-pair` | 219, 229, 239, 249 |

The runner reads `MLAG_INSTANCE`, uses that instance's lab name and management addresses, and records the instance in each `attempt.json`. `mlag-lab evaluate` and `mlag-lab verify` use the recorded instance. The Large lab has no runner cases and no `campaign.sh` support.

`campaign.sh` syncs the copy from the checkout only while no lab is deployed from it. A copy that a running lab uses stays as it was deployed. Different labs at the same instance share one copy, so their deploys run one after the other; their suites then run at the same time.

### Run several suites at once

Run `parallel.sh` inside the VM from the checkout root. First check that no other campaign or run is active and which labs are deployed:

```sh
pgrep -af "mlag-lab|campaign.sh"
sudo containerlab inspect --all
```

Each campaign is `<instance> <lab> <campaign dir> <suite spec>...`, and `--` separates campaigns. A suite spec is `<sub-folder>:<mlag-lab run arguments>`, as for `campaign.sh`. `--destroy` comes first and applies to every campaign:

```sh
labs/parallel.sh --destroy \
  1 small /var/tmp/c-small-1 "baseline:--bridge-mode none --case baseline" -- \
  2 small /var/tmp/c-small-2 "baseline:--bridge-mode none --case baseline" -- \
  3 medium /var/tmp/c-medium-3 "stp-off:--case medium-stp-off-baseline"
```

- Instances: each campaign takes instance 0, 1, 2 or 3. `parallel.sh` refuses two campaigns on the same lab instance or the same campaign folder.
- Removal: with `--destroy`, each campaign removes the lab it deployed when it exits, also after a failure. A lab that was already running stays up. Without `--destroy`, every lab stays up.
- Existing labs: if the instance is already deployed from its copy, the campaign uses it as it is. If it is deployed from another folder, the campaign stops with exit 2 and names that folder.
- Environment: `MLAG_SSH_PASSWORD`, `MLAG_LABS_COPY` and `UV_PROJECT_ENVIRONMENT` pass through to every campaign. The default environment is `/var/tmp/mlag-campaign-venv-<uid>`.
- Sudo: the campaigns run in the background and call `sudo`, so `sudo` must not ask for a password.

### Results and exit status

Each campaign writes its console output to `<campaign dir>/console.log`. The log holds the sync, the deploy, and one `=== <suite> start` and `=== <suite> end ... exit <N>` line per suite. Each suite writes its results to `<campaign dir>/<sub-folder>/`, with `suite.json`, `junit.xml` and one folder per attempt.

`parallel.sh` prints one `Started instance` line per campaign with its PID and console log. When all campaigns have ended, it prints one line per campaign:

```text
PASS instance 1 small: exit 0, results /var/tmp/c-small-1
FAIL instance 3 medium: exit 1, results /var/tmp/c-medium-3
```

A campaign exits with the highest exit code of its suites. It exits 2 when it stops before the suites, for example on a wrong argument, a lab deployed from another folder or a container that does not become healthy. `parallel.sh` exits 0 when every campaign exits 0 and 1 when any campaign fails. It exits 2 on a usage error, before it starts any campaign.

### Deploy and remove an instance by hand

`campaign.sh` does these steps itself. Use them only to keep an instance up for manual work. The copy needs the same syslog rewrite for every lab, because another lab at the same instance may later deploy from it without a new sync. Example for Small instance 2, from the checkout root in the VM:

```sh
n=2
copy=/var/tmp/mlag-labs-i$n
mkdir -p "$copy"
tar -C labs --exclude='clab-*' --exclude='*logs' -cf - . | tar -C "$copy" -xf -
for config in small/small.rsc:215 medium/medium-pair-root.rsc:216 medium/medium.rsc:218 \
    medium/medium-two-pair.rsc:219 large/large.rsc:220; do
  base=${config#*:}
  sed -i "s/172\.30\.$base\./172.30.$((base + 10 * n))./g" "$copy/${config%:*}"
done
mkdir -p "$copy/small/logs" "$copy/medium/logs" "$copy/medium/pair-root-logs" "$copy/medium/two-pair-logs"
chr=$(cat labs/campaign-image.txt)
sudo docker pull rsyslog/rsyslog:latest
syslog=$(sudo docker image inspect --format '{{index .RepoDigests 0}}' rsyslog/rsyslog:latest)
sudo env MLAG_LAB_NAME=mlag-small-i2 MLAG_MGMT_NET=235 MLAG_CHR_IMAGE="$chr" MLAG_SYSLOG_IMAGE="$syslog" \
  containerlab deploy -t "$copy/small/small.clab.yml"
```

Do this only while no lab is deployed from the copy. Wait until every container with a health check is healthy. For Small, wire the virtual cables and pin the probe neighbors with the instance's container names, as in [Reboot the direct-client pair](#reboot-the-direct-client-pair):

```sh
for node in dc1-core-mlag1 dc1-core-mlag2; do
  sudo docker exec "clab-mlag-small-i2-$node" /bin/sh /lab/forward-control.sh --wire
done
sudo docker exec clab-mlag-small-i2-dc1-traffic-host1 ip neigh replace 10.110.0.12 \
  lladdr 02:00:00:11:00:12 nud permanent dev bond0
sudo docker exec clab-mlag-small-i2-dc1-traffic-host2 ip neigh replace 10.110.0.11 \
  lladdr 02:00:00:11:00:11 nud permanent dev bond0
```

Run the runner with `MLAG_INSTANCE` and `--lab-dir` pointing at the copy:

```sh
sudo --preserve-env=MLAG_SSH_PASSWORD env "PATH=$PATH:/usr/sbin:/sbin" MLAG_INSTANCE=2 \
  "UV_PROJECT_ENVIRONMENT=$UV_PROJECT_ENVIRONMENT" uv run --locked mlag-lab run \
  --lab-dir /var/tmp/mlag-labs-i2 --bridge-mode none --case baseline --output /var/tmp/mlag-small-i2-baseline
```

Remove the instance with the same variables, through `sudo env`. Never use `containerlab destroy --name`: Containerlab then reads the topology without the variables and removes another lab.

```sh
sudo env MLAG_LAB_NAME=mlag-small-i2 MLAG_MGMT_NET=235 \
  containerlab destroy -t /var/tmp/mlag-labs-i2/small/small.clab.yml --cleanup
```

### Effect of parallel load

Measured on 25 November 2026 in `mlag-external` (13 CPUs, 31 GB), with RouterOS 7.26beta7 and spanning tree off. The target was Small instance 1 with `baseline`, `primary-power-loss` and `bond-member-loss`. The other labs ran the same suite, and Medium ran `medium-stp-off-baseline` and `medium-stp-off-power-loss-primary`. All suites of a level started together. The idle lab `mlag-medium` of another session was up during every level.

| Labs with cases | State read median / p95, ms | Poll period median / max, ms | Largest probe gap, ms (gaps over 150 ms) | CPU busy median / max, % |
| --- | --- | --- | --- | --- |
| 1 Small (3 runs) | 107–132 / 121–156 | 351 / 355 | 114 (0) | 11–14 / 21 |
| 2 Small (2 runs) | 111–136 / 123–193 | 351 / 387 | 135 (0) | 20–21 / 34 |
| 3 Small (1 run) | 118 / 135 | 351 / 355 | 113 (0) | 26 / 43 |
| 3 Small and Medium, first run | 125 / 150 | 351 / 359 | 122 (0) | 30 / 49 |
| 3 Small and Medium, second run | 131 / 184 | 351 / 666 | 508 (17) | 33 / 53 |

Verdicts did not change with load. The only failed checks at any level were the flood checks 501 and 502. They also failed in single runs without load, so load did not cause them. No loss came near its limit of 5 s for power loss and 3 s for a bond member. Wall time stayed at 90–95 s for baseline plus power loss.

Run at most 3 labs with cases in the VM at once, counting labs of other sessions. At four labs, the second run stalled the probe senders of all three Small labs at the same moment during the bond member restoration, and once during the CHR boots of the power loss. A fourth lab with cases therefore distorts the timing of reboot, power-loss and bond member cases. The cause of the stalls is not known; the CPU was 47–68 % idle at those moments.

### Several sessions in one VM

- Check `pgrep -af "mlag-lab|campaign.sh"` and `sudo containerlab inspect --all` before you start.
- Never use instance 0 of a lab that another session has deployed. Pick an instance that no running lab uses.
- Give each checkout its own `UV_PROJECT_ENVIRONMENT` and `MLAG_LABS_COPY`. The lab copy default is the same for every checkout and the environment default depends only on the user, so a second checkout would re-sync the same environment to its own code and could run from the other checkout's lab copy.
- Destroy only the labs you deployed, with the variables they were deployed with.

## Collect a Networka checkpoint

Networka (`nw`) saves a read-only view of each selected CHR before a fault, while a fault is held open, or after recovery. Operators run the checkpoint CLI separately. The runner uses the Networka SDK for RouterOS command reads. Continuous packet capture, persistent RouterOS polling and syslog supply the fault timeline.

### Install Networka

The runner and checkpoint CLI use **Networka 0.4.1** at the git commit that `pyproject.toml` pins, with its device-state intent layer, and require Python 3.15 or later. `uv sync --locked` installs that commit into the project environment; the lockfile records it. [Networka](https://github.com/narrowin/networka)

```sh
uv sync --locked
uv run --locked nw --version
```

### Profiles and intent files for each lab

Each lab has a profile that names its management addresses and device groups. The device state the runner requires is Networka intent in [src/mlag_lab/intent/state/](../src/mlag_lab/intent/state): one file per lab and one per setup. The runner copies the lab's profile and every intent file into each run's `inputs/` folder. The runner reads the bonds of the traffic hosts (`hosts.yaml`, `host2.yaml`) itself through `nsenter`.

Every Linux lab node runs an SSH server on its management address, because Networka reaches every node over SSH. The login is `root` with the lab password `admin`, because only root sees the LACP details in `/proc/net/bonding`. The profiles list these nodes as `device_type: linux` in the `linux-hosts` group, which holds that login. The SSH server does not listen on the traffic interfaces or bonds.

| Lab | Profile | Intent files |
| --- | --- | --- |
| Small | [small.yml](../labs/networka/small.yml) | `direct.yaml` and `direct-<bridge mode>.yaml` |
| Medium | [medium.yml](../labs/networka/medium.yml) | `medium.yaml` and `medium-<setup>.yaml` |
| Medium, pair-root variant | [medium-pair-root.yml](../labs/networka/medium-pair-root.yml) | `root.yaml` |
| Medium, two-pair variant | [medium-two-pair.yml](../labs/networka/medium-two-pair.yml) | `two-pair.yaml` and `two-pair-<setup>.yaml` |
| Large | [large.yml](../labs/networka/large.yml) | None yet: the Large lab is not deployed and the runner has no Large cases. |

The Medium profiles also have a `dc1-routeros` group with every CHR in the lab. The Large profile has `dc1-routeros` and `dc2-routeros` groups with every CHR at each site, and one group per pair, such as `dc1-core-peers`.

### Run a checkpoint

Run Networka on the host that runs the lab. The profiles in the checkout hold the addresses of instance 0. A campaign's labs copy holds them at the addresses of its instance, under `networka/` in `MLAG_LABS_COPY`. `--interactive-auth` gives one login to every device, so use it only for intent files without Linux nodes. For the CHRs together with Linux nodes, set `NW_USER_DEFAULT=admin` and `NW_PASSWORD_DEFAULT` to the CHR password instead. Local campaign runs use the `mlag-external` OrbStack VM. Verify each CHR's SSH host key and add it to the collector's known-hosts file before connecting. The command prompts for the lab credentials, prints each item's verdict, and saves the intent, evidence and results. Use a distinct folder for each case, repeat and phase. The exit status is 0 for pass, 1 for fail and 2 when an item could not be verified. [Networka intent guide](https://github.com/narrowin/networka/blob/main/docs/intent.md)

```sh
uv run --locked nw intent run --config labs/networka/small.yml --interactive-auth \
  --save networka-results/before src/mlag_lab/intent/state/direct.yaml
uv run --locked nw intent replay networka-results/before
```

A saved gate of any attempt replays the same way, without the lab:

```sh
uv run --locked nw intent replay test-results/link-isolation/01-baseline/gate-baseline
```

**v0.4.1 verification.** In a fresh locked environment on `mlag-external`, the installed SDK loaded the Medium profile and read native bridge-port statistics and monitor JSON over SSH. It observed `forwarding: true` on both core `access-uplink` ports and on the access switch's `uplink`. The prior verified lab host keys were used for these reads.

### Execute a command on the Medium lab

This command executes RouterOS ICMP probes from each of the three CHRs to `dc1-traffic-host1` over the management VRF.

```sh
uv run --locked nw --inventory-prefer config run \
  --config labs/networka/medium.yml --interactive-auth --store-results \
  --results-dir networka-results/dc1-management-ping dc1-routeros \
  '/ping address=172.30.218.16 vrf=mgmt count=3 interval=200ms'
```

Inspect every device's saved output for three sent, three received, and zero loss. The scored baseline separately proves VLAN 110 and the bypass using probes from both Linux hosts.

## Check Markdown

Run the same linter used for this documentation pass from the repository root.

```sh
npx --yes markdownlint-cli2@0.24.2
```

The repository configuration checks project documentation and uses compact tables. Long lines are allowed for prose and link tables. [Documentation entry point](../README.md)
