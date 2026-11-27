# Use the qualified public tc stack and a reproducible engine artifact

On 27 November 2026 the operator requested that the whole lab checkout use our
public CHR image and qualified containerlab clients, removing bridge workarounds.
All maintained topologies pin one image digest. The shared launcher selects the
published client by architecture and verifies its SHA-256 before execution.
It does not replace the host's installed containerlab.

The previous pinned Networka version failed the real cable test because its QEMU
NIC discovery required a Linux bridge. TC connections have no data bridge.
The tc-aware engine passed that test. Its changes stay in Networka's modules;
the lab descriptions contain no replacement engine logic.

Until a qualified upstream release contains these changes, uv.lock pins the
bundled source archive in `vendor/`, with its source base, patch and checksum.
This is reproducible from a single checkout and does not depend on a sibling's
uncommitted working files. A source archive adds repository size, but preserves
reviewable source and avoids introducing a second public release requirement.
Replace it with a qualified upstream pin after release.

The post-deploy bridge-learning step and old QEMU-wrapper instructions are
removed. Management bootstrap and Linux IPv6 suppression remain in the kind.
Historical reports retain their original image, engine and qualification scope.
