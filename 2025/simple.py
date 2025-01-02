import tkinter as tk

class AutoHeightText(tk.Text):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<<Modified>>', self.queue_adjust_height)
        self._adjust_id = None

    def queue_adjust_height(self, event=None):
        if self._adjust_id:
            self.after_cancel(self._adjust_id)  # Cancel any pending adjustments
        self._adjust_id = self.after(100, self.adjust_height)  # Delay height adjustment

    def adjust_height(self):
        if self.edit_modified():
            num_lines = int(self.index('end-1c').split('.')[0])
            self.configure(height=num_lines if num_lines > 0 else 1)
            self.edit_modified(False)
        self._adjust_id = None

# Demo
root = tk.Tk()
root.title("Auto-height Text Area")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill='x')

text = AutoHeightText(frame, width=40, height=1)
text.pack(anchor='n', fill='x', expand=True)

root.mainloop()
