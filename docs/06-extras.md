# 6. Other Important Things

Things not covered elsewhere that will matter during the project and the job search.

---

## 6.1 Legal, privacy and safety rules (read before recording anything)

### Filming the public road

- **Process on the device; keep raw video private.** Store detections, tracks, counts and short clips needed for labelling. Delete raw recordings you no longer need.
- **Blur faces and licence plates** in every image or GIF that leaves the Pi (the `privacy` module in `common/` and the `privacy-guard` agent exist for this).
- **No identification of people.** No face recognition, no long-term re-identification of passers-by. Re-identification embeddings stay in memory for seconds only.
- **Nothing that reveals your location** in public repos or posts: no recognisable buildings, street signs, shop names; no map registration results; no GPS logs. For the navigation module, use a satellite tile of a neutral area.
- **Martial-law restrictions:** do not film or publish military vehicles, convoys, checkpoints, air-defence activity, critical infrastructure or the aftermath of strikes. If something like that appears in a recording, delete it.
- **Drones:** the plan needs **no outdoor flights**. Navigation testing uses the desk rig and PX4 simulation. Check current rules before any flight.

### Electrical safety

- Power servos from a **separate 5V supply**, never from the Pi's 5V pin; connect grounds.
- Use the official-spec 27W supply for the Pi; cheap supplies cause brown-outs that look like software bugs.
- If you build the cat deterrent with water: keep electronics above and away from the water path; use a light mist only.

---

## 6.2 Training without a local GPU

| Option | Good for | Notes |
|---|---|---|
| Google Colab (free / paid tiers) | Short training runs, conversion | Sessions time out; checkpoint every epoch and resume |
| Kaggle notebooks | Longer free GPU quota per week | Datasets can live in Kaggle Datasets |
| Paid cloud GPU by the hour (any provider) | Final training runs, Hailo compilation on x86 Linux | Budget a few dollars per final run; stop instances when done |

Habits that save time:

- The notebook only **calls code from the repo** (`!git clone`, `!pip install -e common/`, `!make -C street-detector train EXP=...`). No logic lives only in a notebook.
- **DVC pull/push** at the start/end of every session.
- **Experiment tracking** (W&B or MLflow) so results survive the session.
- Use the **laptop NPU** for inference benchmarks (OpenVINO or the vendor's ONNX Runtime provider), not training.

---

## 6.3 Risks and how to handle them

| Risk | Effect | Mitigation |
|---|---|---|
| Hardware delivery takes 3+ weeks | Lost time | Start T1 part A (cloud training, laptop benchmarks) immediately; it needs no hardware |
| AI HAT+ stays expensive | Budget | Keep CPU (ncnn) as the main target until a good offer; the benchmark story works with CPU + laptop NPU too |
| Hailo compilation fails on a model | Deployment blocked | Use model architectures from the Hailo model zoo; keep a fallback model that is known to compile |
| Night images unusable through glass | T5 results weak | Black hood, room lights off; if still bad, document it as a finding and plan T7 (thermal, window open) |
| Rare classes (cats, dogs) too few | Weak per-class results | Oversample, add public data for those classes, report honestly |
| Scope creep | Never finishing | Follow the milestone order; apply to jobs after T1–T3 regardless of T4–T6 |
| Over-reliance on AI agents | Can't explain own code in interviews | Write core algorithms yourself; keep the learning log (doc 05, section 5.7) |
| Burn-out alongside a job | Project stops | 10–15 h/week is enough; one measurable step per week is real progress |

---

## 6.4 Learning resources (core, not exhaustive)

**Geometry and calibration**

- *Multiple View Geometry in Computer Vision* (Hartley, Zisserman): homography, epipolar geometry, camera models. Read chapters on projective geometry, cameras, homography estimation.
- *Computer Vision: Algorithms and Applications* (Szeliski, free online): broad reference for everything in T0, T4, T6.
- OpenCV calibration and homography tutorials.

**Estimation and tracking**

- *Probabilistic Robotics* (Thrun, Burgard, Fox): Kalman filter, EKF, particle filters (T2, T6).
- "Kalman and Bayesian Filters in Python" (Labbe, free online, interactive).
- Papers: SORT, DeepSORT, ByteTrack; HOTA metric paper.

**Detection and deployment**

- Ultralytics documentation (training, export).
- Hailo developer documentation and model zoo; ncnn documentation; OpenVINO documentation.
- Papers/guides on post-training quantization vs quantization-aware training; knowledge distillation (Hinton et al.).

**Navigation**

- ORB-SLAM and VINS-Mono papers (to understand what full systems do).
- SuperPoint and LightGlue papers (learned matching).
- PX4 documentation: SITL, Gazebo, using vision instead of GPS (external vision / `VISION_POSITION_ESTIMATE`).

**C++**

- *A Tour of C++* (Stroustrup) for modern C++ essentials.
- *C++ Concurrency in Action* (Williams) for the T3 threading model.
- `perf` and flame-graph tutorials for profiling on Linux.

---

## 6.5 Presenting the project

### On GitHub

- Pin the single `edge-cv` repo. The top-level README links to each task's results; each task README starts with: **one GIF, one results table, three sentences on what it does.**
- The top-level README carries the diagram of how the folders connect and links to each task's results. A component that becomes strong enough to stand alone (e.g. the C++ tracker) can later be split into its own repo with its history.
- Include a "What didn't work" section in every task README. Interviewers love it.

### In the CV

Describe the project as one entry with measurable bullets, for example:

- "Built a real-time edge perception system on Raspberry Pi 5 + Hailo-8L: street detector (own dataset, teacher-student labelling), INT8 deployment at N FPS with X mAP loss vs FP32."
- "Wrote a C++17 multi-object tracker in metric road coordinates (Kalman + ByteTrack-style association); speed estimation within ±Y km/h of GPS."
- "Implemented visual odometry + map matching + EKF localization; Z m ATE on desk rig; PX4 SITL flight with GPS disabled."

Fill in the real numbers as you get them. Name the tools exactly as the vacancies do (YOLO, ONNX, ncnn, Hailo, C++17, OpenCV, Kalman/EKF, PX4, MAVLink, DVC, W&B), so automatic filters find them.

### Interview preparation

Be ready to explain, on a whiteboard, without notes:

- How YOLO-style detection works end to end; what mAP@50-95 means; why INT8 loses accuracy and how calibration helps.
- Kalman filter predict/update equations; what Q and R do; why tracking in metres beats pixels in your setup.
- Homography: what it is, minimal points, why RANSAC, when a homography is wrong (non-planar scenes).
- Your T3 architecture: why bounded queues and dropping frames; where the latency goes.
- One failure you found and fixed, with numbers.

Typical take-home tasks for these roles: train/fine-tune a detector on a small dataset and report metrics; implement a simple tracker; optimise a slow OpenCV pipeline. Your task folders are practice for all three.

---

## 6.6 Job search practicalities

- **When to apply:** after T1 + T2 + T3 (~week 12). Middle roles at Everstar, DroneControl, Milltech Recruitment-type companies and Dwarf Engineering-type C++ roles match this stage.
- **Tailor per cluster:** perception/edge roles → lead with T1/T3 numbers; navigation roles → lead with T6; C++ roles → lead with T2/T3 C++ and profiling.
- **Watch both boards:** DOU (including the DefTech section) and Djinni (DefTech filter). Many roles are posted through recruiting agencies (Everstar, ITExpert, Eleven), which often handle several companies; one good contact there opens several doors.
- **English:** most roles ask for B1–B2 for documentation and papers; practise explaining the project in English.
- **Offer details** in this sector often include official employment and mobilisation reservation; ask about them explicitly during interviews, as conditions vary by company.
- **Communities:** DOU forums and meetups on DefTech/AI, open-source contributions to tools you use (OpenCV, ncnn, ByteTrack implementations, PX4) are visible signals to hiring managers.

---

## 6.7 Budget and time tracking

- Keep a simple `docs/budget.md`: item, date, price, link. Useful for your own control and for future upgrades (thermal, Jetson).
- Track hours per task roughly; after T1 you will know your real speed and can adjust the timeline in `02-project-overview.md`.
