# Both peers of a pair give a bond the same mlag-id, and lacp-rate=1sec lets a member rejoin in seconds, not 30 to 90 s.
{{if eq .ShortName "switch-a1" "switch-a2"}}
# Pair A carries host2 on ether4.
/interface bonding add name=inter-pair mode=802.3ad mlag-id=11 slaves=ether3 lacp-rate=1sec lacp-strict={{.Env.LACP_STRICT}}
/interface bonding add name=host2 mode=802.3ad mlag-id=12 slaves=ether4 lacp-rate=1sec
{{else}}
# Pair B carries host1 on ether4.
/interface bonding add name=inter-pair mode=802.3ad mlag-id=21 slaves=ether3 lacp-rate=1sec lacp-strict={{.Env.LACP_STRICT}}
/interface bonding add name=host1 mode=802.3ad mlag-id=22 slaves=ether4 lacp-rate=1sec
{{end}}
# Lower MLAG priority makes switch-a1 and switch-b1 the MLAG primaries. The bridge settings follow the old two-pair suite, including its fixed bridge MACs.{{/* STP_MODE none keeps spanning tree off. Any other mode makes pair A the root (priority 0x2000) and pair B the next (0x4000), with the same settings on both peers of a pair. The peer link and inter-pair ports keep edge=auto as in the old field setup. */}}
/interface bridge add name=bridge vlan-filtering=yes protocol-mode={{.Env.STP_MODE}}{{if ne .Env.STP_MODE "none"}} priority={{if eq .ShortName "switch-a1" "switch-a2"}}0x2000{{else}}0x4000{{end}}{{end}} mlag-peer-port=ether2 mlag-priority={{if eq .ShortName "switch-a1" "switch-b1"}}10{{else}}20{{end}} auto-mac=no admin-mac=02:00:00:21:00:{{if eq .ShortName "switch-a1"}}11{{else if eq .ShortName "switch-a2"}}14{{else if eq .ShortName "switch-b1"}}12{{else}}13{{end}} frame-types=admit-only-vlan-tagged
# MLAG carries VLAN 110 tagged on the peer link. VLAN 110 matches the host subnet 10.110.0.0/24.
/interface bridge port add bridge=bridge interface=ether2 frame-types=admit-only-vlan-tagged
/interface bridge port add bridge=bridge interface=inter-pair pvid=110
/interface bridge port add bridge=bridge interface={{if eq .ShortName "switch-a1" "switch-a2"}}host2{{else}}host1{{end}} pvid=110 edge=yes
/interface bridge vlan add bridge=bridge tagged=ether2 untagged=inter-pair,{{if eq .ShortName "switch-a1" "switch-a2"}}host2{{else}}host1{{end}} vlan-ids=110
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
