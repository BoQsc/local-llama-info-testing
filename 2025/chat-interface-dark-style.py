import tkinter as tk
from tkinter import ttk

class DarkThemeStyles:
    # Colors
    PRIMARY_BG = "#000000"  # Black background
    SECONDARY_BG = "#1E1E1E"  # Gray for input areas
    HEADER_BG = "#1E3A8A"  # Dark Blue
    TEXT_COLOR = "#FFFFFF"  # White text
    HIGHLIGHT_COLOR = "#FFD700"  # Yellow/Gold
    BUTTON_BG = "#2563EB"  # Blue
    EXPORT_BUTTON_BG = "#10B981"  # Green
    USER_MSG_BG = "#1E1E1E"  # Dark gray for user messages
    ASSISTANT_MSG_BG = "#1E3A8A"  # Dark blue for assistant messages
    
    @classmethod
    def configure_styles(cls):
        style = ttk.Style()
        style.configure("Dark.TButton",
                       background=cls.BUTTON_BG,
                       foreground=cls.TEXT_COLOR,
                       padding=5,
                       relief="flat")
        style.map("Dark.TButton",
                 background=[('active', cls.HIGHLIGHT_COLOR)],
                 foreground=[('active', cls.PRIMARY_BG)])
        
        style.configure("Export.TButton",
                       background=cls.EXPORT_BUTTON_BG,
                       foreground=cls.TEXT_COLOR,
                       padding=5)
        style.map("Export.TButton",
                 background=[('active', '#0D9668')],
                 foreground=[('active', cls.TEXT_COLOR)])

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
        super().__init__(parent, bg=DarkThemeStyles.PRIMARY_BG)
        
        self.canvas = tk.Canvas(self, bg=DarkThemeStyles.PRIMARY_BG,
                              highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical",
                                     command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas,
                                       bg=DarkThemeStyles.PRIMARY_BG)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas_frame = self.canvas.create_window((0, 0),
                                                    window=self.scrollable_frame,
                                                    anchor="nw")
        
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
        
        # Configure dark theme
        self.root.configure(bg=DarkThemeStyles.PRIMARY_BG)
        DarkThemeStyles.configure_styles()
        
        # Create header
        self.header = tk.Frame(root, bg=DarkThemeStyles.HEADER_BG, height=40)
        self.header.pack(fill="x")
        tk.Label(self.header, text="Dark Chat Interface",
                bg=DarkThemeStyles.HEADER_BG,
                fg=DarkThemeStyles.TEXT_COLOR,
                font=("Arial", 12, "bold")).pack(pady=8)
        
        # Create main container
        self.container = ScrollableContainer(root)
        self.container.pack(fill="both", expand=True, padx=10, pady=(10, 0))
        
        # Create input frame
        self.input_frame = tk.Frame(root, bg=DarkThemeStyles.SECONDARY_BG)
        self.input_frame.pack(fill="x", padx=10, pady=10)
        
        # Create input box with dark styling
        self.input_box = tk.Text(self.input_frame, wrap='word', height=3,
                               bg=DarkThemeStyles.SECONDARY_BG,
                               fg=DarkThemeStyles.TEXT_COLOR,
                               insertbackground=DarkThemeStyles.TEXT_COLOR,
                               relief="flat",
                               font=("Arial", 10))
        self.input_box.pack(side=tk.LEFT, fill="x", expand=True)
        
        # Create buttons frame
        self.buttons_frame = tk.Frame(self.input_frame,
                                    bg=DarkThemeStyles.SECONDARY_BG)
        self.buttons_frame.pack(side=tk.LEFT, padx=(5, 0))
        
        # Create message type toggle button
        self.is_user = True
        self.toggle_btn = ttk.Button(self.buttons_frame,
                                   text="User",
                                   style="Dark.TButton",
                                   command=self.toggle_sender)
        self.toggle_btn.pack(pady=(0, 5))
        
        # Create send button
        self.send_btn = ttk.Button(self.buttons_frame,
                                 text="Send",
                                 style="Dark.TButton",
                                 command=self.send_message)
        self.send_btn.pack()
        
        # Bind Enter key
        self.input_box.bind('<Return>', lambda e: self.send_message())
        self.input_box.bind('<Shift-Return>', lambda e: 'break')
        
    def toggle_sender(self):
        self.is_user = not self.is_user
        self.toggle_btn.config(text="User" if self.is_user else "Assistant")
        
    def send_message(self):
        message = self.input_box.get("1.0", "end-1c").strip()
        if not message:
            return "break"
            
        # Create message frame
        frame_bg = DarkThemeStyles.USER_MSG_BG if self.is_user else DarkThemeStyles.ASSISTANT_MSG_BG
        message_frame = tk.Frame(self.container.scrollable_frame,
                               bg=frame_bg,
                               bd=1,
                               relief="solid")
        message_frame.pack(fill="x", padx=5, pady=5)
        
        # Add label
        label_text = "User" if self.is_user else "Assistant"
        tk.Label(message_frame,
                text=label_text,
                bg=frame_bg,
                fg=DarkThemeStyles.TEXT_COLOR,
                font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Add message text
        text_widget = AutoHeightText(message_frame,
                                   bg=frame_bg,
                                   fg=DarkThemeStyles.TEXT_COLOR,
                                   font=("Arial", 10),
                                   relief="flat",
                                   borderwidth=0)
        text_widget.pack(fill='x', expand=True, padx=5, pady=5)
        text_widget.insert_text(message)
        text_widget.config(state='disabled')
        
        # Clear input box
        self.input_box.delete("1.0", "end")
        
        # Scroll to bottom
        self.root.update_idletasks()
        self.container.canvas.yview_moveto(1.0)
        
        return "break"

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatInterface(root)
    root.mainloop()
