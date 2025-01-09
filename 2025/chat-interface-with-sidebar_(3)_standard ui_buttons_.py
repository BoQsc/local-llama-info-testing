import tkinter as tk
from tkinter import ttk

class DarkThemeStyles:
    # Colors remain the same as before
    PRIMARY_BG = "#000000"
    SECONDARY_BG = "#1E1E1E"
    HEADER_BG = "#1E3A8A"
    TEXT_COLOR = "#FFFFFF"
    HIGHLIGHT_COLOR = "#FFD700"
    BUTTON_BG = "#2563EB"
    EXPORT_BUTTON_BG = "#10B981"
    USER_MSG_BG = "#1E1E1E"
    ASSISTANT_MSG_BG = "#1E3A8A"
    SIDEBAR_BG = "#111111"
    SIDEBAR_ITEM_BG = "#222222"
    SIDEBAR_HOVER = "#333333"
    
    @classmethod
    def configure_styles(cls):
        style = ttk.Style()
        style.theme_use('clam')
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

        style.configure("Sidebar.TButton",
                       background=cls.SIDEBAR_BG,
                       foreground=cls.TEXT_COLOR,
                       padding=2)
        style.layout('Gray.Vertical.TScrollbar', 
                    [('Vertical.Scrollbar.trough',
                    {'children': [('Vertical.Scrollbar.thumb', 
                                    {'expand': '1', 'sticky': 'nswe'})],
                        'sticky': 'ns'})])

        # Scrollbar style
        style.configure("Gray.Vertical.TScrollbar",
                           gripcount=0,
    background=DarkThemeStyles.SIDEBAR_ITEM_BG,
    darkcolor=DarkThemeStyles.SIDEBAR_ITEM_BG,
    lightcolor=DarkThemeStyles.SIDEBAR_ITEM_BG,
    troughcolor=DarkThemeStyles.SIDEBAR_BG,
    bordercolor=DarkThemeStyles.SIDEBAR_BG,
    arrowcolor=DarkThemeStyles.HIGHLIGHT_COLOR)     # Arrow color
        style.map("Gray.Vertical.TScrollbar",
                background=[("active", "#5C5C5C")])  # Hover effect

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
        
        # Create canvas with proper background and no highlight
        self.canvas = tk.Canvas(
            self,
            bg=DarkThemeStyles.PRIMARY_BG,
            highlightthickness=0,
            bd=0
        )
        
        # Create scrollbar with style
        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview,
            style="Gray.Vertical.TScrollbar"
        )
        
        # Create the frame that will hold the widgets
        self.scrollable_frame = tk.Frame(
            self.canvas,
            bg=DarkThemeStyles.PRIMARY_BG
        )
        
        # Configure the canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Add bindings for the canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # Create window inside canvas
        self.canvas_frame = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw",
            width=self.canvas.winfo_reqwidth()
        )
        
        # Pack scrollbar and canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Bind to configure events
        self.canvas.bind('<Configure>', self._on_canvas_configure)

    def _on_canvas_configure(self, event):
        # Update the width of the frame to fill the canvas
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

class Sidebar(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=DarkThemeStyles.SIDEBAR_BG, **kwargs)
        
        # Keep track of currently selected conversation
        self.selected_conversation = None
        
        # Initialize the UI components
        self._init_new_chat_button()
        self._init_scroll_container()
        self._init_bindings()
        
        # Add test conversations
        for i in range(20):
            self.add_conversation(f"Chat {i+1}")
    
    def _init_new_chat_button(self):
        self.new_chat_btn = ttk.Button(
            self,
            text="+ New Chat",
            style="Dark.TButton",
            command=self.new_chat
        )
        self.new_chat_btn.pack(fill="x", padx=5, pady=5)
    
    def _init_scroll_container(self):
        self.scroll_container = ScrollableContainer(self)
        self.scroll_container.pack(fill="both", expand=True, padx=5)
        self.conversations_frame = self.scroll_container.scrollable_frame
    
    def _init_bindings(self):
        # Add the scrolling bindings to the Canvas itself
        self.scroll_container.canvas.bind('<MouseWheel>', self._on_mousewheel)
        self.scroll_container.canvas.bind('<Button-4>', self._on_mousewheel)
        self.scroll_container.canvas.bind('<Button-5>', self._on_mousewheel)
        
        # Also bind to the scrollable frame for complete coverage
        self.conversations_frame.bind('<MouseWheel>', self._on_mousewheel)
        self.conversations_frame.bind('<Button-4>', self._on_mousewheel)
        self.conversations_frame.bind('<Button-5>', self._on_mousewheel)
    
    def _on_mousewheel(self, event):
        canvas = self.scroll_container.canvas
        
        # Get the current scroll region
        _, _, _, scroll_height = canvas.bbox("all")
        visible_height = canvas.winfo_height()
        
        # Only scroll if there's content outside the visible area
        if visible_height < scroll_height:
            if event.num == 5 or event.delta < 0:
                canvas.yview_scroll(1, "units")
            elif event.num == 4 or event.delta > 0:
                canvas.yview_scroll(-1, "units")
        
        # Prevent event from propagating
        return "break"
    
    def _on_conversation_click(self, conversation_label, event):
        if self.selected_conversation:
            self.selected_conversation.configure(
                bg=DarkThemeStyles.SIDEBAR_ITEM_BG
            )
        
        conversation_label.configure(bg=DarkThemeStyles.SIDEBAR_HOVER)
        self.selected_conversation = conversation_label
    
    def add_conversation(self, title):
        # Main container for the conversation item
        conv_container = tk.Frame(
            self.conversations_frame,
            bg=DarkThemeStyles.SIDEBAR_ITEM_BG,
        )
        conv_container.pack(fill="x", pady=2)
        
        # Container for the conversation title
        conv_title_frame = tk.Frame(
            conv_container,
            bg=DarkThemeStyles.SIDEBAR_ITEM_BG
        )
        conv_title_frame.pack(fill="x", expand=True)
        
        # Conversation label
        conv_label = tk.Label(
            conv_title_frame,
            text=title,
            bg=DarkThemeStyles.SIDEBAR_ITEM_BG,
            fg=DarkThemeStyles.TEXT_COLOR,
            padx=10,
            pady=5,
            cursor="hand2"
        )
        conv_label.pack(side="left", fill="x", expand=True)
        
        # Button container
        button_frame = tk.Frame(
            conv_container,
            bg=DarkThemeStyles.SIDEBAR_ITEM_BG
        )
        button_frame.pack(fill="x")
        
        # Rename button
        rename_btn = ttk.Button(
            button_frame,
            text="✎",
            width=3,
            style="Sidebar.TButton",
            command=lambda: self.rename_conversation(conv_label)
        )
        rename_btn.pack(side="left", padx=(10, 2), pady=2)
        
        # Delete button
        delete_btn = ttk.Button(
            button_frame,
            text="✖",
            width=3,
            style="Sidebar.TButton",
            command=lambda: self.delete_conversation(conv_container)
        )
        delete_btn.pack(side="left", padx=2, pady=2)
        
        # Bind hover events for the entire container
        for widget in [conv_container, conv_label, button_frame]:
            widget.bind("<Enter>", 
                lambda e: self._on_conversation_hover(conv_container, True))
            widget.bind("<Leave>", 
                lambda e: self._on_conversation_hover(conv_container, False))
        
        # Bind click event
        conv_label.bind("<Button-1>", 
            lambda e: self._on_conversation_click(conv_container, e))
        
        # Add mousewheel bindings
        for widget in [conv_container, conv_label, button_frame, rename_btn, delete_btn]:
            widget.bind('<MouseWheel>', self._on_mousewheel)
            widget.bind('<Button-4>', self._on_mousewheel)
            widget.bind('<Button-5>', self._on_mousewheel)
    
    def _on_conversation_hover(self, container, entering):
        if container != self.selected_conversation:
            bg_color = (DarkThemeStyles.SIDEBAR_HOVER if entering 
                       else DarkThemeStyles.SIDEBAR_ITEM_BG)
            container.configure(bg=bg_color)
            for widget in container.winfo_children():
                widget.configure(bg=bg_color)
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label):
                            child.configure(bg=bg_color)
    
    def _on_conversation_click(self, container, event):
        if self.selected_conversation:
            self._on_conversation_hover(self.selected_conversation, False)
        
        bg_color = DarkThemeStyles.SIDEBAR_HOVER
        container.configure(bg=bg_color)
        for widget in container.winfo_children():
            widget.configure(bg=bg_color)
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.configure(bg=bg_color)
        
        self.selected_conversation = container
    
    def rename_conversation(self, label):
        # Create a popup window for renaming
        popup = tk.Toplevel(self)
        popup.title("Rename Conversation")
        popup.configure(bg=DarkThemeStyles.SECONDARY_BG)
        
        # Position the popup near the parent window
        x = self.winfo_rootx() + 50
        y = self.winfo_rooty() + 50
        popup.geometry(f"+{x}+{y}")
        
        # Entry field for new name
        entry = tk.Entry(
            popup,
            bg=DarkThemeStyles.SECONDARY_BG,
            fg=DarkThemeStyles.TEXT_COLOR,
            insertbackground=DarkThemeStyles.TEXT_COLOR
        )
        entry.insert(0, label.cget("text"))
        entry.pack(padx=10, pady=5)
        entry.select_range(0, tk.END)
        
        def save_name():
            new_name = entry.get().strip()
            if new_name:
                label.configure(text=new_name)
                popup.destroy()
        
        # Save button
        save_btn = ttk.Button(
            popup,
            text="Save",
            style="Dark.TButton",
            command=save_name
        )
        save_btn.pack(pady=5)
        
        # Handle Enter key
        entry.bind('<Return>', lambda e: save_name())
        
        # Focus the entry widget
        entry.focus_set()
    
    def delete_conversation(self, container):
        container.destroy()
        if container == self.selected_conversation:
            self.selected_conversation = None

    def new_chat(self):
        chat_num = len([child for child in self.conversations_frame.winfo_children() 
                       if isinstance(child, tk.Label)]) + 1
        self.add_conversation(f"Chat {chat_num}")
class ChatInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Interface")
        self.root.geometry("800x500")
        
        self.root.configure(bg=DarkThemeStyles.PRIMARY_BG)
        DarkThemeStyles.configure_styles()
        
        self.main_container = tk.Frame(root, bg=DarkThemeStyles.PRIMARY_BG)
        self.main_container.pack(fill="both", expand=True)
        
        self.sidebar_visible = True
        self.sidebar = Sidebar(self.main_container, width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        self.chat_container = tk.Frame(self.main_container,
                                     bg=DarkThemeStyles.PRIMARY_BG)
        self.chat_container.pack(side="left", fill="both", expand=True)
        
        self.header = tk.Frame(self.chat_container,
                             bg=DarkThemeStyles.HEADER_BG,
                             height=40)
        self.header.pack(fill="x")
        
        self.toggle_btn = ttk.Button(
            self.header,
            text="☰",
            style="Sidebar.TButton",
            command=self.toggle_sidebar,
            width=3
        )
        self.toggle_btn.pack(side="left", padx=5, pady=5)
        
        tk.Label(
            self.header,
            text="Dark Chat Interface",
            bg=DarkThemeStyles.HEADER_BG,
            fg=DarkThemeStyles.TEXT_COLOR,
            font=("Arial", 12, "bold")
        ).pack(pady=8)
        
        self.container = ScrollableContainer(self.chat_container)
        self.container.pack(fill="both", expand=True, padx=10, pady=(10, 0))
        
        self.input_frame = tk.Frame(self.chat_container,
                                  bg=DarkThemeStyles.SECONDARY_BG)
        self.input_frame.pack(fill="x", padx=10, pady=10)
        
        self.input_box = tk.Text(
            self.input_frame,
            wrap='word',
            height=3,
            bg=DarkThemeStyles.SECONDARY_BG,
            fg=DarkThemeStyles.TEXT_COLOR,
            insertbackground=DarkThemeStyles.TEXT_COLOR,
            relief="flat",
            font=("Arial", 10)
        )
        self.input_box.pack(side=tk.LEFT, fill="x", expand=True)
        
        self.buttons_frame = tk.Frame(self.input_frame,
                                    bg=DarkThemeStyles.SECONDARY_BG)
        self.buttons_frame.pack(side=tk.LEFT, padx=(5, 0))
        
        self.is_user = True
        self.toggle_msg_btn = ttk.Button(
            self.buttons_frame,
            text="User",
            style="Dark.TButton",
            command=self.toggle_sender
        )
        self.toggle_msg_btn.pack(pady=(0, 5))
        
        self.send_btn = ttk.Button(
            self.buttons_frame,
            text="Send",
            style="Dark.TButton",
            command=self.send_message
        )
        self.send_btn.pack()
        
        self.input_box.bind('<Return>', lambda e: self.send_message())
        self.input_box.bind('<Shift-Return>', lambda e: 'break')
    
    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.pack_forget()
        else:
            self.sidebar.pack(side="left", fill="y", before=self.chat_container)
        self.sidebar_visible = not self.sidebar_visible
    
    def toggle_sender(self):
        self.is_user = not self.is_user
        self.toggle_msg_btn.config(text="User" if self.is_user else "Assistant")
    
    def send_message(self):
        message = self.input_box.get("1.0", "end-1c").strip()
        if not message:
            return "break"
        
        frame_bg = (DarkThemeStyles.USER_MSG_BG if self.is_user
                   else DarkThemeStyles.ASSISTANT_MSG_BG)
        message_frame = tk.Frame(
            self.container.scrollable_frame,
            bg=frame_bg,
            bd=1,
            relief="solid"
        )
        message_frame.pack(fill="x", padx=5, pady=5)
        
        label_text = "User" if self.is_user else "Assistant"
        tk.Label(
            message_frame,
            text=label_text,
            bg=frame_bg,
            fg=DarkThemeStyles.TEXT_COLOR,
            font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        text_widget = AutoHeightText(
            message_frame,
            bg=frame_bg,
            fg=DarkThemeStyles.TEXT_COLOR,
            font=("Arial", 10),
            relief="flat",
            borderwidth=0
        )
        text_widget.pack(fill='x', expand=True, padx=5, pady=5)
        text_widget.insert_text(message)
        text_widget.config(state='disabled')
        
        self.input_box.delete("1.0", "end")
        
        self.root.update_idletasks()
        self.container.canvas.yview_moveto(1.0)
        
        return "break"

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatInterface(root)
    root.mainloop()
