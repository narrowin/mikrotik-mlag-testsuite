#!/bin/bash
# Diagnostic: campus option 1 settings, but the access switch uplink as a non-edge port (edge=no), as in the
# archived layout. Samples the uplink RSTP state once a second for $1 seconds after a bridge reset and captures
# STP frames at the access switch taps and at the MLAG peers' peer-link and client 2 taps.
secs=${1:-70}
ros() { SSHPASS=admin timeout 15 sshpass -e ssh -F /dev/null -o ConnectTimeout=4 -o PubkeyAuthentication=no \
  -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR "admin@$1" "$2"; }
P1=172.30.218.11; P2=172.30.218.12; W=172.30.218.13
out=/var/tmp/pl-tools/diag; sudo -n rm -rf $out; mkdir -p $out
pids=()
for spec in witness:tap1 witness:tap2 core-mlag1:tap1 core-mlag1:tap2 core-mlag1:tap3 core-mlag2:tap1 core-mlag2:tap2 core-mlag2:tap3 traffic-host1:eth1; do
  node=${spec%%:*}; port=${spec#*:}; c=clab-mlag-medium-dc1-$node; [ $node = witness ] && c=clab-mlag-medium-dc1-access-switch1
  pid=$(sudo -n docker inspect -f '{{.State.Pid}}' $c)
  sudo -n nsenter -t $pid -n tcpdump -n -U -i $port -w $out/$node-$port.pcap stp >/dev/null 2>&1 & pids+=($!)
done
sleep 2
for ip in $P1 $P2 $W; do ros $ip "/interface bridge disable bridge"; done
for ip in $P1 $P2; do ros $ip "/interface bridge set bridge protocol-mode=none forward-reserved-addresses=no priority=0x1000"; done
ros $W "/interface bridge set bridge protocol-mode=rstp priority=0x0000; /interface bridge port set [find interface=uplink] edge=no; /interface bridge port set [find interface=ether4] edge=yes bpdu-guard=yes; /interface ethernet set ether4 loop-protect=on"
for ip in $P1 $P2 $W; do ros $ip "/interface bridge enable bridge"; done
t0=$(date +%s.%N)
ros $W "/interface bridge port print detail without-paging where interface=uplink" | grep -o "edge=[a-z-]*" | head -1
for i in $(seq 1 $secs); do
  o=$(ros $W "/interface bridge monitor bridge once; /interface bridge port monitor [find interface=uplink] once")
  t=$(awk -v a="$(date +%s.%N)" -v b="$t0" "BEGIN{print a-b}")
  printf '%5.1f %s\n' "$t" "$(grep -o -E '(root-bridge|root-bridge-id|role|edge-port|learning|forwarding|discard-transitions|forward-transitions): *[^ ]+' <<<"$o" | sed 's/: */=/' | tr '\n' ' ')"
  sleep 1
done
sudo -n kill -INT "${pids[@]}" 2>/dev/null; sleep 1
for f in $out/*.pcap; do echo "$(basename $f .pcap) stp=$(tshark -r $f 2>/dev/null | wc -l) senders=$(tshark -r $f -T fields -e eth.src -e stp.bridge.hw -e stp.flags.port_role 2>/dev/null | sort | uniq -c | tr -s ' ' | tr '\n' ';')"; done
