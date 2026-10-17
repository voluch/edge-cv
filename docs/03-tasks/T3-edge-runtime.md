# T3. Real-time C++ edge runtime (`edge-runtime/`)

**Duration:** ~3 weeks · **Hardware:** Pi 5 + AI HAT+ · **Language:** C++17, CMake, small Python tools

## Goal

Replace the Python prototype with a C++ service that runs **24/7 on the Pi**: camera → NPU detector → tracker → analytics → live stream and phone alerts, with a measured latency budget and a week-long uptime test.

**Vacancy link:** C++ (~10 required, ~8 accepted), video pipelines/GStreamer (~4), profiling/multithreading (Key People, Hiring Bridge, B3), "stable FPS on limited hardware" (Key People), ROS2 (~5), production mindset (most senior roles).

## Architecture

```
[Capture thread] → bounded queue → [Pre-process] → [NPU inference (HailoRT)] → [Post-process + NMS]
       ↓                                                                              ↓
  frame timestamps                                                           [Tracker (T2 lib)]
                                                                                      ↓
                                                    [Analytics] → [Event bus] → [Telegram alerts]
                                                         ↓                    → [Logger (JSON Lines)]
                                                    [Overlay renderer] → [Encoder] → [RTSP/WebRTC stream]
```

- One thread per stage, bounded lock-free or mutex queues; drop frames under load rather than building up latency.
- Every frame carries its capture timestamp, so end-to-end latency is measured, not guessed.

## Components

| Component | Description |
|---|---|
| Capture | libcamera (or GStreamer `libcamerasrc`) with fixed exposure profiles for day/night; also a file source for repeatable tests |
| Inference backends | HailoRT (NPU) and ncnn (CPU) behind one interface; switch by config |
| Post-processing | Box decoding and NMS in C++ (or on the NPU if the compiled model includes it) |
| Tracker | T2 library |
| Streaming | Hardware-free H.264 software encode at reduced resolution (the Pi 5 has no hardware H.264 encoder), served over RTSP or WebRTC to the laptop/phone on the home network only |
| Alerts | Telegram bot: rule-based events (e.g. "dog on the road", unusual traffic count); one alert per event, rate-limited; snapshots blurred |
| Configuration | YAML: model, thresholds, zones, rules |
| Observability | Metrics endpoint or log: FPS, per-stage latency (p50/p95/p99), CPU/NPU temperature, memory, dropped frames |
| Service management | systemd unit with watchdog and automatic restart; log rotation |
| ROS2 node (optional) | Publish detections/tracks as ROS2 messages, for compatibility with robotics stacks |

## Steps

1. CMake project skeleton in `edge-runtime/` (linking `common/` and `tracker/` via `add_subdirectory`); unit tests; clang-format/clang-tidy.
2. File-source pipeline with ncnn CPU inference → reproduce the Python results exactly on a test clip (same detections within tolerance).
3. Add HailoRT backend; compare outputs CPU vs NPU.
4. Live camera capture; per-stage timing; latency histogram.
5. Tracker integration; overlay; stream to the laptop.
6. Telegram alerts with rate limiting; blur faces/plates in every image that leaves the Pi.
7. systemd service, watchdog, log rotation. Run for **7 days**; record crashes, memory growth, temperature.
8. Profile with `perf`; fix the top two hotspots; record before/after.

## Metrics

- End-to-end latency (capture → tracked result) p50/p95/p99.
- Sustained FPS and dropped-frame rate over 24 hours.
- 7-day uptime: restarts, memory growth (MB/day), max temperature, throttling events.
- CPU usage per stage; NPU utilisation.

## Definition of done

- A single binary + config runs the whole pipeline; `systemctl status` shows it healthy after a reboot.
- README: architecture diagram, latency histogram, 7-day uptime report, profiling before/after.
- Identical results between Python prototype and C++ pipeline on the test clip (documented tolerance).

## Risks and tips

- **No hardware video encoder on Pi 5:** stream at reduced resolution/frame rate, or stream only overlays + low-rate JPEG snapshots.
- **Thermal throttling:** watch the SoC temperature; the Active Cooler is required.
- **Memory:** 4GB is enough, but avoid copying full frames between stages; pass shared buffers.

## Stretch

- Custom GStreamer element wrapping the detector (B3 vacancy asks for this exactly).
- Zero-copy path from camera buffer to NPU input.
