# MikroTik MLAG test suite

This suite measures how long traffic stops when a link or switch fails in a virtual MikroTik RouterOS network. With multi-chassis link aggregation (MLAG), a device can combine links to two switches into a single connection. The tests show how well that connection survives a fault, using packet captures to measure lost traffic and score each case.

[Run the lab](#quick-start) · [See example results](#see-example-results) · [Documentation](docs/README.md)

## Quick start

Start with the **Small lab**, which connects two test hosts to the same pair of virtual switches. Your first run checks that packets reach the other host in both directions during normal operation.

### In GitHub Codespaces

You need a GitHub account and available Codespaces usage. The Codespace provides the tools and opens VS Code in your browser.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/narrowin/mikrotik-mlag-testsuite?quickstart=1)

Choose **Create codespace**, wait for setup to finish, then [run the baseline](#run-the-baseline).

### Run on your own machine

Start [OrbStack on Apple Silicon](https://orbstack.dev/download) or [Docker Engine on Linux](https://docs.docker.com/engine/install/). Install [Git](https://git-scm.com/install/), [VS Code](https://code.visualstudio.com/download), and its [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

On Linux, give your user access to Docker so VS Code can start the container. [Docker post-install steps](https://docs.docker.com/engine/install/linux-postinstall/)

1. In VS Code, open **View → Command Palette** and choose **Git: Clone**. Paste `https://github.com/narrowin/mikrotik-mlag-testsuite.git` and open the cloned folder when prompted.
2. In the Command Palette, choose **Dev Containers: Reopen in Container**. VS Code builds the environment with Containerlab and the packet capture tools. When the build finishes, [run the baseline](#run-the-baseline). [VS Code guide](https://code.visualstudio.com/docs/devcontainers/create-dev-container)

Already have a dedicated Linux lab host? Follow the [manual setup](docs/test-framework.md#execute-locally).

### Run the baseline

In VS Code, choose **Terminal → New Terminal**. Run this from the repository folder in the Codespace or local dev container.

```sh
./labs/small/quickstart.sh
```

The first run downloads the virtual switch image and may take a few minutes. `01-baseline: pass` means forwarding worked in both directions. Open the `test-results/<timestamp>/README.md` path printed in the terminal to see what passed or failed.

### Measure a test interruption

Once the baseline passes, leave the lab running and try the calibration. It blocks traffic for two seconds in one direction on a separate link between the test hosts to check that the suite measures the interruption correctly.

```sh
uv run --locked mlag-lab run --case reboot-calibration
```

`01-reboot-calibration: pass` means the measured interval covered the two-second cut. The report is in the new timestamped folder under `test-results/`. [More Small lab cases](docs/cases/README.md#small-lab)

### Clean up

When you're done, remove the lab from the same terminal. Reports stay in `test-results/`.

```sh
sudo containerlab destroy -t labs/small/small.clab.yml --cleanup
```

If you used Codespaces, choose **Stop codespace** to stop compute usage. [Your Codespaces](https://github.com/codespaces)

## See example results

See which Small lab tests passed and how long traffic stopped during link failures and switch reboots. [Small lab report](results/2026-11-24-small-lab/README.md#results)

For comparisons across lab setups, see the [campaign results](results/README.md) and the [machine-readable results index](results/index/schema.md).

## How it works

Containerlab starts virtual switches using the pinned RouterOS Cloud Hosted Router (CHR) image. The runner verifies forwarding, sends numbered probes while it applies and reverses one fault, and uses the packet captures to estimate the length of the interruption in each direction. The report compares those measurements with that test's pass criteria. [Measurement method](docs/reference/measurement.md) · [Pinned image](labs/campaign-image.txt)

## Documentation and help

- See how the Small and Medium labs are wired and what's planned for two sites. [Lab inventory](labs/README.md)
- Choose a test and find its command. [Case index](docs/cases/README.md)
- Run a campaign, inspect reports, or replay packet captures. [Operator guide](docs/operator-guide.md) · [Test framework](docs/test-framework.md#read-or-replay-a-run)
- Report a setup issue or unexpected result. Include the command you ran and the error or verdict. [GitHub issues](https://github.com/narrowin/mikrotik-mlag-testsuite/issues)

[Documentation index](docs/README.md)

## Contributing

Results from other RouterOS versions and real hardware, new test cases and fixes are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for how to share a result or open a pull request, and [SECURITY.md](SECURITY.md) to report a security problem privately.

## License

[Apache License 2.0](LICENSE). Copyright 2026 narrowin.
