def maximizeToggle():
    root.wm_attributes("-topmost", True)
    width, height = root.maxsize()
    root.geometry(f'{width}x{height + 18}+0-0')
