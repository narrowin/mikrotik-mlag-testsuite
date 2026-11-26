# Small MLAG with a mobile host

Both switches run with spanning tree off. Switch1 is configured as MLAG primary and switch2 as secondary. Client1 and client2 have dual LACP links and a direct cable between them. Client3 uses an active-backup bond with the same MAC on either link.

## Run a case

Run from the repository root with host `tc` from iproute2. The pinned Networka 0.5.1 runs every case. [Small host tools and qualified Containerlab build](../README.md)

```sh
CASE=baseline
PROFILE=
AGE=5m
if [ "$CASE" = mac-age-relearn ]; then
  PROFILE=age
  AGE=10s
fi
sudo env "CLAB=$CLAB" tests/small/mobile/start.sh ${PROFILE:+$PROFILE}

lab_nw() {
  sudo env "PATH=/usr/sbin:/sbin:$PATH" "UV_PROJECT_ENVIRONMENT=/var/tmp/mlag-lab-venvs$PWD" \
    uv run --locked nw "$@"
}

mkdir -p test-results/small
RUN=$(mktemp -d test-results/small/mobile.XXXXXX)
lab_nw test run "tests/small/mobile/$CASE.yaml" \
  --lab tests/small/mobile/clab-small-mlag-mobile --config tests/small/devices.yml --save "$RUN"
lab_nw test replay "$RUN/$CASE"
sudo env "SMALL_MOBILE_AGE=$AGE" "$CLAB" destroy -t tests/small/mobile/topology.clab.yml --cleanup
```

Use the default profile for every case except MAC ageing. Its dedicated profile starts both switches at ten seconds of ageing and pins the necessary client neighbours. Teardown discards the profile. The case itself clears both egress filters.

## Cases

| Case | Traffic and evidence |
| --- | --- |
| [Baseline](baseline.yaml) | Switch forwarding, peer carrier, both client bonds and both directions on the independent bypass. |
| [Calibration](calibration.yaml), [reboot calibration](reboot-calibration.yaml) | Two-second one-way bypass cut with seven or four observed streams. |
| [Single member](bond-member-loss.yaml), [repeated member flaps](member-flap-repeat.yaml) | Client1 cable to switch1, once for eight seconds or five times for one second each. The repeated case samples unrelated bridge host entries on both switches. |
| [Peer link](peer-link-loss.yaml) | Fifteen-second cut at both switches, with MLAG and RouterOS carrier checks. |
| [LACP timeout](lacp-timeout.yaml) | Eight seconds without client1 LACPDUs to switch1, with carrier, local timeout flags and restored partner flags checked. |
| [Primary reboot](primary-reboot.yaml), [secondary reboot](secondary-reboot.yaml) | Checked role, native uptime reset and loss-free bypass. The secondary case also checks for returned broadcast and unknown-unicast probes on both sender members. |
| [Primary power loss](primary-power-loss.yaml), [secondary power loss](secondary-power-loss.yaml) | Twenty seconds off, neighbour carrier withdrawal and a new boot. |
| [MAC move](mac-move.yaml), [MAC age and relearn](mac-age-relearn.yaml) | Host table state, switch TAP packet evidence and delivery on all seven streams. |

## Observation limits

The cable cases record switch log events and state samples. Precise guest carrier deadlines, withdrawn member TAP observations and per-port LACP frame histories remain open. The secondary reboot checks baseline flood copies at client2. The historical receiver checks also watched the mobile host.
