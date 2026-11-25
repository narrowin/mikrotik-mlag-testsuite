"""Load the operator-facing definition for the Small secondary reboot."""

from pathlib import Path
from typing import Annotated, Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, PositiveInt, field_validator
import yaml

from .bridge_intent import BridgePortIntent
from .direct_topology import DIRECT_FLOOD_FLOWS, DIRECT_FLOWS, DIRECT_NODES, DIRECT_STREAM_IDS

SMALL_06_PATH = Path(__file__).with_name("small-06.yaml")
SMALL_06_YAML = SMALL_06_PATH.read_text()
Seconds = Annotated[float, Field(strict=True, gt=0, allow_inf_nan=False)]
OutageSeconds = Annotated[float, Field(strict=True, ge=0, allow_inf_nan=False)]
Names = Annotated[tuple[str, ...], Field(min_length=1)]
Streams = Annotated[tuple[PositiveInt, ...], Field(min_length=1)]


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
    mlag_state: Literal["connected"] = Field(validation_alias=AliasChoices("mlag-state", "mlag_state"))
    bridge_forwarding: BridgeForwarding
    router_lacp: RouterLacp
    client_lacp: ClientLacp


class OutageLimits(IntentSection):
    withdrawal: OutageSeconds
    restoration: OutageSeconds


class Traffic(IntentSection):
    loss_free_baseline: Literal[True]
    client_streams: Streams
    max_client_outage_seconds: OutageLimits
    recovery_consecutive_replies: PositiveInt
    loss_free_bypass_streams: Streams
    no_sender_return_streams: Streams

    @field_validator("client_streams", "loss_free_bypass_streams", "no_sender_return_streams", mode="before")
    @classmethod
    def resolve_stream_names(cls, streams):
        if not isinstance(streams, (list, tuple)):
            return streams
        resolved = []
        for stream in streams:
            if isinstance(stream, str) and not stream.isdecimal():
                if stream not in DIRECT_STREAM_IDS:
                    raise ValueError(f"unknown Small lab traffic stream {stream!r}")
                stream = DIRECT_STREAM_IDS[stream]
            resolved.append(stream)
        return resolved

    @property
    def recovery_count_label(self):
        return "ten" if self.recovery_consecutive_replies == 10 else str(self.recovery_consecutive_replies)


class Small06Intent(IntentSection):
    fault: Reboot
    expected_state: ExpectedState = Field(validation_alias=AliasChoices("expected_state", "before_and_after"))
    traffic: Traffic

    @property
    def bridge_ports(self):
        bridge = self.expected_state.bridge_forwarding
        return tuple(BridgePortIntent(peer, bridge.bridge, port, bridge.forwarding)
                     for peer in self.expected_state.peers for port in bridge.ports)

    @property
    def probe_flows(self):
        return {ident: DIRECT_FLOWS[ident] for ident in
                (*self.traffic.client_streams, *self.traffic.loss_free_bypass_streams)}

    @property
    def flood_flows(self):
        return {ident: DIRECT_FLOOD_FLOWS[ident] for ident in self.traffic.no_sender_return_streams}


def load_small_06(raw, source):
    try:
        intent = Small06Intent.model_validate(yaml.safe_load(raw))
        state, traffic = intent.expected_state, intent.traffic
        if set(state.peers) != DIRECT_NODES.keys() or len(state.peers) != len(DIRECT_NODES):
            raise ValueError("peers must name both Small switches once")
        if set(state.client_lacp.members) != {"c1", "c2"}:
            raise ValueError("client_lacp must name both Small clients")
        sets = (state.bridge_forwarding.ports, state.router_lacp.members, *state.client_lacp.members.values(),
                traffic.client_streams + traffic.loss_free_bypass_streams, traffic.no_sender_return_streams)
        if any(len(set(items)) != len(items) for items in sets):
            raise ValueError("port names and stream IDs must be unique within each group")
        if set(traffic.client_streams + traffic.loss_free_bypass_streams) - DIRECT_FLOWS.keys():
            raise ValueError("client and bypass stream IDs must exist in the Small topology")
        if set(traffic.no_sender_return_streams) - DIRECT_FLOOD_FLOWS.keys():
            raise ValueError("flood stream IDs must exist in the Small topology")
        return intent
    except (ValueError, yaml.YAMLError) as error:
        raise ValueError(f"{source}: {error}") from error
