"""Media Optimization.

Thu thap thong tin codec, do phan giai, dropped frames va thong ke mang.
"""

from __future__ import annotations

from ..assets import load_js


class MediaStats:
    """Sinh JS thu thap thong ke media va phan tich codec."""

    @staticmethod
    def build_collector_script() -> str:
        """Sinh JS luu thong ke media vao window.__yttvMediaStats."""
        return load_js("media_stats.js")
