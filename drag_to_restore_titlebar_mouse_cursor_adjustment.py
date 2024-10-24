import tkinter as tk

class CustomWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Drag to Restore")
        self.geometry("300x200")
        self.overrideredirect(True)  # Remove the window decorations
        self.bind("<Button-1>", self.start_drag)
        self.bind("<B1-Motion>", self.do_drag)
        self.bind("<ButtonRelease-1>", self.end_drag)

        self.dragging = False
        self.offset = 0

    def start_drag(self, event):
        self.dragging = True
        self.offset = event.y + 10  # Offset to make cursor 10px below

    def do_drag(self, event):
        if self.dragging:
            self.geometry(f"+{event.x_root}+{event.y_root - self.offset}")

    def end_drag(self, event):
        self.dragging = False
        self.geometry("300x200")  # Restore size for demonstration

if __name__ == "__main__":
    app = CustomWindow()
    app.mainloop()
