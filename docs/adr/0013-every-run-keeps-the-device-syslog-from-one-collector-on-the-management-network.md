# Every run keeps the device syslog from one collector on the management network

Each lab has one collector node, `syslog`, running rsyslog at the fixed management address `.10` of the lab's subnet.
Every CHR sends its log there over UDP port 514 through the management VRF.
The collector writes one line per message with the UTC receive time, the switch name and the text.
Networka saves the lines of each run as `syslog.log`, checks the test's log rules against them, and writes start and end markers to prove the collector received the whole run.

## Why

An audit on 2026-11-26 advised removing the Small collector because no test read it, and the first clean build dropped it.
The operator reversed that the same day: "Where do you actually keep the syslog output of all the devices? It's also important."
The device logs are the evidence a person needs to understand a failure, and they are kept with every run.
The collector sits on the management network so that it keeps receiving from the surviving switches while the data plane is broken.
One collector per lab gives one ordered file, timed by one clock, instead of a log scraped from each switch after the run.
On 2026-11-24 the operator rejected an allowlist of device addresses, because a new device was dropped silently; the collector accepts what reaches it on the lab's own management network.

## Consequences

A lab needs an extra node with a pinned rsyslog image and a fixed address that every startup config names.
The pinned rsyslog image restarts in a loop when its UDP input has no port, so `tests/shared/rsyslog.conf` sets `port="514"` explicitly.
RouterOS 7.26beta7 can leave remote logging silent after a reboot, so every startup config adds a `refresh-collector` scheduler that reselects the management VRF once its route is active.
A stopped collector fails the run's preflight; a running collector that misses the markers gives ERROR for the log checks.
