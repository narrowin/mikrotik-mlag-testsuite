/interface bonding add name=host1 mode=802.3ad mlag-id=11 slaves=ether3 lacp-rate=1sec
/interface bonding add name=host2 mode=802.3ad mlag-id=12 slaves=ether4 lacp-rate=1sec
# Lower MLAG priority elects switch1. Fixed bridge MACs let the gate verify the shared LACP system.
/interface bridge add name=bridge vlan-filtering=yes protocol-mode=none mlag-peer-port=ether2 mlag-lacp-fallback=yes mlag-priority={{if eq .ShortName "switch1"}}10{{else}}20{{end}} auto-mac=no admin-mac=02:00:00:11:01:{{if eq .ShortName "switch1"}}01{{else}}02{{end}} ageing-time={{.Env.SMALL_MAC_MOVE_AGE}} frame-types=admit-only-vlan-tagged
/interface bridge port add bridge=bridge interface=ether2 frame-types=admit-only-vlan-tagged
/interface bridge port add bridge=bridge interface=host1 pvid=110 edge=yes
/interface bridge port add bridge=bridge interface=host2 pvid=110 edge=yes
# The third host's MAC can move between these regular bridge ports.
/interface bridge port add bridge=bridge interface=ether5 pvid=110 edge=yes
/interface bridge vlan add bridge=bridge tagged=ether2 untagged=host1,host2,ether5 vlan-ids=110

/system logging action add name=collector target=remote remote=172.30.101.10 vrf=mgmt
/system logging add action=collector topics=interface
/system logging add action=collector topics=script
/system logging add action=collector topics=warning
/system logging add action=collector topics=error
/system logging add action=collector topics=critical

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
