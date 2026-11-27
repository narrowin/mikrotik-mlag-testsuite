**A per-pair bridge priority does not prevent the outage when the root pair's MLAG primary reboots.** With all pairs on `0x8000` and with the field priorities (pair A `0x2000`, pair B `0x4000`), the root moved to pair B and both VLAN 110 directions lost more than 16 s. Rebooting pair A's secondary lost nothing in either setup.

| Setup | Primary reboot: down / back | Root while CHR 1 was away | Secondary reboot |
| --- | --- | --- | --- |
| `equal`, all `0x8000` | 17.38–17.59 s / 6.71–6.92 s, one gap of 24.2 s | Pair B `0x8000.…:12` from +11.0 s to +23.3 s on CHR 3 and CHR 4 | no loss |
| `field`, A `0x2000`, B `0x4000` | 16.29–16.50 s / 4.60–4.81 s, one gap of 20.9 s | Pair B `0x4000.…:12` from +11.4 s to +22.3 s on CHR 3 and CHR 4 | no loss (rerun) |

**What happens, from the inter-pair captures and state samples.** Times are seconds from the start of the baseline:

1. Only pair A's primary sends BPDUs toward pair B. CHR 1's last one leaves at +5.0 s (equal) and +5.2 s (field), and CHR 1 stops answering at +6.6 s.
2. CHR 2 still reports `mlag-state: connected`, role secondary and bridge ID `…:11` while CHR 1 is away. It sends **no** BPDUs until CHR 1 is coming back (+23.3 s and +22.1 s). It never takes over as MLAG primary.
3. Pair B hears nothing from the root, so its root information expires. From +13.0 s and +13.2 s CHR 3 sends BPDUs with itself as root (`0x8000.…:12`, or `0x4000.…:12` with field priorities), and both pairs reconverge.
4. When CHR 1 returns, CHR 2 briefly sends its own ID `…:14`, then pair A's ID again. Pair B goes back to pair A as root.

**Why priority cannot help here.** A lower priority on pair A only wins while pair A is sending BPDUs. In this failure pair A is silent, so pair B has no better root to compare against. The per-pair priority still matters for a different failure: pairs that are all sending BPDUs and compare equal IDs. That is sirbryan's field report, and it was not reproduced here.

**Agreement with field.** field measured 12 s in each direction when CORE1_BR, the MLAG primary of the root pair, rebooted, against 1–2 s for every other core. That fits this mechanism.

**Spanning tree off is not enough with two pairs either, in this lab.** `stp-off/01-two-pair-stp-off-reboot-a-primary` lost 19.29–19.67 s while CHR 1 was away. The run is INVALID because host 2's sender paused once for 0.51 s, but that pause cannot explain a 19 s gap. No BPDU appeared, and the hosts' bonds and the FDB on every survivor were correct. The loss comes from CHR 3 (pair B primary):

1. CHR 3's member to CHR 1 lost its LACP partner: expired at +11.4 s, defaulted at +14.5 s, never collecting or distributing again until CHR 1 returned.
2. The virtual link kept carrier, and CHR 3 runs the default `lacp-strict=no`, which keeps a port without an LACP partner in use. CHR 3 kept sending host 1's traffic out that link toward the rebooting CHR 1, instead of over its peer link to CHR 4.
3. Every probe that host 1 hashed to CHR 3 was lost. That was both streams here, because each reply from host 1 also went through CHR 3.

A real switch drops carrier when it reboots, which would end this at once, so this part is partly a CHR artifact. It still applies to a switch that hangs with its links up. The candidate fix is `lacp-strict=yes` on the inter-pair bond, which has not been tested yet. The secondary reboot did not run, because the runner stops after an invalid run. `invalid-priority-gate-stp-off/` holds a first baseline that the runner's gate rejected because of a checker bug: RouterOS does not print the bridge priority with spanning tree off.

**Spanning tree off with two pairs.**

- `stp-off`, pair A primary reboot: lost 19.29–19.67 s while CHR 1 was away. The run is INVALID because host 2's sender paused once for 0.51 s, which cannot explain the gap. No BPDU appeared and the FDB was correct. CHR 3 (pair B primary) kept sending host 1's traffic into its member toward the rebooting CHR 1, after that member's LACP partner had expired (+11.4 s) and been defaulted (+14.5 s). The link kept carrier, and the default `lacp-strict=no` keeps such a port in use.
- `stp-off-strict`, the same with `lacp-strict=yes` on the inter-pair bond: going down lost 1.84–2.59 s, within the 5 s limit, so lacp-strict removes that blackhole. Coming back lost 16.13–16.65 s when CHR 1 rejoined. The run is INVALID because the lab VM was overloaded: state samples were more than 1.5 s apart and CHR 1's management window did not close cleanly. The return loss has not been explained yet.
- The secondary reboots did not run, because the runner stops after an invalid run.

So spanning tree off is not enough on its own with two pairs. With `lacp-strict=yes` the failure phase passes, but the return phase still fails. Both need a valid repeat on a quiet lab VM, and a check on real switches, which drop carrier when they reboot.

**Setup notes.**

- The peer link and the inter-pair bond use `edge=auto`, as field does. With `edge=no`, pair A's side stayed discarding: CHR 1 sent RSTP proposals every 2 s and pair B never answered. With `edge=auto`, pair A's side runs as an operational edge port.
- The first `field` secondary reboot (`field/01-two-pair-field-reboot-a-secondary`) is INVALID. CHR 2 rebooted, but the runner's SSH control socket went stale and every state read after the reboot failed with "Permission denied". The runner now clears a dead control socket before it reconnects, and the rerun in `field-secondary-rerun/` passed.
- Each setup ran once. A CHR reboot keeps the virtual links up, so pair A's secondary learns of the loss only through ICCP, which it did not act on during CHR 1's 16–17 s absence. A real switch drops carrier, which may change this. Repeat on hardware before relying on it.

[Case, wiring and commands](https://github.com/narrowin/mikrotik-mlag-testsuite/blob/95c7482/docs/cases/medium-two-pair-root.md) · [Field report](https://forum.mikrotik.com/t/mlag-between-crs326-24s-2q-rm-with-more-than-1-000-hosts-macs/269294) · [Only the primary sends BPDUs (EdPa)](https://forum.mikrotik.com/t/mlag-configuration-for-v7-22-1/269918)
