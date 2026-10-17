---
name: export-model
description: Export a trained model ONNX → ncnn / Hailo HEF / OpenVINO with fixed steps and an accuracy check after each. Use when a new model version needs conversion for an edge target.
argument-hint: [model-version] [targets: onnx,ncnn,hef,openvino]
---

Convert model version `$0` for targets `$1` (default: onnx,ncnn).

For each target, in order:
1. Export or convert from the FP32 ONNX of `$0` (DVC-tracked). Use the calibration set from the data config for INT8, never the test set.
2. Run the accuracy check on the fixed validation set and compare with FP32. Stop and report if mAP drops by more than the threshold in the folder config.
3. Append a result row (target, precision, input size, mAP) to `bench/results.jsonl`.
4. Track the output files with `dvc add`; do not `git add` binaries and do not `dvc push` without asking.

If a layer is unsupported, write the details to `docs/deploy-issues.md` and stop; do not alter the model.
