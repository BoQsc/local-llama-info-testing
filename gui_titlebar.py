import tkinter as tk
from ctypes import windll

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

# Set the window to appear in the taskbar
window.after(10, lambda: set_appwindow(window))

window.mainloop()