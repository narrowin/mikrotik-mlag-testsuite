# A run keeps only the capture slices that prove its verdict, and captures are never published

When a run is judged, the judge cuts out of the packet captures only the slices that prove its verdict and keeps them in the run's folder.
The full captures are then deleted.
A finished run's folder is compressed to save space.
Packet captures and compressed run folders are never committed to git or published anywhere.
Reports, verdicts, configs and the commands to rerun a test are committed; readers who want packets rerun the test.
Raw captures may still go privately to MikroTik support for a ticket.

## Why

On 2026-11-24 one campaign's evidence was about 315 MB, and full captures later piled up to 21 GB on the lab VM.
The operator rejected publishing them: anyone can rerun the committed labs, so a public copy of the packets adds nothing.
Removing large files from git history later takes coordinated work, so they must never enter it.
On 2026-11-25 he also rejected keeping full captures of failed runs for later manual analysis: "get rid of them only keep what is needed for proof after a run".
Cutting the evidence down to the slices that prove the verdict is part of every run, not a cleanup step afterwards.

## Considered options

Git, Git LFS, GitHub release assets, object storage addressed by SHA-256, a GitHub Pages site and a hosted database were all weighed for publishing evidence and rejected.

## What is built

- Networka keeps every per-point capture in `captures/` of the run folder, and `nw test replay` judges from those full captures ([ADR 0010](0010-replay-judges-a-saved-run-again-and-must-give-a-byte-identical-result.md)).
- The root `.gitignore` ignores `test-results/`, where runs are saved, and every `*.pcap`, `*.pcapng` and `*.tar.gz` under `results/`.
- The old suite's `mlag-lab prune` kept the packets that proved a failed run in `proof.tar.gz` and deleted the rest. It was deleted with the old suite; its code is in [`src/mlag_lab/cli.py`](https://github.com/narrowin/mikrotik-mlag-testsuite/blob/95c7482/src/mlag_lab/cli.py) at `95c7482`.

## What is not built

Networka does not cut capture slices, does not delete full captures and does not compress a finished run.
Replay must then judge from the kept slices and still give a byte-identical result; how it does so is not designed yet.
