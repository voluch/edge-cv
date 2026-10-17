"""One interface for Pi camera, USB camera and video files; monotonic timestamps on every frame."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any

from typing_extensions import Self


@dataclass
class Frame:
    index: int
    t_ns: int  # time.monotonic_ns() at capture
    image: Any  # numpy array, HxWx3 BGR


class FrameSource(ABC):
    @abstractmethod
    def read(self) -> Frame | None:
        """Next frame, or None at the end of a file."""

    @abstractmethod
    def close(self) -> None: ...

    def __iter__(self) -> Iterator[Frame]:
        while (f := self.read()) is not None:
            yield f

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc) -> None:
        self.close()


class VideoFileSource(FrameSource):
    def __init__(self, path: str):
        import cv2  # optional dependency: pip install "ecv-common[video]"

        self._cap = cv2.VideoCapture(path)
        if not self._cap.isOpened():
            raise OSError(f"cannot open video: {path}")
        self._i = 0

    def read(self) -> Frame | None:
        ok, img = self._cap.read()
        if not ok:
            return None
        f = Frame(self._i, time.monotonic_ns(), img)
        self._i += 1
        return f

    def close(self) -> None:
        self._cap.release()


class PiCameraSource(FrameSource):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("PiCameraSource is implemented in task T0 (Picamera2)")

    def read(self):  # pragma: no cover
        raise NotImplementedError

    def close(self) -> None:  # pragma: no cover
        raise NotImplementedError
