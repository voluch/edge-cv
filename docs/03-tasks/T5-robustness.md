# T5. Robustness and the data flywheel (`robustness/`)

**Duration:** runs in the background from ~week 9; ~2 weeks of focused work · **Hardware:** Pi (logging), cloud (retraining) · **Language:** Python

## Goal

Show that the detector and tracker work in the real world, not only on benchmarks: measure performance by **condition** (day, dusk, night, rain, snow, fog, glare), find where it breaks, and close the gap with an **active-learning loop** where the Pi collects the frames the model is unsure about.

**Vacancy link:** robustness to blur, low light, occlusion (DoD Solution, Key People, B6), domain shift, failure analysis (A5, B1), MLOps/data versioning (Phantom, map-matching roles), "works in the field, not only offline benchmarks" (DroneOps, Lendurai, Softengi).

## Components

| Component | Description |
|---|---|
| Condition tagging | Automatic tags per clip: time of day (from timestamp + sunrise/sunset), image brightness, weather (manual tag or a public weather history for your city, stored privately) |
| Robustness test set | Small labelled set per condition (e.g. 200 frames each) kept fixed for all model versions |
| Synthetic corruptions | Blur, noise, JPEG artifacts, low light, rain streaks applied to clean frames; measures sensitivity in a controlled way |
| Uncertainty sampling on the Pi | T3 runtime saves frames with low-confidence detections, track fragmentation or disagreement between consecutive frames; rate-limited; blurred before leaving the Pi |
| Labelling loop | Selected frames → teacher model in the cloud → correction in Hasty → new DVC dataset version |
| Retraining and comparison | Retrain the student; compare on the fixed robustness test set; keep a model registry with metrics per version |
| Drift monitor | Weekly report from the Pi logs: detection counts per class and hour, confidence distributions; flags unusual changes |

## Steps

1. Build the per-condition test sets from recorded clips (start with day/night; add weather as it happens).
2. Evaluate the current model per condition; plot accuracy by condition.
3. Implement synthetic corruptions; plot accuracy vs corruption strength.
4. Add uncertainty sampling to T3; collect for 1–2 weeks.
5. Label the selected frames (teacher + correction); retrain; compare against the same test sets.
6. Compare active-learning selection with random selection of the same number of frames (this is the key experiment).

## Metrics

- mAP per condition before and after retraining.
- Active learning vs random sampling: mAP gain per labelled frame.
- Accuracy vs corruption strength curves.

## Definition of done

- README: "accuracy by condition" chart, before/after table, active vs random comparison.
- Model registry (a simple table in the repo or W&B/MLflow) with each model version, its data version and its metrics.
- A documented, repeatable loop: collect → label → retrain → evaluate → deploy.

## Risks and tips

- **Night images through glass** will show room reflections; the hood and turning off room lights matter more than any model change.
- Keep the test sets **fixed**; never train on them.
- Rare weather means slow data collection; start early and let the Pi collect in the background.
