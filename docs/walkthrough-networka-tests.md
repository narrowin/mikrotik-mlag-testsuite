# Walk through the Small MLAG tests

Use the [Small lab README](../tests/small/README.md) to start the lab, run and replay each test, and remove the lab when finished.

1. Run the cable test. Networka checks both switches and all six client bond members, then waits for a clean ping window. It takes each client1 cable down and brings it back.
2. Open `$RUN/bond-member-loss/report.md`. Compare each measured stop with its limit and find the switch's matching port message. The closing ping window and final state check show whether recovery held.
3. Run the reboot test and open `$RUN/switch-reboot/report.md`. The report names switch1, gives uptime before dispatch and after boot, and shows when the full lab passed its state checks again.
4. Replay each saved run. Networka rebuilds the report from the captures, switch log and device observations. It checks the recomputed result byte for byte against the saved `result.json`.

## Measured on 26 November 2026

The native launcher started Small in 52.161 s. A restart of the client1 container changed its process and network namespace, and both bond members recovered. Both cable runs and the named switch reboot passed and replay reproduced the saved result and report bytes. The README shows the [first cable return measurement](../tests/small/README.md#measured-cable-return).

| Action | Stream | Lost pings at one ping every 100 ms | Longest stop | Limit |
| --- | --- | --- | --- | --- |
| First run, switch2 cable down | client1 → client2 | 1 | 0 to 0.209 s | 1 s |
| Second run, switch2 cable down | client1 → client2 | 1 | 0 to 0.208 s | 1 s |
| Second run, switch2 cable back | client1 → client2 | 23 | 2.292 to 2.500 s | 4 s |
| Reboot switch1 | client1 → client2 | 0 | 0 s | 4 s |
| Reboot switch1 | client2 → client3 | 0 | 0 s | 4 s |

In both passing cable runs, client2 to client3 lost zero pings at one ping every 100 ms and saw a stop of 0 s. Client1 to client2 also measured zero lost pings at that cadence and a stop of 0 s when the switch1 cable went down and came back. Switch1 was secondary with 208 s of uptime. It reported 16 s at +22.667 s and all ten lab checks passed at +23.670 s, within the 60 s limit. Both switches delivered their end markers.

A manually down cable gave `fail` (1) before any cable action. The interface snapshots matched, and replay returned the same verdict. Stopping the collector caused a preflight `error` (2). Pausing the running collector produced a saved `error` (2) with four missing markers. Its replay matched after the collector resumed.

For raw evidence, follow the timed actions in `events.jsonl`, collector messages in `syslog.log` and saved device replies under `state-before/`, `state-after/` and `recovery/`.
