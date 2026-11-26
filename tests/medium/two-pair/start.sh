#!/bin/sh
set -eu

case "${CLAB:-}" in
    /*) ;;
    *)
        echo "Set CLAB to the absolute path of the qualified Containerlab binary." >&2
        exit 1
        ;;
esac
if [ ! -f "$CLAB" ] || [ ! -x "$CLAB" ]; then
    echo "Containerlab is not executable at $CLAB" >&2
    exit 1
fi

# The strict variant is the same lab with lacp-strict=yes on the inter-pair bond, in its own folder.
case "${1:-}" in
    "") cd "$(dirname "$0")"; lab=medium-two-pair ;;
    strict) cd "$(dirname "$0")/../two-pair-strict"; lab=medium-two-pair-strict ;;
    *) echo "Usage: $0 [strict]" >&2; exit 1 ;;
esac

# The Small lab's client image serves both hosts. It needs no build context, so the Dockerfile comes on standard input.
docker build -t small-mlag-client:local - < ../../small/client.Dockerfile
# Containerlab checks the collector bind path before it creates the node directory.
mkdir -p "clab-$lab/syslog"
"$CLAB" deploy -t topology.clab.yml
