#!/bin/sh
set -eu

# The host name gives the site VLAN and the host's last address byte.
case "$(hostname)" in
    dc1-traffic) site=110 host=16 ;;
    dc1-service) site=110 host=17 ;;
    dc2-traffic) site=120 host=26 ;;
    dc2-service) site=120 host=27 ;;
esac

# miimon 100 stops sending on a cut cable, lacp_rate fast matches the switches, and the fixed MAC keeps the bond's cable choice in every run.
ip link add bond0 address "02:00:00:42:00:$host" type bond mode 802.3ad miimon 100 lacp_rate fast
# A cable joins a bond only while it is down.
for cable in eth1 eth2; do
    ip link set "$cable" down
    ip link set "$cable" master bond0
done
ip address add "10.$site.0.$host/24" dev bond0
ip link set bond0 up

# A traffic host reaches the other site over VLAN 390 through the DCI.
case "$(hostname)" in
    *-traffic)
        ip link add link bond0 name vlan390 type vlan id 390
        ip address add "198.18.40.$host/24" dev vlan390
        ip link set vlan390 up
        ;;
esac

# start.sh waits for this file, which exists only when every line above succeeded.
touch /run/host-setup.done
