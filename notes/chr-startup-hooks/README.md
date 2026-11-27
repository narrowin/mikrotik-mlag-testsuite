# Generic CHR startup hooks

The prototype adds `iproute2-tc`, an empty `/etc/chr/start.d` directory and seven lines in the official `/start.sh`. The RouterOS guest disk is unchanged. Hooks are optional, sourced in filename order before network and QEMU initialization, and a nonzero status stops startup. An empty directory follows the original startup path.

[Exact startup patch](start.sh.diff) · [Prototype Dockerfile](Dockerfile) · [Measured image changes](image.diff) · [MikroTik reply](../mikrotik-sup-217550-reply.md)

The Dockerfile is for maintainers evaluating the proposal. Users can pull the public prototype and use the published containerlab clients without rebuilding either. The native `mikrotik_chr` kind supplies its hook, launcher and runtime settings; user topologies need no custom entrypoint or manual CHR mounts.

[Public release and deployment instructions](https://github.com/narrowin/mikrotik-mlag-testsuite/releases/tag/chr-startup-hooks-7.26beta7-20261127) · [Artifact inventory](../chr-public-artifacts.json) · [Anonymous ARM64/AMD64 reproduction](PUBLIC-KIT-RESULTS.md)

The containerlab source is on the [hook branch](https://github.com/mischadiehm/containerlab/tree/codex/chr-startup-hooks). It connects data interfaces with reciprocal tc redirects and retains the management bridge and necessary Linux data-interface IPv6 suppression. The image itself contains no containerlab launcher or hook.
