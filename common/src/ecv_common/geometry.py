"""Pixel <-> road-plane transforms. Calibration files are OpenCV-compatible YAML."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class Homography:
    """3x3 matrix H mapping image pixels (u, v) to ground-plane metres (x, y)."""

    H: np.ndarray

    def __post_init__(self) -> None:
        self.H = np.asarray(self.H, dtype=float)
        if self.H.shape != (3, 3):
            raise ValueError(f"homography must be 3x3, got {self.H.shape}")

    @staticmethod
    def _apply(M: np.ndarray, pts: np.ndarray) -> np.ndarray:
        pts = np.atleast_2d(np.asarray(pts, dtype=float))
        homog = np.hstack([pts, np.ones((len(pts), 1))]) @ M.T
        return homog[:, :2] / homog[:, 2:3]

    def pixel_to_ground(self, pts) -> np.ndarray:
        return self._apply(self.H, pts)

    def ground_to_pixel(self, pts) -> np.ndarray:
        return self._apply(np.linalg.inv(self.H), pts)

    def save(self, path: str | Path, name: str = "H") -> None:
        data = ", ".join(repr(float(v)) for v in self.H.ravel())
        Path(path).write_text(
            "%YAML:1.0\n---\n"
            f"{name}: !!opencv-matrix\n   rows: 3\n   cols: 3\n   dt: d\n   data: [ {data} ]\n"
        )

    @classmethod
    def load(cls, path: str | Path, name: str = "H") -> Homography:
        text = Path(path).read_text()
        m = re.search(rf"{re.escape(name)}:\s*!!opencv-matrix.*?data:\s*\[(.*?)\]", text, re.DOTALL)
        if not m:
            raise ValueError(f"matrix '{name}' not found in {path}")
        vals = [float(v) for v in m.group(1).replace("\n", " ").split(",")]
        return cls(np.array(vals).reshape(3, 3))


def undistort_points(pts, camera_matrix, dist_coeffs):
    """Undistort pixel points with the intrinsics. Implemented in T0 (needs OpenCV)."""
    raise NotImplementedError("undistort_points is implemented in task T0 (rig-calib)")
