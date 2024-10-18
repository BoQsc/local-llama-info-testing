from tkinter import *
from tkinter import ttk

# Create an instance of tkinter frame or window
win = Tk()

# Set the size of the window
win.geometry("700x350")

# Remove the title bar of the window
win.overrideredirect(True)

# Initialize variables to track the drag direction
resize_dir = None
border_size = 10  # Width of the resize border area

# Define a function for resizing the window
def moveMouseButton(e):
    global resize_dir
    x1 = win.winfo_pointerx()
    y1 = win.winfo_pointery()
    x0 = win.winfo_rootx()
    y0 = win.winfo_rooty()
    w = win.winfo_width()
    h = win.winfo_height()

    if resize_dir == 'right':
        win.geometry(f"{x1 - x0}x{h}")
    elif resize_dir == 'bottom':
        win.geometry(f"{w}x{y1 - y0}")
    elif resize_dir == 'corner':
        win.geometry(f"{x1 - x0}x{y1 - y0}")
    elif resize_dir == 'left':
        new_width = w - (x1 - x0)
        win.geometry(f"{new_width}x{h}+{x1}+{y0}")
    elif resize_dir == 'top':
        new_height = h - (y1 - y0)
        win.geometry(f"{w}x{new_height}+{x0}+{y1}")

# Function to detect which side or corner is being clicked and change the cursor
def detect_resize_dir(e):
    global resize_dir
    x, y = e.x, e.y
    w, h = win.winfo_width(), win.winfo_height()

    if x > w - border_size and y > h - border_size:
        resize_dir = 'corner'
        win.config(cursor="size_nw_se")
    elif x > w - border_size:
        resize_dir = 'right'
        win.config(cursor="size_we")
    elif y > h - border_size:
        resize_dir = 'bottom'
        win.config(cursor="size_ns")
    elif x < border_size:
        resize_dir = 'left'
        win.config(cursor="size_we")
    elif y < border_size:
        resize_dir = 'top'
        win.config(cursor="size_ns")
    else:
        resize_dir = None
        win.config(cursor="arrow")

# Add a Label widget
label = Label(win, text="Grab any side or corner to resize the window")
label.pack(side="top", fill="both", expand=True)

# Add the gripper for resizing the window
grip = ttk.Sizegrip(win)
grip.place(relx=1.0, rely=1.0, anchor="se")
grip.lift(label)

# Bind the mouse events to detect resizing areas, resize accordingly, and change cursor
win.bind("<B1-Motion>", moveMouseButton)
win.bind("<Motion>", detect_resize_dir)

win.mainloop()
