# Qualified Networka dependency

`networka-0.5.2+chr.5.tar.gz` starts from public Networka commit
`3bd8c10a6671d4fe7393454fc9f12f687bdde16e` and applies
[the source patch](networka-chr.patch). Its upstream licence is retained.
The archive contains source, not a virtual environment or lab captures.

The patch adds reciprocal tc NIC discovery, delayed-queue cleanup and precise
recovery observation. For a Linux member required eligible by the lab file,
impairment recovery first reads it through the normal Linux SSH reader without
repeatedly querying the guests. The complete declared state is then verified
over SSH, with different devices read concurrently. Readers on each device remain serial. The original
hard deadline includes both stages; native cancellation stops pending reads
when that deadline expires, including connection retry delays. No check or
deadline is removed or relaxed.

SHA-256: `0a6e2fe1d872e73ac5a4869e1010762a9db8a91acd9c44a6fd03d058f1270790`.

The suite pins this archive through uv.lock, so normal commands need neither a
sibling checkout nor a temporary dependency override. Replace it with a
qualified upstream revision after release.

The runtime source is committed as [Networka 8b504ba](https://github.com/narrowin/networka/commit/8b504ba1b8f12f6d30ce6496d9e8c08816149424). The bundled artifact changes only the package version to identify this qualification.
