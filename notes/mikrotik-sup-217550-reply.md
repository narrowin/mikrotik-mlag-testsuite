# Reply for MikroTik SUP-217550

Hello Jānis,

Could you add `iproute2-tc` and optional startup hooks to the official CHR Docker image? This would let containerlab and other automation tools use your maintained image without rebuilding it. Tool maintainers would supply their own deployment logic.

`tc` replaces per-port data bridges, removing MAC-learning, multicast-snooping, LACP/LLDP forwarding-mask and bridge-netfilter workarounds. This corrects my earlier statement that tc was unnecessary. Management bootstrap and Linux IPv6 suppression remain our integration's responsibility.

The overhead for MikroTik is one package installation, an empty directory and **seven added lines** in `/start.sh`. No RouterOS changes are required. With no hooks installed, normal startup is unchanged.

This follows the established extension pattern used by the [official NGINX entrypoint](https://github.com/nginx/docker-nginx/blob/2879b26c7dedf1d958b1894a5c1b1dec3c026369/entrypoint/docker-entrypoint.sh#L13-L47), with hooks supplied through [Docker's documented bind mounts](https://docs.docker.com/engine/storage/bind-mounts/#when-to-use-bind-mounts).

Measured on 7.26beta7, the added tc layer **including dependencies** is **0.75 MiB on AMD64 / 0.93 MiB on ARM64 uncompressed**, or **340 / 349 KiB compressed**, respectively.

Image-build addition:

```dockerfile
RUN apk add --no-cache iproute2-tc && mkdir -p /etc/chr/start.d
```

The hooks are sourced before network and QEMU setup. The complete `/start.sh` diff is:

```diff
--- start.sh.orig
+++ start.sh
@@ -108,6 +108,13 @@
     exit 1
 fi
 
+# Optional startup hooks; an empty directory preserves the default startup.
+for startup_script in /etc/chr/start.d/*.sh; do
+    [ -f "$startup_script" ] || continue
+    # shellcheck source=/dev/null
+    . "$startup_script" || exit $?
+done
+
 echo "" > /etc/qemu/bridge.conf
 
 qemu="qemu-system-x86_64"
```

Tested standalone and with rebuilt containerlab clients on ARM64 and AMD64, including LACP, IPv4/IPv6 forwarding and restart. The public download-and-deploy instructions were also reproduced without login or rebuilding on both architectures. Separately, all four Small lab tests passed on ARM64 with the same unchanged image, our updated lab configuration and Networka.

You can download and test everything without login or rebuilding:

- [CHR startup patch](https://github.com/narrowin/mikrotik-mlag-testsuite/releases/download/chr-startup-hooks-7.26beta7-20261127/start.sh.diff) and [image-build overlay](https://github.com/narrowin/mikrotik-mlag-testsuite/releases/download/chr-startup-hooks-7.26beta7-20261127/Dockerfile).
- [Containerlab patch](https://github.com/narrowin/mikrotik-mlag-testsuite/releases/download/chr-startup-hooks-7.26beta7-20261127/containerlab-chr-hooks.patch) and [prebuilt ARM64/AMD64 clients, runnable lab and instructions](https://github.com/narrowin/mikrotik-mlag-testsuite/releases/tag/chr-startup-hooks-7.26beta7-20261127).
- [Public image](https://github.com/orgs/narrowin/packages/container/vrnetlab_mikrotik_routeros/1650973549) and [artifact inventory with digests](https://github.com/narrowin/mikrotik-mlag-testsuite/releases/download/chr-startup-hooks-7.26beta7-20261127/public-artifacts.json).


```sh
docker pull ghcr.io/narrowin/vrnetlab_mikrotik_routeros:chr-7.26beta7-hooks-20261127-01
```

Best regards,
Mischa
