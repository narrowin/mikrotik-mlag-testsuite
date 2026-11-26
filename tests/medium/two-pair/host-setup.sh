#!/bin/sh
set -eu

# Host N is the node hostN and uses 1N as its address and MAC suffix.
n=$(hostname)
n=1${n#host}

# miimon 100 stops sending on a cut cable, lacp_rate fast matches the switches, and the fixed MAC keeps the bond's cable choice in every run.
ip link add bond0 address "02:00:00:22:00:$n" type bond mode 802.3ad miimon 100 lacp_rate fast
# A cable joins a bond only while it is down.
for cable in eth1 eth2; do
    ip link set "$cable" down
    ip link set "$cable" master bond0
done
ip address add "10.110.0.$n/24" dev bond0
ip link set bond0 up

# The bypass cable gives each host a /30 outside the switches.
ip address add "198.51.100.${n#1}/30" dev eth3
ip link set eth3 up
