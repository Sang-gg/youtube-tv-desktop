"""He thong cau hinh ung dung.

Luu va doc cau hinh tu file JSON. Cung cap gia tri mac dinh an toan va API
truy cap kieu thuoc tinh cho phan con lai cua ung dung.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .constants import DEFAULT_AD_BLOCK_DOMAINS, DEFAULT_TV_USER_AGENT


@dataclass
class AppConfig:
    """Doi tuong cau hinh cua ung dung."""

    user_agent: str = DEFAULT_TV_USER_AGENT
    tv_mode: str = "1080p"  # 1080p | 2k | 4k | 8k
    fullscreen_on_start: bool = True
    kiosk_mode: bool = False
    js_injection_enabled: bool = True
    data_dir: str = ""  # rong = dung mac dinh trong AppPaths

    # Ad blocking.
    adblock_enabled: bool = True
    adblock_cosmetic_enabled: bool = True
    adblock_custom_domains: list[str] = field(default_factory=list)
    filter_lists_enabled: bool = True

    # SponsorBlock.
    sponsorblock_enabled: bool = True
    sponsorblock_categories: list[str] = field(
        default_factory=lambda: ["sponsor", "intro", "outro", "selfpromo", "interaction"]
    )

    # UserScript engine.
    userscripts_enabled: bool = True
    userscript_hot_reload: bool = True
    userscript_allow_clipboard: bool = False
    userscript_allow_localstorage: bool = True
    userscript_allow_fetch: bool = True

    def merged_block_domains(self) -> list[str]:
        """Gop danh sach domain mac dinh va domain tuy chinh."""
        return list(dict.fromkeys(DEFAULT_AD_BLOCK_DOMAINS + self.adblock_custom_domains))


class ConfigManager:
    """Doc/ghi cau hinh ra file JSON."""

    def __init__(self, settings_file: Path) -> None:
        self._settings_file = settings_file
        self.config = self.load()

    def load(self) -> AppConfig:
        """Doc cau hinh tu file, tra ve mac dinh neu loi."""
        if self._settings_file.exists():
            try:
                data = json.loads(self._settings_file.read_text(encoding="utf-8"))
                return AppConfig(**{**asdict(AppConfig()), **data})
            except (json.JSONDecodeError, TypeError, ValueError):
                # File hong -> fallback ve mac dinh de khong crash.
                return AppConfig()
        return AppConfig()

    def save(self) -> None:
        """Ghi cau hinh hien tai ra file JSON."""
        self._settings_file.parent.mkdir(parents=True, exist_ok=True)
        self._settings_file.write_text(
            json.dumps(asdict(self.config), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
