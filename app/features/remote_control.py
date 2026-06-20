"""Remote Control Layer.

Map phim ban phim/remote USB sang cac hanh dong dieu huong TV.
"""

from __future__ import annotations

from PySide6.QtCore import Qt

# Map ma phim Qt -> hanh dong TV.
KEY_ACTION_MAP = {
    Qt.Key.Key_Up: "TV_UP",
    Qt.Key.Key_Down: "TV_DOWN",
    Qt.Key.Key_Left: "TV_LEFT",
    Qt.Key.Key_Right: "TV_RIGHT",
    Qt.Key.Key_Return: "OK",
    Qt.Key.Key_Enter: "OK",
    Qt.Key.Key_Backspace: "BACK",
    Qt.Key.Key_Escape: "EXIT",
    Qt.Key.Key_Space: "PLAY_PAUSE",
}

# Map hanh dong -> phim DOM de dispatch vao trang YouTube TV.
ACTION_DOM_KEY = {
    "TV_UP": ("ArrowUp", 38),
    "TV_DOWN": ("ArrowDown", 40),
    "TV_LEFT": ("ArrowLeft", 37),
    "TV_RIGHT": ("ArrowRight", 39),
    "OK": ("Enter", 13),
    "BACK": ("Backspace", 8),
    "PLAY_PAUSE": (" ", 32),
}


class RemoteControl:
    """Chuyen doi su kien phim thanh hanh dong va JS dispatch."""

    @staticmethod
    def action_for_key(qt_key: int) -> str | None:
        """Tra ve ten hanh dong cho mot ma phim Qt, hoac None."""
        return KEY_ACTION_MAP.get(qt_key)

    @staticmethod
    def build_dispatch_script(action: str) -> str | None:
        """Sinh JS dispatch su kien keydown tuong ung vao trang."""
        mapping = ACTION_DOM_KEY.get(action)
        if not mapping:
            return None
        key, code = mapping
        key_js = key.replace("\\", "\\\\").replace('"', '\\"')
        return (
            "(function() {"
            "const ev = new KeyboardEvent('keydown', {"
            f"key: \"{key_js}\", keyCode: {code}, which: {code},"
            "bubbles: true, cancelable: true });"
            "(document.activeElement || document.body).dispatchEvent(ev);"
            "})();"
        )
