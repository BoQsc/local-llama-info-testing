import tkinter as tk
from ctypes import windll

# Restore window on drag after maximization
def drag_to_restore(event):
    global xwin, ywin, drag_start_x, drag_start_y
    drag_start_x = event.x_root
    drag_start_y = event.y_root

    if window.state() == 'zoomed':
        width_ratio = xwin / window.winfo_width()  # Calculate ratio of cursor within window
        window.state('normal')  # Restore window to normal
        window.update_idletasks()  # Ensure geometry updates

        new_x = drag_start_x - int(window.winfo_width() * width_ratio)  # Recalculate X based on ratio
        new_y = drag_start_y - ywin

        new_x = max(0, min(new_x, window.winfo_screenwidth() - window.winfo_width()))  # Stay within bounds
        new_y = max(0, min(new_y, window.winfo_screenheight() - window.winfo_height()))
        
        window.geometry(f'+{new_x}+{new_y}')  # Set new position
        xwin = int(window.winfo_width() * width_ratio)  # Update position values for future dragging

def set_appwindow(root):
    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    hwnd = windll.user32.GetParent(root.winfo_id())
    style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW
    style = style | WS_EX_APPWINDOW
    windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
    root.withdraw()
    root.after(10, root.deiconify)

def minimize_window():
    hwnd = windll.user32.GetParent(window.winfo_id())
    windll.user32.ShowWindow(hwnd, 6)  # SW_MINIMIZE = 6

def toggle_maximize(event):
    if window.state() == 'zoomed':
        window.state('normal')
        titlebar.maximize_button.config(text='🗖')
    else:
        window.state('zoomed')
        titlebar.maximize_button.config(text='❐')

#_____________Create_Window________________
window = tk.Tk()
window.title("Example")
window.geometry("300x300")
window.overrideredirect(True)

#______________Title_Bar___________________
titlebar = tk.Frame(window, bg="#2c2c2c")

#______________Title_Bar_Name___________________
titlebar.name = tk.Label(titlebar, text=window.title(), bg="#2c2c2c", fg="white")

#______________Title_Bar_Buttons___________________
titlebar.minimize_button = tk.Button(titlebar, command=minimize_window)
titlebar.maximize_button = tk.Button(titlebar, command=lambda: window.state('zoomed') if window.state() != 'zoomed' else window.state('normal'))
titlebar.exit_button = tk.Button(titlebar, command=window.destroy)

#______________Button_Configurations___________________
for button in (titlebar.minimize_button, titlebar.maximize_button, titlebar.exit_button):
    button.config(bg="#2c2c2c", fg='white', activebackground="red", activeforeground="white",
                  padx=5, pady=2, bd=0, width=2, highlightthickness=0)
    button.bind("<Enter>", lambda event: event.widget.config(bg="#777777", fg='black'))
    button.bind("<Leave>", lambda event: event.widget.config(bg="#2c2c2c", fg='white'))

#______________Button_Text___________________
titlebar.minimize_button.config(text='🗕', font="bold")
titlebar.maximize_button.config(text='🗖', font="bold")
titlebar.exit_button.config(text='🗙', font="bold")

#_______________Layout_____________________
titlebar.pack(fill=tk.X)  
titlebar.name.pack(side='left', padx=5)  
titlebar.exit_button.pack(side=tk.RIGHT)  
titlebar.maximize_button.pack(side=tk.RIGHT)  
titlebar.minimize_button.pack(side=tk.RIGHT)  

#______________Title_Bar_Dragging___________________
# Add window dragging functionality
def get_pos(event):
    global xwin, ywin
    xwin = event.x
    ywin = event.y

def move_window(event):
    window.geometry(f'+{event.x_root - xwin}+{event.y_root - ywin}')

titlebar.bind('<Button-1>', get_pos)
titlebar.bind('<B1-Motion>', move_window)
titlebar.name.bind('<Button-1>', get_pos)
titlebar.name.bind('<B1-Motion>', move_window)

# Bind double-click to maximize/restore
titlebar.bind('<Double-1>', toggle_maximize)
titlebar.name.bind('<Double-1>', toggle_maximize)

# Bind drag to restore functionality when maximized
titlebar.bind('<Button-1>', drag_to_restore, add="+")
titlebar.name.bind('<Button-1>', drag_to_restore, add="+")

# Set the window to appear in the taskbar
window.after(10, lambda: set_appwindow(window))

#______________Window_Resize_By_Drag___________________
border_size = 10  # Width of the resize border area
resize_dir = None

def moveMouseButton(e):
    global resize_dir
    x1 = window.winfo_pointerx()
    y1 = window.winfo_pointery()
    x0 = window.winfo_rootx()
    y0 = window.winfo_rooty()
    w = window.winfo_width()
    h = window.winfo_height()

    if resize_dir == 'right':
        window.geometry(f"{x1 - x0}x{h}")
    elif resize_dir == 'bottom':
        window.geometry(f"{w}x{y1 - y0}")
    elif resize_dir == 'corner':
        window.geometry(f"{x1 - x0}x{y1 - y0}")
    elif resize_dir == 'left':
        new_width = w - (x1 - x0)
        window.geometry(f"{new_width}x{h}+{x1}+{y0}")
    elif resize_dir == 'top' and window.state() != 'zoomed':  # Disable top resize when maximized
        new_height = h - (y1 - y0)
        window.geometry(f"{w}x{new_height}+{x0}+{y1}")

def detect_resize_dir(e):
    global resize_dir
    x, y = e.x, e.y
    w, h = window.winfo_width(), window.winfo_height()

    if x > w - border_size and y > h - border_size:
        resize_dir = 'corner'
        window.config(cursor="size_nw_se")
    elif x > w - border_size:
        resize_dir = 'right'
        window.config(cursor="size_we")
    elif y > h - border_size:
        resize_dir = 'bottom'
        window.config(cursor="size_ns")
    elif x < border_size:
        resize_dir = 'left'
        window.config(cursor="size_we")
    elif y < border_size and window.state() != 'zoomed':  # Disable top resize when maximized
        resize_dir = 'top'
        window.config(cursor="size_ns")
    else:
        resize_dir = None
        window.config(cursor="arrow")

# Bind mouse events for window resize
window.bind("<B1-Motion>", moveMouseButton)
window.bind("<Motion>", detect_resize_dir)

window.mainloop()
