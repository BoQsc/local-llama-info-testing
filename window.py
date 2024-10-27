import tkinter as tk

window = tk.Tk()
window.title("Example")
window.geometry("300x300")  # Width x Height
window.overrideredirect(True)
window.configure(bg='#2c2c2c')

window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())

window.mainloop()
