# Strict LACP and min-links=1 withdraw a local bond with no negotiated member.
# MLAG then forwards through the peer link instead of the unusable local cable.
/interface bonding add name=host1 mode=802.3ad mlag-id=1 slaves=ether3 lacp-rate=1sec lacp-strict=yes min-links=1
/interface bonding add name=host2 mode=802.3ad mlag-id=2 slaves=ether4 lacp-rate=1sec lacp-strict=yes min-links=1
/interface bonding add name=host3 mode=802.3ad mlag-id=3 slaves=ether5 lacp-rate=1sec lacp-strict=yes min-links=1
# MLAG carries the host VLAN tagged on the peer link. VLAN 10 matches the host subnet 10.0.10.0/24.{{/* STP_MODE none keeps spanning tree off. Any other mode makes the MLAG pair the root, with the same priority and port settings on both peers. */}}
/interface bridge add name=bridge vlan-filtering=yes protocol-mode={{.Env.STP_MODE}}{{if ne .Env.STP_MODE "none"}} priority=0x1000{{end}} mlag-peer-port=ether2
/interface bridge port add bridge=bridge interface=ether2
/interface bridge port add bridge=bridge interface=host1 pvid=10{{if ne .Env.STP_MODE "none"}} edge=yes{{end}}
/interface bridge port add bridge=bridge interface=host2 pvid=10{{if ne .Env.STP_MODE "none"}} edge=yes{{end}}
/interface bridge port add bridge=bridge interface=host3 pvid=10{{if ne .Env.STP_MODE "none"}} edge=yes{{end}}
/interface bridge vlan add bridge=bridge tagged=ether2 vlan-ids=10
# Send the log to the collector from the management VRF via its management interface.
/system logging action add name=collector target=remote remote={{.Env.COLLECTOR}} vrf=mgmt
# interface records port changes and script records test markers. Severity rules capture MLAG problems across topics.
/system logging add action=collector topics=interface
/system logging add action=collector topics=script
/system logging add action=collector topics=warning
/system logging add action=collector topics=error
/system logging add action=collector topics=critical{{if ne .Env.STP_MODE "none"}}
# stp records port role and state changes when spanning tree is on.
/system logging add action=collector topics=stp{{end}}

# RouterOS 7.26beta7 can leave remote logging silent after reboot. Reselect the VRF after its route is active.
# Poll for 10 s to cover the management startup time seen on this CHR.
/system scheduler add name=refresh-collector start-time=startup policy=read,write on-event={
    :for attempt from=1 to=10 do={
        :if ([:len [/ip route find where routing-table=mgmt dst-address=0.0.0.0/0 active]] > 0) do={
            /system logging action set [find where name="collector"] vrf=main
            /system logging action set [find where name="collector"] vrf=mgmt
            :return ""
        }
        :delay 1s
    }
    :log error "collector logging could not find the active management route"
}
