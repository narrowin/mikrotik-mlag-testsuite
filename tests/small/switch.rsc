# Both switches give a client's bond its number as mlag-id, and lacp-rate=1sec lets a cable rejoin in seconds, not 30 to 90 s.
/interface bonding add name=client1 mode=802.3ad mlag-id=1 slaves=ether3 lacp-rate=1sec
/interface bonding add name=client2 mode=802.3ad mlag-id=2 slaves=ether4 lacp-rate=1sec
/interface bonding add name=client3 mode=802.3ad mlag-id=3 slaves=ether5 lacp-rate=1sec
# Spanning tree off from boot, ether2 is the peer link, and the clients are untagged in VLAN 10.
/interface bridge add name=bridge vlan-filtering=yes protocol-mode=none mlag-peer-port=ether2
/interface bridge port add bridge=bridge interface=ether2
/interface bridge port add bridge=bridge interface=client1 pvid=10
/interface bridge port add bridge=bridge interface=client2 pvid=10
/interface bridge port add bridge=bridge interface=client3 pvid=10
# MLAG needs the client VLAN tagged on the peer link.
/interface bridge vlan add bridge=bridge tagged=ether2 vlan-ids=10
# Send the log to the collector from the management VRF, in syslog format with host name and topics.
/system logging action add name=collector target=remote remote=172.30.100.10 remote-port=514 vrf=mgmt remote-log-format=syslog add-topics-string=yes
# interface carries the port link lines, script the test markers, and the severities the MLAG warnings.
/system logging add action=collector topics=interface
/system logging add action=collector topics=script
/system logging add action=collector topics=warning
/system logging add action=collector topics=error
/system logging add action=collector topics=critical
