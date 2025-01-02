import tkinter

window = tkinter.Tk()

# Function to update text area height
def update_text_area_height(event):
    lines = text_area.get("1.0", tkinter.END).count("\n")
    print(lines, text_area.winfo_height())

    text_area.config(height=lines)

# Frame setup
frame = tkinter.Frame(borderwidth=2, relief="groove", bg="gray")
frame.pack()

# Button setup
button = tkinter.Button(frame, text="User")
button.pack(side=tkinter.LEFT, anchor=tkinter.N)

# Text area setup
text_area = tkinter.Text(frame, width=40, height=1)
text_area.pack(side=tkinter.RIGHT, fill=tkinter.Y)

# Bind KeyRelease event for real-time updates
text_area.bind("<KeyPress>", update_text_area_height)

window.mainloop()
