# Edit the lab diagrams

Open [mlag-scenarios.drawio](mlag-scenarios.drawio) and edit the topology’s page. Keep its shared wiring and scenario notes together. In Codex, start with a request such as `$drawio Update the Medium lab page for the external-root trial and regenerate its PNG.` The official draw.io skill is included in the repository. [Local skill](../../.agents/skills/drawio/SKILL.md) · [Pinned upstream source](https://github.com/jgraph/drawio-mcp/tree/b7941af5541ba45edb72d6db164302294bf6cb40/plugins/codex/drawio/skills/drawio)

Each page explains the wiring, the question behind each test, and how to isolate the fault. The evidence links below lead to the recorded runs.

| Page index | Page | Export | Wiring reference |
| --- | --- | --- | --- |
| 1 | Small lab | `docs/diagrams/small-lab.png` | [Small Containerlab topology](../../labs/small/small.clab.yml) · [Bridge-mode comparison](../validation-plan.md#small-lab-bridge-mode-comparison) |
| 2 | Medium lab | `docs/diagrams/medium-lab.png` | [Medium lab inventory](../../labs/medium/README.md) · [Bridge-mode and root placement comparison](../validation-plan.md#matched-comparison-on-the-medium-lab) |
| 3 | Large lab | `docs/diagrams/large-lab.png` | [Proposed Site A/Site B design](../plans/two-site-design.md) · [Bridge-mode comparison](../validation-plan.md#large-lab-bridge-mode-comparison) |

Use draw.io Desktop to export the updated page. From the repo root, the CLI equivalent for page 2 is:

```sh
drawio --export --format png --page-index 2 --border 14 --scale 2 \
  --output docs/diagrams/medium-lab.png docs/diagrams/mlag-scenarios.drawio
```

When the local draw.io MCP server is available, query the workbook and compare its cable endpoints to the wiring references above. Open the PNG at documentation width to check port labels and connector routing.

## Small lab evidence

| Scenario | Evidence files |
| --- | --- |
| Carrier withdrawal and restoration | [Case and threshold](../cases/small-client-link.md) · [First verdict](../../results/2026-11-24-small-lab/reports/01-carrier/result.json) · [First packet timeline](../../results/2026-11-24-small-lab/reports/01-carrier/timeline.tsv) · [Second verdict](../../results/2026-11-24-small-lab/reports/02-carrier/result.json) |
| Silent LACP and bypass calibration | [Numbered packet bounds and checks](../../results/2026-11-24-small-lab/reports/suite.json) · [JUnit verdicts](../../results/2026-11-24-small-lab/reports/junit.xml) |
| Announced MAC move | [Earlier loss-free run](../../results/2026-11-24-small-lab/dual-homed.md#consecutive-mac-moves) · [Later suite with two failures](../../results/2026-11-24-small-lab/reports/suite.json) |
| Peer-link partition | [Measured reply gaps](../../results/2026-11-24-small-lab/postmortem.md#measurements) · [Captures and analysis](../../results/2026-11-24-small-lab/postmortem-evidence.tar.gz) |
| Direct-client reboot of each CHR | [Run commands](../operator-guide.md#reboot-the-direct-client-pair) · `final-runs-evidence.tar.gz` (saved campaign bundle) |

[Planned virtual carrier-down and physical power-loss trials](../validation-plan.md#chassis-loss-and-return)

## Medium lab evidence

| Scenario | Evidence files |
| --- | --- |
| Pair as root, primary and secondary reboot (three-CHR control) | [Report](../../results/2026-11-24-medium-lab-pair-root/README.md#development-726beta7) · [Phase data](../../results/2026-11-24-medium-lab-pair-root/phase-loss.tsv) |
| Access switch as root (three-CHR control) | [Election and failed baseline](../../results/2026-11-24-medium-lab-pair-root/README.md#root-placement-comparison) · [Captures](../../results/2026-11-24-medium-lab-pair-root/witness-root-baseline-evidence.tar.gz) |
| Archived five-CHR diagnostic fixture in both bridge modes | [Readiness summary](../cases/medium-spanning-tree.md#archived-diagnostics) |
| External root and attachment loss | [Report](../cases/medium-spanning-tree.md#archived-diagnostics) · `recovery-evidence.tar.gz` (saved campaign bundle) |
| Core-only and all-bridges-off comparisons | [Report](../cases/medium-spanning-tree.md#archived-diagnostics) · [Offline replay](../test-framework.md#replay-the-stp-off-reboots) |

## Large lab test plan

The Site A/Site B page records expected checks for proposed wiring. [Interconnect options and MikroTik sources](../plans/two-site-design.md#interconnecting-two-mlag-pairs) · [Test order](../plans/two-site-design.md#lab-order-and-stopping-points) · [Site and DCI fault procedures](../reference/site-cases.md#core-and-data-center-outage-matrix)
