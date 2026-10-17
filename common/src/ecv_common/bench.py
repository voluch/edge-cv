"""Benchmark result schema, JSONL storage and Markdown tables for READMEs."""

from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class BenchResult:
    model: str
    target: str  # e.g. cpu, hailo, laptop-npu
    precision: str  # fp32, fp16, int8
    input_size: int
    fps: float
    p50_ms: float
    p95_ms: float
    p99_ms: float
    map50: float | None = None
    map50_95: float | None = None
    notes: str = ""


def append_result(path: str | Path, result: BenchResult) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(result)) + "\n")


def read_results(path: str | Path) -> list[BenchResult]:
    with open(path, encoding="utf-8") as f:
        return [BenchResult(**json.loads(line)) for line in f if line.strip()]


def markdown_table(results: Iterable[BenchResult]) -> str:
    cols = ["model", "target", "precision", "input_size", "map50", "fps", "p99_ms"]
    head = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"

    def fmt(v) -> str:
        if v is None:
            return "–"
        return f"{v:.2f}" if isinstance(v, float) else str(v)

    rows = ["| " + " | ".join(fmt(getattr(r, c)) for c in cols) + " |" for r in results]
    return head + "\n".join(rows) + "\n"
