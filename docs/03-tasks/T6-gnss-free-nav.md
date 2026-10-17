# T6. GPS-free localization (`gnss-free-nav/`)

**Duration:** ~5–6 weeks · **Hardware:** Pi 5 + camera, BNO085 IMU, overhead boom arm, a printed satellite-map poster (A1/A0) with ArUco markers; laptop for PX4 simulation · **Language:** Python first, C++ for the real-time parts

## Goal

Answer "where am I without GPS?" in three settings:

1. **Desk scale:** the camera looks down at a printed satellite map and is moved by hand or on the arm; estimate its position on the map from **visual odometry**, **absolute fixes from map matching**, and the **IMU**, fused in an **EKF**. ArUco markers on the poster give exact ground truth.
2. **Simulation:** PX4 SITL + Gazebo with a satellite-textured world; your estimator replaces GPS and the simulated drone flies on your estimates over MAVLink.
3. **Public aerial data:** geolocalization accuracy on a public UAV-to-satellite dataset.

**Vacancy link:** GPS-free navigation / VO / SLAM / map matching / VPR (~14 of 27, the second largest cluster), feature matching (~8), EKF (~9), PX4/ArduPilot/MAVLink (~5), simulation (~8), keypoint matchers like SuperPoint/LightGlue (B7, B9).

## Components

| Component | Description |
|---|---|
| Desk world | Printed satellite tile at a known scale (metres per pixel of the print), ArUco markers at the corners and scattered, arm or slider to move the camera |
| Ground truth | ArUco pose estimation per frame (PnP) → camera position on the map |
| Visual odometry | Frame-to-frame: KLT or ORB features → homography (camera looking at a plane) → relative motion; then try SuperPoint + LightGlue |
| Map matching | Match the current frame to the map tile: start with ORB + RANSAC homography against the full map; then global descriptor retrieval (find the right map patch) + local matching (exact pose) |
| IMU integration | BNO085 orientation and acceleration over I2C; time-synchronised with frames; camera–IMU extrinsics (Kalibr, or a simple rotation alignment) |
| EKF | State: position, velocity, heading (+ biases as stretch); prediction from IMU; updates from VO (relative) and map fixes (absolute); outlier rejection on fixes |
| PX4 SITL bridge | Gazebo world with a satellite texture; camera in simulation; estimator sends `VISION_POSITION_ESTIMATE` over MAVLink (pymavlink/MAVSDK); PX4 configured to use vision instead of GPS |
| Evaluation | ATE (absolute trajectory error), RPE (relative pose error), drift per metre travelled, fix success rate, time to recover after a failed fix |

## Steps

1. Print the map (local print shop, A1 or A0), fix it flat, add ArUco markers; measure the print scale.
2. Ground-truth pipeline from ArUco; validate by moving the camera along a ruler.
3. VO with homography; plot the trajectory vs ground truth; measure drift.
4. Map matching with ORB + RANSAC; then a retrieval + matching approach; compare success rate and accuracy.
5. Add the IMU; implement the EKF; show that fusing absolute fixes removes VO drift.
6. Move to simulation: PX4 SITL + Gazebo; run the same estimator on simulated camera frames; fly a square mission with GPS disabled.
7. Evaluate on a public UAV-to-satellite dataset for absolute localization error.
8. Port the time-critical parts (feature tracking, EKF) to C++ and measure the speed on the Pi.

## Metrics

- Desk: ATE and RPE (mm on the print, converted to "equivalent metres" at the map scale), drift per metre, map-fix success rate.
- Simulation: position error vs simulator ground truth; whether the mission completes with GPS disabled.
- Public data: localization error in metres, recall within X metres.
- Run time per frame on the Pi for each component.

## Definition of done

- Trajectory plots (VO only vs VO + map fixes + IMU) against ArUco ground truth.
- A screen recording of PX4 in simulation flying on your estimates with GPS disabled.
- README table with all metrics above and a section on failure cases (featureless areas, repetitive textures, fast motion, lighting).

## Risks and tips

- **Repetitive textures** (fields, roofs) cause wrong map matches: always gate fixes by the EKF's predicted position and covariance.
- **Scale:** a desk setup is a scaled-down world; report errors in both print units and equivalent map metres.
- **Simulation setup time:** PX4 + Gazebo installation can take a day; use the official Docker images.
- **Privacy:** use a satellite tile of a neutral, non-sensitive area (not your home, not infrastructure).

## Stretch

- Replace the hand-built pipeline with an existing VIO system (e.g. OpenVINS) on recorded desk data and compare.
- Particle filter instead of EKF for the map-matching stage (global relocalisation when lost).
