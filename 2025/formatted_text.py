import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Formatted Text in Tkinter")

# Create a Text widget
text_widget = tk.Text(root, wrap=tk.WORD)
text_widget.pack(expand=True, fill=tk.BOTH)

# Configure custom tags for formatting
text_widget.tag_configure("bold", font=("Arial", 12, "bold"))
text_widget.tag_configure("italic", font=("Arial", 12, "italic"))
text_widget.tag_configure("color_blue", foreground="blue")
text_widget.tag_configure("color_red", foreground="red")

# Insert text with different formats
text_widget.insert(tk.END, "This is a ", "bold")
text_widget.insert(tk.END, "bold", "bold")
text_widget.insert(tk.END, ", ", "bold")
text_widget.insert(tk.END, "italic", "italic")
text_widget.insert(tk.END, ", and colored ", "italic")
text_widget.insert(tk.END, "blue", "color_blue")
text_widget.insert(tk.END, " and ", "color_blue")
text_widget.insert(tk.END, "red.", "color_red")

# Run the Tkinter event loop
root.mainloop()
