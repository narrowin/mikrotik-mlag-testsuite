FROM alpine:latest
# sshd lets Networka reach the node like any host. Root is needed for the LACP details in /proc/net/bonding.
RUN apk add --no-cache iproute2 iputils openssh-server \
    && ssh-keygen -A \
    && echo 'root:admin' | chpasswd
# Listen on the management address of eth0 only. The traffic interfaces and bonds stay untouched.
CMD exec /usr/sbin/sshd -D -e -o PermitRootLogin=yes -o PasswordAuthentication=yes \
    -o ListenAddress="$(ip -4 -o address show dev eth0 | awk '{ sub("/.*", "", $4); print $4 }')"
