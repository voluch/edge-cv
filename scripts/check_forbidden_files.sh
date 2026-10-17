#!/usr/bin/env bash
# Fail if git tracks files that must never be committed: secrets, data, recordings,
# model binaries, raw media outside docs/media/.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

bad=$(git ls-files | grep -E \
  -e '(^|/)\.env$' -e '(^|/)\.env\.[^/]*$' \
  -e '(^|/)(data|recordings)/' \
  -e '\.(hef|onnx|pt|pth|ckpt|engine|tflite|param|bin|npz)$' \
  -e '\.(mp4|avi|mov|mkv|jpg|jpeg|png|gif|webp)$' \
  | grep -vE -e '(^|/)\.env\.(example|sample|template)$' -e '^docs/media/' || true)

# ncnn .bin / images are allowed only as small test fixtures under tests/ or fixtures/
bad=$(printf '%s\n' "$bad" | grep -vE '/(tests|fixtures)/' || true)

if [ -n "$bad" ]; then
  echo "Forbidden files are tracked:" >&2
  printf '%s\n' "$bad" >&2
  exit 1
fi
echo "no forbidden files"
