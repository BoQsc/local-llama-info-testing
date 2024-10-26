import tkinter as tk
import ctypes as ct

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
    set_immersive_dark_mode(),  
    window.geometry("500x400"),
    window.attributes('-fullscreen', not window.attributes('-fullscreen')),
    set_immersive_dark_mode()  
))
window.bind('<Escape>', lambda event: window.attributes('-fullscreen', False))

print("setting dark color")

set_immersive_dark_mode()
window.geometry("300x300")
window.configure(bg='#2c2c2c')
window.update()
import time
time.sleep(1)

print("setting to fullscreen")
window.attributes('-fullscreen', not window.attributes('-fullscreen'))
window.update()
time.sleep(1)

print("back from fullscreen")
window.attributes('-fullscreen', not window.attributes('-fullscreen'))
set_immersive_dark_mode()
window.update()
window.geometry("300x301")

print("setting to fullscreen")
window.attributes('-fullscreen', not window.attributes('-fullscreen'))
window.update()
time.sleep(1)

print("back from fullscreen")
window.attributes('-fullscreen', not window.attributes('-fullscreen'))
set_immersive_dark_mode()
window.update()
window.geometry("300x300")

print("done")

window.mainloop()
