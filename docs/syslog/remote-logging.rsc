/system/logging/action/add name=mlagLabSyslog target=remote remote=172.30.214.20 remote-port=514 vrf=mgmt remote-protocol=udp remote-log-format=syslog syslog-time-format=bsd-syslog add-topics-string=yes
/system/logging/add action=mlagLabSyslog topics=info,!warning,!error,!critical,!debug comment=mlag-lab-info
/system/logging/add action=mlagLabSyslog topics=warning,!error,!critical,!debug comment=mlag-lab-warning
/system/logging/add action=mlagLabSyslog topics=error,!critical,!debug comment=mlag-lab-error
/system/logging/add action=mlagLabSyslog topics=critical,!debug comment=mlag-lab-critical
/system/logging/add action=mlagLabSyslog topics=bridge,debug,!packet disabled=yes comment=mlag-lab-debug
