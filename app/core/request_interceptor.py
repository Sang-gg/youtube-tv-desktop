"""Request Interceptor cho Qt WebEngine.

Chan cac request quang cao o tang mang va log cac request YouTube InnerTube
phuc vu muc dich debug. Co cache ket qua kiem tra domain de chay nhanh.
"""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWebEngineCore import (
    QWebEngineUrlRequestInfo,
    QWebEngineUrlRequestInterceptor,
)

from ..constants import YOUTUBE_API_ENDPOINTS


class AdRequestInterceptor(QWebEngineUrlRequestInterceptor):
    """Chan request quang cao va log request API."""

    def __init__(
        self,
        block_domains: Callable[[], list[str]],
        adblock_enabled: Callable[[], bool],
        on_api_request: Callable[[str], None] | None = None,
        on_blocked: Callable[[str], None] | None = None,
    ) -> None:
        super().__init__()
        self._block_domains = block_domains
        self._adblock_enabled = adblock_enabled
        self._on_api_request = on_api_request
        self._on_blocked = on_blocked
        # Cache: url -> bi chan hay khong.
        self._cache: dict[str, bool] = {}

    def interceptRequest(self, info: QWebEngineUrlRequestInfo) -> None:  # noqa: N802
        """Duoc Qt goi cho moi request. Khong duoc block luong UI lau."""
        url = info.requestUrl().toString()

        # Log request API InnerTube (khong can thiep).
        if self._on_api_request:
            for endpoint in YOUTUBE_API_ENDPOINTS:
                if endpoint in url:
                    self._on_api_request(url)
                    break

        if not self._adblock_enabled():
            return

        if self._should_block(url):
            info.block(True)
            if self._on_blocked:
                self._on_blocked(url)

    def _should_block(self, url: str) -> bool:
        """Kiem tra (co cache) xem URL co trung domain chan khong."""
        if url in self._cache:
            return self._cache[url]
        blocked = any(domain in url for domain in self._block_domains())
        # Gioi han kich thuoc cache de tranh ro ri bo nho.
        if len(self._cache) > 5000:
            self._cache.clear()
        self._cache[url] = blocked
        return blocked
