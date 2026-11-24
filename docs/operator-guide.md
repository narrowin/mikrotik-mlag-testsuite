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
| `01-CASE/captures/`, `state-*.jsonl`, `syslog.jsonl` | Can I verify that sequence against the packets and device observations? |

[Timing and acceptance rules](reference/measurement.md#provisional-pass-criteria) · [Worked packet reconstruction](../results/2026-11-24-small-lab/postmortem.md) · [Syslog configuration](syslog/README.md) · [Run in CI](test-framework.md#run-in-ci)

## Reboot the root pair

[Root-pair reboot wiring and fault target](cases/medium-core-reboot.md)

Use a dedicated ARM64 OrbStack VM with a local Docker daemon. Install Containerlab, uv, OpenSSH client, sshpass, iproute2 including `tc`, iputils, tcpdump and TShark. The root topology uses three CHRs, two Linux clients, and a separate syslog receiver on `172.30.216.20:1514`. A reboot is issued inside the selected RouterOS guest. The Linux veths, TAPs, captures and other guests stay up to observe it.

From the repository root in that VM, use the shared image from `labs/campaign-image.txt`. The example uses **7.26beta7**, the latest on 24 November 2026. Deploy once by digest and use that image for the full campaign. [MikroTik development releases](https://mikrotik.com/download/changelogs?channelFilter=development) · [Version policy](validation-plan.md#routeros-version-for-live-tests) · [Root topology](../labs/medium/medium-pair-root.clab.yml)

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

The runner sets RSTP on both CHRs before each direct-client case. It selects the reboot target from the observed MLAG election, verifies both client bonds are forwarding edge ports, and scores VLAN 110 and the bypass in both directions. The matching Small lab STP-off run is pending. Validate routed gateway ownership and service separately for BASE-05. [Small lab bridge-mode plan](validation-plan.md#small-lab-bridge-mode-comparison)

Use `--case direct-baseline` immediately before each original Small lab case. It performs the management reset and verifies the direct-client state and packet paths. Run the original selector only after the gate passes. Save each gate and fault under its own evidence directory.

## Run one campaign per machine

[`labs/campaign.sh`](../labs/campaign.sh) runs a list of suites on one lab inside one OrbStack machine. It copies `labs/` to the machine's own disk (`/var/tmp/mlag-labs`, or `MLAG_LABS_COPY`), because Containerlab writes `clab-<name>/` and the syslog feed next to the topology file. It deploys the lab from that copy with the image in `labs/campaign-image.txt` only if the lab is not running. It runs every suite with `--lab-dir` pointing at the copy and a machine-local `UV_PROJECT_ENVIRONMENT`. It never destroys a lab.

The runner accepts only a deployment whose topology file is the one under `--lab-dir`. If the lab in that machine was deployed from another path, for example the shared checkout, the script names that path and stops. Run against that deployment directly, or remove it yourself first.

Start one campaign per machine from the Mac, with one bridge mode per machine. Each suite spec is `<sub-folder>:<mlag-lab run arguments>`. Replace the machine names with your own.

```sh
cd ~/git/narrowin/mikrotik-mlag-testsuite
l2="--case calibration --case bond-member-loss --case lacp-timeout --case mac-move --case peer-link-loss"
campaign="test-results/$(date -u +%Y%m%dT%H%M%SZ)-parallel"
mkdir -p "$campaign"
for pair in rstp:mlag-lab-a none:mlag-lab-b mstp:mlag-lab-c; do
  mode=${pair%%:*} machine=${pair#*:}
  orb -m "$machine" labs/campaign.sh small "$campaign/$mode" "$mode-l2:--bridge-mode $mode $l2" \
    > "$campaign/$mode.log" 2>&1 &
done
wait
```

The script prints the start time, end time and exit code of each suite, and exits with the highest suite exit code. The safe number of labs at once is measured in package 3 of the [forwarding checks plan](plans/forwarding-checks-and-speed-plan.md#package-3-run-labs-in-parallel) and recorded here afterwards.

## Collect a Networka checkpoint

### Execute a command on the Medium lab

Use the [Medium lab Networka profile](../labs/networka/medium.yml) from the `mlag-external` OrbStack VM. This command executes RouterOS ICMP probes from each of the three CHRs to `dc1-traffic-host1` over the management VRF. Use the normal lab credentials and verify the CHRs' SSH host keys before running it.

```sh
uv run --locked --extra checkpoints nw --inventory-prefer config run \
  --config labs/networka/medium.yml --interactive-auth --store-results \
  --results-dir networka-results/dc1-management-ping dc1-routeros \
  '/ping address=172.30.218.16 vrf=mgmt count=3 interval=200ms'
```

Inspect every device's saved output for three sent, three received, and zero loss. Networka v0.2.0 can exit zero on a group run that contains failed devices. Check the per-device records and the printed counts. The scored baseline separately proves VLAN 110 and the bypass using probes from both Linux hosts.

### Collect both cores in the original small lab

Run Networka on the Linux lab host when you want a saved view of both peers before a fault, after recovery, or while a fault is held open. The checkpoint opens SSH sessions to both peers concurrently and runs eight read-only commands on each. The [sequence](../labs/networka/sequences/mikrotik_routeros/common.yml) records the guest carrier for the affected member, both bonds’ actor and partner flags, bridge and STP state, and where VLAN 110 learned client 1’s MAC. Continuous packet capture, persistent RouterOS polling and syslog supply the fault timeline.

From the repository root, enable the optional `checkpoints` extra in the same uv project as the runner. The lockfile records the GitHub release wheel and its digest. The verified release on 24 November 2026 was **v0.2.0**. [Networka releases](https://github.com/narrowin/networka/releases/latest)

```sh
uv sync --locked --extra checkpoints
uv run --locked --extra checkpoints nw --version
```

Verify both CHRs’ SSH host keys and add them to the collector’s known-hosts file before connecting. The [checkpoint profile](../labs/networka/small.yml) names the two management addresses explicitly. `--inventory-prefer config` selects those entries when Containerlab’s generated inventory also contains `p1` and `p2`. The command prompts for the lab credentials and stores a timestamped summary with separate command output files for each peer. Use a distinct results directory for each case, repeat and phase. [Networka CLI reference](https://github.com/narrowin/networka/blob/v0.2.0/docs/reference/cli.md)

```sh
uv run --locked --extra checkpoints nw --inventory-prefer config run \
  --config labs/networka/small.yml --interactive-auth --store-results \
  --results-dir networka-results/before mlag-peers mlag_small_state
```

**OrbStack verification.** Networka v0.2.0 completed all eight reads on both RouterOS 7.26beta7 peers in about **1.02 s**. Both reported `link-ok` on `ether3`, synchronized, collecting and distributing actor and partner flags on the two client bonds, connected MLAG, and the client 1 MAC on `client1` in VLAN 110. Inspect the per-peer command output before using a checkpoint. A preliminary config attempt sent an unresolved sequence name to RouterOS, and Networka marked the SSH command successful even though RouterOS returned a syntax error. The RouterOS sequence file included here was then verified on both peers.

## Check Markdown

Run the same linter used for this documentation pass from the repository root.

```sh
npx --yes markdownlint-cli2@0.24.2
```

The repository configuration checks project documentation and uses compact tables. Long lines are allowed for prose and link tables. [Documentation entry point](../README.md)
