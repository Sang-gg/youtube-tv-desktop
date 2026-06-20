"""Ad Blocking System.

Module doc lap gom 3 tang: network blocking (interceptor), cosmetic filtering,
va JavaScript filtering. Cung quan ly filter list (EasyList/EasyPrivacy/uBlock).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import requests

from ..assets import load_js

# Cac selector CSS an thanh phan quang cao tren YouTube.
COSMETIC_SELECTORS = [
    "ytd-display-ad-renderer",
    "ytd-ad-slot-renderer",
    "ytd-promoted-video-renderer",
    "ytd-in-feed-ad-layout-renderer",
    "ytd-banner-promo-renderer",
    "ytd-statement-banner-renderer",
    "#masthead-ad",
    ".ytp-ad-module",
    ".ytp-ad-overlay-container",
    "tp-yt-paper-dialog.ytd-popup-container",
]

# Cac filter list cong khai duoc ho tro cap nhat tu dong.
FILTER_LIST_URLS = {
    "easylist": "https://easylist.to/easylist/easylist.txt",
    "easyprivacy": "https://easylist.to/easylist/easyprivacy.txt",
    "ublock": "https://raw.githubusercontent.com/uBlockOrigin/uAssets/master/filters/filters.txt",
}


class AdBlocker:
    """Quan ly cosmetic filtering va filter list."""

    def __init__(self, filters_dir: Path) -> None:
        self._filters_dir = filters_dir
        # Tap domain trich xuat tu filter list (cache trong bo nho).
        self._list_domains: set[str] = set()
        self.load_cached_lists()

    def build_cosmetic_script(self) -> str:
        """Sinh JS tiem CSS an quang cao + MutationObserver xoa phan tu moi."""
        selectors = ",".join(COSMETIC_SELECTORS)
        css = selectors + "{display:none !important;visibility:hidden !important;}"
        template = load_js("adblock.js")
        template = template.replace("'__CSS__'", json.dumps(css))
        template = template.replace("__SELECTORS__", json.dumps(COSMETIC_SELECTORS))
        return template

    def load_cached_lists(self) -> None:
        """Doc cac filter list da cache tren dia vao bo nho."""
        self._list_domains.clear()
        for name in FILTER_LIST_URLS:
            cache_file = self._filters_dir / f"{name}.txt"
            if cache_file.exists():
                self._parse_filter_list(
                    cache_file.read_text(encoding="utf-8", errors="ignore")
                )

    def update_lists(self) -> dict[str, bool]:
        """Tai ve va cache cac filter list. Tra ve trang thai tung list."""
        results: dict[str, bool] = {}
        for name, url in FILTER_LIST_URLS.items():
            try:
                resp = requests.get(url, timeout=30)
                resp.raise_for_status()
                (self._filters_dir / f"{name}.txt").write_text(
                    resp.text, encoding="utf-8"
                )
                results[name] = True
            except requests.RequestException:
                results[name] = False
        self.load_cached_lists()
        return results

    def _parse_filter_list(self, content: str) -> None:
        """Trich xuat domain tu cu phap Adblock Plus (||domain^)."""
        pattern = re.compile(r"^\|\|([a-z0-9.\-]+)\^")
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith(("!", "#", "[")):
                continue
            m = pattern.match(line)
            if m:
                self._list_domains.add(m.group(1))

    def list_domains(self) -> list[str]:
        """Tra ve danh sach domain trich tu filter list."""
        return list(self._list_domains)
