{{/* STP_MODE none keeps spanning tree off. With any other mode, STP_ROOT picks the root bridge: "pair" gives both MLAG peers the lower priority 0x1000 and the access switch 0x8000, "access-switch" swaps the two. Both peers always share the same priority and port settings. */}}{{if eq .ShortName "access-switch"}}
# The access switch bonds its two uplinks, ether2 to switch1 and ether3 to switch2, and sees the MLAG pair as one LACP partner.
/interface bonding add name=uplink mode=802.3ad slaves=ether2,ether3 lacp-rate=1sec
/interface bridge add name=bridge vlan-filtering=yes protocol-mode={{.Env.STP_MODE}}{{if ne .Env.STP_MODE "none"}} priority={{if eq .Env.STP_ROOT "access-switch"}}0x1000{{else}}0x8000{{end}}{{end}} auto-mac=no admin-mac=02:00:00:21:01:03 frame-types=admit-only-vlan-tagged
/interface bridge port add bridge=bridge interface=uplink pvid=110{{if ne .Env.STP_MODE "none"}} edge=no{{end}}
# Host1 is on ether4.
/interface bridge port add bridge=bridge interface=ether4 pvid=110{{if ne .Env.STP_MODE "none"}} edge=yes{{end}}
/interface bridge vlan add bridge=bridge untagged=uplink,ether4 vlan-ids=110
{{else}}
# Both peers give a bond its mlag-id, and lacp-rate=1sec lets a cable rejoin in seconds, not 30 to 90 s.
/interface bonding add name=access-switch mode=802.3ad mlag-id=1 slaves=ether3 lacp-rate=1sec
/interface bonding add name=host2 mode=802.3ad mlag-id=2 slaves=ether4 lacp-rate=1sec
# Lower MLAG priority makes switch1 the MLAG primary. Fixed bridge MACs keep the shared LACP system ID the same in every run.
/interface bridge add name=bridge vlan-filtering=yes protocol-mode={{.Env.STP_MODE}}{{if ne .Env.STP_MODE "none"}} priority={{if eq .Env.STP_ROOT "access-switch"}}0x8000{{else}}0x1000{{end}}{{end}} mlag-peer-port=ether2 mlag-priority={{if eq .ShortName "switch1"}}10{{else}}20{{end}} auto-mac=no admin-mac=02:00:00:21:01:{{if eq .ShortName "switch1"}}01{{else}}02{{end}} frame-types=admit-only-vlan-tagged
# MLAG carries VLAN 110 tagged on the peer link.
/interface bridge port add bridge=bridge interface=ether2 frame-types=admit-only-vlan-tagged{{if ne .Env.STP_MODE "none"}} edge=no{{end}}
/interface bridge port add bridge=bridge interface=access-switch pvid=110{{if ne .Env.STP_MODE "none"}} edge=no{{end}}
/interface bridge port add bridge=bridge interface=host2 pvid=110{{if ne .Env.STP_MODE "none"}} edge=yes{{end}}
/interface bridge vlan add bridge=bridge tagged=ether2 untagged=access-switch,host2 vlan-ids=110
{{end}}
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
