import tkinter as tk
from tkinter import ttk
import requests
import json
from threading import Thread, Event

# Global flag to control the assistant's response streaming
stop_event = Event()

class ScrollableText(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.text = tk.Text(self, wrap="word", font=("Arial", 12))
        self.text.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.text.configure(yscrollcommand=self.scrollbar.set)

    def add_message(self, message, tag):
        self.text.configure(state="normal")
        self.text.insert("end", message, tag)
        self.text.configure(state="disabled")
        self.text.see("end")

    def clear(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")

# Function to send user message and process assistant's response
def send_message(event=None):
    user_msg = entry.get("1.0", "end-1c").strip()
    if not user_msg:
        return

    entry.delete("1.0", "end")
    chatbox.add_message(f"User: {user_msg}\n", "user")

    url = "http://localhost:8080/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    
    # Prepare the message history for the API call
    messages = [{"role": "system", "content": " "}]
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
        assistant_msg = "Assistant: "
        chatbox.add_message(assistant_msg, "assistant")
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

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_columnconfigure(0, weight=1)

chatbox = ScrollableText(root)
chatbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Configure tags for user and assistant messages
chatbox.text.tag_configure("user", background="#d1e7dd", lmargin1=10, lmargin2=10)
chatbox.text.tag_configure("assistant", background="#f8d7da", lmargin1=10, lmargin2=10)

entry = tk.Text(root, height=5, wrap="word")
entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
entry.bind("<Return>", lambda e: send_message() if not e.state & 0x1 else None)  # Send on Enter, newline on Shift+Enter

send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

conversation = []

root.mainloop()
