---
name: pi-benchmark
description: Run the standard benchmark on the Raspberry Pi for a given model version and record the results.
disable-model-invocation: true
argument-hint: [model-version] [target: cpu|hailo]
allowed-tools: Bash(ssh *), Bash(scp *)
---

Benchmark model version $0 on target $1. `PI_HOST` comes from the environment (see `.env_template`).

1. Check the Pi is reachable: `ssh $PI_HOST uptime`.
2. Make sure the model files for $0 are on the Pi under ~/models/$0/ (copy them with scp if not).
3. Run `${CLAUDE_SKILL_DIR}/scripts/run_bench.sh $0 $1` on the Pi via ssh. It plays the fixed test clip 3 times and records FPS, p50/p95/p99 latency and SoC temperature.
4. Copy the result JSON back and append it to `bench/results.jsonl`.
5. Show a one-line summary and the comparison with the previous version.

Stop and report if the SoC temperature exceeded 80 °C (thermal throttling makes the numbers invalid).
