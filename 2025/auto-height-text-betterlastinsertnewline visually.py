import tkinter as tk

class AutoHeightText(tk.Text):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind('<<Modified>>', self.adjust_height)
        # Add a small delay to batch height adjustments
        self._adjust_height_timer = None
        
    def adjust_height(self, event=None):
        if self.edit_modified():
            # Cancel any pending timer
            if self._adjust_height_timer is not None:
                self.after_cancel(self._adjust_height_timer)
            
            # Schedule the height adjustment
            self._adjust_height_timer = self.after(10, self._do_adjust_height)
            
            # Reset modified flag
            self.edit_modified(False)
    
    def _do_adjust_height(self):
        # Get current scroll position
        current_view = self.yview()
        
        # Count the number of lines
        num_lines = self.get("1.0", "end-1c").count('\n') + 1
        
        # Update height
        self.configure(height=num_lines)
        
        # Restore scroll position if we were at the bottom
        if current_view[1] == 1.0:  # If we were scrolled to bottom
            self.see("end")
        else:
            self.yview_moveto(current_view[0])

# Demo
root = tk.Tk()
root.title("Auto-height Text Area")

# Create text widget with initial height of 1
text = AutoHeightText(root, width=40, height=1)
text.pack(padx=10, pady=10)

root.mainloop()