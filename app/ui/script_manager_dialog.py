"""Script Manager Dialog.

Giao dien quan ly UserScript: danh sach, bat/tat, reload, mo thu muc, xem metadata.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
)

from ..userscripts.manager import UserScriptManager


class ScriptManagerDialog(QDialog):
    """Cua so quan ly UserScript."""

    def __init__(
        self,
        manager: UserScriptManager,
        on_reload: Callable[[], None],
        on_open_folder: Callable[[], None],
        parent=None,  # noqa: ANN001
    ) -> None:
        super().__init__(parent)
        self._manager = manager
        self._on_reload = on_reload
        self._on_open_folder = on_open_folder
        self.setWindowTitle("Script Manager - YouTube TV Desktop")
        self.resize(640, 480)
        self._build_ui()
        self._refresh_list()

    def _build_ui(self) -> None:
        """Dung giao dien danh sach + nut chuc nang."""
        layout = QVBoxLayout(self)
        self._list = QListWidget()
        self._list.itemChanged.connect(self._on_item_changed)
        self._list.currentItemChanged.connect(self._on_selection_changed)
        layout.addWidget(self._list)

        self._meta_label = QLabel("Chon mot script de xem metadata.")
        self._meta_label.setWordWrap(True)
        layout.addWidget(self._meta_label)

        buttons = QHBoxLayout()
        reload_btn = QPushButton("Reload")
        reload_btn.clicked.connect(self._reload)
        open_btn = QPushButton("Mo thu muc")
        open_btn.clicked.connect(self._on_open_folder)
        close_btn = QPushButton("Dong")
        close_btn.clicked.connect(self.accept)
        buttons.addWidget(reload_btn)
        buttons.addWidget(open_btn)
        buttons.addStretch()
        buttons.addWidget(close_btn)
        layout.addLayout(buttons)

    def _refresh_list(self) -> None:
        """Lam moi danh sach script tu manager."""
        self._list.blockSignals(True)
        self._list.clear()
        for script in self._manager.scripts:
            item = QListWidgetItem(
                f"{script.metadata.name} v{script.metadata.version}"
            )
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(
                Qt.CheckState.Checked if script.enabled else Qt.CheckState.Unchecked
            )
            item.setData(Qt.ItemDataRole.UserRole, str(script.path))
            self._list.addItem(item)
        self._list.blockSignals(False)

    def _on_item_changed(self, item: QListWidgetItem) -> None:
        """Bat/tat script khi tich checkbox."""
        path = Path(item.data(Qt.ItemDataRole.UserRole))
        enabled = item.checkState() == Qt.CheckState.Checked
        self._manager.set_enabled(path, enabled)
        self._on_reload()

    def _on_selection_changed(self, current: QListWidgetItem | None) -> None:
        """Hien thi metadata cua script dang chon."""
        if current is None:
            return
        path = Path(current.data(Qt.ItemDataRole.UserRole))
        for script in self._manager.scripts:
            if script.path == path:
                m = script.metadata
                self._meta_label.setText(
                    f"Ten: {m.name}\nPhien ban: {m.version}\n"
                    f"Tac gia: {m.author}\nMo ta: {m.description}\n"
                    f"Match: {', '.join(m.matches)}\nRun-at: {m.run_at}"
                )
                break

    def _reload(self) -> None:
        """Reload script tu dia roi lam moi danh sach."""
        self._manager.reload()
        self._on_reload()
        self._refresh_list()
