# One startup config for all ten CHRs. Containerlab selects the role by node name.
{{- if eq .ShortName "dc1-firewall" "dc2-firewall"}}
# The firewall is an ordinary LACP partner of both local cores. lacp-rate=1sec matches the cores.
/interface bonding add name=cores mode=802.3ad slaves=ether2,ether3 lacp-rate=1sec
/interface vlan add name=vlan390 interface=cores vlan-id=390
/ip address add address=198.18.40.{{if eq .ShortName "dc1-firewall"}}2{{else}}3{{end}}/24 interface=vlan390
# Both firewalls share VIP 198.18.40.1 over the DCI. The higher priority makes dc1 the owner, and the default preemption returns the VIP to dc1.
/interface vrrp add name=vrrp390 interface=vlan390 vrid=39 priority={{if eq .ShortName "dc1-firewall"}}150{{else}}100{{end}}
/ip address add address=198.18.40.1/32 interface=vrrp390
{{- else if eq .ShortName "dc1-core1" "dc1-core2" "dc2-core1" "dc2-core2"}}
# Each core pair gives a bond the same mlag-id on both peers. lacp-rate=1sec lets a member rejoin in seconds, not 30 to 90 s.
/interface bonding add name=dist mode=802.3ad mlag-id=31 slaves=ether3 lacp-rate=1sec
/interface bonding add name=firewall mode=802.3ad mlag-id=32 slaves=ether5 lacp-rate=1sec
/interface bonding add name=dci mode=802.3ad mlag-id=33 slaves=ether4 lacp-rate=1sec
# Lower MLAG priority makes core1 the MLAG primary in every deployment.
/interface bridge add name=bridge vlan-filtering=yes protocol-mode=none mlag-peer-port=ether2 mlag-priority={{if eq .ShortName "dc1-core1" "dc2-core1"}}10{{else}}20{{end}}
/interface bridge port add bridge=bridge interface=ether2
/interface bridge port add bridge=bridge interface=dist
/interface bridge port add bridge=bridge interface=firewall
/interface bridge port add bridge=bridge interface=dci
# VLAN 390 joins the traffic hosts of both sites and both firewalls. It is the only VLAN on the cores.
/interface bridge vlan add bridge=bridge tagged=ether2,dist,firewall,dci vlan-ids=390
{{- else}}
/interface bonding add name=core mode=802.3ad mlag-id=21 slaves=ether3 lacp-rate=1sec
/interface bonding add name=traffic mode=802.3ad mlag-id=22 slaves=ether4 lacp-rate=1sec
/interface bonding add name=service mode=802.3ad mlag-id=23 slaves=ether5 lacp-rate=1sec
# Lower MLAG priority makes dist1 the MLAG primary in every deployment.
/interface bridge add name=bridge vlan-filtering=yes protocol-mode=none mlag-peer-port=ether2 mlag-priority={{if eq .ShortName "dc1-dist1" "dc2-dist1"}}10{{else}}20{{end}}
# The site VLAN, 110 at dc1 and 120 at dc2, stays on the distribution pair. It matches the host subnets 10.110.0.0/24 and 10.120.0.0/24.
{{- $site := "120"}}{{if eq .ShortName "dc1-dist1" "dc1-dist2"}}{{$site = "110"}}{{end}}
/interface bridge port add bridge=bridge interface=ether2
/interface bridge port add bridge=bridge interface=core
/interface bridge port add bridge=bridge interface=traffic pvid={{$site}}
/interface bridge port add bridge=bridge interface=service pvid={{$site}}
/interface bridge vlan add bridge=bridge tagged=ether2 vlan-ids={{$site}}
/interface bridge vlan add bridge=bridge tagged=ether2,core,traffic vlan-ids=390
{{- end}}

# Send the log to the collector from the management VRF via its management interface.
/system logging action add name=collector target=remote remote=172.30.120.10 vrf=mgmt
# interface records port changes and script records test markers. Severity rules capture MLAG and VRRP problems across topics.
/system logging add action=collector topics=interface
/system logging add action=collector topics=script
/system logging add action=collector topics=warning
/system logging add action=collector topics=error
/system logging add action=collector topics=critical
{{- if eq .ShortName "dc1-firewall" "dc2-firewall"}}
# vrrp records each firewall's master and backup changes.
/system logging add action=collector topics=vrrp
{{- end}}

# RouterOS 7.26beta7 can leave remote logging silent after reboot. Reselect the VRF after its route is active.
# Poll for 10 s to cover the management startup time seen on this CHR.
/system scheduler add name=refresh-collector start-time=startup policy=read,write on-event={
    :for attempt from=1 to=10 do={
        :if ([:len [/ip route find where routing-table=mgmt dst-address=0.0.0.0/0 active]] > 0) do={
            /system logging action set [find where name="collector"] vrf=main
            /system logging action set [find where name="collector"] vrf=mgmt
            :return ""
        }
        :delay 1s
    }
    :log error "collector logging could not find the active management route"
}
