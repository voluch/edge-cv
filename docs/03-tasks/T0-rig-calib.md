# T0. Window rig and calibration (`rig-calib/`)

**Duration:** ~1–2 weeks · **Hardware:** Pi 5, Camera Module 3, black hood, printed checkerboard · **Language:** Python

## Goal

Know exactly how pixels in the camera image relate to the real world:

1. the camera's **intrinsics** (focal length, principal point, lens distortion);
2. a **homography** that maps image pixels to positions on the road surface in metres.

Every later task depends on this: speed in km/h (T2), ground-plane tracking (T2), motion compensation (T4), and the navigation module (T6) all reuse this code.

**Vacancy link:** camera calibration / camera models (~12 of 27 roles), homography/RANSAC (~8), "experience with physical cameras" (Dwarf, DroneControl, Defensetech).

## Components

| Component | Description |
|---|---|
| Pi setup script | Raspberry Pi OS Lite 64-bit, SSH, camera stack (libcamera/Picamera2), Python venv, `common/` installed (editable) |
| Window mount | Camera fixed flush to the glass, black hood (cardboard/cloth) against reflections, cable routing, fixed autofocus |
| Capture tool | Grab stills and clips with fixed exposure settings; save with metadata |
| Intrinsic calibration | Checkerboard (or ChArUco) calibration with OpenCV; reprojection error report; undistortion preview |
| Road-plane homography | Pick ≥4 (better 8–12) image points with known ground positions; fit homography with RANSAC; residual report |
| Ground-truth tools | A simple GUI to click points; a "bird's-eye view" warp of the road for visual checking |

## Steps

1. **Pi bring-up.** Flash OS, enable SSH, install the camera stack, confirm a test capture. Fix autofocus to a set distance (the road), so focus does not jump during recording.
2. **Mount the camera.** Lens against the glass with a black hood. Check reflections at night with room lights on. Note: if you later add a thermal camera, the window must be open, because glass blocks long-wave infrared.
3. **Intrinsic calibration.** Print a checkerboard (or ChArUco board) on A4/A3, glue to a rigid board. Capture 20–40 images at different positions and angles **with the same focus setting you will use at the window**. Run calibration. Target: reprojection error below ~0.5 px.
4. **Ground reference points.** Find points on the road with known distances: lane-marking dashes (standard lengths), curb segments, manhole covers, poles. Measure distances on a public map's measuring tool or with a tape measure on the pavement. Record point pairs (pixel ↔ metres) in a YAML file.
5. **Fit the homography** from undistorted pixels to road coordinates with RANSAC. Report the residual on held-out points (target: well under 0.5 m within the central area).
6. **Bird's-eye-view check:** warp the image to a top view; straight lane markings should look straight and parallel.
7. **Publish** intrinsics + homography as versioned YAML files consumed by T2/T3.

## Metrics

- Intrinsics: RMS reprojection error (px).
- Homography: error on held-out ground points (m), shown as a heat map over the image.

## Definition of done

- `rig-calib/calib/intrinsics.yaml` and `rig-calib/calib/road_homography.yaml` committed, with the report that produced them.
- A notebook or script that converts any pixel to road metres and back, with tests.
- README with: reprojection error, homography error map, bird's-eye-view image (with people/plates blurred, no landmarks that reveal the location).

## Risks and tips

- **Autofocus drift:** lock focus; recalibrate if you change it.
- **Camera moved:** the homography is only valid while the camera does not move. Add a quick check (match a few static keypoints against a reference frame on start-up and warn if they shifted).
- **Non-flat road:** a homography assumes a flat plane. Restrict speed measurement to a flat stretch.

## Stretch

- Estimate the camera pose (PnP) relative to the road; derive height and tilt, compare with a tape-measured height.
- Self-check: compute the length of a known car model from its box over a long sequence.
