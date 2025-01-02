import tkinter

window = tkinter.Tk()

def update_text_area_height(event):
    lines = text_area.get("1.0", tkinter.END).count("\n")
    text_area.config(height=lines)
    text_area.yview_moveto(1.0)  # Scroll to the bottom after adjusting height

frame = tkinter.Frame(borderwidth=2, relief="groove", bg="gray")
frame.pack()

button = tkinter.Button(frame, text="User")
button.pack(side=tkinter.LEFT, anchor=tkinter.N)

text_area = tkinter.Text(frame, width=40, height=0)
text_area.pack(side=tkinter.RIGHT, fill=tkinter.Y)

text_area.bind("<KeyRelease>", update_text_area_height)  # Use KeyRelease to detect changes

window.mainloop()
