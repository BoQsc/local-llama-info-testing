import tkinter as tk

class AutoHeightText(tk.Text):
    def __init__(self, master=None, **kwargs):
        # Enable word wrap and set initial height
        kwargs['wrap'] = 'word'  # Enable word wrap
        kwargs['height'] = 1
        super().__init__(master, **kwargs)
        
        # Bind to content changes and key events
        self.bind('<<Modified>>', self._on_modify)
        self.bind('<KeyRelease>', self._on_key)  # Changed to KeyRelease
        
    def _calculate_height(self):
        # Get the widget width in characters
        widget_width = self.cget('width')
        
        # Get all the text content
        text_content = self.get("1.0", "end-1c")
        
        # Count how many lines we need based on text width
        needed_lines = 1
        current_line_length = 0
        
        for char in text_content:
            if char == '\n':
                needed_lines += 1
                current_line_length = 0
            else:
                current_line_length += 1
                if current_line_length >= widget_width:
                    needed_lines += 1
                    current_line_length = 0
        
        return max(1, needed_lines)
            
    def _update_height(self):
        # Calculate required height
        needed_height = self._calculate_height()
        
        # Update height if needed
        current_height = int(self.cget('height'))
        if needed_height != current_height:
            self.configure(height=needed_height)
            
        # Reset modified flag
        self.edit_modified(False)
        
    def _on_modify(self, event):
        if self.edit_modified():
            self._update_height()
            
    def _on_key(self, event):
        self._update_height()

# Example usage
if __name__ == "__main__":
    window = tk.Tk()
    frame = tk.Frame(borderwidth=2, relief="groove", bg="gray")
    frame.pack(padx=10, pady=10, expand=True, fill='both')
    
    button = tk.Button(frame, text="User")
    button.pack(side=tk.LEFT)
    
    text_area = AutoHeightText(frame, width=40)
    text_area.pack(side=tk.RIGHT, expand=True, fill='both')
    
    window.mainloop()