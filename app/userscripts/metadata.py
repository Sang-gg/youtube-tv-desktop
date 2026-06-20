"""Metadata Parser cho UserScript.

Doc khoi metadata ==UserScript== ... ==/UserScript== va trich xuat cac truong
@name, @version, @description, @author, @match, @exclude, @run-at.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

_META_BLOCK = re.compile(
    r"//\s*==UserScript==(.*?)//\s*==/UserScript==", re.DOTALL | re.IGNORECASE
)
_META_LINE = re.compile(r"//\s*@(\S+)\s+(.*)")


@dataclass
class UserScriptMetadata:
    """Metadata trich tu mot file UserScript."""

    name: str = "Unnamed Script"
    version: str = "0.0.0"
    description: str = ""
    author: str = ""
    matches: list[str] = field(default_factory=list)
    excludes: list[str] = field(default_factory=list)
    run_at: str = "document-idle"  # document-start | document-end | document-idle

    @classmethod
    def parse(cls, source: str) -> "UserScriptMetadata":
        """Phan tich source code de tao metadata."""
        meta = cls()
        block = _META_BLOCK.search(source)
        if not block:
            return meta
        for line in block.group(1).splitlines():
            m = _META_LINE.match(line.strip())
            if not m:
                continue
            key, value = m.group(1).lower(), m.group(2).strip()
            if key == "name":
                meta.name = value
            elif key == "version":
                meta.version = value
            elif key == "description":
                meta.description = value
            elif key == "author":
                meta.author = value
            elif key == "match":
                meta.matches.append(value)
            elif key == "exclude":
                meta.excludes.append(value)
            elif key == "run-at":
                meta.run_at = value
        # Mac dinh match tat ca YouTube neu khong khai bao.
        if not meta.matches:
            meta.matches = ["*://*.youtube.com/*"]
        return meta

    @staticmethod
    def _glob_to_regex(pattern: str) -> re.Pattern[str]:
        """Chuyen mot pattern glob (*) thanh regex."""
        escaped = re.escape(pattern).replace(r"\*", ".*")
        return re.compile("^" + escaped + "$")

    def matches_url(self, url: str) -> bool:
        """Kiem tra URL co thoa @match va khong bi @exclude khong."""
        for ex in self.excludes:
            if self._glob_to_regex(ex).match(url):
                return False
        for mt in self.matches:
            if self._glob_to_regex(mt).match(url):
                return True
        return False
