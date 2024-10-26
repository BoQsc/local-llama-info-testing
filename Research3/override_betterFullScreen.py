def maximizeToggle(self, event=None):
    if not self.maximized:
        self.winfo_update()
        # Maximize the current window
        self.maximize_btn.config(text="❐")
        self.parent.wm_attributes("-topmost", True)
        width, height = self.parent.maxsize()
        self.parent.geometry(f'{width}x{height + 18}+0-0')
        self.maximized = True
        self.move_window_bindings(status=False)
    else:
        from ctypes import windll

        # Restore down window
        self.maximize_btn.config(text="🗖")
        self.parent.wm_attributes("-topmost", False)
        hwnd = windll.user32.GetParent(self.parent.winfo_id())
        SWP_SHOWWINDOW = 0x40
        windll.user32.SetWindowPos(hwnd, 0, 
            self.previousPosition[0],
            self.previousPosition[1],
            int(self.parent.windowSize[0]),
            int(self.parent.windowSize[1]),
            SWP_SHOWWINDOW)
        self.maximized = False
        self.move_window_bindings(status=True)
    print("Overridden maximizeToggle")