# Later and optional tasks

## T7. Thermal camera (`thermal/`), later

**Hardware:** InfiRay P2 Pro (256×192, USB-C, ~$240) or Topdon TC001 · **Duration:** ~3–4 weeks

**Goal:** a detector trained on public thermal data that works on **your own** cheap thermal sensor at night, plus RGB–thermal fusion so the street pipeline works day and night.

**Vacancy link:** thermal (~6/27, required in Everstar A2), low-data training, domain gap, multi-sensor fusion (B8, B11, A11).

| Component | Description |
|---|---|
| Capture | UVC on Linux; the stream contains the image and a 16-bit temperature value per pixel |
| Calibration | Heated foil checkerboard for intrinsics; RGB↔thermal registration (homography to the road plane from T0) |
| Data | Public aerial thermal datasets (e.g. HIT-UAV) + 300–1000 own labelled frames |
| Training | Pre-train on public data, fine-tune on own data; learning curve vs number of own frames |
| Fusion | Late fusion of RGB and thermal detections on the road plane; compare with single-sensor results by condition |

**Important practical note:** window glass blocks long-wave infrared completely. Thermal recording requires the window open (or a mount outside).

**Definition of done:** mAP on own thermal test set before/after fine-tuning; learning curve; day/night fusion results added to the T5 condition chart.

---

## F1. Cat-on-the-table deterrent (`cat-deterrent/`), optional fun project

**Hardware:** the same Pi + camera indoors, an SG90/MG90S servo pressing a spray bottle (light mist) or a small buzzer · **Duration:** ~1–2 weeks

**Goal:** detect the cat, decide whether it is really **on** the table (not just overlapping it in the image), trigger a gentle deterrent with low latency and almost no false triggers.

| Component | Description |
|---|---|
| Zone | Table surface as a polygon in a homography-rectified view (reuses T0 code) |
| Logic | State machine: enters zone → stays N frames → act → cooldown; ignores people |
| Actuator | Servo via the PCA9685 from T4, or a buzzer on a GPIO pin |
| Logging | Every trigger saved as a short clip for false-positive review |

**Keep it humane:** a light mist or a sound, aimed away from the face; never a strong jet.

**Why it is still useful for the CV:** glass-to-actuation latency, false-trigger rate, and decision logic over detections are the same engineering questions as in T4.

---

## Yard monitor with known/unknown people: only for your own property

The earlier idea (alert only on people not in an enrolled set) **does not apply to the street view**: recognising passers-by is processing personal data without consent. If you ever monitor your own yard or entrance, enrol only people who agree, keep everything local, and mask areas outside your property. It is not part of the main plan.
