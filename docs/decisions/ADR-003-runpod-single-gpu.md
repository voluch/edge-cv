# ADR-003: RunPod pods, one GPU, S3 for data

**Date:** 2026-10-17 · **Status:** accepted

**Decision.** Training runs on RunPod GPU pods with a network volume; one GPU per run. Data and model files are tracked with DVC and stored in a private AWS S3 bucket. Colab and Kaggle are optional for quick tests. Labelling uses Hasty.

**Why no multi-GPU.** None of the 27 analysed vacancies asks for multi-GPU or distributed training (searched: multi-GPU, DDP, distributed, DeepSpeed, FSDP, NCCL, Horovod). YOLO nano/small fits one 24 GB card.

**Revisit** if a target job asks for it; a small DDP experiment would be an add-on, not a task.
