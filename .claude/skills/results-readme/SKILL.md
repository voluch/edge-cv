---
name: results-readme
description: Regenerate the results section of a task README from bench/ and reports/ files. Use after new results are recorded.
argument-hint: [task-folder]
---

Regenerate the results section of `$0/README.md`.

1. Build tables from `$0/bench/results.jsonl` with `ecv_common.bench.markdown_table`, and read any metrics in `$0/reports/`.
2. Replace only the block between `<!-- results:start -->` and `<!-- results:end -->` (add the markers under the top of the README if missing). Results come first: table and one GIF, then how to reproduce, then what failed and why.
3. Every number must trace to a file; never type a number by hand.
4. Check that all images in the README live under `docs/media/` and have passed `/privacy-check`.
