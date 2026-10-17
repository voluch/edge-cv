# Setup plan: from now to the first development step

Goal: everything needed before T1 part A (training the detector on VisDrone on a cloud GPU). Effort figures are rough.

## Already done

- [x] Monorepo `edge-cv` on GitHub (`voluch/edge-cv`), root `README.md`, `CLAUDE.md`, `Makefile`, `.claude/settings.json`
- [x] 8 agents, 10 skills, `.env` protection hook, `.env_template`
- [x] `common/` skeleton (Python + C++), tests passing
- [x] Planning pack in `docs/`

## Phase A: Fix and verify what exists (~1 h)

- [ ] **A1.** Tighten the `.env` hook: block only when the redirect or the `rm`/`mv`/`sed -i` target is the `.env` file itself (today any command mentioning `.env` plus `>` is blocked). *Done when:* a commit message mentioning `.env` passes and the hook tests still pass.
- [ ] **A2.** Start a fresh Claude Code session: run `/agents` and check all 8 agents and 10 skills load; ask Claude to edit `.env` and confirm it is blocked. Fix frontmatter errors. Check the permission syntax in `.claude/settings.json` against the docs.
- [ ] **A3.** Install `cmake`; build and test `common/` with it (so far only the `g++` fallback was tested).

## Phase B: Repo scaffolding (~3–4 h)

- [ ] **B1.** Fill `docs/`: `roadmap.md`, `decisions/` (ADR-001 monorepo, ADR-002 privacy and public repo, ADR-003 RunPod + single GPU), `conventions.md`, `privacy.md`, `learning-log.md`, `budget.md`.
- [ ] **B2.** CI in `.github/workflows/`: pytest + ruff + C++ build for `common/`; path filters (a `common/` change runs everything); a job that fails on forbidden files (media outside `docs/media/`, `data/`, `recordings/`, model binaries, `.env`).
- [ ] **B3.** `pre-commit` config: block large files and media, ruff, clang-format, secret scan (gitleaks).
- [ ] **B4.** `LICENSE`, issue labels (`T0`…`T7`, `common`, `docs`), a GitHub Project or milestones.
- [ ] **B5.** Turn the T1 steps from `docs/03-tasks/T1-street-detector.md` into GitHub issues, one measurable step each.
- [ ] **B6.** Pin the Python setup: one root env (`uv`, Python 3.12) and `make setup` installs `common/[dev]`.

## Phase C: Accounts and data infrastructure (~3 h)

- [ ] **C1. DVC** (no account needed; it is a free command-line tool that works like git for large files). Use a private **AWS S3** bucket as the remote (decided; Backblaze B2, Cloudflare R2 or Google Drive are alternatives). Create the bucket with Block Public Access on, a dedicated IAM user limited to that bucket, and a budget alert; keep it in the same region as your RunPod pods where possible to limit transfer cost. Then `uv pip install "dvc[s3]"`, `dvc init`, `dvc remote add -d storage s3://<bucket>/edge-cv`, put the credentials in `.env` (you fill it in), and test with a dummy file: `dvc add`, `dvc push`, delete locally, `dvc pull`.
- [x] **C2.** W&B account (you have it). [ ] Create project `edge-cv`; put `WANDB_API_KEY` in `.env`.
- [ ] **C3. RunPod** (main training platform): add credits, create an API key (`RUNPOD_API_KEY` in `.env`), create a **network volume** (e.g. 50–100 GB) in one region for code, dataset cache and checkpoints. Write a pod start script (`scripts/cloud_train.sh`: clone repo, `pip install -e common/`, `dvc pull`, `make train`). Test with a 10-minute run on the cheapest GPU and confirm the pod stops afterwards. Set a spending cap or low credit balance.
- [ ] **C4.** (optional) Colab/Kaggle account for quick tests only.
- [ ] **C5.** Labelling: choose where CVAT runs (CVAT cloud or local Docker) for T1 part B.
- [ ] **C6.** Check the VisDrone download and licence; decide where it lives (DVC remote, not git).
- [ ] **C7.** Sign up for the Hailo Developer Zone now (the compiler download may need approval; needed around week 7).

## Phase D: Hardware and the Pi

- [ ] **D1.** Order Phase 1 hardware (Pi 5, Camera Module 3, power supply, microSD, hood materials). AI HAT+ later, around the 11.11 sale. Shipping takes 2–3 weeks, so do this first.
- [ ] **D2.** Check that the laptop NPU runtime works (OpenVINO or the vendor's ONNX Runtime provider); it is a benchmark target in T1.
- [ ] **D3.** When the Pi arrives: flash OS, hostname `ecv-pi`, SSH key, set `PI_HOST` in `.env`, run the `common/` tests on the Pi.

## Phase E: First task folder

- [ ] **E1.** Create `street-detector/`: `README.md` (results first, empty tables), local `CLAUDE.md`, `Makefile` (`setup`, `test`, `lint`, `train`), `configs/`, `bench/`, `tests/`.
- [ ] **E2.** Smoke-test the agent workflow: `cv-researcher` writes `street-detector/docs/design.md`; run `/new-experiment street-detector baseline-yolo-n`; fix whatever is awkward in agents, skills or `CLAUDE.md` files.

## Start of development

T1 part A can begin when **C1, C2, C3 and E1** are done. The rest of A, B, C and D can run in parallel.

Suggested order: A → B1–B3 → C1–C3 → E1–E2 → start T1. Do **D1 today**: shipping time is the only step on the critical path.

## Decisions recorded here

- Data and model files are stored in a private **AWS S3** bucket via DVC.
- Training runs on **RunPod pods with one GPU**; Colab and Kaggle are optional.
- **No multi-GPU training**: none of the 27 analysed vacancies asks for it (searched for multi-GPU, DDP, distributed, DeepSpeed, FSDP, NCCL, Horovod). Revisit only if a target job asks for it.
