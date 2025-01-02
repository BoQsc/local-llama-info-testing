
import tkinter as tk

class AutoHeightText(tk.Text):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<<Modified>>', self.adjust_height)
        
    def adjust_height(self, event=None):
        if self.edit_modified():
            # Count the number of lines
            num_lines = int(self.index('end-1c').split('.')[0])
            # Update height
            self.configure(height=num_lines)
            self.edit_modified(False)

# Demo
root = tk.Tk()
root.title("Auto-height Text Area")

frame = tk.Frame(root)  # Add a container frame
frame.pack(padx=10, pady=10, fill='x')

text = AutoHeightText(frame, width=40, height=1)
text.pack(anchor='n')  # Explicitly anchor to top

root.mainloop()
