import os
import utils
import time
import _thread
import ctypes

from tkinter import *
from tkinter import messagebox
from yt_dlp import YoutubeDL

from typing import (
    Any,
    AnyStr,
)

client = YoutubeDL({"format": "bestvideo[ext=mp4]/best"})

colors = ("#EEECEC", "#DAD9D9", "#C1C0C0", "#ABAAAA", "#929090", "#828181")
colors_white = tuple(reversed(("white", "#EEECEC", "#DAD9D9", "#C1C0C0", "#ABAAAA", "#929090", "#828181")))
gray = False

def download(url: AnyStr) -> Any:
    global client, download_button
    
    download_button.config(state=DISABLED)
    download_button.update()

    is_valid_url = utils.check_url_youtube(url)
    
    if not is_valid_url:
        messagebox.showwarning("경고", "올바르지 않은 링크가 입력 되었습니다.")
        download_button.config(state=ACTIVE)
        return download_button.update()

    client.download([url])
    download_button.config(state=ACTIVE)
    download_button.update()

def exit():
    global root

    alpha = root.attributes("-alpha")

    if alpha > 0.0:
        alpha -= 0.01
        root.attributes("-alpha", alpha)
        root.after(1, exit)
    else:
        root.destroy()
        os._exit(1)

def change_color():
    global root, colors, colors_white, gray, dark_mode_button, program_name, info

    dark_mode_button.config(state=DISABLED)
    dark_mode_button.update()

    if not gray:
        for gray in colors:
            root.config(bg=gray)
            time.sleep(0.1)
            root.update()
            program_name.config(bg=gray, fg="white")
            program_name.update()
            info.config(bg=gray, fg="white")
            info.update()
            
        gray = True
        dark_mode_button.config(text="다크모드 끄기")
        dark_mode_button.update()
    else:
        for white in colors_white:
            root.config(bg=white)
            time.sleep(0.1)
            root.update()
            program_name.config(bg=white, fg="black")
            program_name.update()
            info.config(bg=white, fg="black")
            info.update()

        gray = False
        dark_mode_button.config(text="다크모드 켜기")
        dark_mode_button.update()

    dark_mode_button.config(state=ACTIVE)
    dark_mode_button.update()

utils.TkUtils.SetProcessDpiAwareness(True)

root = Tk("유튜브 다운로더")
root.title("유튜브 다운로더")
root.geometry("300x100+200+200" if ctypes.windll.user32.GetDpiForWindow(root.winfo_id()) < 105 else "300x300+200+200")
root.resizable(False, False)
root.config(bg="white")
root.overrideredirect(True)
root.after(10, utils.TkUtils.resolve_taskbar, root)

root.grid_rowconfigure(0, weight=0)
root.grid_columnconfigure(0, weight=1)

exit_button = Button(root, text="X", bd=0, bg="#FF6969", fg="white", width=5, command=exit)
program_name = Label(root, text="유튜브 다운로더", fg="black", bg=root["bg"], bd=0)
dark_mode_button = Button(root, text="다크모드 켜기", fg="black", bg="#DDD8D8", bd=0, command=change_color)
info = Label(root, text="▼ 아래에 유튜브 링크를 입력하세요!", bg=root["bg"])

youtube_link_entry = Entry(root, bg="#BDB9B9", fg="black", bd=0, width=45)

download_button = Button(root, text="다운로드", bd=0, fg="black", bg="#E0E0E0", command=lambda: _thread.start_new_thread(download, (youtube_link_entry.get(), )))

exit_button.grid(row=0, column=0, sticky=W)
program_name.grid(row=0, column=0, sticky=S)
dark_mode_button.grid(row=2, column=0, sticky=W)
youtube_link_entry.grid(row=3, column=0, sticky=W)
info.grid(row=2, column=0, sticky=E)
download_button.grid(row=4, sticky=S, ipadx=30, ipady=3)

root.bind("<Button-1>", lambda event: utils.TkUtils.save_cursor_location(event))
root.bind("<B1-Motion>", lambda event: utils.TkUtils.dragging(root, event))
root.mainloop()
