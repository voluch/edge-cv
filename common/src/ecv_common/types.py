"""Shared data formats: Detection, Track, FrameRecord, with JSON Lines serialization.

Keep identical to include/ecv/common/types.hpp.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Detection:
    cls: str
    score: float
    xyxy: tuple[float, float, float, float]

    def to_dict(self) -> dict:
        return {"cls": self.cls, "score": self.score, "xyxy": list(self.xyxy)}

    @classmethod
    def from_dict(cls, d: dict) -> Detection:
        return cls(d["cls"], float(d["score"]), tuple(d["xyxy"]))


@dataclass
class Track:
    id: int
    cls: str
    xyxy: tuple[float, float, float, float]
    ground_xy_m: tuple[float, float] | None = None
    speed_kmh: float | None = None

    def to_dict(self) -> dict:
        d: dict = {"id": self.id, "cls": self.cls, "xyxy": list(self.xyxy)}
        if self.ground_xy_m is not None:
            d["ground_xy_m"] = list(self.ground_xy_m)
        if self.speed_kmh is not None:
            d["speed_kmh"] = self.speed_kmh
        return d

    @classmethod
    def from_dict(cls, d: dict) -> Track:
        g = d.get("ground_xy_m")
        return cls(
            int(d["id"]),
            d["cls"],
            tuple(d["xyxy"]),
            tuple(g) if g is not None else None,
            d.get("speed_kmh"),
        )


@dataclass
class FrameRecord:
    """One JSON Lines record: everything known about one frame."""

    frame: int
    t_ns: int
    dets: list[Detection] = field(default_factory=list)
    tracks: list[Track] = field(default_factory=list)

    def to_json(self) -> str:
        return json.dumps(
            {
                "frame": self.frame,
                "t_ns": self.t_ns,
                "dets": [d.to_dict() for d in self.dets],
                "tracks": [t.to_dict() for t in self.tracks],
            },
            separators=(",", ":"),
        )

    @classmethod
    def from_json(cls, line: str) -> FrameRecord:
        d = json.loads(line)
        return cls(
            int(d["frame"]),
            int(d["t_ns"]),
            [Detection.from_dict(x) for x in d.get("dets", [])],
            [Track.from_dict(x) for x in d.get("tracks", [])],
        )


def write_jsonl(path: str | Path, records: Iterable[FrameRecord]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(r.to_json() + "\n" for r in records)


def read_jsonl(path: str | Path) -> Iterator[FrameRecord]:
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield FrameRecord.from_json(line)
