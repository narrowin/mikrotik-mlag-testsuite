# One run of a Networka lab test

Networka is the test engine. This repo holds the lab and the test files. One command runs a test.

## The files

| File | Repo | What it is |
| --- | --- | --- |
| [tests/small/lab.yaml](../tests/small/lab.yaml) | this repo | What all tests of the Small lab share: the 22 checks of a healthy lab, the 5 ping streams and the capture points. |
| [tests/small/bond-member-loss.yaml](../tests/small/bond-member-loss.yaml) | this repo | The test: its purpose and two steps with their limits. |
| [labs/small/small.clab.yml](../labs/small/small.clab.yml) | this repo | The lab: two CHR switches, the Linux clients and the cables. |
| [labs/networka/small.yml](../labs/networka/small.yml) | this repo | The device list with addresses and logins for Networka. |
| `commands/test.py`, `labtest.py`, `lab.py`, `traffic.py`, `intent.py` | Networka | The engine: the command, the order of a test, captures and pings, the outage measurement, the device checks. |

## What happens

You start `nw test run` on the lab host as root. One `nw` process does everything below. The device checks go over SSH. The pings and captures are processes on the lab host that run inside the network namespace of a node.

1. It reads the test file and the lab file and checks every field.
2. It reads the node and cable list that containerlab wrote when the lab was deployed.
3. It runs the 22 checks on both switches and both clients. If one fails, nothing else happens.
4. It starts one capture per capture point.
5. It starts the 5 ping streams. Each sends one ping every 100 ms.
6. It waits for a quiet window of 5 s. No ping may be lost. Otherwise no cable is touched.
7. Step "Member down": it takes the cable from client 1 to switch 1 down at both ends and waits 8 s.
8. Step "Member back": it brings the cable back and waits 11 s.
9. It runs the 22 checks again.
10. It stops the pings and captures, measures from the captures how long each stream stopped, compares that with the limit and saves the folder.

## Run it

```sh
sudo nw test run tests/small/bond-member-loss.yaml --lab <lab folder> --config <device list> --save out
nw test replay out/bond-member-loss
```

The first command runs the test. The second one judges the saved folder again without the lab and must give the same result. The exit status is 0 for pass, 1 for fail and 2 for error.

## What came out

Live run on 26 November 2026. The verdict was pass, and the replay gave the same result. Every stream sent one ping every 100 ms, so 24 lost pings mean that traffic stopped for about 2.4 s. All five streams run through the two switches.

| Stream | Cable down | Cable back | Limit |
| --- | --- | --- | --- |
| 101, client 1 to the third host | 0 to 0.21 s, 1 ping lost | 2.41 to 2.62 s, 24 lost | 3 s |
| 201, the third host to client 1 | 0 to 0.21 s, 1 ping lost | 2.41 to 2.61 s, 24 lost | 3 s |
| 302, client 1 to client 2 | nothing lost | 2.41 to 2.61 s, 24 lost | 3 s |
| 102 and 202, client 2 and the third host | nothing lost | nothing lost | 0 s |

That run used the same test with the earlier file layout. The layout with `lab.yaml` has not run live yet.

## The saved folder

`test.yaml` and `lab.yaml` as they ran, the device replies of both state checks, one capture per capture point, one ping log per stream, `events.jsonl` with every action and its time, `result.json` and `timeline.tsv`.

## Not built yet

- The lab is deployed by `labs/campaign.sh`, and spanning tree is switched off by hand before the test.
- The lab still has a direct cable between the two clients. No stream uses it.
- Nothing checks that the cable that goes down carried the test streams.
- The only action is a cable that goes down or comes back.
- The engine has not been reviewed.
