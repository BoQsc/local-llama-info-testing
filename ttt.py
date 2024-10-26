import tkinter as tk
import ctypes as ct

window = tk.Tk()
window.title("Example")
window.update()

DWMWA_USE_IMMERSIVE_DARK_MODE = 20
set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
get_parent = ct.windll.user32.GetParent
hwnd = get_parent(window.winfo_id())
rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
value = ct.c_int(2)
set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))

window.geometry("300x300")  
window.configure(bg='#2c2c2c')

window.bind('<F11>',    lambda event: window.attributes('-fullscreen', not window.attributes('-fullscreen')))
window.bind('<Escape>', lambda event: window.attributes('-fullscreen', False))

window.mainloop()
