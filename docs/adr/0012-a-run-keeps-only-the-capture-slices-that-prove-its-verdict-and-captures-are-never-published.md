# A run keeps only the capture slices that prove its verdict, and captures are never published

Networka decides which packets a run keeps ([Networka ADR 0008](https://narrowin.github.io/networka/adr/0008-a-run-keeps-only-the-capture-slices-that-prove-its-verdict/)).
This repository never commits or publishes packet captures or compressed run folders.
Reports, verdicts, configs and the commands to rerun a test are committed; readers who want packets rerun the test.
Raw captures may still go privately to MikroTik support for a ticket.

## Why

The operator rejected publishing captures: anyone can rerun the committed labs, so a public copy of the packets adds nothing.
Removing large files from git history later takes coordinated work, so they must never enter it.

## Considered options

Git, Git LFS, GitHub release assets, object storage addressed by SHA-256, a GitHub Pages site and a hosted database were all weighed for publishing evidence and rejected.

## What is built

- The root `.gitignore` ignores `test-results/`, where runs are saved, and every `*.pcap`, `*.pcapng` and `*.tar.gz` under `results/`.
- The old suite's `mlag-lab prune` kept the packets that proved a failed run in `proof.tar.gz` and deleted the rest. It was deleted with the old suite; its code is in [`src/mlag_lab/cli.py`](https://github.com/narrowin/mikrotik-mlag-testsuite/blob/95c7482/src/mlag_lab/cli.py) at `95c7482`.

See also [Networka ADR 0008](https://narrowin.github.io/networka/adr/0008-a-run-keeps-only-the-capture-slices-that-prove-its-verdict/).
