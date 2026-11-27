# Every run keeps the device syslog from one collector on the management network

Each lab has one collector node, `syslog`, running rsyslog at the fixed management address `.10` of the lab's subnet.
Every CHR sends its log there over UDP port 514 through the management VRF.
The collector writes one line per message with the UTC receive time, the switch name and the text.
How Networka keeps those lines with a run and proves them complete is [Networka ADR 0009](https://narrowin.github.io/networka/adr/0009-switch-logs-come-from-one-collector-and-markers-prove-they-are-complete/).

## Why

On 2026-11-24 the operator rejected an allowlist of device addresses, because a new device was dropped silently; the collector accepts what reaches it on the lab's own management network.

## Consequences

Every startup config names the collector's fixed address, and the collector runs a pinned rsyslog image.
The pinned rsyslog image restarts in a loop when its UDP input has no port, so `tests/shared/rsyslog.conf` sets `port="514"` explicitly.
RouterOS 7.26beta7 can leave remote logging silent after a reboot, so every startup config adds a `refresh-collector` scheduler that reselects the management VRF once its route is active.

See also [Networka ADR 0009](https://narrowin.github.io/networka/adr/0009-switch-logs-come-from-one-collector-and-markers-prove-they-are-complete/).
