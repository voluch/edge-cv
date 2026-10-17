# Conventions

## Code
- Python 3.12, `ruff` (line length 100). C++17, `clang-format` (Google-based, see `.clang-format`), `-Wall -Wextra`.
- Shared code lives only in `common/`; never copy it into task folders.
- Configs in `configs/*.yaml`; no hard-coded paths, thresholds or calibration values.
- Every task folder provides `make setup`, `make test`, `make lint`.

## Data formats
- One JSON Lines record per frame, defined in `common/` (`types.py` and `types.hpp` must stay identical). See `common/README.md`.
- Calibration is OpenCV-compatible YAML under `rig-calib/calib/`.
- Benchmark rows go to `<folder>/bench/results.jsonl` using `ecv_common.bench.BenchResult`.

## Results
- Every README starts with a results table and one GIF, then how to reproduce, then what failed and why.
- README numbers must be generated from `bench/` or `reports/` files (`/results-readme`), never typed by hand.
- Report latency as p50/p95/p99, not only averages.

## Git
- Small commits, imperative subject (`Add homography round-trip test`).
- Cross-component changes in one commit or PR, with all users updated.
- Branch per issue, PR to `main`, `test-and-review` before merge.
- Never commit data, recordings, model binaries, media outside `docs/media/`, or `.env`.

## Experiments
- One folder per experiment under `<folder>/experiments/<name>/` with config and README (`/new-experiment`).
- Fixed seeds; record git commit and DVC data version with every run.
