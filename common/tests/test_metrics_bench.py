import pytest

from ecv_common.bench import BenchResult, append_result, markdown_table, read_results
from ecv_common.metrics import latency_stats


def test_latency_stats():
    s = latency_stats(range(1, 101))
    assert s["p50"] == pytest.approx(50.5)
    assert s["p99"] == pytest.approx(99.01)
    assert s["max"] == 100


def test_latency_empty():
    with pytest.raises(ValueError):
        latency_stats([])


def test_bench_roundtrip_and_table(tmp_path):
    p = tmp_path / "results.jsonl"
    r = BenchResult("yolo-n", "cpu", "int8", 640, 12.5, 70, 85, 99.5, map50=0.41)
    append_result(p, r)
    assert read_results(p) == [r]
    table = markdown_table([r])
    assert "| yolo-n | cpu | int8 | 640 | 0.41 | 12.50 | 99.50 |" in table
