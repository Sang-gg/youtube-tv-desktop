"""QWebEnginePage tuy chinh.

Xu ly bat console message (log API/GM_log) va ho tro fullscreen tu noi dung web.
"""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile


class TVWebPage(QWebEnginePage):
    """Trang web tuy chinh cho YouTube TV."""

    def __init__(
        self,
        profile: QWebEngineProfile,
        on_api_console: Callable[[str, str], None] | None = None,
    ) -> None:
        super().__init__(profile)
        self._on_api_console = on_api_console
        # Cho phep noi dung web yeu cau fullscreen (vd: trinh phat video).
        self.fullScreenRequested.connect(self._on_fullscreen_requested)

    def _on_fullscreen_requested(self, request) -> None:  # noqa: ANN001
        """Chap nhan moi yeu cau fullscreen tu trang."""
        request.accept()

    def javaScriptConsoleMessage(  # noqa: N802
        self,
        level,  # noqa: ANN001
        message: str,
        line_number: int,
        source_id: str,
    ) -> None:
        """Bat console message; chuyen tiep cac log API InnerTube."""
        if self._on_api_console and message.startswith("[YTTV_API]"):
            # Dinh dang: [YTTV_API]<source>|<url>
            payload = message[len("[YTTV_API]"):]
            if "|" in payload:
                source, url = payload.split("|", 1)
                self._on_api_console(url, source)
