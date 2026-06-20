"""SponsorBlock Integration.

Lay cac segment tu API SponsorBlock cong khai va sinh JS de tu dong tua qua
sponsor/intro/outro/selfpromo/interaction.
"""

from __future__ import annotations

import json

import requests

from ..assets import load_js
from ..constants import SPONSORBLOCK_API


class SponsorBlock:
    """Client SponsorBlock + sinh script auto-skip."""

    def __init__(self, categories: list[str]) -> None:
        self.categories = categories

    def fetch_segments(self, video_id: str) -> list[dict]:
        """Lay danh sach segment cho mot video_id."""
        try:
            resp = requests.get(
                SPONSORBLOCK_API,
                params={
                    "videoID": video_id,
                    "categories": json.dumps(self.categories),
                },
                timeout=15,
            )
            if resp.status_code == 200:
                return resp.json()
        except (requests.RequestException, ValueError):
            pass
        return []

    def build_autoskip_script(self) -> str:
        """Sinh JS theo doi video_id va tua qua cac segment."""
        template = load_js("sponsorblock.js")
        return template.replace("__CATS__", json.dumps(self.categories))
