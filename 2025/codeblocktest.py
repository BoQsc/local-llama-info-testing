import tkinter as tk

def create_code_block_tag(text_widget):
    text_widget.tag_configure("codeblock", foreground="blue", background="lightgray", font=("Courier New", 10))

def add_code_block(text_widget, code):
    text_widget.insert(tk.END, code, "codeblock")
    text_widget.insert(tk.END, "\n")

root = tk.Tk()
root.title("Tkinter Code Block Tag Example")

text = tk.Text(root, wrap=tk.WORD, height=15, width=60)
text.pack(padx=10, pady=10)

# Define the code block tag
create_code_block_tag(text)

# Add some code as an example
sample_code = """def example_function():
    print("This is a code block")
"""
add_code_block(text, sample_code)

root.mainloop()
