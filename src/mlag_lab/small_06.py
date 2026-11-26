"""The SMALL-06 rules that no other case field holds: fault timing and flood streams.

The switch and client state SMALL-06 requires is the Networka intent in intent/state/direct*.yaml.
"""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, model_validator

from .direct_topology import DIRECT_FLOOD_FLOWS

Seconds = Annotated[float, Field(strict=True, gt=0, allow_inf_nan=False)]
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


class Traffic(IntentSection):
    loss_free_baseline: Literal[True]
    recovery_consecutive_replies: PositiveInt
    no_sender_return_streams: Streams

    @property
    def recovery_count_label(self):
        return "ten" if self.recovery_consecutive_replies == 10 else str(self.recovery_consecutive_replies)


class Small06Intent(IntentSection):
    fault: Reboot
    traffic: Traffic

    @model_validator(mode="after")
    def check_streams(self):
        streams = self.traffic.no_sender_return_streams
        if len(set(streams)) != len(streams):
            raise ValueError("flood stream IDs must be unique")
        if set(streams) - DIRECT_FLOOD_FLOWS.keys():
            raise ValueError("flood stream IDs must exist in the Small topology")
        return self

    @property
    def flood_flows(self):
        return {ident: DIRECT_FLOOD_FLOWS[ident] for ident in self.traffic.no_sender_return_streams}
