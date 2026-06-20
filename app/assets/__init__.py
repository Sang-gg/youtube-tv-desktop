"""Goi chua cac tai nguyen JS template duoc doc luc runtime."""

from __future__ import annotations

from pathlib import Path

_ASSETS_DIR = Path(__file__).parent / "js"


def load_js(name: str) -> str:
    """Doc noi dung mot file JS template trong thu muc assets/js."""
    return (_ASSETS_DIR / name).read_text(encoding="utf-8")
