import tkinter as tk
from ctypes import windll

class ResizeBorder:
    def __init__(self, master):
        self.master = master
        self.border_size = 5
        self.corner_size = 10
        
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
        
        # Configure borders
        for border in self.borders.values():
            border.configure(bg='#1a1a1a')
            border.bind('<Enter>', lambda e: e.widget.configure(bg='#777777'))
            border.bind('<Leave>', lambda e: e.widget.configure(bg='#1a1a1a'))
        
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
        
        # Bind resize events
        self._bind_resize_events()
        
    def _bind_resize_events(self):
        # Direction vectors for each border
        resize_directions = {
            'n':  (False, True,  False, True),   # x, y, width, height
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
            
        # Enforce minimum size
        if new_width < min_width:
            if self.resize_data['move_x']:
                new_x = self.resize_data['window_x'] + self.resize_data['width'] - min_width
            new_width = min_width
            
        if new_height < min_height:
            if self.resize_data['move_y']:
                new_y = self.resize_data['window_y'] + self.resize_data['height'] - min_height
            new_height = min_height
            
        # Update window geometry
        self.master.geometry(f'{new_width}x{new_height}+{new_x}+{new_y}')

# Update the main window creation code
window = tk.Tk()
window.title("Example")
window.geometry("300x300")
window.overrideredirect(True)
window.configure(bg='#2c2c2c')  # Match the titlebar color

# Create main content frame with padding for borders
content_frame = tk.Frame(window, bg='white')
content_frame.place(x=5, y=25, relwidth=1, relheight=1, width=-10, height=-30)

titlebar = tk.Frame(window, bg="#2c2c2c")

# Rest of your existing titlebar code here...
# (Keep all the existing titlebar code from your original script)

# Add the resize border system
resize_border = ResizeBorder(window)

# Set the window to appear in the taskbar
window.after(10, lambda: set_appwindow(window))

window.mainloop()