from contextlib import contextmanager
from tkinter import Tk, Frame, Label
import tkinter as tk

@contextmanager
def tk_app():
    class AutoPackTk(Tk):
        def __init__(self):
            super().__init__()
            self._unpacked = []
        
        def auto_pack(self):
            def pack_recursive(widget):
                for child in widget.winfo_children():
                    pack_recursive(child)
                if not widget.winfo_manager():
                    widget.pack(fill='x') if isinstance(widget, Frame) else widget.pack()

            for widget in self.winfo_children():
                pack_recursive(widget)

    root = AutoPackTk()
    try:
        yield root
        root.auto_pack()
        root.mainloop()
    finally:
        root.destroy()

with tk_app() as window:
    window.title("Example")
    window.geometry("300x300")
    window.overrideredirect(True)
    
    titlebar = Frame(window, bg="#2c2c2c", height=30)  
    title_label = Label(titlebar, text="Custom Title Bar", bg="#2c2c2c", fg="white")
    
    content = Frame(window, bg="white")
    Label(content, text="Window Content", bg="white")