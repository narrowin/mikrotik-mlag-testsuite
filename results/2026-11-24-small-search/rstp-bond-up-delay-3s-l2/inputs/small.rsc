/interface bonding add name=client1 mode=802.3ad mlag-id=11 slaves=ether3 lacp-rate=1sec
/interface bonding add name=client2 mode=802.3ad mlag-id=12 slaves=ether4 lacp-rate=1sec
/interface bridge add name=bridge vlan-filtering=yes mlag-peer-port=ether2 priority=0x1000 frame-types=admit-only-vlan-tagged protocol-mode=rstp
/interface bridge port add bridge=bridge interface=ether2 frame-types=admit-only-vlan-tagged
/interface bridge port add bridge=bridge interface=client1 pvid=110 edge=yes
/interface bridge port add bridge=bridge interface=client2 pvid=110 edge=yes
/interface bridge port add bridge=bridge interface=ether5 pvid=110 edge=yes
/interface bridge vlan add bridge=bridge tagged=ether2 untagged=client1,client2,ether5 vlan-ids=110
/system/logging/action/add name=mlagLabSyslog target=remote remote=172.30.215.20 remote-port=1514 vrf=mgmt remote-protocol=udp remote-log-format=syslog syslog-time-format=bsd-syslog add-topics-string=yes
/system/logging/add action=mlagLabSyslog topics=info,!warning,!error,!critical,!debug comment=mlag-lab-info
/system/logging/add action=mlagLabSyslog topics=warning,!error,!critical,!debug comment=mlag-lab-warning
/system/logging/add action=mlagLabSyslog topics=error,!critical,!debug comment=mlag-lab-error
/system/logging/add action=mlagLabSyslog topics=critical,!debug comment=mlag-lab-critical
/system/logging/add action=mlagLabSyslog topics=bridge,debug,!packet comment=mlag-lab-debug
/system/logging/add action=mlagLabSyslog topics=stp,debug,!bridge,!packet comment=mlag-lab-stp-debug
/system/logging/add action=mlagLabSyslog topics=interface,debug,!bridge,!stp,!packet comment=mlag-lab-interface-debug
:log info "mlag-lab-startup-config-ready"
