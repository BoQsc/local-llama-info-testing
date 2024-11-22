import tkinter as tk

# Toggle maximize/restore window state
def toggle_maximize(event):
    if window.state() == 'zoomed':
        window.state('normal')
        titlebar.maximize_button.config(text='🗖')
    else:
        window.state('zoomed')
        titlebar.maximize_button.config(text='❐')

# Function to drag the window to restore it when maximized
def drag_to_restore(event):
    global xwin, ywin, drag_start_x, drag_start_y
    drag_start_x = event.x_root
    drag_start_y = event.y_root

    if window.state() == 'zoomed':
        # Save the current position of the mouse relative to the window
        width_ratio = xwin / window.winfo_width()
        height_ratio = ywin / window.winfo_height()

        # Restore the window
        window.state('normal')
        window.update_idletasks()

        # Calculate the new position of the window
        new_x = drag_start_x - int(window.winfo_width() * width_ratio)
        new_y = drag_start_y - int(window.winfo_height() * height_ratio) - 10  # Adjust for 10 pixels below the title bar

        # Ensure the window stays within the screen bounds
        new_x = max(0, min(new_x, window.winfo_screenwidth() - window.winfo_width()))
        new_y = max(0, min(new_y, window.winfo_screenheight() - window.winfo_height()))
        
        window.geometry(f'+{new_x}+{new_y}')
        xwin = int(window.winfo_width() * width_ratio)
        ywin = int(window.winfo_height() * height_ratio) + 10  # Adjust for 10 pixels below the title bar

# Create main window
window = tk.Tk()
window.title("Drag to Restore and Maximize Example")
window.geometry("300x300")
window.overrideredirect(True)
window.configure(bg='#2c2c2c')

# Title Bar
titlebar = tk.Frame(window, bg="#2c2c2c")
titlebar.name = tk.Label(titlebar, text=window.title(), bg="#2c2c2c", fg="white")
titlebar_buttons = tk.Frame(titlebar, bg="#2c2c2c")

# Maximize button
titlebar.maximize_button = tk.Button(titlebar_buttons, command=lambda: toggle_maximize(None))
titlebar.maximize_button.config(bg="#2c2c2c", fg='white', activebackground="red", activeforeground="white", padx=5, pady=2, bd=0, width=2, highlightthickness=0)
titlebar.maximize_button.config(text='🗖', font="bold")

# Arrange buttons
titlebar.pack(fill=tk.X)
titlebar.name.pack(side='left', padx=5)
titlebar_buttons.pack(side=tk.RIGHT)
titlebar.maximize_button.pack(side=tk.LEFT)

# Window dragging functionality
def get_pos(event):
    global xwin, ywin
    xwin = event.x
    ywin = event.y

def move_window(event):
    window.geometry(f'+{event.x_root - xwin}+{event.y_root - ywin}')

# Bind dragging functionality to titlebar
titlebar.bind('<Button-1>', get_pos)
titlebar.bind('<B1-Motion>', move_window)
titlebar.name.bind('<Button-1>', get_pos)
titlebar.name.bind('<B1-Motion>', move_window)

# Double-click to toggle maximize/restore window state
titlebar.bind('<Double-1>', toggle_maximize)
titlebar.name.bind('<Double-1>', toggle_maximize)

# Bind drag-to-restore functionality when maximized
titlebar.bind('<Button-1>', drag_to_restore, add="+")
titlebar.name.bind('<Button-1>', drag_to_restore, add="+")

# Start the Tkinter main loop
window.mainloop()
