import tkinter as tk

window = tk.Tk()

window.title("Example")
window.geometry("300x200")
window.overrideredirect(True)



window.mainloop()




#window.geometry("300x300")  # Width x Height
#window.overrideredirect(True)
#window.configure(bg='#2c2c2c')

# Center the window with a small offset
#window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
#print(window.geometry())
#window.geometry("+50+30")  # Apply the small offset from the center
#window.geometry()
#print(window.geometry())
window.mainloop()
