"""Metrics: latency statistics now; detection and tracking metrics are stubs."""

from __future__ import annotations

import numpy as np


def latency_stats(latencies_ms) -> dict[str, float]:
    """p50 / p95 / p99 / mean / max of a list of latencies in milliseconds."""
    a = np.asarray(latencies_ms, dtype=float)
    if a.size == 0:
        raise ValueError("no latencies given")
    p50, p95, p99 = np.percentile(a, [50, 95, 99])
    return {
        "p50": float(p50),
        "p95": float(p95),
        "p99": float(p99),
        "mean": float(a.mean()),
        "max": float(a.max()),
    }


def detection_map(*args, **kwargs):
    """mAP@50 and mAP@50-95. Implemented in T1."""
    raise NotImplementedError("detection_map is implemented in task T1")


def tracking_metrics(*args, **kwargs):
    """HOTA / IDF1 / MOTA via TrackEval. Implemented in T2."""
    raise NotImplementedError("tracking_metrics is implemented in task T2")
