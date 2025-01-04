import tkinter as tk

class AutoHeightText(tk.Text):
    def __init__(self, parent, width=40, **kwargs):
        super().__init__(parent, wrap='word', width=width, height=1, **kwargs)
        self.width = width
        self.bind('<<Modified>>', self._update_height)
        # Bind to Configure event to handle resizing
        self.bind('<Configure>', self._on_resize)
        self.last_width = self.winfo_width()
        
    def _on_resize(self, event):
        # Only update if width actually changed
        current_width = self.winfo_width()
        if current_width != self.last_width:
            self.last_width = current_width
            # Use after_idle to avoid multiple updates during resize
            self.after_idle(self._update_height)
    
    def _update_height(self, event=None):
        content = self.get("1.0", "end-1c")
        self.update_idletasks()
        
        # Calculate width in characters based on pixel width
        avg_char_width = self.tk.call('font', 'measure', self.cget('font'), '0')
        width_in_chars = max(20, (self.winfo_width() - 10) // avg_char_width)  # -10 for padding
        
        total_lines = 0
        for line in content.split('\n'):
            if not line:
                total_lines += 1
                continue
            
            # Calculate wrapped lines based on actual widget width
            line_length = len(line)
            if line_length == 0:
                wrapped_lines = 1
            else:
                wrapped_lines = (line_length // width_in_chars) + 1
            
            words = line.split()
            current_line_length = 0
            additional_wraps = 0
            
            for word in words:
                word_length = len(word) + 1
                if current_line_length + word_length > width_in_chars:
                    additional_wraps += 1
                    current_line_length = word_length
                else:
                    current_line_length += word_length
            
            total_lines += max(wrapped_lines, additional_wraps + 1)
        
        # Add a small buffer to ensure no scrolling is needed
        total_lines += 1
        
        self.configure(height=total_lines)
        self.edit_modified(False)
        
    def insert_text(self, text):
        self.delete('1.0', 'end')
        self.insert('1.0', text)
        self._update_height()

class ScrollableContainer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        # Configure canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Bind frame configuration to canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Create canvas window
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Bind canvas resize to frame resize
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        
        # Pack widgets
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
    def _on_canvas_configure(self, event):
        # Update the width of the frame to fill the canvas
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chat Interface")
    root.geometry("600x400")
    
    # Create main container
    container = ScrollableContainer(root)
    container.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Create frames for user and assistant
    user_frame = tk.Frame(container.scrollable_frame, bd=2, relief="groove", bg="lightgray")
    user_frame.pack(fill="x", padx=5, pady=5)
    
    assistant_frame = tk.Frame(container.scrollable_frame, bd=2, relief="groove", bg="lightblue")
    assistant_frame.pack(fill="x", padx=5, pady=5)
    
    # Create labels
    tk.Label(user_frame, text="User", bg="lightgray").pack(side=tk.LEFT, padx=5)
    tk.Label(assistant_frame, text="Assistant", bg="lightblue").pack(side=tk.LEFT, padx=5)
    
    # Create text widgets
    user_text = AutoHeightText(user_frame)
    user_text.pack(fill='x', expand=True, padx=5, pady=5)
    
    assistant_text = AutoHeightText(assistant_frame)
    assistant_text.pack(fill='x', expand=True, padx=5, pady=5)
    
    # Example button to demonstrate text insertion
    def insert_sample_text():
        user_text.insert_text("This is a test with a very long line that should wrap automatically to the next line.\n\nAnd this is another paragraph with some more text to show multiple paragraphs working correctly.")
        assistant_text.insert_text("This is the assistant's response that also automatically wraps and adjusts its height based on content.\n\nIt can handle multiple paragraphs as well, and the container will scroll when needed.")
    
    tk.Button(root, text="Insert Sample Text", command=insert_sample_text).pack(pady=5)
    
    root.mainloop()
