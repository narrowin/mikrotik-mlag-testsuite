# Walk through the Small MLAG tests

Use the [Small lab README](../tests/small/README.md) to start the lab, run and replay each test, and remove the lab when finished.

1. Run the cable test. Networka checks both switches and all six client bond members, then waits for a clean ping window. It takes each client1 cable down and brings it back.
2. Open `$RUN/bond-member-loss/report.md`. Compare each measured stop with its limit and find the switch's matching port message. The closing ping window and final state check show whether recovery held.
3. Run the reboot test and open `$RUN/switch-reboot/report.md`. The report names switch1, gives uptime before dispatch and after boot, and shows when the full lab passed its state checks again.
4. Replay each saved run. Networka rebuilds the report from the captures, switch log and device observations. It checks the recomputed result byte for byte against the saved `result.json`.

## Measured on 26 November 2026

These runs used the committed Small baseline before adopting the native CHR launcher. Both cable runs and the named reboot passed. Each replay reproduced the saved result and report bytes. The README shows the [first cable return measurement](../tests/small/README.md#measured-cable-return).

| Action | Stream | Lost pings at one ping every 100 ms | Longest stop | Limit |
| --- | --- | --- | --- | --- |
| First run, switch2 cable down | client1 → client2 | 1 | 0 to 0.206 s | 1 s |
| Second run, switch2 cable back | client1 → client2 | 24 | 2.399 to 2.603 s | 4 s |
| Reboot switch1 | client1 → client2 | 0 | 0 s | 4 s |
| Reboot switch1 | client2 → client3 | 10 | 0.670 to 0.896 s | 4 s |

The other cable measurements showed zero lost pings at one ping every 100 ms and a stop of 0 s. Before rebooting, switch1 was primary with 335 s of uptime. It reported 17 s of uptime at +23.762 s. All ten checks passed at +24.751 s, within the 60 s limit. Both switches delivered their end markers.

With a cable already down, the state check returned `fail` (1) before any cable action. Replay returned the same verdict and the captured interface states were identical before and after the run. Stopping the collector container gave a preflight `error` (2) without a run folder. Pausing the running collector gave a saved `error` (2) with four missing markers. Replay reproduced the error after the collector resumed.

For raw evidence, follow the timed actions in `events.jsonl`, collector messages in `syslog.log` and saved device replies under `state-before/`, `state-after/` and `recovery/`.
