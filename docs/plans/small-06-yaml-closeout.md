# SMALL-06 secondary reboot verification

The SMALL-06 test reads its [intent YAML](../../src/mlag_lab/intent/small.yaml), checks a clean baseline, reboots the elected secondary and measures both the disruption and recovery. Each attempt saves the exact YAML and the switch replies so the same checks can be replayed.

## Result on RouterOS 7.26beta7

Two fresh Small labs ran in parallel on the same image and both rebooted `dc1-core-mlag2` after a zero-loss baseline. Both client directions and the bypass stayed loss-free. Peer roles, LACP and bridge forwarding recovered in both runs.

| Mode | Verdict | Observation |
| --- | --- | --- |
| RSTP | Pass, 45 of 45 assertions | No flood frames returned to the sender. |
| Spanning tree off | Fail, 43 of 45 assertions | Broadcast and unknown-unicast probes with sequences `271`, `272` and `275` returned to the sender during withdrawal. |

The old and current evaluators produced identical existing result fields and timelines on eight complete attempts. The added report marked flood evidence in one older archive as unverified. Changing only the YAML withdrawal limit from five seconds to two on a saved run with a measured outage changed exactly the two client-direction assertions affected by that limit.

## Reproduce

Use two free disposable Small instances and the [parallel lab procedure](../operator-guide.md#run-suites-in-parallel). From the checkout root in the lab VM, with `out` set to a fresh output directory, run:

```sh
labs/parallel.sh --destroy \
  1 small "$out/stp-off" "run:--bridge-mode none --case direct-reboot-secondary" -- \
  2 small "$out/rstp" "run:--bridge-mode rstp --case direct-reboot-secondary"
```

Inspect `run/01-secondary-reboot/result.json` and its `secondary_reboot_intent` entries. A failing run retains the packet windows behind the failure. For full replay, keep the complete captures before pruning and run `uv run --locked mlag-lab evaluate PATH` on a copy. The original comparison captures and verification logs remain in the operator's local `test-results/small-06-proof/` directory.

Next work is tracked in the [suite YAML migration plan](suite-intent-yaml-migration.md).
