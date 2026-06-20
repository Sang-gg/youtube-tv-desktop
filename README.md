# YouTube TV Desktop

Ung dung Desktop bang Python + PySide6 mang lai trai nghiem **YouTube TV** tren
Windows tuong tu Smart TV Samsung Tizen. Dung **Qt WebEngine** lam loi trinh
duyet, tu dong mo `https://www.youtube.com/tv`, fullscreen mac dinh, tang toc
GPU va luu phien dang nhap giua cac lan mo.

## Tinh nang

- **Browser Core**: Qt WebEngine, fullscreen, zoom, reload, kiosk.
- **TV Environment Emulator**: gia lap `navigator`, `window.tizen`,
  `window.webapis` (avplay, productinfo) va do phan giai 1080p/2K/4K/8K.
- **YouTube API Layer**: log request `youtubei/v1/{player,browse,next,search}`
  qua interceptor + hook fetch/XHR (khong can thiep DRM).
- **Remote Control**: map phim mui ten / Enter / Backspace / Escape / Space cho
  ban phim va remote USB (HID).
- **Media Optimization**: hien codec (VP9/AV1/H264), do phan giai, dropped
  frames, thong ke mang.
- **Pairing Support**: dang nhap bang ma ghep noi (youtube.com/activate), luu
  token cuc bo.
- **Settings System**: User-Agent, che do TV, fullscreen, kiosk, JS injection,
  thu muc du lieu.
- **Debug Console**: User-Agent, URL, do phan giai, codec, nhat ky request,
  thong tin WebEngine.
- **Ad Blocking System**: network blocking, cosmetic filtering, JS filtering,
  SponsorBlock, filter lists (EasyList/EasyPrivacy/uBlock), domain tuy chinh.
- **UserScript Engine**: nap *.js kieu Tampermonkey, metadata parser, run-at,
  URL matching, GM API (GM_log/GM_addStyle/GM_getValue/GM_setValue), hot reload.

## Cau truc thu muc

```text
.
├── run.py                     # Diem khoi chay tien loi
├── requirements.txt
├── youtube_tv_desktop.spec    # Cau hinh PyInstaller
└── app/
    ├── main.py                # Entry point + cau hinh flag Chromium/GPU
    ├── config.py              # He thong cau hinh (JSON)
    ├── constants.py           # Hang so toan cuc
    ├── paths.py               # Quan ly duong dan userdata
    ├── assets/                # JS template (doc luc runtime)
    │   └── js/
    ├── core/                  # Browser core, emulator, interceptor, api
    ├── features/              # Adblock, sponsorblock, media, remote, pairing
    ├── userscripts/           # UserScript engine (metadata, manager, reload)
    └── ui/                    # MainWindow, Settings, Debug, Script Manager
```

## Yeu cau

- Python 3.12+
- PySide6 (moi nhat)

## Cai dat & chay

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
python run.py
```

## Phim tat

| Phim | Chuc nang |
|------|-----------|
| Mui ten | Dieu huong TV (Up/Down/Left/Right) |
| Enter | OK |
| Backspace | Back |
| Escape | Exit (bi vo hieu trong kiosk) |
| Space | Play/Pause |
| Ctrl+S | Mo Settings |
| Ctrl+D | Mo Debug Console |
| Ctrl+M | Mo Script Manager |
| Ctrl+R | Reload trang |
| Ctrl+F | Bat/tat fullscreen |
| Ctrl++ / Ctrl+- | Zoom in/out |

## UserScripts

Dat cac file `*.js` vao `userdata/userscripts/`. Vi du metadata:

```javascript
// ==UserScript==
// @name My Script
// @version 1.0
// @author User
// @match https://www.youtube.com/*
// @exclude https://www.youtube.com/live_chat*
// @run-at document-start
// ==/UserScript==
```

Ho tro `GM_log`, `GM_addStyle`, `GM_getValue`, `GM_setValue`. Hot reload tu dong
phat hien thay doi file (can goi `watchdog`).

## Build file .exe (PyInstaller)

```bash
pip install pyinstaller
pyinstaller youtube_tv_desktop.spec
```

File .exe nam trong `dist/YouTubeTVDesktop/`. Lenh nhanh (khong dung spec):

```bash
pyinstaller --noconfirm --windowed --name YouTubeTVDesktop ^
  --add-data "app/assets/js;app/assets/js" run.py
```

> Luu y: tren Windows dung dau `;` de phan tach trong `--add-data`; tren
> Linux/macOS dung dau `:`.

## Ghi chu phap ly

Ad blocking va API logging chi phuc vu muc dich phan tich/debug ca nhan. Ung
dung **khong** can thiep DRM hay co che bao ve cua YouTube.
