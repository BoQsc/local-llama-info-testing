import tkinter as tk

class AutoHeightText(tk.Text):
    def __init__(self, parent, width=40, **kwargs):
        super().__init__(parent, wrap='word', width=width, height=1, **kwargs)
        self.width = width
        self.bind('<<Modified>>', self._update_height)
        
    def _update_height(self, event=None):
        # Get the content
        content = self.get("1.0", "end-1c")
        
        # Count the number of displayed lines
        self.update_idletasks()  # Ensure widget is updated
        total_lines = 0
        
        for line in content.split('\n'):
            if not line:  # Empty line
                total_lines += 1
                continue
                
            # Calculate how many display lines this logical line will take
            # Add 1 to width to account for some buffer space
            line_length = len(line)
            if line_length == 0:
                wrapped_lines = 1
            else:
                wrapped_lines = (line_length // (self.width - 1)) + 1
                
            # Account for words that might wrap to next line
            words = line.split()
            current_line_length = 0
            additional_wraps = 0
            
            for word in words:
                word_length = len(word) + 1  # +1 for space
                if current_line_length + word_length > (self.width - 1):
                    additional_wraps += 1
                    current_line_length = word_length
                else:
                    current_line_length += word_length
                    
            total_lines += max(wrapped_lines, additional_wraps + 1)
        
        # Update the height
        self.configure(height=total_lines)
        self.edit_modified(False)
        
    def insert_text(self, text):
        """Helper method to insert text and update height"""
        self.delete('1.0', 'end')
        self.insert('1.0', text)
        self._update_height()

def create_auto_height_text(parent, width=40):
    """Factory function to create an AutoHeightText widget"""
    return AutoHeightText(parent, width=width)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Auto-height Text Demo")
    
    frame = tk.Frame(root, bd=2, relief="groove", bg="gray")
    frame.pack(padx=10, pady=10, expand=True)
    
    # Create a button to demonstrate text insertion
    def insert_sample_text():
        sample = "This is a test with a very long line that should wrap automatically to the next line.\n\nAnd this is another paragraph with some more text to show multiple paragraphs working correctly."
        text_widget.insert_text(sample)
        
    tk.Button(frame, text="User", command=insert_sample_text).pack(side=tk.LEFT)
    
    # Create the auto-height text widget
    text_widget = create_auto_height_text(frame)
    text_widget.pack(side=tk.RIGHT, expand=True, fill='both')
    
    root.mainloop()
