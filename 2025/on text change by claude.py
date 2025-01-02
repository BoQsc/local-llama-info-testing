import tkinter as tk
from tkinter import ttk

class TextMonitor(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Text Modification Monitor")
        self.geometry("400x300")
        
        # Create and configure the text widget
        self.text_widget = tk.Text(self, wrap=tk.WORD, height=10)
        self.text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Create a label to show modification status
        self.status_label = ttk.Label(self, text="Status: No changes")
        self.status_label.pack(padx=10, pady=5)
        
        # Bind events to track modifications
        self.text_widget.bind('<<Modified>>', self.on_modify)
        self.text_widget.bind('<Key>', self.on_key)
        
        # Keep track of previous content for comparison
        self.previous_content = ""
        
    def on_modify(self, event):
        """Handle the Modified flag event"""
        if self.text_widget.edit_modified():
            current_content = self.text_widget.get("1.0", "end-1c")
            print(f"Text modified: {current_content}")
            self.status_label.config(text="Status: Modified")
            self.text_widget.edit_modified(False)
    
    def on_key(self, event):
        """Handle individual keystrokes"""
        # Schedule a check after the key event is processed
        self.after(1, self.check_changes)
    
    def check_changes(self):
        """Compare current content with previous content"""
        current_content = self.text_widget.get("1.0", "end-1c")
        if current_content != self.previous_content:
            print(f"Change detected:")
            print(f"Previous: {self.previous_content}")
            print(f"Current:  {current_content}")
            print("-" * 40)
            self.previous_content = current_content

if __name__ == "__main__":
    app = TextMonitor()
    app.mainloop()