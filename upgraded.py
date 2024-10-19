# main.py
import tkinter as tk
from guit_titlebar_test import RootFrame
from override_betterFullScreen import maximizeToggle

# Override the method
RootFrame.maximizeToggle = maximizeToggle

root = tk.Tk()
root.geometry("300x300")

root_frame = RootFrame(root, bg="white", highlightthickness=1, highlightbackground="#2c2c2c")
root_frame.pack(fill=tk.BOTH, expand=True)

txt = tk.Label(root_frame, bg='white', text="Prototype window")
txt.pack(anchor="center")

def resize(self):
    root.wm_attributes("-topmost", True)
    width, height = root.maxsize()
    root.geometry(f'{width}x{height + 18}+0-0')

def toggle_fullscreen(event=None):
    if root.attributes("-fullscreen"):
        root.attributes("-fullscreen", False)
    else:
        root.attributes("-fullscreen", True)

# Bind F11 key to the toggle_fullscreen function
root.bind("<F11>", resize)

rsz = tk.Button(root_frame, text="Resize", command=resize)
rsz.pack()

root.mainloop()
