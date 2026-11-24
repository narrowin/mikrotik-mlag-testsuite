{
    :local node [/system identity get name]
    :if ($node = "dc1-access-switch1") do={
        /interface bonding add name=uplink mode=802.3ad slaves=ether2,ether3 lacp-rate=1sec
        /interface bridge add name=bridge protocol-mode=rstp priority=0x8000 auto-mac=no admin-mac=02:00:00:21:00:13 vlan-filtering=yes frame-types=admit-only-vlan-tagged
        /interface bridge port add bridge=bridge interface=uplink pvid=110 edge=no
        /interface bridge port add bridge=bridge interface=ether4 pvid=110 edge=yes
        /interface bridge vlan add bridge=bridge untagged=uplink,ether4 vlan-ids=110
    } else={
        :if (($node != "dc1-core-mlag1") && ($node != "dc1-core-mlag2")) do={ :error "Unknown MLAG root experiment identity" }
        /interface bonding add name=access-uplink mode=802.3ad mlag-id=11 slaves=ether3 lacp-rate=1sec
        /interface bonding add name=client2 mode=802.3ad mlag-id=12 slaves=ether4 lacp-rate=1sec
        /interface bridge add name=bridge protocol-mode=rstp priority=0x1000 vlan-filtering=yes mlag-peer-port=ether2 frame-types=admit-only-vlan-tagged
        :if ($node = "dc1-core-mlag1") do={
            /interface bridge set bridge mlag-priority=10 auto-mac=no admin-mac=02:00:00:21:00:11
        } else={
            /interface bridge set bridge mlag-priority=20 auto-mac=no admin-mac=02:00:00:21:00:12
        }
        /interface bridge port add bridge=bridge interface=ether2 frame-types=admit-only-vlan-tagged edge=no
        /interface bridge port add bridge=bridge interface=access-uplink pvid=110 edge=no
        /interface bridge port add bridge=bridge interface=client2 pvid=110 edge=yes
        /interface bridge vlan add bridge=bridge tagged=ether2 untagged=access-uplink,client2 vlan-ids=110
    }
}
/system/logging/action/add name=mlagLabSyslog target=remote remote=172.30.216.20 remote-port=1514 vrf=mgmt remote-protocol=udp remote-log-format=syslog syslog-time-format=bsd-syslog add-topics-string=yes
{
    :local node [/system identity get name]
    :local source "172.30.216.13"
    :if ($node = "dc1-core-mlag1") do={ :set source "172.30.216.11" }
    :if ($node = "dc1-core-mlag2") do={ :set source "172.30.216.12" }
    /system logging action set [find where name=mlagLabSyslog] src-address=$source
}
/system/logging/add action=mlagLabSyslog topics=info,!warning,!error,!critical,!debug comment=mlag-lab-info
/system/logging/add action=mlagLabSyslog topics=warning,!error,!critical,!debug comment=mlag-lab-warning
/system/logging/add action=mlagLabSyslog topics=error,!critical,!debug comment=mlag-lab-error
/system/logging/add action=mlagLabSyslog topics=critical,!debug comment=mlag-lab-critical
/system/logging/add action=mlagLabSyslog topics=bridge,debug,!packet comment=mlag-lab-debug
/system/logging/add action=mlagLabSyslog topics=stp,debug,!bridge,!packet comment=mlag-lab-stp-debug
/system/logging/add action=mlagLabSyslog topics=interface,debug,!bridge,!stp,!packet comment=mlag-lab-interface-debug
:log info "mlag-lab-startup-config-ready"
