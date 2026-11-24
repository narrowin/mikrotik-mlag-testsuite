# Security policy

## Reporting a vulnerability

Report security problems privately through GitHub: open the repository's **Security** tab and choose **Report a vulnerability**. Do not open a public issue.

Include what you found, how to reproduce it and what it affects. We aim to reply within five working days.

## Scope

This repository is a test lab. It deploys RouterOS CHR and Linux containers on isolated Docker networks and runs privileged lab commands with `sudo` on the machine you run it on.

- **In scope:** problems in this repository's scripts, runner and container setup, for example a command that exposes a lab device outside its Docker network or runs untrusted input with root rights.
- **Out of scope:** vulnerabilities in RouterOS itself. Report those to MikroTik at [mikrotik.com/support](https://mikrotik.com/support).

## Lab credentials

The lab CHRs use Containerlab's documented default login. Never expose a lab management network beyond your machine, and never reuse lab settings on production devices.
