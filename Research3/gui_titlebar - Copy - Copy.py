import tkinter as tk
from ctypes import windll

class ResizeBorder:
    def __init__(self, master):
        self.master = master
        self.border_size = 2
        self.corner_size = 4
        
        # Create border frames
        self.borders = {
            'n':  tk.Frame(master, cursor='sb_v_double_arrow'),
            's':  tk.Frame(master, cursor='sb_v_double_arrow'),
            'e':  tk.Frame(master, cursor='sb_h_double_arrow'),
            'w':  tk.Frame(master, cursor='sb_h_double_arrow'),
            'ne': tk.Frame(master, cursor='size_ne_sw'),
            'nw': tk.Frame(master, cursor='size_nw_se'),
            'se': tk.Frame(master, cursor='size_nw_se'),
            'sw': tk.Frame(master, cursor='size_ne_sw')
        }
        
        # Configure borders with dimmed white-gray color
        for border in self.borders.values():
            border.configure(bg='#3a3a3a')
            border.bind('<Enter>', lambda e: e.widget.configure(bg='#4a4a4a'))
            border.bind('<Leave>', lambda e: e.widget.configure(bg='#3a3a3a'))
        
        # Place borders
        self._place_borders()
        self._bind_resize_events()
        
        # Bind to window state changes
        self.master.bind('<Configure>', self._check_window_state)
        self.previous_state = self.master.state()
        
    def _place_borders(self):
        # Place borders
        self.borders['n'].place(x=self.corner_size, y=0, 
                              relwidth=1, width=-2*self.corner_size, height=self.border_size)
        self.borders['s'].place(x=self.corner_size, rely=1, y=-self.border_size,
                              relwidth=1, width=-2*self.corner_size, height=self.border_size)
        self.borders['e'].place(relx=1, x=-self.border_size, y=self.corner_size,
                              width=self.border_size, relheight=1, height=-2*self.corner_size)
        self.borders['w'].place(x=0, y=self.corner_size,
                              width=self.border_size, relheight=1, height=-2*self.corner_size)
        
        # Place corners
        self.borders['ne'].place(relx=1, x=-self.corner_size, y=0,
                               width=self.corner_size, height=self.corner_size)
        self.borders['nw'].place(x=0, y=0,
                               width=self.corner_size, height=self.corner_size)
        self.borders['se'].place(relx=1, x=-self.corner_size, rely=1, y=-self.corner_size,
                               width=self.corner_size, height=self.corner_size)
        self.borders['sw'].place(x=0, rely=1, y=-self.corner_size,
                               width=self.corner_size, height=self.corner_size)

    def _check_window_state(self, event=None):
        current_state = self.master.state()
        if current_state != self.previous_state:
            if current_state == 'zoomed':
                # Hide top border and corners when maximized
                self.borders['n'].place_forget()
                self.borders['ne'].place_forget()
                self.borders['nw'].place_forget()
            else:
                # Show top border and corners when restored
                self.borders['n'].place(x=self.corner_size, y=0, 
                                      relwidth=1, width=-2*self.corner_size, height=self.border_size)
                self.borders['ne'].place(relx=1, x=-self.corner_size, y=0,
                                       width=self.corner_size, height=self.corner_size)
                self.borders['nw'].place(x=0, y=0,
                                       width=self.corner_size, height=self.corner_size)
            self.previous_state = current_state
        
    def _bind_resize_events(self):
        resize_directions = {
            'n':  (False, True,  False, True),
            's':  (False, False, False, True),
            'e':  (False, False, True,  False),
            'w':  (True,  False, True,  False),
            'ne': (False, True,  True,  True),
            'nw': (True,  True,  True,  True),
            'se': (False, False, True,  True),
            'sw': (True,  False, True,  True)
        }
        
        for direction, (move_x, move_y, resize_w, resize_h) in resize_directions.items():
            self.borders[direction].bind('<Button-1>', 
                lambda e, mv_x=move_x, mv_y=move_y, rs_w=resize_w, rs_h=resize_h: 
                self._start_resize(e, mv_x, mv_y, rs_w, rs_h))
            self.borders[direction].bind('<B1-Motion>', self._resize)
    
    def _start_resize(self, event, move_x, move_y, resize_w, resize_h):
        if self.master.state() == 'zoomed':
            return
            
        self.resize_data = {
            'x': event.x_root,
            'y': event.y_root,
            'window_x': self.master.winfo_x(),
            'window_y': self.master.winfo_y(),
            'width': self.master.winfo_width(),
            'height': self.master.winfo_height(),
            'move_x': move_x,
            'move_y': move_y,
            'resize_w': resize_w,
            'resize_h': resize_h
        }
    
    def _resize(self, event):
        if not hasattr(self, 'resize_data') or self.master.state() == 'zoomed':
            return
            
        dx = event.x_root - self.resize_data['x']
        dy = event.y_root - self.resize_data['y']
        
        new_x = self.resize_data['window_x']
        new_y = self.resize_data['window_y']
        new_width = self.resize_data['width']
        new_height = self.resize_data['height']
        
        min_width = 200
        min_height = 100
        
        if self.resize_data['move_x']:
            new_x += dx
            new_width -= dx
        if self.resize_data['move_y']:
            new_y += dy
            new_height -= dy
        if self.resize_data['resize_w'] and not self.resize_data['move_x']:
            new_width += dx
        if self.resize_data['resize_h'] and not self.resize_data['move_y']:
            new_height += dy
            
        if new_width < min_width:
            if self.resize_data['move_x']:
                new_x = self.resize_data['window_x'] + self.resize_data['width'] - min_width
            new_width = min_width
            
        if new_height < min_height:
            if self.resize_data['move_y']:
                new_y = self.resize_data['window_y'] + self.resize_data['height'] - min_height
            new_height = min_height
            
        self.master.geometry(f'{new_width}x{new_height}+{new_x}+{new_y}')

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
    windll.user32.ShowWindow(hwnd, 6)

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
window.configure(bg='#2c2c2c')

#______________Title_Bar___________________
# Create main content frame with padding for borders
content_frame = tk.Frame(window, bg='white')
content_frame.place(x=2, y=25, relwidth=1, relheight=1, width=-4, height=-27)

#______________Title_Bar_Name___________________
titlebar = tk.Frame(window, bg="#2c2c2c")
titlebar.name = tk.Label(titlebar, text=window.title(), bg="#2c2c2c", fg="white")

#______________Title_Bar_Buttons Group___________________
titlebar_buttons = tk.Frame(titlebar, bg="#2c2c2c")

titlebar.minimize_button = tk.Button(titlebar_buttons, command=minimize_window)
titlebar.maximize_button = tk.Button(titlebar_buttons, command=lambda: toggle_maximize(None))
titlebar.exit_button = tk.Button(titlebar_buttons, command=window.destroy)

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

# Pack buttons into the titlebar_buttons frame
titlebar_buttons.pack(side=tk.RIGHT)  
titlebar.minimize_button.pack(side=tk.LEFT)  
titlebar.maximize_button.pack(side=tk.LEFT)  
titlebar.exit_button.pack(side=tk.LEFT)  
#______________Title_Bar_Dragging___________________
# Add window dragging functionality
def get_pos(event):
    global xwin, ywin
    xwin = event.x
    ywin = event.y

def move_window(event):
    window.geometry(f'+{event.x_root - xwin}+{event.y_root - ywin}')

# Bind window dragging
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

# Add the resize border system
resize_border = ResizeBorder(window)

# Set the window to appear in the taskbar
window.after(10, lambda: set_appwindow(window))

window.mainloop()