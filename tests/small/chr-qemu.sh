#!/bin/sh
# LACP needs equal, known speeds and full duplex on its ports. 10G supplies one common speed.
for arg do
    shift
    case "$arg" in
        virtio-net,id=nic*) arg="$arg,speed=10000,duplex=full" ;;
    esac
    set -- "$@" "$arg"
done
exec "/usr/bin/${0##*/}" "$@"
