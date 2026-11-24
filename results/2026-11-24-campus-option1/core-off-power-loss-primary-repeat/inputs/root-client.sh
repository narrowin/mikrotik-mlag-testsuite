#!/bin/sh
set -eu

case "$1" in
    11)
        ip link set dev eth1 address 02:00:00:11:00:11
        ip address replace 10.110.0.11/24 dev eth1
        ip link set dev eth1 up
        ip address replace 198.51.100.1/30 dev eth3
        ip link set dev eth3 up
        ip neigh replace 10.110.0.12 lladdr 02:00:00:11:00:12 nud permanent dev eth1
        ;;
    12)
        /bin/sh /lab/client-network.sh 12
        ip neigh replace 10.110.0.11 lladdr 02:00:00:11:00:11 nud permanent dev bond0
        ;;
    *) exit 1 ;;
esac
