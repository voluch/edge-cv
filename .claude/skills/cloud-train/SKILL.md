---
name: cloud-train
description: Prepare and check a training run for Colab or Kaggle - config, DVC pull, checkpoint/resume, metric logging. Use only when the user asks to prepare a cloud run.
disable-model-invocation: true
argument-hint: [task-folder] [experiment-name]
---

Prepare cloud training for `$1`, experiment `$2`.

1. Verify `$1/experiments/$2/config.yaml` exists and sets a seed, data version, epochs, checkpoint interval and resume path.
2. Verify the training entry point is a `make` target (`make -C $1 train EXP=$2`); no logic may live only in a notebook.
3. Generate or update `$1/notebooks/cloud_train.ipynb` containing only: `git clone`, `pip install -e common/`, `dvc pull`, `make train`, and `dvc push` / metric upload at the end. Take credentials from environment variables listed in `.env_template`; never write secret values into the notebook.
4. Do a dry run locally with a tiny config (1 epoch, few images) and report the result.
5. List what the user must do in Colab/Kaggle (set secrets, pick GPU). Do not push anything.
