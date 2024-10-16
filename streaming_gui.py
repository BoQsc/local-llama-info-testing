from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
import tkinter as tk
from tkinter import ttk
import requests
import json
from threading import Thread, Event
import time

class ScrollableText(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.text = tk.Text(self, wrap="word", font=("Arial", 12), bg="#1A2027", fg="#C7C5B8")
        self.text.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.text.configure(yscrollcommand=self.scrollbar.set)
        
        # Track whether autoscrolling is enabled
        self.autoscroll = True

    def add_message(self, message, tag):
        self.text.configure(state="normal")
        self.text.insert("end", message, tag)
        self.text.configure(state="disabled")
        
        # Autoscroll to the bottom if enabled
        if self.autoscroll:
            self.text.see("end")

    def clear(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")

    def toggle_autoscroll(self):
        self.autoscroll = not self.autoscroll

class CustomTitlebar(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="#151A22")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = tk.Label(self, text="Chat with Assistant", bg="#151A22", fg="#C7C5B8")
        self.title_label.grid(row=0, column=0)

        self.minimize_button = tk.Button(self, text="_", bg="#151A22", fg="#C7C5B8", command=self.minimize)
        self.minimize_button.grid(row=0, column=1)

        self.full_screen_button = tk.Button(self, text="[]", bg="#151A22", fg="#C7C5B8", command=self.full_screen)
        self.full_screen_button.grid(row=0, column=2)

        self.exit_button = tk.Button(self, text="X", bg="#151A22", fg="#C7C5B8", command=self.exit)
        self.exit_button.grid(row=0, column=3)

        self.bind("<Button-1>", self.drag_start)
        self.bind("<B1-Motion>", self.drag_motion)
        self.last_click_time = 0
        self.bind("<Double-Button-1>", self.toggle_full_screen)

        self.is_maximized = False

    def drag_start(self, event):
        self.x = event.x
        self.y = event.y

    def drag_motion(self, event):
        x = event.x + root.winfo_x() - self.x
        y = event.y + root.winfo_y() - self.y
        root.geometry(f"+{x}+{y}")

    def toggle_full_screen(self, event):
        if self.is_maximized:
            self.minimize()
        else:
            self.full_screen()

    def minimize(self):
        if self.is_maximized:
            screen_width = 800
            screen_height = 600
            x = 100
            y = 100
            root.geometry(f"{screen_width}x{screen_height}+{x}+{y}")
            self.is_maximized = False
        else:
            root.overrideredirect(False)
            root.iconify()
            root.overrideredirect(True)

    def full_screen(self):
        if not self.is_maximized:
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            x = 0
            y = 0
            root.geometry(f"{screen_width}x{screen_height}+{x}+{y}")
            self.is_maximized = True

    def exit(self):
        root.destroy()

# Global flag to control the assistant's response streaming
stop_event = Event()

def send_message(event=None):
    user_msg = entry.get("1.0", "end-1c").strip()
    if not user_msg:
        return

    entry.delete("1.0", "end")
    chatbox.add_message(f"User:\n{user_msg}\n\n", "user")

    url = "http://localhost:8080/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    
    # Prepare the message history for the API call
    messages = [{"role": "system", "content": "You are an assistant."}]
    for msg in conversation:
        messages.append({"role": "user", "content": msg["user"]})
        messages.append({"role": "assistant", "content": msg["assistant"]})

    messages.append({"role": "user", "content": user_msg})
    
    data = {
        "stream": True,
        "messages": messages,
        "max_new_tokens": 0,
        "top_k": 40,
        "top_p": 0.95,
        "temperature": 0.8,
        "repetition_penalty": 1.1
    }

    def process_stream():
        assistant_msg = ""
        chatbox.add_message("Assistant:\n", "assistant")
        try:
            with requests.post(url, headers=headers, json=data, stream=True) as response:
                for line in response.iter_lines(decode_unicode=True):
                    if stop_event.is_set():
                        break
                    if line.strip():
                        if line.startswith("data: "):
                            line = line[len("data: "):]
                        try:
                            json_line = json.loads(line)
                            choices = json_line.get("choices", [])
                            for choice in choices:
                                delta = choice.get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    assistant_msg += content
                                    update_chatbox(content, "assistant")
                        except json.JSONDecodeError:
                            print(f"Error decoding JSON: {line}")
        except Exception as e:
            update_chatbox(f"Error: {str(e)}\n", "assistant")

        chatbox.add_message("\n", "assistant")  # Add a newline after the assistant's message
        conversation.append({"user": user_msg, "assistant": assistant_msg})
        with open("conversation.json", "w") as f:
            json.dump(conversation, f, indent=4)

        update_button()

    def update_chatbox(content, sender):
        chatbox.add_message(content, sender)

    stop_event.clear()
    send_button.config(text="Stop", command=stop_assistant)
    Thread(target=process_stream).start()

def stop_assistant():
    stop_event.set()
    update_button()

def update_button():
    send_button.config(text="Send", command=send_message)

root = tk.Tk()
root.title("Chat with Assistant")
root.configure(bg="#151A22")
root.overrideredirect(True)

titlebar = CustomTitlebar(root)
titlebar.grid(row=0, column=0, sticky="ew")

root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)
root.grid_columnconfigure(0, weight=1)

chatbox = ScrollableText(root)
chatbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Configure tags for user and assistant messages
chatbox.text.tag_configure("user", background="#1A2027", foreground="#C7C5B8", lmargin1=10, lmargin2=10)
chatbox.text.tag_configure("assistant", background="#1A2027", foreground="#C7C5B8", lmargin1=10, lmargin2=10)

entry = tk.Text(root, height=5, wrap="word", bg="#363F4A", fg="#C7C5B8")
entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
entry.bind("<Return>", lambda e: send_message() if not e.state & 0x1 else None)  # Send on Enter, newline on Shift+Enter

send_button = tk.Button(root, text="Send", command=send_message, bg="#363F4A", fg="#C7C5B8")
send_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

# Add a button to toggle autoscrolling
toggle_scroll_button = tk.Button(root, text="Toggle Autoscroll", command=chatbox.toggle_autoscroll, bg="#363F4A", fg="#C7C5B8")
toggle_scroll_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

conversation = []

root.mainloop()