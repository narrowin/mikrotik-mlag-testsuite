# The old mlag-lab suite was replaced as a whole and deleted

The old suite was the `mlag-lab` runner in `src/mlag_lab/` and the labs in `labs/`.
On 2026-11-25 the operator chose to replace it as a whole with Networka tests under `tests/`, not one test at a time.
He asked: "why not replace the whole thing when we're on it now? ... Why selectively?"
It was deleted on 2026-11-27 in commit `5f68809`.
Its code, and how `results/` was produced, are at commit [`95c7482`](https://github.com/narrowin/mikrotik-mlag-testsuite/tree/95c7482).

`results/` stays in the repository as the frozen record of the old suite.
Nothing writes to it any more, and it is quoted only as that record, at a pinned commit.
Runs of the old suite are not in Networka's evidence format, so `nw test replay` does not judge them.
