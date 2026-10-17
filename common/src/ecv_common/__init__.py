"""Shared code for the edge-cv project."""

from ecv_common.types import Detection, FrameRecord, Track, read_jsonl, write_jsonl

__version__ = "0.1.0"
__all__ = ["Detection", "FrameRecord", "Track", "__version__", "read_jsonl", "write_jsonl"]
