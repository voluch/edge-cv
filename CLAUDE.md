# edge-cv

Edge-CV portfolio project: detection, tracking, calibration and GPS-free navigation on a Raspberry Pi 5. Plan and task specs: `docs/` (start with `docs/02-project-overview.md`, task files in `docs/03-tasks/`).

## Layout
One folder per task (`rig-calib`, `street-detector`, `tracker`, `edge-runtime`, `pan-tilt`, `robustness`, `gnss-free-nav`, `thermal`, `cat-deterrent`); shared code in `common/`. Folders are created when their task starts. Each has its own `CLAUDE.md` with local context.

## Commands
- `make setup`, `make test`, `make lint` for all folders; `make -C <folder> test` for one.

## Rules
- Shared code lives only in `common/`. Do not copy it into task folders.
- Cross-component changes go in one commit/PR with all users updated.
- Data formats are defined once in `common/types` (JSON Lines).
- Never commit data, recordings or model binaries (use DVC). Calibration YAML stays in git under `rig-calib/calib/`.
- Results go to `bench/` or `reports/` as JSON/JSONL; README tables are generated from them. Never edit numbers by hand.
- Configs in `configs/*.yaml`; no hard-coded paths, thresholds or calibration values.
- Write core algorithms (Kalman, association, homography, EKF) by hand first; agents help with tests, tooling and refactoring. Be able to explain every merged change.
- Ask before `git push`, `dvc push`, `gh release create`, or anything that writes to the Pi.

## Privacy (hard rules)
- No raw street video or unblurred images in the repo.
- No identity recognition of people; re-identification embeddings stay in memory only.
- No content that reveals the camera location (buildings, signs, GPS logs, map registration).
- No military vehicles, checkpoints or infrastructure in any recording.
