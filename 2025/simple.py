import tkinter
# Containter, left aligned button, left aligned text area. As the text area grows left aligned button should center in the container vertically.
window = tkinter.Tk()


frame = tkinter.Frame(borderwidth=2, relief="groove", bg="gray")
frame.pack()

button = tkinter.Button(frame, text="User")
button.pack(side=tkinter.LEFT)

text_area = tkinter.Text(frame, wrap=tkinter.WORD, width=40, height=5)
text_area.pack(side=tkinter.RIGHT)


window.mainloop()
