# Public CHR kit reproduction — 27 November 2026

The published download-and-deploy instructions passed on Linux ARM64 and AMD64. Both labs used clients, topology and startup configs downloaded anonymously from the public release. No image or client build, source checkout or login was used.

| Check | ARM64 | AMD64 |
| --- | --- | --- |
| Anonymous README, kit and client downloads | PASS | PASS |
| Published SHA256SUMS verification | PASS | PASS |
| Exact published deployment commands | PASS | PASS |
| Client hash matches the public inventory | PASS | PASS |
| Hook, launcher and startup-config mounts come from the downloaded kit directory | PASS | PASS |
| Management SSH over IPv4/IPv6, credentials, identity and startup config | PASS | PASS |
| Both LACP members and guest IPv4/IPv6 data forwarding | PASS | PASS |
| Port gaps, 10G full duplex, MTU matching and reciprocal tc filters | PASS | PASS |
| Only management bridge br0; zero Linux data IPv6 output | PASS | PASS |
| Published node restart; unchanged guest MACs and container identities | PASS | PASS |
| Published inspect and cleanup commands | PASS | PASS |
| Every required image config/layer freshly downloaded and hashed anonymously | PASS | PASS |

ARM64 used Debian with Docker 26.1.5+dfsg1; AMD64 used Debian with Docker 29.3.0. Both used QEMU TCG. Docker credential files, curl configuration and registry-auth environment variables were absent.

The shared Docker image cache was preserved because other labs use it. Anonymous Docker pulls verified the public image digest, and every required image blob was separately fetched over HTTPS on each VM and checked for size and SHA-256, without Docker cache or account credentials.

One documentation clarification was published: deployment initially shows `health: starting`; wait for both switches to be `healthy` before SSH or forwarding checks. The download-and-deploy command block, clients, image and topology are unchanged. The revised public README and SHA256SUMS were downloaded and verified on both VMs, and its inspect command passed.

The temporary public-kit labs were removed using their downloaded topology and client. The populated Small lab remains healthy and running; unrelated labs were not operated on.

Release: https://github.com/narrowin/mikrotik-mlag-testsuite/releases/tag/chr-startup-hooks-7.26beta7-20261127

Image: `ghcr.io/narrowin/vrnetlab_mikrotik_routeros@sha256:dbd8a548b23d2009372ff20dcd8f345cc3eaf31b39422b0e659c1f72e2656f10`

Evidence: `public-kit-verification-20261127.tar.gz`. Checksums: `PUBLIC-KIT-SHA256SUMS`.
