# T2. Multi-object tracker in real-world metres (`tracker/`)

**Duration:** ~2–3 weeks · **Hardware:** Pi 5 (development can start on the laptop with recorded video) · **Language:** C++17 core, Python bindings (pybind11)

## Goal

A tracker you wrote yourself, in C++, that keeps a stable ID for every person/vehicle/animal, works in **road coordinates (metres)** instead of pixels, and outputs **speed in km/h**, **line-crossing counts** and **trajectories**. Then measure how much re-identification helps after occlusions.

**Vacancy link:** tracking (~22/27), Kalman filtering (~9/27), C++ (~18/27 required or accepted), homography (~8/27), re-identification (Quantum, Everstar ReID), "deep understanding of tracking: tuning, stability, recovery" (B6).

## Components

| Component | Description |
|---|---|
| Kalman filter | Constant-velocity (and optionally constant-acceleration) model in road metres; process and measurement noise tuned per class |
| Measurement model | Box bottom-centre pixel → road metres via the T0 homography; measurement noise grows with distance from the camera |
| Association | ByteTrack-style two-stage matching (high-score then low-score detections); Hungarian algorithm; cost = gated distance in metres + IoU in pixels |
| Track lifecycle | Tentative → confirmed → lost → re-acquired → deleted; per-class time-outs |
| Re-identification (optional module) | Small appearance-embedding network on the NPU or CPU; used only to re-link lost tracks; embeddings anonymous and kept in memory only |
| Analytics | Speed (smoothed), direction, line-crossing counters, dwell time in zones |
| Python bindings | Use the C++ tracker from notebooks for evaluation |
| Evaluation | TrackEval (HOTA, IDF1, MOTA) on VisDrone-MOT and on a small hand-labelled street sequence |

## Steps

1. Write the Kalman filter and its unit tests (simulated straight-line motion with noise; check the estimate converges).
2. Implement association and track lifecycle. First in pixel space, to compare with a reference ByteTrack implementation.
3. Switch the state to road metres using the T0 homography; handle the distance-dependent measurement noise.
4. Speed: derive from the filter's velocity state; smooth over a short window.
5. **Validate speed:** walk past at a steady pace and ride/drive past with a phone logging GPS speed; compare. Report mean and max error.
6. Label 2–3 short street clips with track IDs (check that Hasty exports track IDs; if not, use a local CVAT for this step only). Evaluate HOTA/IDF1.
7. Add the re-identification module; measure ID switches with and without it, especially through occlusions (trees, parked cars, buses).
8. Profile on the Pi: time per frame vs number of objects.

## Metrics

- HOTA, IDF1, MOTA, number of ID switches (VisDrone-MOT + own clips).
- Speed error vs GPS (km/h), by distance from the camera.
- Counting accuracy on a manually counted 10-minute clip.
- Tracker time per frame on the Pi (µs/ms) for 10, 50, 100 objects.

## Definition of done

- C++ library with tests, installable with CMake; Python package via pybind11.
- README table: tracking metrics, speed error, counting accuracy, run time.
- Plot: speed estimate vs GPS for a validation run.
- Short write-up of tuning choices (noise values, gates, time-outs) and why.

## Risks and tips

- **Perspective:** far objects are small and noisy in metres. Use distance-dependent measurement noise; restrict speed reporting to a calibrated zone.
- **Occlusion by parked cars:** use the lost/re-acquire states before reaching for re-identification.
- **Privacy:** re-identification embeddings must not be stored or used to recognise people across days. Keep them in memory for a few seconds only.

## Stretch

- Interacting multiple-model filter (switching between constant-velocity and turning models).
- JPDA or a global association method; compare with ByteTrack-style matching.
