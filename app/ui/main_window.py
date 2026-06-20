"""MainWindow: dieu phoi toan bo ung dung.

Ket noi browser core, emulator, adblock, sponsorblock, media stats, remote
control, pairing, userscripts, settings va debug console.
"""

from __future__ import annotations

import os

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QKeyEvent
from PySide6.QtWebEngineCore import QWebEngineScript
from PySide6.QtWidgets import QMainWindow, QMessageBox

from ..config import ConfigManager
from ..constants import YOUTUBE_TV_URL
from ..core.browser import BrowserCore
from ..core.request_interceptor import AdRequestInterceptor
from ..core.tv_emulator import TVEmulator
from ..core.youtube_api import YouTubeApiLogger
from ..features.adblock import AdBlocker
from ..features.media_stats import MediaStats
from ..features.pairing import PairingManager
from ..features.remote_control import RemoteControl
from ..features.sponsorblock import SponsorBlock
from ..paths import AppPaths
from ..userscripts.hot_reload import HotReloadWatcher
from ..userscripts.manager import UserScriptManager
from .debug_console import DebugConsole
from .script_manager_dialog import ScriptManagerDialog
from .settings_window import SettingsWindow


class MainWindow(QMainWindow):
    """Cua so chinh cua YouTube TV Desktop."""

    def __init__(self, paths: AppPaths, config_manager: ConfigManager) -> None:
        super().__init__()
        self._paths = paths
        self._config_manager = config_manager
        self._config = config_manager.config

        self.setWindowTitle("YouTube TV Desktop")

        # Cac module nghiep vu.
        self._api_logger = YouTubeApiLogger()
        self._adblocker = AdBlocker(paths.filters_dir)
        self._pairing = PairingManager(paths.token_file)
        self._userscript_manager = UserScriptManager(
            scripts_dir=paths.userscripts_dir,
            allow_clipboard=self._config.userscript_allow_clipboard,
            allow_fetch=self._config.userscript_allow_fetch,
        )
        self._media_codec = "unknown"
        self._media_resolution = ""

        # Request interceptor (network adblock + log API).
        self._interceptor = AdRequestInterceptor(
            block_domains=self._config.merged_block_domains,
            adblock_enabled=lambda: self._config.adblock_enabled,
            on_api_request=lambda url: self._api_logger.log(url, "network"),
        )

        # Browser core.
        self._browser = BrowserCore(
            profile_dir=paths.profile_dir,
            user_agent=self._config.user_agent,
            interceptor=self._interceptor,
            on_api_console=self._api_logger.log,
        )
        self.setCentralWidget(self._browser)

        # Hot reload watcher.
        self._hot_reload = HotReloadWatcher(paths.userscripts_dir, self._on_hot_reload)

        # Timer cap nhat thong ke media.
        self._stats_timer = QTimer(self)
        self._stats_timer.setInterval(1500)
        self._stats_timer.timeout.connect(self._poll_media_stats)
        self._stats_timer.start()

        self._debug_console: DebugConsole | None = None

        self._setup_scripts()
        self._userscript_manager.reload()
        self._apply_userscripts()
        self._browser.load_url(YOUTUBE_TV_URL)
        self._apply_window_mode()

        if self._config.userscript_hot_reload:
            self._hot_reload.start()

    # ---- Thiet lap script thuong truc ----
    def _setup_scripts(self) -> None:
        """Inject cac script he thong (emulator, api hook, adblock, sponsorblock)."""
        self._browser.clear_scripts()
        if not self._config.js_injection_enabled:
            return

        # TV emulator (document creation - truoc khi DOM tao).
        emulator = TVEmulator(self._config.user_agent, self._config.tv_mode)
        self._browser.add_document_script(
            "tv_emulator",
            emulator.build_script(),
            QWebEngineScript.InjectionPoint.DocumentCreation,
        )

        # API hook (document creation de hook truoc khi fetch chay).
        self._browser.add_document_script(
            "api_hook",
            YouTubeApiLogger.build_hook_script(),
            QWebEngineScript.InjectionPoint.DocumentCreation,
        )

        # Media stats collector (sau khi DOM san sang).
        self._browser.add_document_script(
            "media_stats",
            MediaStats.build_collector_script(),
            QWebEngineScript.InjectionPoint.Deferred,
        )

        # Adblock cosmetic + JS filtering.
        if self._config.adblock_enabled and self._config.adblock_cosmetic_enabled:
            self._browser.add_document_script(
                "adblock_cosmetic",
                self._adblocker.build_cosmetic_script(),
                QWebEngineScript.InjectionPoint.DocumentReady,
            )

        # SponsorBlock auto-skip.
        if self._config.sponsorblock_enabled:
            sponsor = SponsorBlock(self._config.sponsorblock_categories)
            self._browser.add_document_script(
                "sponsorblock",
                sponsor.build_autoskip_script(),
                QWebEngineScript.InjectionPoint.Deferred,
            )

    def _apply_userscripts(self) -> None:
        """Them cac UserScript da bat vao collection."""
        if not self._config.userscripts_enabled:
            return
        self._userscript_manager.allow_clipboard = self._config.userscript_allow_clipboard
        self._userscript_manager.allow_fetch = self._config.userscript_allow_fetch
        for script in self._userscript_manager.build_engine_scripts():
            self._browser.add_engine_script(script)

    def _on_hot_reload(self) -> None:
        """Callback khi file userscript thay doi: nap lai va re-inject."""
        self._userscript_manager.reload()
        self._reinject_all()

    def _reinject_all(self) -> None:
        """Xoa va inject lai toan bo script he thong + userscript."""
        self._setup_scripts()
        self._apply_userscripts()

    # ---- Che do cua so ----
    def _apply_window_mode(self) -> None:
        """Ap dung fullscreen / kiosk theo cau hinh."""
        if self._config.kiosk_mode:
            self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
            self.showFullScreen()
        elif self._config.fullscreen_on_start:
            self.showFullScreen()
        else:
            self.showMaximized()

    # ---- Remote control ----
    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802
        """Xu ly phim ban phim/remote USB."""
        action = RemoteControl.action_for_key(event.key())
        modifiers = event.modifiers()

        # Phim tat ung dung (Ctrl + ...).
        if modifiers & Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_S:
                self.open_settings()
                return
            if event.key() == Qt.Key.Key_D:
                self.open_debug_console()
                return
            if event.key() == Qt.Key.Key_M:
                self.open_script_manager()
                return
            if event.key() == Qt.Key.Key_R:
                self._browser.reload_page()
                return
            if event.key() == Qt.Key.Key_F:
                self._toggle_fullscreen()
                return
            if event.key() == Qt.Key.Key_Plus:
                self._browser.zoom_in()
                return
            if event.key() == Qt.Key.Key_Minus:
                self._browser.zoom_out()
                return

        if action == "EXIT":
            if self._config.kiosk_mode:
                # Trong kiosk, Escape khong thoat ung dung.
                return
            self.close()
            return

        if action:
            script = RemoteControl.build_dispatch_script(action)
            if script:
                self._browser.run_js(script)
            return

        super().keyPressEvent(event)

    def _toggle_fullscreen(self) -> None:
        """Bat/tat fullscreen."""
        if self.isFullScreen():
            self.showMaximized()
        else:
            self.showFullScreen()

    # ---- Media stats ----
    def _poll_media_stats(self) -> None:
        """Doc window.__yttvMediaStats tu trang va luu lai."""
        self._browser.page().runJavaScript(
            "window.__yttvMediaStats || null", self._on_media_stats
        )

    def _on_media_stats(self, stats) -> None:  # noqa: ANN001
        """Nhan ket qua thong ke media tu JS."""
        if isinstance(stats, dict):
            self._media_codec = stats.get("codec", "unknown")
            self._media_resolution = stats.get("resolution", "")
            if self._debug_console is not None and self._debug_console.isVisible():
                self._update_debug_console()

    # ---- Cac cua so phu ----
    def open_settings(self) -> None:
        """Mo cua so Settings."""
        dialog = SettingsWindow(
            self._config,
            on_save=self._on_settings_saved,
            on_update_filters=self._update_filter_lists,
            parent=self,
        )
        dialog.exec()

    def _on_settings_saved(self, config) -> None:  # noqa: ANN001
        """Luu config va ap dung lai cac thay doi."""
        self._config = config
        self._config_manager.config = config
        self._config_manager.save()

        # Ap dung thu muc du lieu moi neu co.
        if config.data_dir:
            self._paths.update_base_dir(config.data_dir)

        self._browser.set_user_agent(config.user_agent)
        self._reinject_all()
        self._apply_window_mode()

        # Cap nhat hot reload.
        if config.userscript_hot_reload and self._hot_reload.available:
            self._hot_reload.start()
        else:
            self._hot_reload.stop()

        self._browser.reload_page()

    def _update_filter_lists(self) -> None:
        """Cap nhat filter list adblock va thong bao ket qua."""
        results = self._adblocker.update_lists()
        ok = sum(1 for v in results.values() if v)
        QMessageBox.information(
            self,
            "Cap nhat filter list",
            f"Da cap nhat {ok}/{len(results)} danh sach.",
        )

    def open_debug_console(self) -> None:
        """Mo Debug Console."""
        if self._debug_console is None:
            self._debug_console = DebugConsole(
                self._browser.page().profile().httpUserAgent(), parent=self
            )
        self._update_debug_console()
        self._debug_console.show()
        self._debug_console.raise_()

    def _update_debug_console(self) -> None:
        """Cap nhat noi dung Debug Console."""
        if self._debug_console is None:
            return
        emulator = TVEmulator(self._config.user_agent, self._config.tv_mode)
        w, h = emulator.resolution()
        self._debug_console.update_info(
            user_agent=self._browser.page().profile().httpUserAgent(),
            url=self._browser.current_url(),
            resolution=self._media_resolution or f"{w}x{h}",
            codec=self._media_codec,
        )
        self._debug_console.set_logs(
            [e.formatted() for e in self._api_logger.entries()]
        )

    def open_script_manager(self) -> None:
        """Mo Script Manager."""
        dialog = ScriptManagerDialog(
            self._userscript_manager,
            on_reload=self._reinject_all,
            on_open_folder=self._open_scripts_folder,
            parent=self,
        )
        dialog.exec()

    def _open_scripts_folder(self) -> None:
        """Mo thu muc userscripts bang trinh quan ly file he thong."""
        path = str(self._paths.userscripts_dir)
        if os.name == "nt":
            os.startfile(path)  # type: ignore[attr-defined]  # noqa: S606
        else:
            import subprocess

            opener = "open" if os.uname().sysname == "Darwin" else "xdg-open"
            subprocess.Popen([opener, path])  # noqa: S603

    def closeEvent(self, event) -> None:  # noqa: N802, ANN001
        """Don dep khi dong ung dung."""
        self._hot_reload.stop()
        self._stats_timer.stop()
        super().closeEvent(event)
