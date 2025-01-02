import tkinter
# Containter, left aligned button, left aligned text area. As the text area grows left aligned button should center in the container vertically.
window = tkinter.Tk()


frame = tkinter.Frame(borderwidth=2, relief="groove", bg="gray")
frame.pack()

button = tkinter.Button(frame, text="User")
button.pack(side=tkinter.LEFT)

text_area = tkinter.Text(frame, wrap=tkinter.WORD, width=40, height=0)
text_area.pack(side=tkinter.RIGHT)


def on_modify(event):
    if text_area.edit_modified():
        print(text_area.get("1.0", "end-1c"))
        num_lines = text_area.get("1.0", "end-1c").count('\n') + 1
        text_area.configure(height=num_lines)
        text_area.edit_modified(False)

text_area.bind('<<Modified>>', on_modify)
window.mainloop()
