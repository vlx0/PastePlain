"""PastePlain GUI."""

from __future__ import annotations

import ctypes
import tkinter as tk

from . import __version__
from .hotkeys import HotkeyManager, format_hotkey
from .instance import WINDOW_TITLE
from .plain import paste_plain
from .tray import TrayIcon

BG = "#111111"
FG = "#ffffff"
MUTED = "#999999"
CARD = "#1a1a1a"
OK = "#86efac"
WARN = "#f87171"
ACCENT = "#93c5fd"


class PastePlainApp(tk.Tk):
    def __init__(self, start_hidden: bool = False) -> None:
        super().__init__()
        self.title(WINDOW_TITLE)
        self.geometry("440x300")
        self.minsize(380, 260)
        self.configure(bg=BG)
        self._exiting = False
        self._start_hidden = start_hidden
        self._tray: TrayIcon | None = None
        self._hotkeys = HotkeyManager(self, self.do_paste)

        pad = tk.Frame(self, bg=BG)
        pad.pack(fill="both", expand=True, padx=24, pady=20)

        tk.Label(pad, text="PastePlain", bg=BG, fg=FG, font=("Segoe UI Semibold", 18)).pack(anchor="w")
        tk.Label(
            pad,
            text="Вставка из буфера без форматирования",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(4, 18))

        card = tk.Frame(pad, bg=CARD, padx=20, pady=18)
        card.pack(fill="x")

        tk.Label(
            card,
            text="Скопируй что угодно → встань в поле → хоткей",
            bg=CARD,
            fg=FG,
            font=("Segoe UI", 10),
            wraplength=360,
            justify="center",
        ).pack(anchor="center")

        self._btn = tk.Label(
            card,
            text="Вставить сейчас",
            bg=ACCENT,
            fg=BG,
            font=("Segoe UI", 10),
            padx=16,
            pady=9,
            cursor="hand2",
        )
        self._btn.pack(anchor="center", pady=(16, 0))
        self._btn.bind("<Button-1>", lambda _e: self.do_paste())

        self._status = tk.Label(
            pad,
            text=f"хоткей: {format_hotkey()} · v{__version__}",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 9),
            anchor="w",
        )
        self._status.pack(fill="x", pady=(16, 0))

        self.protocol("WM_DELETE_WINDOW", self.hide_to_tray)
        self._hotkeys.start()
        if not self._hotkeys.registered:
            self._status.configure(text=f"хоткей {format_hotkey()} занят", fg=WARN)
        self.after(20, self._place)
        self.after(200, self._start_tray)
        if start_hidden:
            self.after(350, self.hide_to_tray)

    def _place(self) -> None:
        self.update_idletasks()
        w, h = self.winfo_width() or 440, self.winfo_height() or 300
        sw = ctypes.windll.user32.GetSystemMetrics(0)
        sh = ctypes.windll.user32.GetSystemMetrics(1)
        self.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 3}")

    def _start_tray(self) -> None:
        try:
            self._tray = TrayIcon(self, on_show=self.show_window, on_paste=self.do_paste, on_quit=self.quit_app)
            self._tray.start()
            if self._start_hidden:
                self.after(
                    800,
                    lambda: self._tray
                    and self._tray.notify(f"PastePlain · {format_hotkey()}", "PastePlain"),
                )
        except Exception as e:
            self._status.configure(text=f"трей: {e}", fg=WARN)

    def do_paste(self) -> None:
        ok, msg = paste_plain()
        self._status.configure(text=msg, fg=OK if ok else WARN)

    def show_window(self) -> None:
        self.deiconify()
        self.lift()
        self.attributes("-topmost", True)
        self.after(80, lambda: self.attributes("-topmost", False))
        self.focus_force()

    def hide_to_tray(self) -> None:
        self.withdraw()

    def quit_app(self) -> None:
        if self._exiting:
            return
        self._exiting = True
        self._hotkeys.stop()
        if self._tray is not None:
            try:
                self._tray.stop()
            except Exception:
                pass
        self.destroy()


def run(start_hidden: bool = False) -> None:
    PastePlainApp(start_hidden=start_hidden).mainloop()
