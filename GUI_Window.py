import tkinter as tk
from tkinter import Tk, Frame, Label
from contextlib import contextmanager


def main():
    with tk_app() as window:
        window.title("Example")
        window.geometry("300x300")
        window.overrideredirect(True)

        # Create a title bar frame
        titlebar = Frame(window, bg="#2c2c2c", height=30)
        titlebar.pack(fill='x')

        # Add title label
        title_label = Label(titlebar, text="Custom Title Bar", bg="#2c2c2c", fg="white")
        title_label.pack(side='left', padx=5)

        # Bind mouse events for dragging
        titlebar.bind("<Button-1>", lambda event: on_button_press(event, window))
        titlebar.bind("<B1-Motion>", lambda event: on_mouse_drag(event, window))

        # Add window content
        content_frame = Frame(window, bg="white")
        content_frame.pack(fill='both', expand=True)
        Label(content_frame, text="Window Content", bg="white").pack()


def on_button_press(event, window):
    # Store the current mouse position
    global x_offset, y_offset
    x_offset = event.x
    y_offset = event.y


def on_mouse_drag(event, window):
    # Calculate new position and move the window
    x = event.x_root - x_offset
    y = event.y_root - y_offset
    window.geometry(f"+{x}+{y}")


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
