import tkinter as tk
import ctypes as ct


# Function to set immersive dark mode
def set_immersive_dark_mode():
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = ct.c_int(2)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))


window = tk.Tk()
window.title("Program")
window.update()

window.bind('<F11>', lambda event: (
    window.update(),
    set_immersive_dark_mode(),  # Set dark mode again
    window.geometry("500x400"),
    window.attributes('-fullscreen', not window.attributes('-fullscreen')),
    set_immersive_dark_mode()  # Set dark mode after fullscreen toggle
))
window.bind('<Escape>', lambda event: window.attributes('-fullscreen', False))

set_immersive_dark_mode()
window.geometry("300x300")
window.configure(bg='#2c2c2c')

import time
time.sleep(2)
window.attributes('-fullscreen', not window.attributes('-fullscreen'))
window.geometry("300x300")
time.sleep(4)
window.attributes('-fullscreen', not window.attributes('-fullscreen'))
window.geometry("300x300")
time.sleep(4)
set_immersive_dark_mode()
print("done")

window.mainloop()
