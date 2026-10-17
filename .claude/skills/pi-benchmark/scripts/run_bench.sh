#!/usr/bin/env bash
# Runs on the Pi: ./run_bench.sh <model-version> <cpu|hailo>
# Expects ~/models/<version>/ and ~/bench/bench_runner (the folder's benchmark binary/script).
set -euo pipefail

version="${1:?model version}"
target="${2:?target cpu|hailo}"
runner="${BENCH_RUNNER:-$HOME/bench/bench_runner}"
clip="${BENCH_CLIP:-$HOME/bench/test_clip.mp4}"
out="$HOME/bench/results_${version}_${target}.json"

[ -x "$runner" ] || { echo "benchmark runner not found: $runner" >&2; exit 1; }
[ -f "$clip" ] || { echo "test clip not found: $clip" >&2; exit 1; }

max_temp=0
for run in 1 2 3; do
  "$runner" --model "$HOME/models/$version" --target "$target" --clip "$clip" --out "$out.$run"
  t=$(vcgencmd measure_temp | sed -E "s/temp=([0-9.]+).*/\1/")
  max_temp=$(awk -v a="$max_temp" -v b="$t" 'BEGIN{print (b>a)?b:a}')
done

# merge the 3 runs and attach metadata (jq is installed on the Pi image)
jq -s --arg v "$version" --arg t "$target" --argjson temp "$max_temp" \
  '{model:$v, target:$t, max_soc_temp_c:$temp, runs:.}' "$out".1 "$out".2 "$out".3 > "$out"
rm -f "$out".1 "$out".2 "$out".3
echo "$out"
