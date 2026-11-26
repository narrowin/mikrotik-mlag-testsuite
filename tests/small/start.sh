#!/bin/sh
set -eu
cd "$(dirname "$0")"

# The image needs no build context, so the Dockerfile comes on standard input.
docker build -t small-mlag-client:local - < client.Dockerfile
# Containerlab checks the collector bind path before it creates the node directory.
mkdir -p clab-small-mlag/syslog
containerlab deploy -t topology.clab.yml
