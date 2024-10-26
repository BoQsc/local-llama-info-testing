import tkinter as tk
from tkinter import Tk, Frame, Label
from contextlib import contextmanager

class DraggableWindow:
    def __init__(self, window):
        self.window = window
        self.drag_data = {"x": 0, "y": 0}

    def on_mouse_drag(self, event):
        if self.drag_data["x"] == 0 and self.drag_data["y"] == 0:
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
        x = self.window.winfo_x() + (event.x - self.drag_data["x"])
        y = self.window.winfo_y() + (event.y - self.drag_data["y"])
        self.window.geometry(f"+{x}+{y}")

    def reset_drag(self):
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0


def main():
    with tk_app() as window:
        window.title("Example")
        window.geometry("300x300")
        window.overrideredirect(True)

        titlebar = Frame(window, bg="#2c2c2c", height=30)
        titlebar.pack(fill='x')

        title_label = Label(titlebar, text="Custom Title Bar", bg="#2c2c2c", fg="white")
        title_label.pack(side='left', padx=5)

        dragger = DraggableWindow(window)

        titlebar.bind("<B1-Motion>", dragger.on_mouse_drag)
        titlebar.bind("<ButtonRelease-1>", lambda event: dragger.reset_drag())
        title_label.bind("<B1-Motion>", dragger.on_mouse_drag)
        title_label.bind("<ButtonRelease-1>", lambda event: dragger.reset_drag())

        content_frame = Frame(window, bg="white")
        content_frame.pack(fill='both', expand=True)
        Label(content_frame, text="Window Content", bg="white").pack()

        # Bind F11 to maximize the window
        window.bind("<F11>", lambda event: toggle_maximize(window))


def toggle_maximize(window):
    if window.winfo_width() == window.winfo_screenwidth() and window.winfo_height() == window.winfo_screenheight():
        window.geometry("300x300")  # Restore to default size
    else:
        window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")  # Maximize to screen size


@contextmanager
def _tk_app():
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

tk_app = _tk_app

if __name__ == "__main__":
    main()
