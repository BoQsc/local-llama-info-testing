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
            # Reset modified flag
            self.edit_modified(False)

# Demo
root = tk.Tk()
root.title("Auto-height Text Area")

text = AutoHeightText(root, width=40, height=1)
text.pack(padx=10, pady=10)

root.mainloop()