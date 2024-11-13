import window
import tkinter as tk

titlebar = tk.Frame(window, bg="#2c2c2c")
titlebar.name = tk.Label(titlebar, text=window.title(), bg="#2c2c2c", fg="white")
titlebar.pack(fill=tk.X)  
titlebar.name.pack(side='left', padx=5)  