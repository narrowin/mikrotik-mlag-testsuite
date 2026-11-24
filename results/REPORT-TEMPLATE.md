# Report layout

Reports are generated from saved results. Do not write or edit them by hand.

## Per suite: `results/<campaign>/<suite>/README.md`

Written by `mlag-lab run` at the end of every suite and by `mlag-lab evaluate` on replay (`src/mlag_lab/readme.py`).

1. **Title:** lab, suite folder and RouterOS version.
2. **Setup:** lab, devices, RouterOS, CHR image, platform, bridge mode, MLAG roles, MLAG and bond settings, links to the configs used.
3. **TL;DR:** one line per case with PASS, FAIL, INCOMPLETE or INVALID, and the phase that failed with its measured loss against the limit.
4. **Summary:** one row per case with the fault phase and the return phase, each with limit and measured loss.
5. **Cases:** per case, expected behaviour per phase with its source, and per run the verdict, a link to the failed check, the timeline and the device configs.
6. **Analysis:** copied from `notes.md` in the suite folder, if present.
7. **Evidence:** links to `suite.json`, `junit.xml`, `builds.json` and `inputs/`.

## All results: `results/README.md`

Written by `mlag-lab export` (`src/mlag_lab/summary.py`) from `results/index/phases.jsonl`.

1. **TL;DR:** generated. Which setups pass every case in both labs. Per lab, the setups that pass, with the number of cases each ran, and how many fail, with the longest interruption. Then how many need repeats.
2. **Recommendation:** copied from `results/notes.md`, the only hand-written part.
3. **At a glance:** per lab, the number of setups that pass, fail, are incomplete or are invalid.
4. **How to read:** the indicator: the longest traffic interruption per phase against its limit, and what PASS, FAIL, INCOMPLETE and INVALID mean.
5. **One table per lab:** one row per suite with the result, the setup in words, run counts, the longest interruption and a link to the suite report.
6. **Where the data is:** suite reports, `results/index/` and raw captures.

## Commands

```sh
uv run mlag-lab run --case <name>          # runs a suite and writes its README
uv run mlag-lab evaluate results/<campaign>/<suite>   # rebuilds verdicts and README from saved evidence
uv run mlag-lab export                     # rebuilds results/index/ and results/README.md
```
