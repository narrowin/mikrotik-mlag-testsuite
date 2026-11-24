"""Capture points and flow IDs for the original small lab."""

CASES = ("calibrate", "mobile-move", "carrier", "silent-lacp", "peer-link-loss")
# Descriptive small-lab case names and the internal selector each one runs.
# Run folders use the descriptive name; attempt.json keeps the selector in "case".
CASE_NAMES = {
    "baseline": "direct-baseline",
    "calibration": "calibrate",
    "reboot-calibration": "direct-calibrate",
    "bond-member-loss": "carrier",
    "lacp-timeout": "silent-lacp",
    "mac-move": "mobile-move",
    "secondary-reboot": "direct-reboot-secondary",
    "primary-reboot": "direct-reboot-primary",
    "peer-link-loss": "peer-link-loss",
}
FLOWS = {
    101: ("c1-bond0", "mobile-bond0", "10.110.0.50", "client 1 to mobile"),
    102: ("c2-bond0", "mobile-bond0", "10.110.0.50", "client 2 to mobile"),
    201: ("mobile-bond0", "c1-bond0", "10.110.0.11", "mobile to client 1"),
    202: ("mobile-bond0", "c2-bond0", "10.110.0.12", "mobile to client 2"),
    301: ("c1-eth3", "c2-eth3", "198.51.100.2", "bypass forward"),
    302: ("c1-bond0", "c2-bond0", "10.110.0.12", "client 1 to client 2 on VLAN 110"),
    303: ("c2-eth3", "c1-eth3", "198.51.100.1", "bypass reverse"),
}
CAPTURES = tuple(sorted({p for flow in FLOWS.values() for p in flow[:2]} | {
    "c1-eth1", "c1-eth2", "p1-eth2", "p1-tap1", "p2-tap1", "p1-tap2", "p2-tap2",
    "p1-tap4", "p2-tap4",
}))
# The peer-link case adds both CHR TAPs toward client 2, so every MLAG bond member's LACPDUs are recorded.
PEER_LINK_CAPTURES = tuple(sorted((*CAPTURES, "p1-tap3", "p2-tap3")))
# Link monitors for the peer link (container eth1 behind RouterOS ether2) and both legs of each client bond.
PEER_LINK_PORTS = (("p1", "eth1"), ("p2", "eth1"), ("c1", "eth1"), ("c1", "eth2"), ("c2", "eth1"), ("c2", "eth2"))
CLIENT_MAC = "02:00:00:11:00:11"
MOBILE_MAC = "02:00:00:11:00:50"
NS = 1_000_000_000


def case_captures(name):
    return PEER_LINK_CAPTURES if name == "peer-link-loss" else CAPTURES


def case_name(selector):
    """Descriptive name for an internal selector; Medium and root selectors keep their own names."""
    return next((name for name, internal in CASE_NAMES.items() if internal == selector), selector)
