"""Quan ly duong dan luu tru du lieu nguoi dung.

Module nay tap trung hoa toan bo logic ve thu muc userdata, dam bao cac thu muc
con luon ton tai truoc khi duoc su dung boi cac module khac.
"""

from __future__ import annotations

import os
from pathlib import Path


class AppPaths:
    """Tap trung hoa cac duong dan luu tru cua ung dung."""

    def __init__(self, base_dir: str | os.PathLike[str] | None = None) -> None:
        # Mac dinh luu trong thu muc 'userdata' canh thu muc lam viec.
        if base_dir is None:
            base_dir = Path.cwd() / "userdata"
        self.base_dir = Path(base_dir)
        self._ensure_dirs()

    def _ensure_dirs(self) -> None:
        """Tao toan bo thu muc con can thiet neu chua ton tai."""
        for path in (
            self.base_dir,
            self.profile_dir,
            self.userscripts_dir,
            self.storage_dir,
            self.filters_dir,
        ):
            path.mkdir(parents=True, exist_ok=True)

    @property
    def profile_dir(self) -> Path:
        """Thu muc luu cookie va phien dang nhap WebEngine."""
        return self.base_dir / "profile"

    @property
    def userscripts_dir(self) -> Path:
        """Thu muc chua cac file UserScript (*.js)."""
        return self.base_dir / "userscripts"

    @property
    def storage_dir(self) -> Path:
        """Thu muc luu du lieu GM_setValue/GM_getValue."""
        return self.base_dir / "storage"

    @property
    def filters_dir(self) -> Path:
        """Thu muc cache cac filter list adblock."""
        return self.base_dir / "filters"

    @property
    def settings_file(self) -> Path:
        """File JSON luu cau hinh ung dung."""
        return self.base_dir / "settings.json"

    @property
    def token_file(self) -> Path:
        """File luu token pairing cuc bo."""
        return self.base_dir / "pairing_token.json"

    def update_base_dir(self, new_base: str | os.PathLike[str]) -> None:
        """Cap nhat thu muc goc (dung khi nguoi dung doi trong Settings)."""
        self.base_dir = Path(new_base)
        self._ensure_dirs()
