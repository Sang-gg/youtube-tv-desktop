"""Browser Core.

Dong goi QWebEngineProfile + TVWebPage + QWebEngineView. Chiu trach nhiem luu
cookie/phien, cau hinh User-Agent, gan interceptor, quan ly script collection
va cung cap cac thao tac reload/zoom/fullscreen/dispatch remote key.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEngineScript
from PySide6.QtWebEngineWidgets import QWebEngineView

from .request_interceptor import AdRequestInterceptor
from .web_page import TVWebPage


class BrowserCore(QWebEngineView):
    """Loi trinh duyet dua tren Qt WebEngine."""

    def __init__(
        self,
        profile_dir: Path,
        user_agent: str,
        interceptor: AdRequestInterceptor,
        on_api_console: Callable[[str, str], None] | None = None,
        parent=None,  # noqa: ANN001
    ) -> None:
        super().__init__(parent)
        self._zoom = 1.0

        # Profile persistent: luu cookie + cache giua cac lan mo.
        self._profile = QWebEngineProfile("yttv-profile", self)
        self._profile.setPersistentStoragePath(str(profile_dir))
        self._profile.setCachePath(str(profile_dir / "cache"))
        self._profile.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies
        )
        self._profile.setHttpUserAgent(user_agent)
        self._profile.setUrlRequestInterceptor(interceptor)

        # Trang web tuy chinh.
        self._page = TVWebPage(self._profile, on_api_console=on_api_console)
        self.setPage(self._page)

    @property
    def profile(self) -> QWebEngineProfile:
        """Profile WebEngine dang dung."""
        return self._profile

    def set_user_agent(self, user_agent: str) -> None:
        """Cap nhat User-Agent."""
        self._profile.setHttpUserAgent(user_agent)

    def clear_scripts(self) -> None:
        """Xoa toan bo script trong collection."""
        self._page.scripts().clear()

    def add_document_script(
        self,
        name: str,
        source: str,
        injection_point: QWebEngineScript.InjectionPoint,
    ) -> None:
        """Them mot script chay tu dong vao collection."""
        script = QWebEngineScript()
        script.setName(name)
        script.setInjectionPoint(injection_point)
        script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
        script.setRunsOnSubFrames(False)
        script.setSourceCode(source)
        self._page.scripts().insert(script)

    def add_engine_script(self, script: QWebEngineScript) -> None:
        """Them mot QWebEngineScript da tao san (vd: tu UserScript)."""
        self._page.scripts().insert(script)

    def load_url(self, url: str) -> None:
        """Tai mot URL."""
        self.load(QUrl(url))

    def reload_page(self) -> None:
        """Tai lai trang hien tai."""
        self.reload()

    def set_zoom(self, factor: float) -> None:
        """Dat he so zoom (gioi han 0.25 - 5.0)."""
        self._zoom = max(0.25, min(5.0, factor))
        self.setZoomFactor(self._zoom)

    def zoom_in(self) -> None:
        """Phong to."""
        self.set_zoom(self._zoom + 0.1)

    def zoom_out(self) -> None:
        """Thu nho."""
        self.set_zoom(self._zoom - 0.1)

    def run_js(self, script: str) -> None:
        """Chay JS tam thoi (dung cho remote key, khong cho script thuong truc)."""
        self._page.runJavaScript(script)

    def current_url(self) -> str:
        """URL hien tai."""
        return self.url().toString()
