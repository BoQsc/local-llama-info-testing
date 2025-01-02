import tkinter as tk

class AutoHeightText(tk.Text):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<KeyRelease>', self.adjust_height)  # Adjust height after key releases

    def adjust_height(self, event=None):
        self.update_idletasks()  # Ensure geometry updates are processed
        num_lines = int(self.index('end-1c').split('.')[0])
        self.configure(height=num_lines if num_lines > 0 else 1)

# Demo
root = tk.Tk()
root.title("Auto-height Text Area")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill='x')

text = AutoHeightText(frame, width=40, height=1)
text.pack(anchor='n', fill='x', expand=True)

root.mainloop()
