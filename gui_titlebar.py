import tkinter as tk
from ctypes import windll

#_____________Create_Window________________
window = tk.Tk()
window.title("Example")
window.geometry("300x300")
window.overrideredirect(True)

#______________Title_Bar___________________
titlebar = tk.Frame(window)

#______________Title_Bar_Name___________________
titlebar.name = tk.Label(titlebar, text=window.title())

#______________Title_Bar_Buttons___________________
titlebar.minimize_button = tk.Button(titlebar, command=lambda: window.iconify())
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



window.mainloop()
