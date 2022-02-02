import ctypes

from tkinter import (
    Tk,
    Event,
)
from typing import (
    Any,
    AnyStr,
    ClassVar,
    Union,
)

def check_url_youtube(url: AnyStr):
    URL_STRINGS = (
        "youtu.be",
        "youtube.com"
    )

    return any([i in url for i in URL_STRINGS])

class _TkUtils:
    GWL_EXSTYLE: ClassVar[int] = -20
    WS_EX_APPWINDOW: ClassVar[int] = 0x00040000
    WS_EX_TOOLWINDOW: ClassVar[int] = 0x00000080
    x: ClassVar[int] = 0
    y: ClassVar[int] = 0

    def resolve_taskbar(self, master: Union[Tk, Any]):
        hwnd = ctypes.windll.user32.GetParent(master.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, self.GWL_EXSTYLE)
        style = style & ~self.WS_EX_TOOLWINDOW
        style = style | self.WS_EX_APPWINDOW
        ctypes.windll.user32.SetWindowLongW(hwnd, self.GWL_EXSTYLE, style)
        master.wm_withdraw()
        return master.after(10, master.wm_deiconify)

    def save_cursor_location(self, event: Union[Event, Any]):
        self.x = event.x
        self.y = event.y

    def dragging(self, master: Union[Tk, Any], event: Union[Tk, Any]):
        x, y = event.x - self.x + master.winfo_x(), event.y - self.y + master.winfo_y()
        master.geometry(f"+{x}+{y}")

    def SetProcessDpiAwareness(self, value: Union[bool, int]):
        try:
            return ctypes.windll.shcore.SetProcessDpiAwareness(value.as_integer_ratio()[0] if isinstance(value, bool) else value)
        except:
            try:
                return ctypes.windll.user32.SetProcessDpiAware()
            except:
                return None

TkUtils = _TkUtils()    
