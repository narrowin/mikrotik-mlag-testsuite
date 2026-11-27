# The Large lab joins its sites with two straight DCI links and has one VRRP firewall per site

The Large lab has two sites, `dc1` and `dc2`, each with a core MLAG pair and a distribution MLAG pair.
The core pairs are joined by a DCI of two straight cables, `dc1-core1` to `dc2-core1` and `dc1-core2` to `dc2-core2`, bundled as one LACP bond with the same `mlag-id` at both sites.
Each site has one CHR firewall, bonded by LACP to both local cores.
The two firewalls share the VRRP address 198.18.40.1; the dc1 firewall has priority 150 and owns it, the dc2 firewall has priority 100.

## Why

On 2026-11-24 the operator kept the two straight DCI links on the condition that MikroTik documents or approves them.
The research found no MikroTik recommendation or approval for two straight links between two MLAG pairs, and one forum report of 5 to 7 s of loss on rejoin with exactly this wiring.
MikroTik's approval was never received, and on 2026-11-27 the operator kept the straight design without it.
A full mesh with diagonal links is the named alternative, needed if every loss of one chassis per tier must keep a physical path.

Earlier drafts had two gateway routers per site, then a VPN gateway and a firewall.
The operator asked: "We would have one gateway and one firewall, right? Why would there be two?"
He cut them to one firewall per site, a CHR running VRRP, and removed the VPN gateway as needless complexity.
The firewalls stay on the core; moving them to the distribution pair would change the failure path and the cabling.

## Consequences

The Large lab's DCI results describe this wiring only, not a full mesh.
A FAIL on the DCI means "this design fails", not that MikroTik says it works or does not.
The lab runs ten CHRs, about 4 GiB of memory, and counts as one of the three labs that may run with tests at once.
