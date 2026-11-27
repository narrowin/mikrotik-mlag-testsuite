# Every live test runs on one pinned RouterOS development build

Every CHR in every lab runs `mikrotik/chr:7.26beta7`, pinned by its SHA-256 digest.
Other RouterOS releases are tested only after the whole suite runs on this build.
No test runs an older release as a control or for comparison.
An older version appears in the documents only as the version a forum or support report saw.

## Why

Early runs on 2026-11-24 mixed RouterOS versions, and their results could not be compared.
The operator ruled the same day that all tests run on the 7.26 development build first.
Later that day a plan added 7.25.1 runs as a positive control, and the operator removed them: "We're all doing the test with [7.26]."
One build keeps every result comparable with every other.
A floating tag would change the build under the tests without a commit.

## Considered options

- **Several releases in parallel.** Rejected: it multiplies runs before one release is understood.
- **A stable release, or a stable release as a control.** Rejected: the operator wants the development build tested first, and a control doubles every run.

## Consequences

The suite cannot show that a check would fail on another build.
Every result and comparison is tied to this one build, so changing it means rerunning every lab.
The digest is written in each `tests/*/lab/topology.clab.yml`.
The old suite's single pin, [`labs/campaign-image.txt`](https://github.com/narrowin/mikrotik-mlag-testsuite/blob/95c7482/labs/campaign-image.txt), was deleted with it, so a change of build must update every topology file.
