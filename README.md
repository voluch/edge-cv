# edge-cv

Real-time computer vision on a Raspberry Pi 5: a camera at a 4th-floor window watches a public road and, entirely on the device, **detects** people, cars, bikes, cats and dogs, **tracks** them in real-world metres, measures **speed and counts**, and keeps working in any light and weather. A pan-tilt mount adds moving-camera tracking, and a desk rig adds **GPS-free localization** against a printed satellite map.

> **Status:** planning done, implementation starting. Results tables and GIFs will appear here as each task lands.

## Hardware

Raspberry Pi 5 (4 GB), Camera Module 3, AI HAT+ (Hailo-8L), pan-tilt kit. Training runs in the cloud; a laptop NPU is an extra inference target.

## Tasks

One folder per task. Each has its own README with results first.

| ID | Folder | What | Results |
|---|---|---|---|
| — | `common/` | Shared library: camera I/O, calibration types, data formats, metrics, logging | — |
| T0 | `rig-calib/` | Window rig, camera calibration, image-to-road homography | *soon* |
| T1 | `street-detector/` | Train and deploy a street detector (VisDrone → own data → INT8 on NPU) | *soon* |
| T2 | `tracker/` | C++ multi-object tracker in metric road coordinates; speed and counts | *soon* |
| T3 | `edge-runtime/` | 24/7 C++ pipeline on the Pi: capture → NPU → tracker → stream and alerts | *soon* |
| T4 | `pan-tilt/` | Scanning with motion compensation, click-to-follow | *soon* |
| T5 | `robustness/` | Accuracy by condition, active-learning data loop | *soon* |
| T6 | `gnss-free-nav/` | Visual odometry + map matching + EKF, PX4 simulation | *soon* |
| T7 | `thermal/` | Thermal camera fine-tuning and fusion (later) | — |
| F1 | `cat-deterrent/` | Optional fun project | — |

Folders appear as each task starts.

## How the parts connect

```
common/ ──► T0 rig-calib ──► T1 street-detector ──► T2 tracker
                 │                   │                   │
                 └───────────────────┴──► T3 edge-runtime ◄── T4 pan-tilt
                                              │
                                              ▼
                                  T5 robustness ──► new labels ──► T1
T6 gnss-free-nav: separate desk-rig track, reuses common/
```

## Documentation

Plan, task specs and conventions are in [`docs/`](docs/README.md):

- [Project overview and timeline](docs/02-project-overview.md)
- [Task specs](docs/03-tasks/)
- [Agentic development setup](docs/05-agentic-development.md)
- [Privacy, risks, extras](docs/06-extras.md)

## Privacy

Raw street video is never published. Faces and licence plates are blurred in any shared media, there is no identification of people, and nothing reveals the camera location. Details in [`docs/06-extras.md`](docs/06-extras.md).

## Repo layout

```
common/  rig-calib/  street-detector/  tracker/  edge-runtime/  pan-tilt/
robustness/  gnss-free-nav/  thermal/  cat-deterrent/   # one folder per task
docs/        plan, roadmap, decisions, privacy rules, learning log
.claude/     shared agents and skills for Claude Code
Makefile     top-level runner (setup, test, lint per folder)
```
