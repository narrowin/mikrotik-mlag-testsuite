"""Drive the two-pair topology: reset bridge priorities per setup and read both pairs' state."""

from contextlib import contextmanager

from .external_run import BridgeComparisonLab, observe_ports
from .root_run import RootLab
from .run import run
from .two_pair_evaluate import baseline_issues, bpdu_coverage
from .two_pair_topology import (
    SETUPS, TWO_PAIR_CAPTURES, TWO_PAIR_DEVICES, TWO_PAIR_FLOWS, TWO_PAIR_LAB, TWO_PAIR_LINKS,
    TWO_PAIR_NODES, TWO_PAIR_PORTS, TWO_PAIR_PROBES, TWO_PAIR_TARGETS, two_pair_lacp_strict, two_pair_mode, two_pair_setup,
)


# The inter-pair member flap also counts each CHR's bridge host table entries.
HOST_COUNT = (':put ("host-entries=" . [:len [/interface bridge host find]])',)


class TwoPairLab(BridgeComparisonLab):
    name = TWO_PAIR_LAB
    device_names = {**RootLab.device_names, **TWO_PAIR_DEVICES}
    peers = TWO_PAIR_NODES
    nodes = (*peers, "c1", "c2", "syslog")
    links = TWO_PAIR_LINKS
    ports = TWO_PAIR_PORTS
    captures = TWO_PAIR_CAPTURES
    flows = TWO_PAIR_FLOWS
    management_probes = TWO_PAIR_PROBES
    log_dir = "two-pair-logs"
    client1_probe_port = "bond0"
    count_hosts = False

    def read_router(self, peer):
        sequence = "mlag_two_pair_core_state" if peer in ("p1", "p2") else "mlag_two_pair_access_state"
        return observe_ports(self, peer, sequence, HOST_COUNT if self.count_hosts else ())

    def readiness(self):
        state = super().readiness()
        state["linux_client1"] = run(self.ns("c1", "cat", "/proc/net/bonding/bond0"))
        return state

    def case_target(self, name):
        return TWO_PAIR_TARGETS[name]

    def check_baseline(self, name, before, config, target):
        return baseline_issues(name, before, config)

    def check_wire(self, path, name, start, end):
        wire = bpdu_coverage(path, name, start, end)
        if wire["missing"] or wire["unexpected"]:
            return [f"Baseline BPDU coverage missing {wire['missing']}, unexpected {wire['unexpected']}"]
        return []

    @contextmanager
    def case_mode(self, name):
        self.count_hosts = name.endswith("-interpair-member-flap")
        priorities, mode, strict = SETUPS[two_pair_setup(name)], two_pair_mode(name), two_pair_lacp_strict(name)
        for node in self.peers:
            reply = self.ros(node, f"/interface bonding set [find where name=interpair] lacp-strict={strict}")
            if reply.strip():
                raise RuntimeError(f"{node}: setting lacp-strict={strict} on interpair returned {reply.strip()}")
        reset = self.reset_bridges({node: f"protocol-mode={mode} priority={value}" for node, value in priorities.items()})
        yield {**reset, "interpair_lacp_strict": strict}
