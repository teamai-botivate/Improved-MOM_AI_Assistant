"""In-memory log buffer + /logs endpoint for streaming backend logs to the frontend console."""

import logging
import time
from collections import deque
from threading import Lock
from typing import Deque, Dict, List

from fastapi import APIRouter, Query

router = APIRouter()

_BUFFER_SIZE = 2000
_buffer: Deque[Dict] = deque(maxlen=_BUFFER_SIZE)
_lock = Lock()
_seq = 0


class BufferLogHandler(logging.Handler):
    """Logging handler that pushes formatted records into the in-memory ring buffer."""

    def emit(self, record: logging.LogRecord) -> None:
        global _seq
        try:
            msg = self.format(record)
        except Exception:
            msg = record.getMessage()
        entry = {
            "ts": time.time(),
            "level": record.levelname,
            "logger": record.name,
            "message": msg,
        }
        with _lock:
            _seq += 1
            entry["id"] = _seq
            _buffer.append(entry)


def install_buffer_handler() -> None:
    """Attach the buffer handler to the root logger so every logger.* call is captured."""
    root = logging.getLogger()
    for h in root.handlers:
        if isinstance(h, BufferLogHandler):
            return
    handler = BufferLogHandler(level=logging.INFO)
    handler.setFormatter(logging.Formatter("%(asctime)s | %(name)s | %(message)s"))
    root.addHandler(handler)
    if root.level > logging.INFO or root.level == logging.NOTSET:
        root.setLevel(logging.INFO)


@router.get("/")
async def get_logs(since: int = Query(0, ge=0), limit: int = Query(500, ge=1, le=2000)) -> Dict:
    """Return log entries with id > `since`, up to `limit` items."""
    with _lock:
        items: List[Dict] = [e for e in _buffer if e["id"] > since]
        last_id = _buffer[-1]["id"] if _buffer else since
    if len(items) > limit:
        items = items[-limit:]
    return {"last_id": last_id, "logs": items}
