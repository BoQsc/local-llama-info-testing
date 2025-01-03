import tkinter as tk

def create_auto_height_text(parent, width=40):
    text = tk.Text(parent, wrap='word', width=width, height=1)
    def update_height(_=None):
        text.configure(height=len(text.get("1.0", "end-1c").split('\n')) + sum(len(line) // width for line in text.get("1.0", "end-1c").split('\n')))
        text.edit_modified(False)
    text.bind('<<Modified>>', update_height)
    return text

if __name__ == "__main__":
    root = tk.Tk()
    frame = tk.Frame(root, bd=2, relief="groove", bg="gray")
    frame.pack(padx=10, pady=10, expand=True, )
    tk.Button(frame, text="User").pack(side=tk.LEFT)
    create_auto_height_text(frame).pack(side=tk.RIGHT, expand=True, fill='both')
    root.mainloop()