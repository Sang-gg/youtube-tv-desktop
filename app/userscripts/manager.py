"""Script Manager + Injection cho UserScript Engine.

Quet thu muc userscripts, doc metadata, quan ly bat/tat tung script va tao cac
QWebEngineScript de inject truc tiep vao WebEngine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from PySide6.QtWebEngineCore import QWebEngineScript

from ..assets import load_js
from .metadata import UserScriptMetadata

# Map @run-at -> thoi diem inject cua QWebEngineScript.
_RUN_AT_MAP = {
    "document-start": QWebEngineScript.InjectionPoint.DocumentCreation,
    "document-end": QWebEngineScript.InjectionPoint.DocumentReady,
    "document-idle": QWebEngineScript.InjectionPoint.Deferred,
}


@dataclass
class UserScript:
    """Mot UserScript da nap."""

    path: Path
    source: str
    metadata: UserScriptMetadata
    enabled: bool = True
    mtime: float = 0.0


@dataclass
class UserScriptManager:
    """Quet, nap va quan ly cac UserScript."""

    scripts_dir: Path
    allow_clipboard: bool = False
    allow_fetch: bool = True
    scripts: list[UserScript] = field(default_factory=list)

    def reload(self) -> None:
        """Quet lai thu muc va nap toan bo *.js (giu trang thai enabled cu)."""
        previous = {s.path: s.enabled for s in self.scripts}
        self.scripts.clear()
        for js_file in sorted(self.scripts_dir.glob("*.js")):
            try:
                source = js_file.read_text(encoding="utf-8")
            except OSError:
                continue
            meta = UserScriptMetadata.parse(source)
            self.scripts.append(
                UserScript(
                    path=js_file,
                    source=source,
                    metadata=meta,
                    enabled=previous.get(js_file, True),
                    mtime=js_file.stat().st_mtime,
                )
            )

    def set_enabled(self, path: Path, enabled: bool) -> None:
        """Bat/tat mot script theo duong dan."""
        for script in self.scripts:
            if script.path == path:
                script.enabled = enabled
                break

    def _gm_api_script(self) -> str:
        """Sinh JS GM API voi cac quyen tuong ung."""
        template = load_js("gm_api.js")
        template = template.replace(
            "__ALLOW_CLIPBOARD__", "true" if self.allow_clipboard else "false"
        )
        template = template.replace(
            "__ALLOW_FETCH__", "true" if self.allow_fetch else "false"
        )
        return template

    def build_engine_scripts(self) -> list[QWebEngineScript]:
        """Tao danh sach QWebEngineScript de them vao collection."""
        result: list[QWebEngineScript] = []
        for script in self.scripts:
            if not script.enabled:
                continue
            engine_script = QWebEngineScript()
            engine_script.setName(f"userscript::{script.path.name}")
            engine_script.setInjectionPoint(
                _RUN_AT_MAP.get(
                    script.metadata.run_at,
                    QWebEngineScript.InjectionPoint.Deferred,
                )
            )
            engine_script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
            engine_script.setRunsOnSubFrames(False)
            safe_name = script.metadata.name.replace("'", "")
            wrapped = (
                "(function(){\n"
                + self._gm_api_script()
                + "\ntry{\n"
                + script.source
                + "\n}catch(e){console.error('[UserScript] "
                + safe_name
                + "', e);}\n})();"
            )
            engine_script.setSourceCode(wrapped)
            result.append(engine_script)
        return result
