"""Application entry point.

Cau hinh cac flag Chromium (tang toc GPU phan cung), khoi tao QApplication,
AppPaths, ConfigManager va MainWindow.
"""

from __future__ import annotations

import os
import sys


def _configure_chromium_flags(kiosk: bool) -> None:
    """Dat cac flag Chromium truoc khi QApplication khoi tao."""
    flags = [
        "--enable-gpu-rasterization",
        "--enable-accelerated-video-decode",
        "--enable-accelerated-2d-canvas",
        "--ignore-gpu-blocklist",
        "--enable-features=VaapiVideoDecoder,CanvasOopRasterization",
        "--autoplay-policy=no-user-gesture-required",
    ]
    if kiosk:
        flags.append("--kiosk")
    existing = os.environ.get("QTWEBENGINE_CHROMIUM_FLAGS", "")
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = (existing + " " + " ".join(flags)).strip()


def main() -> int:
    """Ham main khoi chay ung dung."""
    # Doc cau hinh som de biet co bat kiosk khong (anh huong flag Chromium).
    from .config import ConfigManager
    from .paths import AppPaths

    paths = AppPaths()
    config_manager = ConfigManager(paths.settings_file)
    config = config_manager.config

    # Neu nguoi dung da chon thu muc du lieu rieng, ap dung lai.
    if config.data_dir:
        paths.update_base_dir(config.data_dir)
        config_manager = ConfigManager(paths.settings_file)

    _configure_chromium_flags(config_manager.config.kiosk_mode)

    # Import sau khi da dat flag de dam bao co hieu luc.
    from PySide6.QtWidgets import QApplication

    from .ui.main_window import MainWindow

    app = QApplication(sys.argv)
    app.setApplicationName("YouTube TV Desktop")

    window = MainWindow(paths, config_manager)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
