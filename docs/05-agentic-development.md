# 5. Agentic Development Setup

How to organise the monorepo and set up Claude Code (agents, skills, hooks, conventions) so that AI coding agents do most of the routine work while you keep control of the design and the results.

*Claude Code file formats in this document were checked against the official docs on 17 October 2026: [subagents](https://code.claude.com/docs/en/sub-agents.md), [skills](https://code.claude.com/docs/en/skills.md), [memory / CLAUDE.md](https://code.claude.com/docs/en/memory.md). Check them again when you set up; the tools change quickly.*

---

## 5.1 Repository strategy: one monorepo, one folder per task

The project is **one repository, `edge-cv`**, with a top-level folder per task. For a single developer this avoids cross-repo version tags, release-based artifact passing and ten CI setups, and lets Claude Code see the whole system. A component that grows strong enough to stand alone (most likely the C++ tracker) can be split out later with its history (`git filter-repo` / `git subtree split`).

### Layout

```
edge-cv/
├── README.md              # project story, diagram, links to each task's results
├── CLAUDE.md              # repo-wide rules for Claude Code (short)
├── .claude/
│   ├── settings.json      # permissions (allow / ask / deny)
│   ├── agents/            # all subagents, defined once
│   └── skills/            # all skills, defined once
├── docs/                  # plan, roadmap, decisions (ADRs), privacy rules, learning log, budget
├── common/                # Python package + C++ CMake library
├── rig-calib/             # T0
├── street-detector/       # T1
├── tracker/               # T2
├── edge-runtime/          # T3
├── pan-tilt/              # T4
├── robustness/            # T5
├── gnss-free-nav/         # T6
├── thermal/               # T7 (later)
├── cat-deterrent/         # F1 (optional)
├── Makefile               # top-level task runner (setup, test, lint per folder)
└── .github/workflows/     # CI with path filters
```

Each task folder has its own `README.md` (results first), its own `CLAUDE.md`, `configs/`, `bench/` or `reports/`, and tests.

| Folder | Type | Depends on | Main outputs |
|---|---|---|---|
| `common/` | Library (Python + C++) | — | Python package, C++ CMake library |
| `rig-calib/` (T0) | Task | common | Calibration YAML files (in git, `rig-calib/calib/`) |
| `street-detector/` (T1) | Task | common | Model files (`.onnx`, ncnn, `.hef`) via DVC; dataset card |
| `tracker/` (T2) | Task + library | common, T0 YAML | C++ library + Python wheel |
| `edge-runtime/` (T3) | Task + service | common, T1 models, T2 library, T0 YAML | Pi binary, systemd unit, Docker image |
| `pan-tilt/` (T4) | Task | common, T3 (as a module) | Control library |
| `robustness/` (T5) | Task | common, T1 training code, T3 logs | Reports, new dataset versions |
| `gnss-free-nav/` (T6) | Task | common | Estimator library, PX4 SITL scenarios |
| `thermal/` (T7, later) | Task | common, T1 | Thermal model files |

### Rules

1. **Shared code lives only in `common/`.** Task folders import it directly (Python: editable install of `common/`; C++: `add_subdirectory(common)` or a CMake target). No version tags between folders.
2. **Cross-component changes happen in one commit/PR** (e.g. changing the detection format in `common/` together with its users in `tracker/` and `edge-runtime/`).
3. **Data formats are defined once** in `common/types` (JSON Lines).
4. **Large artifacts never go into git:** datasets and recordings via DVC (private remote); model files via DVC or GitHub release assets (only for public downloads). Calibration YAML files are small and stay in git under `rig-calib/calib/`.
5. **One `.claude/` at the root** holds all agents and skills. No plugin, no marketplace. Skills are invoked as `/<skill-name>`.
6. **Nested `CLAUDE.md` files:** the root file holds global rules; each task folder's file holds local context and is loaded when working in that folder.
7. **CI uses path filters:** a change in `tracker/` runs tracker tests (and those of folders that depend on it); a change in `common/` runs everything.
8. **Privacy rules apply everywhere:** no raw street video, blurring, no identity recognition, no location clues.

### Visibility

- Public: the repository (good for the portfolio).
- Private: the DVC data remote, raw recordings, any file revealing your location.

---

## 5.2 Layers of AI configuration

| Layer | Where | What goes there |
|---|---|---|
| **Personal** | `~/.claude/CLAUDE.md`, `~/.claude/agents/`, `~/.claude/skills/` | Your personal preferences (language, explanation style, review habits). Not shared |
| **Repo root** | `/CLAUDE.md`, `/.claude/settings.json`, `/.claude/agents/`, `/.claude/skills/` | Shared agents, skills, permissions and global rules used by every task |
| **Task folder** | `<folder>/CLAUDE.md` | Local context: what the folder does, commands, what not to touch. Loaded when working in that folder |

### Agents and skills layout

```
.claude/
├── settings.json
├── agents/
│   ├── cv-researcher.md
│   ├── ml-trainer.md
│   ├── edge-deployer.md
│   ├── cpp-engineer.md
│   ├── geometry-estimation.md
│   ├── test-and-review.md
│   ├── benchmark-reporter.md
│   └── privacy-guard.md
└── skills/
    ├── new-experiment/SKILL.md
    ├── cloud-train/SKILL.md
    ├── export-model/SKILL.md
    ├── pi-deploy/SKILL.md
    ├── pi-benchmark/SKILL.md
    ├── calibrate-camera/SKILL.md
    ├── dataset-version/SKILL.md
    ├── results-readme/SKILL.md
    ├── privacy-check/SKILL.md
    └── weekly-status/SKILL.md
```

Hooks (e.g. run formatters after edits; block committing media files) go in `.claude/settings.json`. Skills run as `/<skill-name>`; agents are referenced by name.

---

## 5.3 Agents (subagents)

Subagents are Markdown files with YAML frontmatter. Only `name` and `description` are required; `tools` and `model` are the most useful optional fields. Keep each agent narrow: one area of expertise, a clear "when to use", and an explicit list of what it must not do.

| Agent | Use it for | Tools | Must not |
|---|---|---|---|
| `cv-researcher` | Reading papers and docs, comparing approaches, writing a short design note before implementation | Read, Grep, Glob, WebSearch, WebFetch | Write code |
| `ml-trainer` | Training configs, cloud notebooks, data loaders, evaluation scripts, experiment tracking | Read, Edit, Write, Bash | Change test sets; delete experiments |
| `edge-deployer` | ONNX export, ncnn/Hailo/OpenVINO conversion, quantization calibration, deployment scripts | Read, Edit, Write, Bash | Change model architecture without a note |
| `cpp-engineer` | C++17 code, CMake, threading, performance, pybind11 bindings | Read, Edit, Write, Bash | Add dependencies without approval |
| `geometry-estimation` | Calibration, homography, PnP, Kalman/EKF design and tuning, VO | Read, Edit, Write, Bash | Hard-code calibration values in code |
| `test-and-review` | Writing tests, reviewing diffs, checking that results match the claims in the README | Read, Grep, Glob, Bash | Edit production code (it reports; the others fix) |
| `benchmark-reporter` | Running benchmark scripts, producing tables and charts for READMEs | Read, Bash, Write | Edit benchmark numbers by hand |
| `privacy-guard` | Checking every media file and README before commit or publish: blurring, no location clues, no raw video | Read, Grep, Glob, Bash | Approve anything it has not opened |

### Example: `agents/edge-deployer.md`

```markdown
---
name: edge-deployer
description: Converts trained models for edge targets (ONNX, ncnn, Hailo HEF, OpenVINO), runs INT8 calibration and checks accuracy after conversion. Use after a new model is trained or when deployment fails on the Pi.
tools: Read, Edit, Write, Bash, Grep, Glob
model: sonnet
---

You deploy models to edge hardware for the ecv project.

Always:
1. Start from the ONNX export of a tracked model version (DVC tag).
2. For INT8, use the calibration set listed in the folder's data config (never the test set).
3. After conversion, run the accuracy check on the fixed validation clip and compare with FP32.
4. Record target, input size, precision, mAP, FPS and p99 latency in bench/results.jsonl.

Never:
- Change the model architecture or training config. If conversion fails because of an unsupported layer, write a short note in docs/deploy-issues.md and stop.
- Commit model binaries to git. Track them with DVC (GitHub release assets only for public downloads).
```

### Example: `agents/test-and-review.md`

```markdown
---
name: test-and-review
description: Reviews diffs and results before merge. Checks tests pass, numbers in README match bench/ files, and no data or media files are committed. Use before every merge to main.
tools: Read, Grep, Glob, Bash
model: opus
---

Review the current branch against main.
Report, do not fix. For each issue: file, line, why it matters, suggested fix.
Check specifically:
- tests and linters pass;
- every number in README.md can be found in bench/ or reports/ outputs;
- no files under data/, recordings/, or *.mp4/*.jpg outside docs/media/ are added;
- docs/media/ images are blurred (ask privacy-guard if unsure).
```

---

## 5.4 Skills

Skills are folders with a `SKILL.md` (YAML frontmatter + instructions) and optional scripts and reference files. Claude loads a skill automatically when its `description` matches the request, or you run it as a slash command. Use `disable-model-invocation: true` for anything with side effects (deploying, publishing) so it only runs when you ask.

| Skill | What it does | Invocation |
|---|---|---|
| `new-experiment` | Creates an experiment folder with a config, a README stub and an entry in the experiment log | auto or `/` |
| `cloud-train` | Prepares and checks a training run for Colab/Kaggle: config, DVC pull, checkpoint/resume, metric logging | `/` only |
| `export-model` | ONNX → ncnn / HEF / OpenVINO with fixed steps and an accuracy check after each | auto or `/` |
| `pi-deploy` | Builds and copies a build to the Pi over SSH, installs the systemd unit, checks health | `/` only (side effects) |
| `pi-benchmark` | Runs the benchmark harness on the Pi, collects results into `bench/results.jsonl` | `/` only |
| `calibrate-camera` | Guided intrinsic calibration and road-homography fitting, with the error report | `/` |
| `dataset-version` | Adds new labelled data, writes the dataset card update, creates a DVC version and tag | `/` only |
| `results-readme` | Regenerates the results section of README.md from `bench/` and `reports/` | auto or `/` |
| `privacy-check` | Runs face/plate blurring on `docs/media/`, scans for location clues, blocks raw video | auto before commits |
| `weekly-status` | Summarises the week across folders (merged PRs, new results, blockers) into `docs/roadmap.md` | `/` only |

### Example: `skills/pi-benchmark/SKILL.md`

```markdown
---
name: pi-benchmark
description: Run the standard benchmark on the Raspberry Pi for a given model version and record the results.
disable-model-invocation: true
argument-hint: [model-version] [target: cpu|hailo]
allowed-tools: Bash(ssh pi@ecv-pi *), Bash(scp *)
---

Benchmark model version $0 on target $1.

1. Check the Pi is reachable: `ssh pi@ecv-pi uptime`.
2. Make sure the model files for $0 are on the Pi under ~/models/$0/.
3. Run `${CLAUDE_SKILL_DIR}/scripts/run_bench.sh $0 $1` on the Pi via ssh.
   It plays the fixed test clip 3 times and records FPS, p50/p95/p99 latency, SoC temperature.
4. Copy the result JSON back and append it to bench/results.jsonl.
5. Show a one-line summary and the comparison with the previous version.
Stop and report if the SoC temperature exceeded 80 °C (thermal throttling makes the numbers invalid).
```

---

## 5.5 `CLAUDE.md` templates

Keep each file short (a page). The root file is loaded in every session; a task-folder file is loaded when working in that folder.

### Root `CLAUDE.md`

```markdown
# edge-cv

Edge-CV portfolio project: detection, tracking, calibration and GPS-free navigation on a Raspberry Pi 5. Plan: docs/.

## Layout
One folder per task (rig-calib, street-detector, tracker, edge-runtime, ...), shared code in common/.

## Commands
- `make setup`, `make test`, `make lint` (all folders); `make -C <folder> test` for one.

## Rules
- Shared code lives only in common/. Do not copy it into task folders.
- Cross-component changes go in one commit, with all users updated.
- Data formats are defined in common/types (JSON Lines).
- Never commit data, recordings or model binaries (DVC).
- Results go to bench/ or reports/ as JSON/JSONL; README tables are generated from them (/results-readme).

## Privacy (hard rules)
- No raw street video or unblurred images in the repo.
- No identity recognition of people. Re-identification embeddings stay in memory only.
- No content that reveals the camera location.
```

### Task-folder `CLAUDE.md`

```markdown
# <folder>/ (T<n>: <task name>)

## What this folder does
<two sentences>

## Commands
- Setup: `make setup`
- Tests: `make test`
- Lint/format: `make lint`
- Main experiment: `make run EXP=<name>`

## Layout
<short tree with one line per subfolder>

## Local conventions
- Configs in configs/*.yaml; never hard-code paths, thresholds or calibration values.
- Do not touch: <other folders, test sets, calibration files>.

## Definition of done
<copied from the task file in docs/ or 03-tasks/>
```

---

## 5.6 `.claude/settings.json` (permissions)

Allow the routine commands, ask for anything that changes the outside world, deny the dangerous ones:

- **Allow:** running tests, linters, build, `dvc pull`, `git status/diff/log`, `ssh` to the Pi for read-only checks.
- **Ask:** `git push`, `dvc push`, `gh release create`, anything that writes to the Pi.
- **Deny:** `rm -rf` outside the build folder, `git push --force`, committing files under `data/` or `recordings/`.

Check the settings and permissions documentation for the exact syntax when you set this up.

---

## 5.7 How a typical task is developed with agents

1. **Design note** (`cv-researcher`): one page in `<folder>/docs/design.md`: approach, alternatives, metrics, risks. You review and decide.
2. **Plan**: break the task file from `03-tasks/` into GitHub issues (one tracker for the whole repo), one measurable step each.
3. **Implement per issue** on a branch: `ml-trainer` / `cpp-engineer` / `geometry-estimation` write code and tests.
4. **Review** (`test-and-review`) before merge; you read the diff yourself for anything non-trivial.
5. **Run and record** with skills (`/pi-benchmark`, `/export-model`).
6. **Report** (`benchmark-reporter` + `/results-readme`), then `privacy-guard` on any media.
7. **Weekly** `/weekly-status` to update the roadmap.

### Keep your own understanding

Employers will ask you to explain everything in the repo. A few habits:

- Write the **core algorithms yourself first** (Kalman filter, association, homography fitting, EKF), then let agents help with tests, tooling, refactoring and optimisation.
- For every merged PR, be able to answer "why this way and not another?" Add the answer to the PR description.
- Keep a **learning log** (`docs/learning-log.md`): what you learned, what broke, how you fixed it. It is also great interview material.
- Several vacancies (e.g. DoD Solution) explicitly ask for "effective use of AI coding agents while keeping technical judgment". Your setup and learning log are evidence of exactly that; mention it in the CV.

---

## 5.8 Setup checklist (week 0)

- [ ] Create the `edge-cv` repository on your personal GitHub account.
- [ ] Install Claude Code on the laptop; log in.
- [ ] Root: `CLAUDE.md`, `.claude/settings.json`, the first 3 agents (`cv-researcher`, `ml-trainer`, `test-and-review`) and 3 skills (`new-experiment`, `cloud-train`, `results-readme`). Add the others when the matching task starts.
- [ ] `docs/` (roadmap, decisions, conventions, privacy, learning log, budget), top-level `Makefile`, `.github/workflows/` with path filters, `.gitignore` that excludes data and media.
- [ ] `common/` skeleton: `types`, `geometry`, `metrics` stubs with tests; editable install works.
- [ ] Create `street-detector/` with its README and `CLAUDE.md`; start T1 part A.
- [ ] DVC remote (private) and an experiment tracker account (W&B or MLflow).
- [ ] SSH key for the Pi; a hostname like `ecv-pi` on the home network (when the hardware arrives).
