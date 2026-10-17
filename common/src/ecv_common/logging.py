"""Structured JSON logs with consistent fields."""

from __future__ import annotations

import json
import logging as _logging
import time


class JsonFormatter(_logging.Formatter):
    def format(self, record: _logging.LogRecord) -> str:
        out = {
            "t_ns": time.time_ns(),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        extra = getattr(record, "fields", None)
        if isinstance(extra, dict):
            out.update(extra)
        if record.exc_info:
            out["exc"] = self.formatException(record.exc_info)
        return json.dumps(out)


def get_logger(name: str, level: int = _logging.INFO) -> _logging.Logger:
    logger = _logging.getLogger(name)
    if not logger.handlers:
        h = _logging.StreamHandler()
        h.setFormatter(JsonFormatter())
        logger.addHandler(h)
        logger.setLevel(level)
        logger.propagate = False
    return logger
