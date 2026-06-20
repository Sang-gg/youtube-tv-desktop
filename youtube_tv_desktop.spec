# -*- mode: python ; coding: utf-8 -*-
"""Cau hinh PyInstaller cho YouTube TV Desktop.

Build: pyinstaller youtube_tv_desktop.spec
Ket qua: dist/YouTubeTVDesktop/
"""

from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

# Dong goi cac file JS template trong app/assets/js.
datas = [("app/assets/js", "app/assets/js")]

a = Analysis(
 ["run.py"],
 pathex=[],
 binaries=[],
 datas=datas,
 hiddenimports=["watchdog", "watchdog.observers", "watchdog.events"],
 hookspath=[],
 hooksconfig={},
 runtime_hooks=[],
 excludes=[],
 win_no_prefer_redirects=False,
 win_private_assemblies=False,
 cipher=block_cipher,
 noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
 pyz,
 a.scripts,
 [],
 exclude_binaries=True,
 name="YouTubeTVDesktop",
 debug=False,
 bootloader_ignore_signals=False,
 strip=False,
 upx=True,
 console=False, # ung dung windowed (khong console)
 disable_windowed_traceback=False,
 target_arch=None,
 codesign_identity=None,
 entitlements_file=None,
)

coll = COLLECT(
 exe,
 a.binaries,
 a.zipfiles,
 a.datas,
 strip=False,
 upx=True,
 upx_exclude=[],
 name="YouTubeTVDesktop",
)
