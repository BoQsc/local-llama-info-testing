import tkinter as tk
from tkinter import Tk, Frame, Label
from contextlib import contextmanager

class DraggableWindow:
    def __init__(self, window):
        self.window = window
        self.drag_data = {"x": 0, "y": 0}

    def on_mouse_drag(self, event):
        # Use the current mouse position to set the initial drag position
        if self.drag_data["x"] == 0 and self.drag_data["y"] == 0:
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

        # Calculate the new position and move the window
        x = self.window.winfo_x() + (event.x - self.drag_data["x"])
        y = self.window.winfo_y() + (event.y - self.drag_data["y"])
        self.window.geometry(f"+{x}+{y}")

    def reset_drag(self):
        # Reset drag data when the mouse button is released
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0


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

        # Create the draggable functionality
        dragger = DraggableWindow(window)

        # Bind mouse events for dragging
        titlebar.bind("<B1-Motion>", dragger.on_mouse_drag)
        titlebar.bind("<ButtonRelease-1>", lambda event: dragger.reset_drag())  # Reset drag on release

        # Add window content
        content_frame = Frame(window, bg="white")
        content_frame.pack(fill='both', expand=True)
        Label(content_frame, text="Window Content", bg="white").pack()


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
