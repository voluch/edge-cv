# T1. Street detector: train in the cloud, run on the Pi (`street-detector/`)

**Duration:** ~5–6 weeks (part A starts before the hardware arrives) · **Hardware:** cloud GPU (RunPod), Pi 5, AI HAT+ (from week ~6), laptop NPU · **Language:** Python

## Goal

A small object detector for **person, bicycle, car, bus/truck, motorbike, cat, dog** as seen from a 4th-floor window, running in real time on the Pi, with an honest benchmark of accuracy vs speed on three hardware targets.

**Vacancy link:** detection (~21/27), edge deployment (~24/27), quantization (~11/27), TensorRT/ONNX (~13/27), ncnn/OpenVINO/TFLite (~8/27), NPU conversion (~5/27), dataset building (~10/27), distillation, low-data training, small objects (~5/27).

## Components

| Component | Description |
|---|---|
| Data: public | VisDrone (aerial/elevated views, persons and vehicles). Map its classes to the project class list |
| Data: own street | Clips recorded from the window over several days and lighting conditions; frames sampled for labelling |
| Auto-labelling (teacher) | A large open-vocabulary or large YOLO model run in the cloud over your frames to produce draft labels |
| Label correction | Hasty project; correct teacher labels; track label quality (how many teacher boxes were wrong) |
| Dataset versioning | DVC with remote storage (Google Drive or similar); fixed train/val/test split by **day**, not by frame, to avoid leakage |
| Training (student) | Ultralytics YOLO nano/small in a cloud notebook; config files in the repo; experiment tracking (W&B or MLflow) |
| Export | ONNX → (a) ncnn for the Pi CPU, (b) Hailo HEF via the Hailo Dataflow Compiler (x86 Linux, run in the cloud), (c) OpenVINO or vendor runtime for the laptop NPU |
| Quantization study | FP32 vs FP16 vs INT8; calibration-set size; post-training quantization vs quantization-aware training |
| Benchmark harness | Same test clips on every target; records FPS, p50/p95/p99 latency, power if measurable, accuracy |
| Failure gallery | Automatic collection of false positives/negatives by class, size and lighting |

## Steps

**Part A (weeks 1–3, no hardware needed):**

1. Set up the cloud notebook workflow: notebook clones the repo, pulls data with DVC, trains from a config file, pushes metrics and weights.
2. Prepare VisDrone with the project class mapping. Train YOLO-nano and YOLO-small baselines.
3. Export to ONNX and ncnn; benchmark on the laptop CPU and laptop NPU (first rows of the benchmark table).
4. Write the evaluation script: mAP@50, mAP@50-95, per-class AP, **AP by object size** (small objects matter here).

**Part B (weeks 4–7, hardware):**

5. Record street clips: different times of day, weekday/weekend, rain if possible. Save only what you need; keep it private.
6. Sample ~1,500–3,000 frames (more from rare moments: cats, dogs, cyclists). Run the teacher model in the cloud.
7. Correct the labels in Hasty (upload only selected frames with faces and plates already blurred). Record how much correction was needed (this is a nice result to report).
8. Fine-tune the student on VisDrone + street data. Compare: VisDrone-only vs street-only vs both.
9. Deploy on the Pi CPU (ncnn). Then, when the AI HAT+ arrives, compile to HEF and deploy on the NPU.
10. Run the benchmark harness on all three targets and write the results table.

## Metrics

- Accuracy: mAP@50, mAP@50-95, per-class AP, AP for small objects, on a **held-out day** of street video.
- Speed: FPS, latency p50/p95/p99 at the input sizes you test (e.g. 640 and 960).
- Quantization: mAP drop from FP32 to INT8 on each target.
- Data: teacher label precision/recall vs your corrected labels.

## Definition of done

- Results table at the top of the README:

  | Model | Input | Target | Precision | mAP@50 | Small-object AP | FPS | p99 latency |
  |---|---|---|---|---|---|---|---|

- Dataset card: classes, number of frames, conditions covered, split method, how labels were made.
- Failure gallery with 3–5 identified failure types and what you tried for each.
- Model files tracked with DVC (or attached to a GitHub release if public download is wanted); no raw street video in the repo.

## Risks and tips

- **Small objects** (cats/dogs/pedestrians far away): try a larger input size, tiled inference (SAHI-style slicing), and a small-object-aware augmentation. Measure the speed cost of each.
- **Class imbalance:** cats and dogs are rare. Oversample, and report per-class results honestly.
- **Pod interruptions and cost:** checkpoint often to the network volume; resume from the last checkpoint; stop the pod when a run ends.
- **Hailo compilation:** not every layer is supported; keep the model to standard YOLO architectures and check the Hailo model zoo for known-good configurations.

## Stretch

- Knowledge distillation with an explicit loss (teacher logits), not just pseudo-labels.
- Pruning experiment and its effect on FPS on each target.
- A night-specific model vs a single model with night augmentation.
