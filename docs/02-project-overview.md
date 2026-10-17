# 2. Project Overview: Tasks, Flow and Plan

## 2.1 The idea in one sentence

A Raspberry Pi 5 with a camera at a 4th-floor window watches a public road and, entirely on the device, **detects** people, cars, bikes, cats and dogs, **tracks** them in real-world metres, measures **speed and counts**, keeps working in **any light and weather**, follows a chosen object with a **moving pan-tilt camera**; a second module on a desk rig solves **GPS-free localization** against a printed satellite map.

Why this setup fits the vacancies:

- A camera ~12 m up looking down at an angle sees the world roughly like a low-flying drone or a surveillance camera, the viewpoint in VisDrone and most miltech job ads.
- The street provides real, unlimited, ever-changing data in all weather, for free.
- The pan-tilt mount adds the "moving platform" problems (ego-motion, gimbal tracking) without flying anything.
- The desk rig covers navigation, which the window cannot.

## 2.2 Task list (one repository, one folder per task)

| ID | Folder | Task in one line | Main skills | Hardware |
|---|---|---|---|---|
| — | `common/` | Shared library: camera I/O, calibration types, detection/track data formats, metrics, logging | Software design, Python packaging, C++ CMake | none |
| **T0** | `rig-calib/` | Window rig, camera calibration, image-to-road homography | Camera models, calibration, homography | Pi + camera |
| **T1** | `street-detector/` | Train and deploy a street detector: VisDrone → own auto-labelled data → INT8 on NPU | Detection, datasets, distillation, quantization, edge runtimes | cloud GPU; Pi + HAT |
| **T2** | `tracker/` | C++ multi-object tracker in metric road coordinates; speed, counts, re-identification | Kalman, association, C++, geometry | Pi |
| **T3** | `edge-runtime/` | 24/7 C++ pipeline on the Pi: capture → NPU → tracker → stream and alerts | C++ concurrency, GStreamer, HailoRT, profiling, reliability | Pi + HAT |
| **T4** | `pan-tilt/` | Moving camera: scanning with motion compensation, and click-to-follow gimbal tracking | Optical flow, ego-motion, PID control, closed-loop latency | Pi + pan-tilt kit |
| **T5** | `robustness/` | Day/night/weather robustness measurement and an active-learning data loop | Robustness, domain shift, MLOps, data flywheel | Pi + cloud |
| **T6** | `gnss-free-nav/` | Visual odometry + satellite-map matching + EKF on a desk rig, plus PX4 simulation | VO, feature matching, EKF, MAVLink, simulation | Pi + camera + IMU + arm |
| **T7** | `thermal/` *(later)* | Thermal camera: own-sensor fine-tuning, RGB-thermal fusion | Thermal, low-data, fusion | + thermal camera |
| F1 | `cat-deterrent/` *(optional, fun)* | Indoor: detect the cat on the table, trigger a gentle deterrent | Zone logic, actuation, latency | Pi + servo/pump |

## 2.3 How the tasks connect

```
                   ┌──────────────────────┐
                   │  common/ (lib)       │  used by every folder
                   └──────────┬───────────┘
                              │
   ┌──────────────┐    ┌──────┴──────────┐    ┌───────────────┐
   │ T0 rig-calib │───►│ T1 detector     │───►│ T2 tracker    │
   │ (homography) │    │ (model files)   │    │ (C++ lib)     │
   └──────┬───────┘    └──────┬──────────┘    └──────┬────────┘
          │                   │                      │
          │                   ▼                      ▼
          │            ┌─────────────────────────────────┐
          └───────────►│ T3 edge-runtime (C++ service)   │◄── T4 pan-tilt (control module)
                       └──────────────┬──────────────────┘
                                      │ uncertain frames, logs
                                      ▼
                       ┌─────────────────────────────────┐
                       │ T5 robustness + active learning │──► new labels ──► T1 (retrain)
                       └─────────────────────────────────┘

   T6 gnss-free-nav: separate track (desk rig), reuses common/, T0 calibration code, EKF ideas from T2
   T7 thermal: later; plugs into T1 (training), T3 (second stream), T5 (night robustness)
```

What passes between folders (everything is in one repo, so code is imported from `common/`; files live in the repo or in DVC):

| From → To | Artifact | Format |
|---|---|---|
| T0 → T2, T3 | Camera intrinsics and image-to-road homography | YAML (OpenCV-compatible), committed in `rig-calib/calib/` |
| T1 → T3 | Detector model | `.hef` (Hailo), `.param/.bin` (ncnn), `.onnx`; tracked with DVC (GitHub release only for public downloads) |
| T1 → T2 | Detection format | Defined in `common/types` (frame id, timestamp, boxes, classes, scores) |
| T2 → T3 | Tracker | C++ library (CMake target, `add_subdirectory`) + Python bindings |
| T3 → T5 | Logged uncertain frames, run statistics | Files on the Pi, synced to cloud storage |
| T5 → T1 | New labelled data | DVC-tracked dataset version |

## 2.4 Timeline (part-time, ~10–15 hours per week)

Hardware takes ~2–3 weeks to arrive from AliExpress. The plan uses that time for cloud work.

| Weeks | Work | Hardware needed | Milestone |
|---|---|---|---|
| 0 | Order Phase 1 hardware. Create the `edge-cv` repo with `docs/`, root `.claude/`, `common/` skeleton (doc 05) | none | Repo and agent setup in place |
| 1–3 | **T1 part A:** cloud training on VisDrone; ONNX export; ncnn conversion and a laptop CPU/NPU benchmark | none | First trained model, first benchmark table |
| 3–4 | **T0:** hardware arrives; Pi setup, window rig, calibration, road homography | Pi, camera | Calibrated camera, map of the road in metres |
| 4–6 | **T1 part B:** record street video; auto-label with a large model in the cloud; correct labels in CVAT; fine-tune; deploy on Pi CPU (ncnn) | Pi | Street detector running on the Pi |
| 6–7 | Order AI HAT+ (Phase 2) around 11.11 sale; Hailo conversion; CPU vs NPU vs laptop benchmark | + AI HAT+ | **Benchmark table: 3 runtimes** |
| 7–9 | **T2:** C++ tracker, metric Kalman, speed and counts; validate speed with phone GPS | Pi | **Speed in km/h with a measured error** |
| 9–12 | **T3:** C++ runtime, HailoRT, GStreamer stream, Telegram alerts; 7-day uptime test | Pi + HAT | **Checkpoint: apply to middle roles** |
| 12–14 | **T4:** pan-tilt scanning + motion compensation, click-to-follow | + pan-tilt | Moving-camera demo |
| 12–16 | **T5** (runs in background from week 9): robustness by condition, active-learning loop, one retraining round | Pi + cloud | Accuracy per condition; before/after retraining |
| 14–20 | **T6:** desk rig VO, map matching, EKF, PX4 SITL | + IMU, desk arm, printed map | **Trajectory vs ground truth; PX4 flying on your estimates** |
| later | T7 thermal, F1 cat deterrent | + thermal camera | |

**Apply early.** After T1 + T2 + T3 (~week 12), the project already covers the "must know" list and most "should know" items from `01-vacancies-analysis.md`. Start applying to middle roles then; continue T4–T6 while interviewing. The navigation module (T6) strengthens applications to the ~14 roles that mention GPS-free navigation.

## 2.5 Milestones and what each proves

| Milestone | Proves to an employer | Covers vacancy cluster |
|---|---|---|
| Benchmark table: ncnn CPU vs Hailo NPU vs laptop NPU, with mAP, FPS, p99 latency, INT8 accuracy loss | You can take a model to edge hardware and measure it honestly | Edge deployment (~24/27), quantization (~11/27), runtimes |
| Own street dataset built with a teacher model + corrections; fine-tuned student | Full data cycle, distillation, low-data training | Datasets (~10/27), distillation |
| Speed in km/h with measured error vs GPS | Camera geometry and Kalman filtering applied correctly | Calibration (~12/27), homography (~8/27), Kalman (~9/27) |
| Tracking metrics (IDF1/HOTA) with and without re-identification | Tracking depth beyond "ran ByteTrack" | Tracking (~22/27) |
| 7-day uptime of the C++ service, p99 latency histogram | Production C++ on embedded Linux | C++ (~18/27), pipelines |
| Pan-tilt follow with motion compensation | Moving-platform problems, closed-loop control | Ego-motion (~6/27), gimbal-like tracking |
| Accuracy by condition and after one active-learning round | Robustness and a data flywheel | Robustness, MLOps |
| VO + map matching + EKF trajectory error; PX4 SITL flight | GPS-free navigation | Navigation (~14/27), EKF, MAVLink, simulation |

## 2.6 Rules that apply to every task

- **Results first in every README:** a table of numbers and one GIF at the top, then how to reproduce, then what failed and why.
- **Everything reproducible:** pinned dependencies, DVC for data, a single `make` command (or script) per experiment.
- **Privacy:** no raw street video in public repos; faces and licence plates blurred in any published media; no identity recognition of passers-by; nothing that reveals your location. See `06-extras.md`.
- **Small steps:** each task is split into steps that each end in something measurable. Details are in `03-tasks/`.
