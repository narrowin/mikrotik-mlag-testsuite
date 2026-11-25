{
    :local node [/system identity get name]
    :local mlagPriority 20
    :local bridgePriority 0x4000
    :local interpairId 21
    :local client "client1"
    :local clientId 22
    :local mac ""
    :if ($node = "dc1-core-mlag1") do={ :set mac "02:00:00:21:00:11" }
    :if ($node = "dc1-core-mlag2") do={ :set mac "02:00:00:21:00:14" }
    :if ($node = "dc1-access-mlag1") do={ :set mac "02:00:00:21:00:12" }
    :if ($node = "dc1-access-mlag2") do={ :set mac "02:00:00:21:00:13" }
    :if ($mac = "") do={ :error "Unknown MLAG two-pair identity" }
    :if (($node = "dc1-core-mlag1") || ($node = "dc1-access-mlag1")) do={ :set mlagPriority 10 }
    :if (($node = "dc1-core-mlag1") || ($node = "dc1-core-mlag2")) do={
        :set bridgePriority 0x2000
        :set interpairId 11
        :set client "client2"
        :set clientId 12
    }
    /interface bonding add name=interpair mode=802.3ad mlag-id=$interpairId slaves=ether3 lacp-rate=1sec
    /interface bonding add name=$client mode=802.3ad mlag-id=$clientId slaves=ether4 lacp-rate=1sec
    /interface bridge add name=bridge protocol-mode=rstp priority=$bridgePriority vlan-filtering=yes mlag-peer-port=ether2 frame-types=admit-only-vlan-tagged
    /interface bridge set bridge mlag-priority=$mlagPriority auto-mac=no admin-mac=$mac
    /interface bridge port add bridge=bridge interface=ether2 frame-types=admit-only-vlan-tagged edge=auto
    /interface bridge port add bridge=bridge interface=interpair pvid=110 edge=auto path-cost=2000 internal-path-cost=2000
    /interface bridge port add bridge=bridge interface=$client pvid=110 edge=yes path-cost=2000 internal-path-cost=2000
    /interface bridge vlan add bridge=bridge tagged=ether2 untagged="interpair,$client" vlan-ids=110
}
/system/logging/action/add name=mlagLabSyslog target=remote remote=172.30.219.20 remote-port=1514 vrf=mgmt remote-protocol=udp remote-log-format=syslog syslog-time-format=bsd-syslog add-topics-string=yes
{
    :local node [/system identity get name]
    :local source "172.30.219.14"
    :if ($node = "dc1-core-mlag1") do={ :set source "172.30.219.11" }
    :if ($node = "dc1-core-mlag2") do={ :set source "172.30.219.12" }
    :if ($node = "dc1-access-mlag1") do={ :set source "172.30.219.13" }
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
