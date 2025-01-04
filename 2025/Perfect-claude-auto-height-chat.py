import tkinter as tk

class AutoHeightText(tk.Text):
    def __init__(self, parent, width=40, **kwargs):
        # Remove scrollbar completely and disable any internal scrolling
        kwargs['yscrollcommand'] = None
        super().__init__(parent, wrap='word', width=width, height=1, **kwargs)
        
        # Disable internal text widget scrolling
        self.config(state='disabled')  # Temporarily disable to configure
        self.config(yscrollcommand=lambda *args: None)  # Disable scroll
        self.config(state='normal')  # Re-enable editing
        
        self.width = width
        self.bind('<<Modified>>', self._update_height)
        self.bind('<Configure>', self._on_resize)
        self.last_width = self.winfo_width()
        
    def _on_resize(self, event):
        # Force immediate height update on any resize
        self.after_idle(lambda: self._force_height_update())
    
    def _force_height_update(self):
        try:
            # Get actual content height
            content_height = self.count('1.0', 'end', 'displaylines')[0]
            
            # Update widget height to match content
            self.config(height=content_height)
            
            # Force the widget to update its display
            self.update_idletasks()
            
            # Double-check if we need more height
            if self.yview()[1] < 1.0:
                self.config(height=content_height + 1)
        except tk.TclError:
            # Handle potential errors during update
            pass
        
    def _update_height(self, event=None):
        self._force_height_update()
        self.edit_modified(False)
        
    def insert_text(self, text):
        self.delete('1.0', 'end')
        self.insert('1.0', text)
        self._force_height_update()

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
        long_text = """This is a test with a very long line that should wrap automatically to the next line without requiring any scrolling inside the text widget itself.

This is another paragraph with more text to demonstrate that the widget properly expands to show all content regardless of window size.

And here's even more text to really test the wrapping and height adjustment. The text widget should always show all of this content without requiring its own scrollbar."""
        
        user_text.insert_text(long_text)
        assistant_text.insert_text(long_text)
    
    tk.Button(root, text="Insert Sample Text", command=insert_sample_text).pack(pady=5)
    
    root.mainloop()
