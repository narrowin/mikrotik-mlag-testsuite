# Both switches give a client's bond its number as mlag-id, and lacp-rate=1sec lets a cable rejoin in seconds, not 30 to 90 s.
/interface bonding add name=client1 mode=802.3ad mlag-id=1 slaves=ether3 lacp-rate=1sec
/interface bonding add name=client2 mode=802.3ad mlag-id=2 slaves=ether4 lacp-rate=1sec
/interface bonding add name=client3 mode=802.3ad mlag-id=3 slaves=ether5 lacp-rate=1sec
# MLAG carries the client VLAN tagged on the peer link. VLAN 10 matches the client subnet 10.0.10.0/24.
/interface bridge add name=bridge vlan-filtering=yes protocol-mode=none mlag-peer-port=ether2
/interface bridge port add bridge=bridge interface=ether2
/interface bridge port add bridge=bridge interface=client1 pvid=10
/interface bridge port add bridge=bridge interface=client2 pvid=10
/interface bridge port add bridge=bridge interface=client3 pvid=10
/interface bridge vlan add bridge=bridge tagged=ether2 vlan-ids=10
# Send the log to the collector from the management VRF via its management interface.
/system logging action add name=collector target=remote remote=172.30.100.10 vrf=mgmt
# interface records port changes and script records test markers. Severity rules capture MLAG problems across topics.
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
