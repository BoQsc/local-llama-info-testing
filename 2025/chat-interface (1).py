import tkinter as tk

class AutoHeightText(tk.Text):
    def __init__(self, parent, width=40, **kwargs):
        kwargs['yscrollcommand'] = None
        super().__init__(parent, wrap='word', width=width, height=1, **kwargs)
        
        self.config(state='disabled')
        self.config(yscrollcommand=lambda *args: None)
        self.config(state='normal')
        
        self.width = width
        self.bind('<<Modified>>', self._update_height)
        self.bind('<Configure>', self._on_resize)
        self.last_width = self.winfo_width()
        
    def _on_resize(self, event):
        self.after_idle(lambda: self._force_height_update())
    
    def _force_height_update(self):
        try:
            content_height = self.count('1.0', 'end', 'displaylines')[0]
            self.config(height=content_height)
            self.update_idletasks()
            if self.yview()[1] < 1.0:
                self.config(height=content_height + 1)
        except tk.TclError:
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
        
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

class ChatInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Interface")
        self.root.geometry("600x400")
        
        # Create main container
        self.container = ScrollableContainer(root)
        self.container.pack(fill="both", expand=True, padx=10, pady=(10, 0))
        
        # Create input frame at the bottom
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(fill="x", padx=10, pady=10)
        
        # Create input box
        self.input_box = tk.Text(self.input_frame, wrap='word', height=3)
        self.input_box.pack(side=tk.LEFT, fill="x", expand=True)
        
        # Create message type toggle button
        self.is_user = True
        self.toggle_btn = tk.Button(self.input_frame, text="User", command=self.toggle_sender)
        self.toggle_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Create send button
        self.send_btn = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Bind Enter key to send message
        self.input_box.bind('<Return>', lambda e: self.send_message())
        self.input_box.bind('<Shift-Return>', lambda e: 'break')  # Allow Shift+Enter for new line
        
    def toggle_sender(self):
        self.is_user = not self.is_user
        self.toggle_btn.config(text="User" if self.is_user else "Assistant")
        
    def send_message(self):
        message = self.input_box.get("1.0", "end-1c").strip()
        if not message:
            return "break"
            
        # Create message frame
        frame_color = "lightgray" if self.is_user else "lightblue"
        message_frame = tk.Frame(self.container.scrollable_frame, bd=2, relief="groove", bg=frame_color)
        message_frame.pack(fill="x", padx=5, pady=5)
        
        # Add label
        label_text = "User" if self.is_user else "Assistant"
        tk.Label(message_frame, text=label_text, bg=frame_color).pack(side=tk.LEFT, padx=5)
        
        # Add message text
        text_widget = AutoHeightText(message_frame)
        text_widget.pack(fill='x', expand=True, padx=5, pady=5)
        text_widget.insert_text(message)
        text_widget.config(state='disabled')  # Make text read-only
        
        # Clear input box
        self.input_box.delete("1.0", "end")
        
        # Scroll to bottom
        self.root.update_idletasks()
        self.container.canvas.yview_moveto(1.0)
        
        return "break"  # Prevent default Enter behavior

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatInterface(root)
    root.mainloop()
