---
name: pi-deploy
description: Build and copy a build to the Raspberry Pi over SSH, install the systemd unit and check health. Use only when the user asks to deploy.
disable-model-invocation: true
argument-hint: [component: edge-runtime|tracker|pan-tilt] [version]
allowed-tools: Bash(ssh *), Bash(scp *), Bash(rsync *), Bash(make *)
---

Deploy `$0` (version `$1`) to the Pi. Read `PI_HOST` from the environment (see `.env_template`; never print other `.env` values).

1. Confirm with the user which host will be written to.
2. Check the Pi is reachable: `ssh $PI_HOST uptime`; abort on failure.
3. Build for the Pi (`make -C $0 build-pi` or cross-build); run the tests first.
4. Copy the binary, config and model files to `~/ecv/$0/$1/` and switch the `current` symlink; keep the previous version for rollback.
5. Install or restart the systemd unit; wait 10 s and check `systemctl is-active` and the health endpoint.
6. On failure roll back to the previous symlink and report the logs. Report the final status in two lines.
