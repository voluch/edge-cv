---
name: weekly-status
description: Summarise the week across folders (merged PRs, new results, blockers) into docs/roadmap.md. Use only when the user asks for the weekly status.
disable-model-invocation: true
---

Update `docs/roadmap.md` for the past 7 days.

1. Collect: `git log --since="7 days ago" --stat`, merged PRs (`gh pr list --state merged --search "merged:>=<date>"`), new rows in each `*/bench/results.jsonl`, open issues.
2. Append a dated section: done (per task folder), new numbers (with file references), blockers, next week's plan, hours spent if known.
3. Compare with the timeline in `docs/02-project-overview.md` and say whether the schedule slipped.
4. Add anything worth remembering to `docs/learning-log.md`. Do not commit or push.
