#!/bin/sh
set -eu

# Client N is the node clientN.
n=$(hostname)
n=${n#client}

# miimon 100 stops sending on a cut cable, lacp_rate fast matches the switches, and the fixed MAC keeps the bond's cable choice in every run.
ip link add bond0 address "02:00:00:00:00:0$n" type bond mode 802.3ad miimon 100 lacp_rate fast
# A cable joins a bond only while it is down.
for cable in eth1 eth2; do
    ip link set "$cable" down
    ip link set "$cable" master bond0
done
ip address add "10.0.10.$n/24" dev bond0
ip link set bond0 up

# start.sh waits for this file, which exists only when every line above succeeded.
touch /run/host-setup.done
