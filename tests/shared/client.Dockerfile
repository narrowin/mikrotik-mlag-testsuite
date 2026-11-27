FROM alpine:3.22@sha256:49340b346798875b5592e5d420241f2f9cfba5f47e62ebb1446a1b34734e898f
# iproute2 builds the bond and reports it as JSON, and sshd lets Networka log in as root with the password in devices.yml.
RUN apk add --no-cache iproute2 openssh-server \
    && ssh-keygen -A \
    && echo 'root:admin' | chpasswd
CMD ["/usr/sbin/sshd", "-D", "-o", "PermitRootLogin=yes"]
