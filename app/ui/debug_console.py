"""Debug Console.

Hien thi User-Agent, URL, do phan giai, codec, nhat ky request va thong tin
WebEngine. Du lieu duoc cap nhat dinh ky tu MainWindow.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QPlainTextEdit,
    QVBoxLayout,
)


class DebugConsole(QDialog):
    """Cua so debug hien thi thong tin runtime."""

    def __init__(self, webengine_info: str, parent=None) -> None:  # noqa: ANN001
        super().__init__(parent)
        self.setWindowTitle("Debug Console - YouTube TV Desktop")
        self.resize(720, 560)

        layout = QVBoxLayout(self)
        form = QFormLayout()
        self._ua = QLabel("-")
        self._ua.setWordWrap(True)
        self._url = QLabel("-")
        self._url.setWordWrap(True)
        self._resolution = QLabel("-")
        self._codec = QLabel("-")
        self._webengine = QLabel(webengine_info)
        form.addRow("User-Agent:", self._ua)
        form.addRow("URL:", self._url)
        form.addRow("Do phan giai:", self._resolution)
        form.addRow("Codec:", self._codec)
        form.addRow("WebEngine:", self._webengine)
        layout.addLayout(form)

        layout.addWidget(QLabel("Nhat ky request API:"))
        self._log = QPlainTextEdit()
        self._log.setReadOnly(True)
        layout.addWidget(self._log)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

    def update_info(
        self,
        user_agent: str,
        url: str,
        resolution: str,
        codec: str,
    ) -> None:
        """Cap nhat cac truong thong tin co ban."""
        self._ua.setText(user_agent)
        self._url.setText(url)
        self._resolution.setText(resolution)
        self._codec.setText(codec)

    def set_logs(self, lines: list[str]) -> None:
        """Cap nhat noi dung nhat ky request."""
        self._log.setPlainText("\n".join(lines))
