"""Settings System.

Cua so cai dat cho phep dieu chinh User-Agent, che do TV, fullscreen, kiosk,
JS injection, adblock, sponsorblock, userscripts va thu muc luu du lieu.
"""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ..config import AppConfig
from ..constants import TV_RESOLUTIONS


class SettingsWindow(QDialog):
    """Cua so cai dat ung dung."""

    def __init__(
        self,
        config: AppConfig,
        on_save: Callable[[AppConfig], None],
        on_update_filters: Callable[[], None],
        parent=None,  # noqa: ANN001
    ) -> None:
        super().__init__(parent)
        self._config = config
        self._on_save = on_save
        self._on_update_filters = on_update_filters
        self.setWindowTitle("Cai dat - YouTube TV Desktop")
        self.resize(560, 520)
        self._build_ui()

    def _build_ui(self) -> None:
        """Dung giao dien voi cac tab General / AdBlock / Scripts."""
        layout = QVBoxLayout(self)
        tabs = QTabWidget()
        tabs.addTab(self._general_tab(), "Chung")
        tabs.addTab(self._adblock_tab(), "Ad Blocking")
        tabs.addTab(self._scripts_tab(), "UserScripts")
        layout.addWidget(tabs)

        buttons = QHBoxLayout()
        save_btn = QPushButton("Luu")
        save_btn.clicked.connect(self._save)
        cancel_btn = QPushButton("Huy")
        cancel_btn.clicked.connect(self.reject)
        buttons.addStretch()
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)
        layout.addLayout(buttons)

    def _general_tab(self) -> QWidget:
        """Tab cai dat chung."""
        widget = QWidget()
        form = QFormLayout(widget)

        self._ua_edit = QLineEdit(self._config.user_agent)
        form.addRow("User-Agent:", self._ua_edit)

        self._tv_mode = QComboBox()
        self._tv_mode.addItems(list(TV_RESOLUTIONS.keys()))
        self._tv_mode.setCurrentText(self._config.tv_mode)
        form.addRow("Che do TV:", self._tv_mode)

        self._fullscreen = QCheckBox("Fullscreen khi khoi dong")
        self._fullscreen.setChecked(self._config.fullscreen_on_start)
        form.addRow(self._fullscreen)

        self._kiosk = QCheckBox("Che do kiosk")
        self._kiosk.setChecked(self._config.kiosk_mode)
        form.addRow(self._kiosk)

        self._js_inject = QCheckBox("Bat JavaScript injection")
        self._js_inject.setChecked(self._config.js_injection_enabled)
        form.addRow(self._js_inject)

        data_row = QHBoxLayout()
        self._data_dir = QLineEdit(self._config.data_dir)
        browse = QPushButton("Chon...")
        browse.clicked.connect(self._browse_data_dir)
        data_row.addWidget(self._data_dir)
        data_row.addWidget(browse)
        container = QWidget()
        container.setLayout(data_row)
        form.addRow("Thu muc du lieu:", container)

        return widget

    def _adblock_tab(self) -> QWidget:
        """Tab cai dat ad blocking & sponsorblock."""
        widget = QWidget()
        form = QFormLayout(widget)

        self._adblock = QCheckBox("Bat chan quang cao")
        self._adblock.setChecked(self._config.adblock_enabled)
        form.addRow(self._adblock)

        self._cosmetic = QCheckBox("Bat cosmetic filtering (an phan tu)")
        self._cosmetic.setChecked(self._config.adblock_cosmetic_enabled)
        form.addRow(self._cosmetic)

        self._filter_lists = QCheckBox("Dung filter list (EasyList...)")
        self._filter_lists.setChecked(self._config.filter_lists_enabled)
        form.addRow(self._filter_lists)

        self._custom_domains = QLineEdit(
            ",".join(self._config.adblock_custom_domains)
        )
        self._custom_domains.setPlaceholderText("domain1.com, domain2.com")
        form.addRow("Domain tuy chinh:", self._custom_domains)

        update_btn = QPushButton("Cap nhat filter list ngay")
        update_btn.clicked.connect(self._on_update_filters)
        form.addRow(update_btn)

        self._sponsorblock = QCheckBox("Bat SponsorBlock (tua qua sponsor)")
        self._sponsorblock.setChecked(self._config.sponsorblock_enabled)
        form.addRow(self._sponsorblock)

        return widget

    def _scripts_tab(self) -> QWidget:
        """Tab cai dat UserScript engine."""
        widget = QWidget()
        form = QFormLayout(widget)

        self._userscripts = QCheckBox("Bat UserScript engine")
        self._userscripts.setChecked(self._config.userscripts_enabled)
        form.addRow(self._userscripts)

        self._hot_reload = QCheckBox("Hot reload khi file .js thay doi")
        self._hot_reload.setChecked(self._config.userscript_hot_reload)
        form.addRow(self._hot_reload)

        self._allow_clip = QCheckBox("Cho phep truy cap clipboard")
        self._allow_clip.setChecked(self._config.userscript_allow_clipboard)
        form.addRow(self._allow_clip)

        self._allow_ls = QCheckBox("Cho phep truy cap local storage")
        self._allow_ls.setChecked(self._config.userscript_allow_localstorage)
        form.addRow(self._allow_ls)

        self._allow_fetch = QCheckBox("Cho phep goi fetch/XHR")
        self._allow_fetch.setChecked(self._config.userscript_allow_fetch)
        form.addRow(self._allow_fetch)

        return widget

    def _browse_data_dir(self) -> None:
        """Mo hop thoai chon thu muc du lieu."""
        path = QFileDialog.getExistingDirectory(self, "Chon thu muc du lieu")
        if path:
            self._data_dir.setText(path)

    def _save(self) -> None:
        """Gom gia tri tu form vao config va goi callback luu."""
        cfg = self._config
        cfg.user_agent = self._ua_edit.text().strip()
        cfg.tv_mode = self._tv_mode.currentText()
        cfg.fullscreen_on_start = self._fullscreen.isChecked()
        cfg.kiosk_mode = self._kiosk.isChecked()
        cfg.js_injection_enabled = self._js_inject.isChecked()
        cfg.data_dir = self._data_dir.text().strip()

        cfg.adblock_enabled = self._adblock.isChecked()
        cfg.adblock_cosmetic_enabled = self._cosmetic.isChecked()
        cfg.filter_lists_enabled = self._filter_lists.isChecked()
        cfg.adblock_custom_domains = [
            d.strip() for d in self._custom_domains.text().split(",") if d.strip()
        ]
        cfg.sponsorblock_enabled = self._sponsorblock.isChecked()

        cfg.userscripts_enabled = self._userscripts.isChecked()
        cfg.userscript_hot_reload = self._hot_reload.isChecked()
        cfg.userscript_allow_clipboard = self._allow_clip.isChecked()
        cfg.userscript_allow_localstorage = self._allow_ls.isChecked()
        cfg.userscript_allow_fetch = self._allow_fetch.isChecked()

        self._on_save(cfg)
        self.accept()
