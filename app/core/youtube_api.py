"""YouTube API Layer.

Theo doi va log cac request fetch/XHR toi cac endpoint InnerTube quan trong.
Khong can thiep DRM hoac co che bao ve cua YouTube; chi phuc vu phan tich.
"""

from __future__ import annotations

import json
import time
from collections import deque
from dataclasses import dataclass

from ..assets import load_js
from ..constants import YOUTUBE_API_ENDPOINTS


@dataclass
class ApiLogEntry:
    """Mot ban ghi log request API."""

    timestamp: float
    url: str
    source: str  # 'network' | 'fetch' | 'xhr'

    def formatted(self) -> str:
        """Chuoi hien thi than thien cho Debug Console."""
        ts = time.strftime("%H:%M:%S", time.localtime(self.timestamp))
        return f"[{ts}] ({self.source}) {self.url}"


class YouTubeApiLogger:
    """Luu tru lich su request API duoi dang ring buffer."""

    def __init__(self, max_entries: int = 500) -> None:
        self._entries: deque[ApiLogEntry] = deque(maxlen=max_entries)

    def log(self, url: str, source: str = "network") -> None:
        """Ghi nhan mot request neu thuoc danh sach endpoint quan tam."""
        if any(ep in url for ep in YOUTUBE_API_ENDPOINTS):
            self._entries.append(ApiLogEntry(time.time(), url, source))

    def entries(self) -> list[ApiLogEntry]:
        """Tra ve ban sao danh sach log."""
        return list(self._entries)

    def clear(self) -> None:
        """Xoa toan bo log."""
        self._entries.clear()

    @staticmethod
    def build_hook_script() -> str:
        """Sinh JS hook fetch/XHR de gui log ve Python qua console."""
        template = load_js("api_hook.js")
        return template.replace("__ENDPOINTS__", json.dumps(YOUTUBE_API_ENDPOINTS))
