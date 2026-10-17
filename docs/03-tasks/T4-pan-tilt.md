# T4. Moving camera: pan-tilt scanning and follow mode (`pan-tilt/`)

**Duration:** ~2 weeks · **Hardware:** pan-tilt bracket with 2 servos (MG90S recommended), PCA9685 servo driver, separate 5V supply for servos · **Language:** C++ (control loop) + Python (analysis)

## Goal

Turn the fixed window camera into a **moving platform**, because drones and gimbals move:

1. **Scan mode:** the camera sweeps across the road; tracking must survive the camera's own motion → **ego-motion / camera-motion compensation**.
2. **Follow mode:** you click an object on the stream and the mount keeps it centred with a **PID loop** → closed-loop latency, overshoot, losing and re-acquiring the object.

**Vacancy link:** ego-motion compensation / stabilization / frame registration (~6/27, central in Everstar ReID A14), optical flow (~9/27), "decision logic over inference" (A14), closed-loop real-time systems (B1, B2).

## Components

| Component | Description |
|---|---|
| Mechanics | 2-axis bracket, MG90S metal-gear servos (less jitter than SG90), camera fixed to the tilt plate, cable slack for the ribbon |
| Servo driver | PCA9685 over I2C (stable PWM, no jitter from the Pi's software PWM); servos powered from a separate 5V supply with common ground |
| Calibration | Servo command → angle mapping; camera rotation per servo step; homing and soft limits |
| Camera-motion compensation | Sparse optical flow (KLT) on background points → RANSAC homography between consecutive frames → warp track predictions into the new frame. Optionally use commanded servo angles as a prior |
| Scan controller | Slow sweep pattern; pause points; tracker keeps IDs across the sweep |
| Follow controller | Error = target centre − image centre; PID on pan and tilt; dead-band; velocity limits; feed-forward from the tracker's predicted motion |
| Target management | States: idle → locked → temporarily lost (coast on prediction) → re-acquired or released |
| Logging | Command, measured error, latency per loop iteration, for step-response plots |

## Steps

1. Assemble the mount; wire PCA9685 (I2C) and the separate servo supply; test sweeps. Note: servos must not be powered from the Pi's 5V pin under load.
2. Calibrate servo steps to angles; set soft limits so the cable never pulls.
3. **Motion compensation:** record sweeps; implement KLT + homography; compare tracking (IDF1, ID switches) with and without compensation.
4. **Follow mode:** implement the PID loop; tune on a slowly walking person/car; record step responses (time to centre, overshoot).
5. Measure the full loop latency: detection timestamp → servo command → object centred.
6. Handle loss: coast on the Kalman prediction for N frames, then search, then release.

## Metrics

- Tracking with vs without compensation during sweeps: IDF1, ID switches, track fragmentation.
- Follow mode: centring error (pixels, RMS), settling time, overshoot, % of time the target stays within the central zone.
- Control-loop latency (ms) and its effect on centring error.

## Definition of done

- Side-by-side video: sweep with and without motion compensation (blurred).
- Step-response plots and the tuned PID values with a short explanation.
- README table: compensation ablation, follow-mode metrics, latency.

## Risks and tips

- **Servo jitter and backlash** make the image shake; that is realistic and good for testing stabilisation, but MG90S + PCA9685 keep it manageable.
- **Ribbon cable fatigue:** leave slack and limit pan range to ~±60°.
- **Privacy:** follow mode is for cars, bikes and animals in the demo. Do not publish footage that follows a specific person.

## Stretch

- Electronic stabilisation (warp each frame to cancel jitter) and compare with mechanical-only.
- Use commanded angles + homography together in a small filter to estimate camera rotation more robustly.
