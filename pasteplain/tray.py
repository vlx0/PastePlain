"""System tray icon."""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .ui import PastePlainApp


def make_tray_image():
    from PIL import Image, ImageDraw

    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((10, 8, size - 10, size - 8), radius=8, fill=(147, 197, 253, 255))
    draw.rectangle((20, 20, 44, 44), outline=(17, 17, 17, 255), width=3)
    draw.line((26, 28, 38, 28), fill=(17, 17, 17, 255), width=2)
    draw.line((26, 34, 34, 34), fill=(17, 17, 17, 255), width=2)
    return img


class TrayIcon:
    def __init__(
        self,
        app: PastePlainApp,
        on_show: Callable[[], None],
        on_paste: Callable[[], None],
        on_quit: Callable[[], None],
    ) -> None:
        self._app = app
        self._on_show = on_show
        self._on_paste = on_paste
        self._on_quit = on_quit
        self._icon = None
        self._thread: threading.Thread | None = None
        self._ready = threading.Event()

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._run, daemon=True, name="PastePlainTray")
        self._thread.start()
        self._ready.wait(timeout=5)

    def _run(self) -> None:
        import pystray
        from pystray import MenuItem as item

        menu = pystray.Menu(
            item("Открыть", lambda _i, _it: self._app.after(0, self._on_show)),
            item("Вставить без формата", lambda _i, _it: self._app.after(0, self._on_paste)),
            pystray.Menu.SEPARATOR,
            item("Выход", lambda _i, _it: self._app.after(0, self._on_quit)),
        )
        self._icon = pystray.Icon(
            "PastePlain",
            make_tray_image(),
            "PastePlain — вставка без формата",
            menu,
        )
        self._ready.set()
        self._icon.run()

    def notify(self, text: str, title: str = "PastePlain") -> None:
        if self._icon is not None:
            try:
                self._icon.notify(text, title)
            except Exception:
                pass

    def stop(self) -> None:
        if self._icon is not None:
            try:
                self._icon.stop()
            except Exception:
                pass
            self._icon = None
