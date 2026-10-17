---
name: dataset-version
description: Add new labelled data, update the dataset card, create a DVC version and tag. Use only when the user asks to publish a new dataset version.
disable-model-invocation: true
argument-hint: [dataset-dir] [version e.g. v0.3]
---

Create dataset version `$1` from `$0`.

1. Validate the data: label files match images, classes are in the class list, no duplicates, no frames from the validation/test split in training.
2. Run `/privacy-check` on anything that could be published. Raw frames stay in the private DVC remote.
3. Update the dataset card (`$0/DATASET.md`): classes, frame counts per class and condition, split method, how labels were made, correction effort.
4. `dvc add $0`, commit the `.dvc` file and card, and `git tag data-$1`.
5. Ask before `dvc push` and `git push --tags`.
