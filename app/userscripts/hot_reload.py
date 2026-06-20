"""Hot Reload cho UserScript Engine.

Theo doi thay doi cua cac file *.js trong thu muc userscripts va goi callback de
nap lai ma khong can khoi dong lai ung dung. Dung watchdog neu co.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer

    _WATCHDOG_AVAILABLE = True
except ImportError:  # pragma: no cover - watchdog la phu thuoc tuy chon
    _WATCHDOG_AVAILABLE = False
    FileSystemEventHandler = object  # type: ignore[assignment,misc]


class _ScriptChangeHandler(FileSystemEventHandler):  # type: ignore[misc]
    """Handler watchdog: goi callback khi file *.js thay doi."""

    def __init__(self, callback: Callable[[], None]) -> None:
        super().__init__()
        self._callback = callback

    def on_any_event(self, event) -> None:  # noqa: ANN001
        """Goi callback cho moi su kien lien quan toi file .js."""
        src = getattr(event, "src_path", "")
        if str(src).endswith(".js"):
            self._callback()


class HotReloadWatcher:
    """Bao boc Observer cua watchdog (neu co)."""

    def __init__(self, scripts_dir: Path, callback: Callable[[], None]) -> None:
        self._scripts_dir = scripts_dir
        self._callback = callback
        self._observer = None

    @property
    def available(self) -> bool:
        """True neu watchdog kha dung."""
        return _WATCHDOG_AVAILABLE

    def start(self) -> None:
        """Bat dau theo doi thu muc."""
        if not _WATCHDOG_AVAILABLE or self._observer is not None:
            return
        self._observer = Observer()
        handler = _ScriptChangeHandler(self._callback)
        self._observer.schedule(handler, str(self._scripts_dir), recursive=False)
        self._observer.start()

    def stop(self) -> None:
        """Dung theo doi."""
        if self._observer is not None:
            self._observer.stop()
            self._observer.join(timeout=2)
            self._observer = None
