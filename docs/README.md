# Edge CV Portfolio Project: Planning Pack

*Prepared 17 October 2026.*

**Goal:** build a portfolio project that covers what Ukrainian miltech computer-vision vacancies ask for at middle level (2–3 years), with stretch goals toward senior: real-time detection and tracking on an embedded device, camera geometry, C++, and GPS-free navigation.

**Repository:** one monorepo, `edge-cv`, with a top-level folder per task (`rig-calib/`, `street-detector/`, `tracker/`, ...) and shared code in `common/`. See `02-project-overview.md` and `05-agentic-development.md`.

**Setup it assumes:**

- Raspberry Pi 5 (4GB) + Camera Module 3 + AI HAT+ (Hailo-8L)
- A 4th-floor window over a public road as the main data source
- No local GPU: training happens in the cloud
- A laptop with an NPU, used as an extra inference target

## Contents

| File | What it is |
|---|---|
| `02-project-overview.md` | The tasks, how they connect, the timeline and the milestones |
| `03-tasks/` | One detailed file per task (one task = one folder of the `edge-cv` monorepo) |
| `05-agentic-development.md` | Monorepo layout, Claude Code agents, skills and conventions for setting up the projects |
| `06-extras.md` | Legal and privacy rules, risks, learning resources, interview preparation, CV presentation |

## How to use this pack

1. Read `02-project-overview.md` first. It is the map.
2. Order the Phase 1 hardware (Pi 5, Camera Module 3, power supply, microSD; the AI HAT+ later).
3. While it ships (2–3 weeks), create the `edge-cv` monorepo and set up agents following `05-agentic-development.md` and start task T1 (detector training in the cloud), which needs no hardware.
4. Work through `03-tasks/` in order. Each task file ends with a "definition of done".
