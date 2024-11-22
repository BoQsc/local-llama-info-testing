import tkinter as tk

class CustomWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Initially disable original titlebar
        self.overrideredirect(True)

        # Create the custom titlebar frame
        self.titlebar = tk.Frame(self, bg="gray", relief="raised", bd=2)
        self.titlebar.pack(fill="x")

        # Add the custom title label
        self.title_label = tk.Label(self.titlebar, text="Custom Titlebar", fg="white", bg="gray")
        self.title_label.pack(side="left", padx=10)

        # Add a button to toggle fullscreen
        self.fullscreen_button = tk.Button(self.titlebar, text="Fullscreen", command=self.toggle_fullscreen)
        self.fullscreen_button.pack(side="right", padx=10)

        # Add content area for testing
        self.content = tk.Label(self, text="Content goes here", font=("Arial", 20))
        self.content.pack(expand=True)

        # Variables for drag functionality
        self._drag_data = {"x": 0, "y": 0}

        # Store the original geometry before going fullscreen
        self._normal_geometry = self.geometry()

        # Bind mouse events for dragging
        self.titlebar.bind("<ButtonPress-1>", self.on_drag_start)
        self.titlebar.bind("<B1-Motion>", self.on_drag_motion)

    def on_drag_start(self, event):
        """Initiate the drag action when the titlebar is clicked."""
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_drag_motion(self, event):
        """Move the window as the mouse is dragged."""
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        new_x = self.winfo_x() + delta_x
        new_y = self.winfo_y() + delta_y
        self.geometry(f"+{new_x}+{new_y}")

    def toggle_fullscreen(self):
        """Toggle fullscreen mode for testing drag-to-restore."""
        if self.attributes("-fullscreen"):
            # Exit fullscreen mode
            self.attributes("-fullscreen", False)
            self.geometry(self._normal_geometry)  # Restore the original geometry
            self.overrideredirect(True)  # Re-enable the custom titlebar
        else:
            # Save the current window state (geometry) before entering fullscreen
            self._normal_geometry = self.geometry()

            # Disable the custom titlebar for fullscreen mode
            self.overrideredirect(False)

            # Enable fullscreen mode
            self.attributes("-fullscreen", True)
            self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")  # Set to fullscreen size

if __name__ == "__main__":
    window = CustomWindow()
    window.geometry("800x600")  # Initial size
    window.mainloop()
