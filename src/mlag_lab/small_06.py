"""The SMALL-06 rules that no other case field holds: fault timing, switch and client state, flood streams."""

from dataclasses import dataclass
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, model_validator

from .direct_topology import DIRECT_FLOOD_FLOWS, DIRECT_NODES

Seconds = Annotated[float, Field(strict=True, gt=0, allow_inf_nan=False)]
Names = Annotated[tuple[str, ...], Field(min_length=1)]
Streams = Annotated[tuple[PositiveInt, ...], Field(min_length=1)]


@dataclass(frozen=True)
class BridgePortIntent:
    node: str
    bridge: str
    port: str
    forwarding: bool

    @property
    def target(self):
        return f"{self.node}:{self.bridge}/{self.port}"


class IntentSection(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Reboot(IntentSection):
    reboot_role: Literal["secondary"]
    surviving_role: Literal["primary"]
    require_uptime_reset: Literal[True]
    baseline_seconds: Seconds
    observe_after_boot_seconds: Seconds
    recovery_seconds: Seconds


class BridgeForwarding(IntentSection):
    bridge: str
    ports: Names
    forwarding: Annotated[bool, Field(strict=True)]


class RouterLacp(IntentSection):
    members: Names
    actor_and_partner_flags: Annotated[str, Field(pattern=r"^[S-][C-][D-]$")]


class ClientLacp(IntentSection):
    members: dict[Literal["c1", "c2"], Names]
    carrier: Annotated[bool, Field(strict=True)]
    eligible: Annotated[bool, Field(strict=True)]


class ExpectedState(IntentSection):
    peers: Names
    mlag_state: Literal["connected"]
    bridge_forwarding: BridgeForwarding
    router_lacp: RouterLacp
    client_lacp: ClientLacp


class Traffic(IntentSection):
    loss_free_baseline: Literal[True]
    recovery_consecutive_replies: PositiveInt
    no_sender_return_streams: Streams

    @property
    def recovery_count_label(self):
        return "ten" if self.recovery_consecutive_replies == 10 else str(self.recovery_consecutive_replies)


class Small06Intent(IntentSection):
    fault: Reboot
    expected_state: ExpectedState
    traffic: Traffic

    @model_validator(mode="after")
    def check_names(self):
        state, traffic = self.expected_state, self.traffic
        if set(state.peers) != DIRECT_NODES.keys() or len(state.peers) != len(DIRECT_NODES):
            raise ValueError("peers must name both Small switches once")
        if set(state.client_lacp.members) != {"c1", "c2"}:
            raise ValueError("client_lacp must name both Small clients")
        groups = (state.bridge_forwarding.ports, state.router_lacp.members, *state.client_lacp.members.values(),
                  traffic.no_sender_return_streams)
        if any(len(set(items)) != len(items) for items in groups):
            raise ValueError("port names and stream IDs must be unique within each group")
        if set(traffic.no_sender_return_streams) - DIRECT_FLOOD_FLOWS.keys():
            raise ValueError("flood stream IDs must exist in the Small topology")
        return self

    @property
    def bridge_ports(self):
        bridge = self.expected_state.bridge_forwarding
        return tuple(BridgePortIntent(peer, bridge.bridge, port, bridge.forwarding)
                     for peer in self.expected_state.peers for port in bridge.ports)

    @property
    def flood_flows(self):
        return {ident: DIRECT_FLOOD_FLOWS[ident] for ident in self.traffic.no_sender_return_streams}
