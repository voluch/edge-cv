---
name: privacy-check
description: Scan media, READMEs and staged changes for unblurred faces/plates, location clues, raw video, secrets and sensitive content. Use before commits that include images, video, maps or logs.
---

Run the privacy checks on staged changes (or the paths given).

1. List changed files with `git diff --cached --name-only` (plus untracked files under `docs/media/`).
2. Block immediately: raw video (`*.mp4`, `*.avi`), images outside `docs/media/`, anything under `data/` or `recordings/`, `.env`.
3. For each image/GIF, check EXIF for GPS (`exiftool`) and ask the `privacy-guard` agent to open it and judge blurring and landmarks.
4. Grep text for coordinates, street names, hostnames/IPs and tokens.
5. Print pass/fail per file. Do not fix automatically; if blurring is missing, offer to run `ecv_common.privacy` (once implemented).
