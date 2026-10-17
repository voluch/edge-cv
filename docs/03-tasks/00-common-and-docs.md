# Shared parts of the monorepo: `docs/`, `.claude/` and `common/`

These parts are not portfolio pieces on their own. They keep the task folders consistent and stop the same code being written several times. All of it lives in the single `edge-cv` repository.

---

## Repo root: docs, Claude Code config, tooling

**Purpose:** the single source of truth for the plan, shared agent and skill definitions, the task runner and CI.

**Contents:**

```
edge-cv/
├── README.md                  # project story, diagram, links to each task's results
├── CLAUDE.md                  # repo-wide rules for Claude Code (short)
├── .claude/
│   ├── settings.json          # permissions (allow / ask / deny)
│   ├── agents/                # all subagents, defined once
│   └── skills/                # all skills, defined once
├── docs/
│   ├── roadmap.md             # timeline from 02-project-overview.md, updated weekly
│   ├── decisions/             # architecture decision records (ADR-001-... .md)
│   ├── conventions.md         # naming, data formats, commit style, results format
│   ├── privacy.md             # the recording and publishing rules
│   ├── learning-log.md
│   └── budget.md
├── Makefile                   # top-level runner: setup, test, lint per folder
└── .github/workflows/         # CI with path filters
```

**Definition of done:** `make test` runs the tests of every folder that exists; the CI runs only the affected folders; a new task folder can be started by copying a short checklist (README, CLAUDE.md, configs, tests, Makefile targets).

---

## `common/` (shared library)

**Purpose:** code that more than one task needs. A Python package (editable install) and a C++ CMake library, used directly by the other folders. No version tags: a change in `common/` and its users goes in one commit.

### Components

| Module | Python | C++ | What it does |
|---|---|---|---|
| `io.camera` | ✓ | ✓ | Open Pi camera (Picamera2 / libcamera), USB/V4L2 camera, or a video file through one interface; monotonic timestamps on every frame |
| `io.recorder` | ✓ | | Record clips with metadata (timestamp, camera settings) for datasets |
| `geometry` | ✓ | ✓ | Load/save intrinsics and homographies (OpenCV YAML); pixel ↔ road-plane transforms; undistortion |
| `types` | ✓ | ✓ | Shared data formats: `Detection`, `Track`, `FrameMeta`; JSON Lines serialization |
| `metrics` | ✓ | | Wrappers for mAP (detection), HOTA/IDF1/MOTA (tracking, via TrackEval), latency statistics (p50/p95/p99) |
| `bench` | ✓ | ✓ | Timing helpers, benchmark result schema, Markdown table generator for READMEs |
| `privacy` | ✓ | ✓ | Face and licence-plate blurring for any exported media |
| `logging` | ✓ | ✓ | Structured logs (JSON) with consistent fields |

### Shared data format (JSON Lines, one record per frame)

```json
{"frame": 1234, "t_ns": 1739000000123456789, "dets": [{"cls": "car", "score": 0.91, "xyxy": [412, 233, 520, 301]}],
 "tracks": [{"id": 17, "cls": "car", "xyxy": [410, 231, 519, 300], "ground_xy_m": [12.4, 3.1], "speed_kmh": 34.2}]}
```

Every task reads and writes this format, so outputs from T1 feed T2, T2 feeds T3, and T3 logs feed T5 without glue code.

### Definition of done

- `pip install -e common/` works on the laptop, on a RunPod pod or Colab (after `git clone`) and on the Pi.
- The C++ part builds on the Pi with CMake and is used by other folders with `add_subdirectory(common)` or a CMake target.
- Unit tests for geometry (round-trip pixel → ground → pixel), serialization and metrics.
