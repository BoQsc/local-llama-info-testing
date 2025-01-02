from tkinter import *

# Main window
root = Tk()

# Create a text widget
text = Text(root, width=40, height=4)
text.pack(expand=True, fill="both")

# Function to update the window title based on text modification
def update_title(event=None):
    if text.edit_modified():
        root.title('* Unsaved Changes')
    else:
        root.title('No Unsaved Changes')

# Bind text modification event
text.bind('<<Modified>>', update_title)

# Initialize window title
root.title('No Unsaved Changes')

# Run the main loop
root.mainloop()
