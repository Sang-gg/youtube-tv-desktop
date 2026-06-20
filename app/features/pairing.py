"""Pairing Support.

Ho tro dang nhap bang ma ghep noi qua youtube.com/activate va luu token cuc bo.
"""

from __future__ import annotations

import json
import time
from pathlib import Path


class PairingManager:
    """Quan ly token pairing luu cuc bo."""

    def __init__(self, token_file: Path) -> None:
        self._token_file = token_file

    def save_token(self, code: str, extra: dict | None = None) -> None:
        """Luu ma ghep noi va metadata kem theo."""
        data = {"code": code, "saved_at": time.time(), "extra": extra or {}}
        self._token_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def load_token(self) -> dict | None:
        """Doc token da luu, tra ve None neu khong co."""
        if self._token_file.exists():
            try:
                return json.loads(self._token_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, ValueError):
                return None
        return None

    def clear_token(self) -> None:
        """Xoa token da luu."""
        if self._token_file.exists():
            self._token_file.unlink()
