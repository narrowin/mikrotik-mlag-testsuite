#!/bin/sh
set -eu

# Host N is the node hostN.
n=$(hostname)
n=${n#host}

# Independent LACP control stops transmitting when the partner stops collecting.
# The fixed MAC keeps the bond's cable choice in every run.
ip link add bond0 address "02:00:00:00:00:0$n" type bond mode 802.3ad miimon 100 lacp_rate fast coupled_control off
# A cable joins a bond only while it is down.
for cable in eth1 eth2; do
    ip link set "$cable" down
    ip link set "$cable" master bond0
done
ip address add "10.0.10.$n/24" dev bond0
ip link set bond0 up

# start.sh waits for this file, which exists only when every line above succeeded.
touch /run/host-setup.done
