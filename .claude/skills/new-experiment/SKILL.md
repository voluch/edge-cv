---
name: new-experiment
description: Create an experiment folder with a config, a README stub and an entry in the experiment log. Use when starting a new training run, benchmark or parameter study in a task folder.
argument-hint: [task-folder] [experiment-name]
---

Create experiment `$1/experiments/$2` (ask for the missing argument if either is absent).

1. Check `$1/CLAUDE.md` for local conventions and copy the closest existing config from `$1/configs/` (or create `config.yaml` with seed, data version, model, metrics).
2. Create `$1/experiments/$2/README.md` with: goal, hypothesis, config, how to run (`make -C $1 run EXP=$2`), expected metric, and an empty "Results" and "What failed" section.
3. Append a line to `$1/experiments/LOG.md`: date, name, one-line goal, status `planned`.
4. Do not start the run. Print the paths created.
