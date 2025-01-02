import tkinter as tk

root = tk.Tk()
text = tk.Text(root)
text.pack()

def on_modify(event):
    if text.edit_modified():
        print(text.get("1.0", "end-1c"))
        num_lines = text.get("1.0", "end-1c").count('\n') + 1
        text.configure(height=num_lines)
        text.edit_modified(False)

text.bind('<<Modified>>', on_modify)
root.mainloop()
