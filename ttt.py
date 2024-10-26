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



def toggle_fullscreen(event=None):
    is_fullscreen = window.attributes('-fullscreen')
    window.attributes('-fullscreen', not is_fullscreen)



# Bind the F11 key
window.bind('<F11>', toggle_fullscreen)

# Initial fullscreen setting
window.attributes('-fullscreen', True)

# Optional: to exit fullscreen mode with the Escape key
window.bind('<Escape>', lambda event: window.attributes('-fullscreen', False))

window.mainloop()
