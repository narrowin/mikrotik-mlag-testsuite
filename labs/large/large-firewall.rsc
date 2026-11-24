{
    :local node [/system identity get name]
    :local peerAddress "198.18.40.2/24"
    :local peerPriority 150
    :if ($node = "dc2-firewall1") do={
        :set peerAddress "198.18.40.3/24"
        :set peerPriority 100
    } else={
        :if ($node != "dc1-firewall1") do={ :error "Unexpected Large lab firewall identity" }
    }

    /interface bonding add name=core-uplink mode=802.3ad slaves=ether2,ether3 lacp-rate=1sec
    /interface vlan add name=vrrp-test interface=core-uplink vlan-id=390
    /ip address add address=$peerAddress interface=vrrp-test
    /interface vrrp add name=vrrp390 interface=vrrp-test vrid=39 version=3 v3-protocol=ipv4 priority=$peerPriority interval=1s preemption-mode=yes sync-connection-tracking=no disabled=no
    /ip address add address=198.18.40.1/32 interface=vrrp390
}
