import http.client
import json
import tkinter as tk
from tkinter import ttk
import os
import threading

class DarkThemeStyles:
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

class Sidebar(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=DarkThemeStyles.SIDEBAR_BG, **kwargs)

        self.new_chat_btn = ttk.Button(
            self,
            text="+ New Chat",
            style="Dark.TButton",
            command=self.new_chat
        )
        self.new_chat_btn.pack(fill="x", padx=5, pady=5)

        self.conversations_frame = tk.Frame(
            self,
            bg=DarkThemeStyles.SIDEBAR_BG
        )
        self.conversations_frame.pack(fill="both", expand=True, padx=5)

    def new_chat(self):
        chat_num = len(self.conversations_frame.winfo_children()) + 1
        self.add_conversation(f"Chat {chat_num}")

    def add_conversation(self, title):
        conv_btn = tk.Label(
            self.conversations_frame,
            text=title,
            bg=DarkThemeStyles.SIDEBAR_ITEM_BG,
            fg=DarkThemeStyles.TEXT_COLOR,
            padx=10,
            pady=5,
            cursor="hand2"
        )
        conv_btn.pack(fill="x", pady=2)

        conv_btn.bind("<Enter>", lambda e: conv_btn.configure(
            bg=DarkThemeStyles.SIDEBAR_HOVER))
        conv_btn.bind("<Leave>", lambda e: conv_btn.configure(
            bg=DarkThemeStyles.SIDEBAR_ITEM_BG))

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
            text="",
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

        self.conversation_num = 1
        self.conversation_history = {}
        self.load_conversations()

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

        self.save_conversation(message)

        threading.Thread(target=self.get_response, args=(message,)).start()

    def load_conversations(self):
        for i in range(1, 100):
            filename = f"{i}_conversations.json"
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    self.conversation_history[i] = json.load(f)
                    self.sidebar.add_conversation(f"Chat {i}")
            else:
                break

    def save_conversation(self, message):
        if self.conversation_num not in self.conversation_history:
            self.conversation_history[self.conversation_num] = []
        self.conversation_history[self.conversation_num].append(message)

        filename = f"{self.conversation_num}_conversations.json"
        with open(filename, 'w') as f:
            json.dump(self.conversation_history[self.conversation_num], f)

    def get_response(self, message):
        global messages_history
        messages_history = []
        response = alpaca_agent(message)
        frame_bg = DarkThemeStyles.ASSISTANT_MSG_BG
        message_frame = tk.Frame(
            self.container.scrollable_frame,
            bg=frame_bg,
            bd=1,
            relief="solid"
        )
        message_frame.pack(fill="x", padx=5, pady=5)

        label_text = "Assistant"
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
        text_widget.config(state='disabled')

        for content in response:
            text_widget.config(state='normal')
            text_widget.insert('end', content)
            text_widget.config(state='disabled')
            self.root.update_idletasks()
            self.container.canvas.yview_moveto(1.0)

        self.save_conversation(text_widget.get('1.0', 'end-1c'))

def alpaca_agent(user_message="Hello, who am I?", system_prompt="You are a waffle capybara that's chill"):
    alpaca_system_prompt = "\nBelow is an instruction that describes a task. Write a response that appropriately completes the request."
    if system_prompt == "":
        alpaca_system_prompt = ""

    assistant_prefill = ""  # "```html"
    global messages_history
    if messages_history == []:
        messages_history += [
            "\n\n### Instruction:\nboqsc is wow player.",
            "\n\n### Response:\nunderstood.",
            "\n\n### Response:\nMy name is hamham.",
        ]
        messages_history= []

    alpaca_prompt_template = [
        system_prompt +
        "".join(messages_history) +
        alpaca_system_prompt +
        "\n\n### Instruction:\n" +
        user_message +
        "\n\n### Response:\n" +
        (assistant_message := assistant_prefill + "")
    ]

    data = {
        "stop": ["</s>", "###"],
        "stream": True,
        "prompt": alpaca_prompt_template,  # . as prompt leads to utf error.
    }

    def api_request():
        conn = http.client.HTTPConnection("localhost", 8080)
        json_data = json.dumps(data)
        conn.request("POST", "/completion", body=json_data, headers={"Content-Type": "application/json"})

        response = conn.getresponse()

        def stream_response(response):
            buffer = ""
            for chunk in iter(lambda: response.read(1), b''):
                buffer += chunk.decode('utf-8')
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line.startswith("data: "):
                        yield line[6:]

        if response.status == 200 and data.get("stream"):
            answer = ""
            for data_line in stream_response(response):
                try:
                    json_line = json.loads(data_line)
                    content = json_line.get("content")
                    if content:
                        answer += content
                        yield content
                except json.JSONDecodeError:
                    print(f"Error decoding JSON: {data_line}")
            print(json_line["timings"]["predicted_per_second"])
        conn.close()
        global messages_history
        messages_history.append("\n\n### Instruction:\n" + user_message)
        messages_history.append("\n\n### Response:\n" + answer)
        print(messages_history)
        return json_line

    return api_request()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatInterface(root)
    root.mainloop()