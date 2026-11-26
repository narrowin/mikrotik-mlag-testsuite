# Lab tests

These files describe MLAG cases as data for Networka's lab tests, `nw test run` and `nw test replay`. The [Networka guide](https://github.com/narrowin/networka/blob/main/docs/lab-tests.md) describes the format.

- `small/state.yaml` lists the statements that hold in a healthy Small lab with spanning tree off. Each statement names the Networka intent checks that prove it.
- `small/baseline.yaml` observes the seven streams of the link-fault runner for 5 s without an action and allows no lost probe.
- `small/bond-member-loss.yaml` is the catalogue case `bond-member-loss`. Client 1's cable to CHR 1 goes down for 8 s and comes back, and each step limits each stream's outage.

Run the tests as root on the lab host, in the `mlag-external` VM, against a deployed Small lab. The lab starts with RSTP, so set spanning tree off on both CHRs first. Otherwise the state check fails and the test applies no action. `--lab` is the lab directory that containerlab wrote, and `--config` is the Networka profile of the same labs copy. `NW_USER_DEFAULT` and `NW_PASSWORD_DEFAULT` give the CHR login. The Linux nodes carry their own login in the profile. The profile checks SSH host keys, so add the keys of the four devices in state.yaml to root's known-hosts file first.

```sh
export NW_USER_DEFAULT=admin NW_PASSWORD_DEFAULT="$CHR_PASSWORD" NWK=/path/to/networka LABS=/var/tmp/mlag-labs
uv run --locked --project "$NWK" nw run dc1-core-mlag1,dc1-core-mlag2 "/interface bridge set bridge protocol-mode=none" --config "$LABS/networka/small.yml"
sudo -E env "PATH=$PATH" uv run --locked --project "$NWK" nw test run tests/small/baseline.yaml tests/small/bond-member-loss.yaml \
  --lab "$LABS/small/clab-mlag-small" --config "$LABS/networka/small.yml" --save out
uv run --locked --project "$NWK" nw test replay out/bond-member-loss
```
