import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

class DarkThemeStyles:
    # Colors
    PRIMARY_BG = "#000000"  # Black background
    SECONDARY_BG = "#1E1E1E"  # Gray for input areas
    HEADER_BG = "#1E3A8A"  # Dark Blue
    TEXT_COLOR = "#FFFFFF"  # White text
    BUTTON_TEXT = "#CCCCCC"  # Lighter gray for button text
    HIGHLIGHT_COLOR = "#FFD700"  # Yellow/Gold
    BUTTON_BG = "#2A2A2A"  # Darker button background
    EXPORT_BUTTON_BG = "#10B981"  # Green
    USER_MSG_BG = "#1E1E1E"  # Dark gray for user messages
    ASSISTANT_MSG_BG = "#1E3A8A"  # Dark blue for assistant messages
    SCROLLBAR_BG = "#2A2A2A"  # Scrollbar background
    SCROLLBAR_FG = "#404040"  # Scrollbar foreground
    
    @classmethod
    def configure_styles(cls):
        # Configure scrollbar style
        style = ttk.Style()
        style.configure("Dark.Vertical.TScrollbar",
                       background=cls.SCROLLBAR_BG,
                       troughcolor=cls.SCROLLBAR_BG,
                       arrowcolor=cls.BUTTON_TEXT)
        
        # Configure button styles
        style.configure("Dark.TButton",
                       background=cls.BUTTON_BG,
                       foreground=cls.BUTTON_TEXT,
                       borderwidth=0,
                       focuscolor='none',
                       padding=5)
        style.map("Dark.TButton",
                 background=[('active', cls.SECONDARY_BG)],
                 foreground=[('active', cls.TEXT_COLOR)])

class RoundedFrame(tk.Frame):
    def __init__(self, parent, bg_color, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg=parent["bg"])
        
        # Create inner rounded frame
        self.canvas = tk.Canvas(self,
                              bg=parent["bg"],
                              highlightthickness=0,
                              height=40)  # Minimum height
        self.canvas.pack(fill="both", expand=True)
        
        # Draw rounded rectangle
        def draw_rounded_rect(event=None):
            self.canvas.delete("all")
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            radius = 10
            self.canvas.create_rounded_rectangle(2, 2, width-2, height-2,
                                              radius=radius,
                                              fill=bg_color,
                                              outline=bg_color)
        
        self.canvas.bind('<Configure>', draw_rounded_rect)

class ScrollableContainer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=DarkThemeStyles.PRIMARY_BG)
        
        self.canvas = tk.Canvas(self,
                              bg=DarkThemeStyles.PRIMARY_BG,
                              highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self,
                                     orient="vertical",
                                     command=self.canvas.yview,
                                     style="Dark.Vertical.TScrollbar")
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

# Add rounded rectangle method to Canvas
tk.Canvas.create_rounded_rectangle = lambda self, x1, y1, x2, y2, radius=25, **kwargs: self.create_polygon(
    x1+radius, y1,
    x1+radius, y1,
    x2-radius, y1,
    x2-radius, y1,
    x2, y1,
    x2, y1+radius,
    x2, y1+radius,
    x2, y2-radius,
    x2, y2-radius,
    x2, y2,
    x2-radius, y2,
    x2-radius, y2,
    x1+radius, y2,
    x1+radius, y2,
    x1, y2,
    x1, y2-radius,
    x1, y2-radius,
    x1, y1+radius,
    x1, y1+radius,
    x1, y1,
    smooth=True,
    **kwargs)

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
        tk.Label(self.header,
                text="Dark Chat Interface",
                bg=DarkThemeStyles.HEADER_BG,
                fg=DarkThemeStyles.TEXT_COLOR,
                font=("Arial", 12, "bold")).pack(pady=8)
        
        # Create main container
        self.container = ScrollableContainer(root)
        self.container.pack(fill="both", expand=True, padx=10, pady=(10, 0))
        
        # Create input frame
        self.input_frame = tk.Frame(root, bg=DarkThemeStyles.PRIMARY_BG)
        self.input_frame.pack(fill="x", padx=10, pady=10)
        
        # Create rounded input box container
        self.input_container = RoundedFrame(self.input_frame,
                                          DarkThemeStyles.SECONDARY_BG,
                                          height=80)
        self.input_container.pack(side=tk.LEFT, fill="x", expand=True)
        
        # Create input box with dark styling
        self.input_box = tk.Text(self.input_container.canvas,
                               wrap='word',
                               height=3,
                               bg=DarkThemeStyles.SECONDARY_BG,
                               fg=DarkThemeStyles.TEXT_COLOR,
                               insertbackground=DarkThemeStyles.TEXT_COLOR,
                               relief="flat",
                               font=("Arial", 10))
        self.input_box.place(relx=0.02, rely=0.1,
                           relwidth=0.96, relheight=0.8)
        
        # Create buttons frame
        self.buttons_frame = tk.Frame(self.input_frame,
                                    bg=DarkThemeStyles.PRIMARY_BG)
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
            
        # Create message frame with rounded corners
        frame_bg = DarkThemeStyles.USER_MSG_BG if self.is_user else DarkThemeStyles.ASSISTANT_MSG_BG
        message_frame = RoundedFrame(self.container.scrollable_frame,
                                   frame_bg)
        message_frame.pack(fill="x", padx=5, pady=5)
        
        # Add label
        label_text = "User" if self.is_user else "Assistant"
        tk.Label(message_frame.canvas,
                text=label_text,
                bg=frame_bg,
                fg=DarkThemeStyles.TEXT_COLOR,
                font=("Arial", 10, "bold")).place(x=10, y=10)
        
        # Add message text
        message_label = tk.Label(message_frame.canvas,
                               text=message,
                               bg=frame_bg,
                               fg=DarkThemeStyles.TEXT_COLOR,
                               font=("Arial", 10),
                               justify=tk.LEFT,
                               wraplength=500)
        message_label.place(x=10, y=35)
        
        # Adjust frame height based on content
        message_frame.canvas.configure(height=message_label.winfo_reqheight() + 45)
        
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
