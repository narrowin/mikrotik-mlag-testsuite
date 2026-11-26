#!/bin/sh
set -eu
cd "$(dirname "$0")"

# The image needs no build context, so the Dockerfile comes on standard input.
docker build -t small-mlag-client:local - < client.Dockerfile
containerlab deploy -t topology.clab.yml
