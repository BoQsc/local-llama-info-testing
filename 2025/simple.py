import tkinter as tk

class CustomTextBox:
    def __init__(self, master, width, height):
        self.master = master
        self.width = width
        self.height = height
        self.text = []
        self.font = ("Arial", 12)
        self.line_height = 20
        self.canvas = tk.Canvas(self.master, width=width, height=height)
        self.canvas.pack()
        self.entry = tk.Entry(self.master)
        self.entry.pack()
        self.button = tk.Button(self.master, text="Add Text", command=self.add_text)
        self.button.pack()

    def add_text(self):
        text = self.entry.get()
        self.text.append(text)
        self.entry.delete(0, tk.END)
        self.draw_text()

    def draw_text(self):
        self.canvas.delete("all")
        x = 10
        y = 10
        for line in self.text:
            words = line.split()
            current_line = ""
            for word in words:
                if self.canvas.winfo_width() - x < self.get_text_width(word + " "):
                    x = 10
                    y += self.line_height
                current_line += word + " "
                self.canvas.create_text(x, y, text=current_line, anchor="nw", font=self.font)
                x += self.get_text_width(word + " ")
            x = 10
            y += self.line_height

    def get_text_width(self, text):
        return len(text) * 8

root = tk.Tk()
custom_text_box = CustomTextBox(root, 400, 300)
root.mainloop()