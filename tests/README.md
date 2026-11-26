# Lab tests

These files describe MLAG cases as data for Networka's lab tests, `nw test run` and `nw test replay`. The [Networka guide](https://github.com/narrowin/networka/blob/main/docs/lab-tests.md) describes the format.

- `small/lab.yaml` is the lab file of the Small lab with spanning tree off. It lists the statements that hold in a healthy lab, each with the Networka intent checks that prove it. It also lists the five streams of the link-fault runner and the extra capture points. Every test of the Small lab runs these streams and checks this state before its first step and after its last step.
- `small/bond-member-loss.yaml` is the catalogue case `bond-member-loss`. Client 1's cable to CHR 1 goes down for 8 s and comes back. The file states the purpose of the test and what should happen in each step, and each step limits each stream's outage.

Every test starts with a 5 s baseline in which no stream may lose a probe, so the lab needs no separate baseline test.

Run the tests as root on the lab host, in the `mlag-external` VM, against a deployed Small lab. The lab starts with RSTP, so set spanning tree off on both CHRs first. Otherwise the state check fails and the test applies no action. `--lab` is the lab directory that containerlab wrote, and `--config` is the Networka profile of the same labs copy. `NW_USER_DEFAULT` and `NW_PASSWORD_DEFAULT` give the CHR login. The Linux nodes carry their own login in the profile. The profile does not check SSH host keys, because labs are disposable.

```sh
export NW_USER_DEFAULT=admin NW_PASSWORD_DEFAULT="$CHR_PASSWORD" NWK=/path/to/networka LABS=/var/tmp/mlag-labs
uv run --locked --project "$NWK" nw run dc1-core-mlag1,dc1-core-mlag2 "/interface bridge set bridge protocol-mode=none" --config "$LABS/networka/small.yml"
sudo -E env "PATH=$PATH" uv run --locked --project "$NWK" nw test run tests/small/bond-member-loss.yaml \
  --lab "$LABS/small/clab-mlag-small" --config "$LABS/networka/small.yml" --save out
uv run --locked --project "$NWK" nw test replay out/bond-member-loss
```
