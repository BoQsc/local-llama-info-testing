import tkinter as tk
from ctypes import windll

#_____________Create_Window________________
window = tk.Tk()
window.title("Example")
window.geometry("300x300")
window.overrideredirect(True)

#______________Title_Bar___________________
titlebar = tk.Frame(window)
titlebar.label = tk.Label(titlebar, text=window.title())

titlebar.button = tk.Button(titlebar, command=lambda: minimize())
titlebar.button.config(bg="#2c2c2c", fg='white', activebackground="red", activeforeground="white")
titlebar.button.config(padx=5, pady=2, bd=0, width=2, highlightthickness=0)
titlebar.button.bind("<Enter>", lambda event: event.widget.config(bg="#777777", fg='black'))
titlebar.button.bind("<Leave>", lambda event: event.widget.config(bg="#2c2c2c", fg='white'))
titlebar.button.config(text='🗕', font="bold")

#_______________Layout_____________________
titlebar.pack(fill=tk.X)  
titlebar.label.pack()  
titlebar.button.pack()  

#button handlers
def minimize():
    print("testz")


window.mainloop()
