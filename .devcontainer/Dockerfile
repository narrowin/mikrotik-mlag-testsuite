FROM ghcr.io/astral-sh/uv:0.13.9 AS uv
FROM ghcr.io/srl-labs/containerlab/devcontainer-dind-slim:0.83.0

USER root
COPY --from=uv /uv /usr/local/bin/uv
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tshark \
    && rm -rf /var/lib/apt/lists/*

USER vscode
