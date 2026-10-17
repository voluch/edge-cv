---
name: calibrate-camera
description: Guided intrinsic calibration and road-homography fitting with an error report. Use when calibrating the camera or re-fitting the road homography in rig-calib.
argument-hint: [images-dir] [ground-points.csv]
---

Calibrate using images in `$0` and ground points in `$1` (ask if missing).

1. Intrinsics: detect checkerboard/ChArUco corners with OpenCV, reject blurred or duplicate views, calibrate, and report mean reprojection error and per-image outliers (target well below 1 px). Save `rig-calib/calib/intrinsics.yaml`.
2. Undistort the ground points, fit the homography with RANSAC (`ecv_common.geometry.Homography`), hold out about 25 % of the points, and report the held-out error in metres (target under 0.5 m in the central area).
3. Save `rig-calib/calib/road_homography.yaml` and produce a residual heat map and a bird's-eye-view image in `rig-calib/reports/`.
4. Write the numbers to `rig-calib/reports/calibration.json`. Never hard-code calibration values anywhere else.
5. Before any image leaves `reports/`, run `/privacy-check`.
