/system/logging/action/add name=mlagLabSyslog target=remote remote=172.30.220.20 remote-port=1514 vrf=mgmt remote-protocol=udp remote-log-format=syslog syslog-time-format=bsd-syslog add-topics-string=yes
{
    :local node [/system identity get name]
    :local role ""
    :local mlagPriority 20
    :local siteVlan 110
    :local mac ""
    :local source ""
    :if ($node = "dc1-core-mlag1") do={ :set role "core"; :set mlagPriority 10; :set mac "02:00:00:41:00:11"; :set source "172.30.220.11" }
    :if ($node = "dc1-core-mlag2") do={ :set role "core"; :set mac "02:00:00:41:00:12"; :set source "172.30.220.12" }
    :if ($node = "dc1-access-mlag1") do={ :set role "access"; :set mlagPriority 10; :set mac "02:00:00:41:00:13"; :set source "172.30.220.13" }
    :if ($node = "dc1-access-mlag2") do={ :set role "access"; :set mac "02:00:00:41:00:14"; :set source "172.30.220.14" }
    :if ($node = "dc2-core-mlag1") do={ :set role "core"; :set mlagPriority 10; :set siteVlan 120; :set mac "02:00:00:41:00:21"; :set source "172.30.220.21" }
    :if ($node = "dc2-core-mlag2") do={ :set role "core"; :set siteVlan 120; :set mac "02:00:00:41:00:22"; :set source "172.30.220.22" }
    :if ($node = "dc2-access-mlag1") do={ :set role "access"; :set mlagPriority 10; :set siteVlan 120; :set mac "02:00:00:41:00:23"; :set source "172.30.220.23" }
    :if ($node = "dc2-access-mlag2") do={ :set role "access"; :set siteVlan 120; :set mac "02:00:00:41:00:24"; :set source "172.30.220.24" }
    :if ($role = "") do={ :error "Unknown Large lab switch identity" }
    :if ($role = "core") do={
        /interface bonding add name=access-downlink mode=802.3ad mlag-id=31 slaves=ether3 lacp-rate=1sec
        /interface bonding add name=dci mode=802.3ad mlag-id=33 slaves=ether4 lacp-rate=1sec
        /interface bonding add name=firewall1 mode=802.3ad mlag-id=32 slaves=ether5 lacp-rate=1sec
    } else={
        /interface bonding add name=core-uplink mode=802.3ad mlag-id=21 slaves=ether3 lacp-rate=1sec
        /interface bonding add name=traffic1 mode=802.3ad mlag-id=22 slaves=ether4 lacp-rate=1sec
        /interface bonding add name=service1 mode=802.3ad mlag-id=23 slaves=ether5 lacp-rate=1sec
    }
    /interface bridge add name=bridge protocol-mode=none vlan-filtering=yes mlag-peer-port=ether2 frame-types=admit-only-vlan-tagged
    /interface bridge set bridge mlag-priority=$mlagPriority auto-mac=no admin-mac=$mac
    /interface bridge port add bridge=bridge interface=ether2 frame-types=admit-only-vlan-tagged edge=auto
    :if ($role = "core") do={
        /interface bridge port add bridge=bridge interface=access-downlink frame-types=admit-only-vlan-tagged edge=no path-cost=2000 internal-path-cost=2000
        /interface bridge port add bridge=bridge interface=dci frame-types=admit-only-vlan-tagged edge=no path-cost=2000 internal-path-cost=2000
        /interface bridge port add bridge=bridge interface=firewall1 frame-types=admit-only-vlan-tagged edge=yes path-cost=2000 internal-path-cost=2000
        /interface bridge vlan add bridge=bridge tagged="ether2,access-downlink,dci,firewall1" vlan-ids=390
    } else={
        /interface bridge port add bridge=bridge interface=core-uplink frame-types=admit-only-vlan-tagged edge=no path-cost=2000 internal-path-cost=2000
        /interface bridge port add bridge=bridge interface=traffic1 pvid=$siteVlan edge=yes path-cost=2000 internal-path-cost=2000
        /interface bridge port add bridge=bridge interface=service1 pvid=$siteVlan edge=yes path-cost=2000 internal-path-cost=2000
        /interface bridge vlan add bridge=bridge tagged="ether2,core-uplink,traffic1" vlan-ids=390
        /interface bridge vlan add bridge=bridge tagged=ether2 untagged="traffic1,service1" vlan-ids=$siteVlan
    }
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
