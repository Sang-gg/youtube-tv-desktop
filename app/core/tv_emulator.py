"""TV Environment Emulator.

Sinh ra ma JavaScript gia lap moi truong Smart TV (Tizen) de YouTube TV hoat dong dung.
"""

from __future__ import annotations

import json

from ..assets import load_js
from ..constants import TV_RESOLUTIONS


class TVEmulator:
    """Tao script gia lap moi truong TV."""

    def __init__(self, user_agent: str, tv_mode: str) -> None:
        self.user_agent = user_agent
        self.tv_mode = tv_mode

    def resolution(self) -> tuple[int, int]:
        """Tra ve do phan giai theo che do TV hien tai."""
        return TV_RESOLUTIONS.get(self.tv_mode, (1920, 1080))

    def build_script(self) -> str:
        """Sinh ma JS gia lap navigator, tizen, webapis va do phan giai."""
        width, height = self.resolution()
        template = load_js("tv_emulator.js")
        template = template.replace("__UA__", json.dumps(self.user_agent))
        template = template.replace("__WIDTH__", str(width))
        template = template.replace("__HEIGHT__", str(height))
        template = template.replace("__IS8K__", "true" if width >= 7680 else "false")
        return template
