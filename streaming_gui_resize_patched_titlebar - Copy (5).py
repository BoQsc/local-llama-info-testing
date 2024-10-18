from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

from tkinter import *
from tkinter import ttk
import tkinter as tk
from ctypes import windll
import requests
import json
from threading import Thread, Event
import time
import os
import random
import re

class RootFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        self.parent = parent
        super().__init__(self.parent, **kwargs)

        self.maximized = False
        self.hasstyle = False
        self.parent.windowSize = [self.parent.winfo_width(), 
                                  self.parent.winfo_height()]

        for key, val in kwargs.items():
            if key == 'highlightbackground':
                self.back_ground = val
            else:
                self.back_ground = "#2c2c2c"

        self.parent.withdraw()
        self.parent.update()
        dims = [int(x) for x in self.parent.geometry().split('+')[0].split('x')]
        dimension = (dims[0], dims[1])

        x = (self.parent.winfo_screenwidth()/2)-(dimension[0]/2)
        y = (self.parent.winfo_screenheight()/2)-250
        self.parent.geometry(f'{dimension[0]}x{dimension[1]}+{int(x)}+{int(y)}')
        self.parent.minsize(dimension[0], dimension[1])
        self.previousPosition = [int(x), int(y)]

        self.__ParentFrame__()
        self.__events__()
        self.loop_control()

        self.resize_dir = None
        self.border_size = 10  # Width of the resize border area

        self.parent.bind("<B1-Motion>", self.moveMouseButton)
        self.parent.bind("<Motion>", self.detect_resize_dir)

    def __events__(self):
        self.title_bar.bind('<Double-1>', self.maximizeToggle)
        self.title_name.bind('<Double-1>', self.maximizeToggle)

        self.minimize_btn.bind('<Enter>', lambda x: self.minimize_btn.configure(bg='#777777'))
        self.minimize_btn.bind('<Leave>', lambda x: self.minimize_btn.configure(bg=self.back_ground))
        self.maximize_btn.bind('<Enter>', lambda x: self.maximize_btn.configure(bg='#777777'))
        self.maximize_btn.bind('<Leave>', lambda x: self.maximize_btn.configure(bg=self.back_ground))
        self.close_button.bind('<Enter>', lambda x: self.close_button.configure(bg='red'))
        self.close_button.bind('<Leave>', lambda x: self.close_button.configure(bg=self.back_ground))

    def __ParentFrame__(self):
        self.parent.overrideredirect(True)

        #title bar
        self.title_bar = tk.Frame(self.parent, bg=self.back_ground, bd=1,
                             highlightcolor=self.back_ground, 
                             highlightthickness=0)

        #window title
        self.title_window = "Chat with Assistant"
        self.title_name = tk.Label(self.title_bar, text=self.title_window, 
                             font="Arial 12", bg=self.back_ground, fg="white")

        #minimize btn
        self.minimize_btn = tk.Button(self.title_bar, text='🗕', bg=self.back_ground, padx=5, pady=2, 
                                 bd=0, font="bold", fg='white', width=2,
                                 activebackground="red",
                                 activeforeground="white", 
                                 highlightthickness=0, 
                                 command=self.minimize)

        #maximize btn
        self.maximize_btn = tk.Button(self.title_bar, text='🗖', bg=self.back_ground, padx=5, pady=2, 
                                 bd=0, font="bold", fg='white', width=2,
                                 activebackground="red",
                                 activeforeground="white", 
                                 highlightthickness=0, 
                                 command=self.maximizeToggle)

        #close btn
        self.close_button = tk.Button(self.title_bar, text='🗙', bg=self.back_ground, padx=5, pady=2, 
                                 bd=0, font="bold", fg='white', width=2,
                                 activebackground="red",
                                 activeforeground="white", 
                                 highlightthickness=0, 
                                 command=self.quit)

        # pack the widgets
        self.title_bar.pack(fill='x', side=tk.TOP)
        self.title_name.pack(side='left', padx=5)
        self.close_button.pack(side='right')
        self.maximize_btn.pack(side=tk.RIGHT)
        self.minimize_btn.pack(side=tk.RIGHT)
        self.move_window_bindings(status=True)

    def get_pos(self, event):
        self.xwin = event.x
        self.ywin = event.y

    def loop_control(self):
        self.parent.update_idletasks()
        self.parent.withdraw()
        self.set_appwindow()

    def maximizeToggle(self, event=None):
        if not self.maximized:
            self.winfo_update()
            self.maximize_btn.config(text="❐")
            self.maximize_window()
            self.maximized = True
        else:
            self.maximize_btn.config(text="🗖")
            self.restore_window()
            self.maximized = False

    def maximize_window(self):
        hwnd = windll.user32.GetParent(self.parent.winfo_id())
        SWP_SHOWWINDOW = 0x40
        windll.user32.SetWindowPos(hwnd, 0, 0, 0, 
            int(self.parent.winfo_screenwidth()),
            int(self.parent.winfo_screenheight()-48),
            SWP_SHOWWINDOW)

    def restore_window(self):
        hwnd = windll.user32.GetParent(self.parent.winfo_id())
        SWP_SHOWWINDOW = 0x40
        windll.user32.SetWindowPos(hwnd, 0, 
            self.previousPosition[0],
            self.previousPosition[1],
            int(self.parent.windowSize[0]),
            int(self.parent.windowSize[1]),
            SWP_SHOWWINDOW)

    def minimize(self):
        hwnd = windll.user32.GetParent(self.parent.winfo_id())
        windll.user32.ShowWindow(hwnd, 6)

    def move_window(self, event):
        if self.maximized:
            # Calculate the relative mouse position as a fraction of the window width
            relative_x = event.x_root / self.parent.winfo_width()
            
            # Restore the window
            self.restore_window()
            self.maximized = False
            self.maximize_btn.config(text="🗖")
            
            # Calculate new position based on the relative mouse position
            new_x = event.x_root - (self.parent.winfo_width() * relative_x)
            new_y = event.y_root - self.ywin
            self.parent.geometry(f'+{int(new_x)}+{int(new_y)}')
            
            # Update xwin for smooth transition to dragging
            self.xwin = int(self.parent.winfo_width() * relative_x)
        else:
            new_x = event.x_root - self.xwin
            new_y = event.y_root - self.ywin
            self.parent.geometry(f'+{int(new_x)}+{int(new_y)}')
        
        self.previousPosition = [self.parent.winfo_x(), self.parent.winfo_y()]

    def move_window_bindings(self, *args, status=True):
        if status:
            self.title_bar.bind("<B1-Motion>", self.move_window)
            self.title_bar.bind("<Button-1>", self.get_pos)
            self.title_name.bind("<B1-Motion>", self.move_window)
            self.title_name.bind("<Button-1>", self.get_pos)
        else:
            self.title_bar.unbind("<B1-Motion>")
            self.title_bar.unbind("<Button-1>")
            self.title_name.unbind("<B1-Motion>")
            self.title_name.unbind("<Button-1>")

    def quit(self):
        self.parent.destroy()

    def set_appwindow(self):
        GWL_EXSTYLE=-20
        WS_EX_APPWINDOW=0x00040000
        WS_EX_TOOLWINDOW=0x00000080
        if not self.hasstyle:
            hwnd = windll.user32.GetParent(self.parent.winfo_id())
            style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style = style & ~WS_EX_TOOLWINDOW
            style = style | WS_EX_APPWINDOW
            res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
            self.parent.withdraw()
            self.parent.after(10, lambda:self.parent.wm_deiconify())
            self.hasstyle=True

    def winfo_update(self):
        self.parent.windowSize = [self.parent.winfo_width(),
                                  self.parent.winfo_height()]

    def moveMouseButton(self, e):
        x1 = self.parent.winfo_pointerx()
        y1 = self.parent.winfo_pointery()
        x0 = self.parent.winfo_rootx()
        y0 = self.parent.winfo_rooty()
        w = self.parent.winfo_width()
        h = self.parent.winfo_height()

        if self.resize_dir == 'right':
            self.parent.geometry(f"{x1 - x0}x{h}")
        elif self.resize_dir == 'bottom':
            self.parent.geometry(f"{w}x{y1 - y0}")
        elif self.resize_dir == 'corner':
            self.parent.geometry(f"{x1 - x0}x{y1 - y0}")
        elif self.resize_dir == 'left':
            new_width = w - (x1 - x0)
            if new_width < 100:  # Minimum window width
                new_width = 100
            self.parent.geometry(f"{new_width}x{h}+{x1}+{y0}")
        elif self.resize_dir == 'top':
            new_height = h - (y1 - y0)
            if new_height < 100:  # Minimum window height
                new_height = 100
            self.parent.geometry(f"{w}x{new_height}+{x0}+{y1}")
        elif self.resize_dir == 'topleft':
            new_width = w - (x1 - x0)
            if new_width < 100:  # Minimum window width
                new_width = 100
            new_height = h - (y1 - y0)
            if new_height < 100:  # Minimum window height
                new_height = 100
            self.parent.geometry(f"{new_width}x{new_height}+{x1}+{y1}")
        elif self.resize_dir == 'topright':
            new_width = x1 - x0
            if new_width < 100:  # Minimum window width
                new_width = 100
            new_height = h - (y1 - y0)
            if new_height < 100:  # Minimum window height
                new_height = 100
            self.parent.geometry(f"{new_width}x{new_height}+{x0}+{y1}")
        elif self.resize_dir == 'bottomleft':
            new_width = w - (x1 - x0)
            if new_width < 100:  # Minimum window width
                new_width = 100
            new_height = y1 - y0
            if new_height < 100:  # Minimum window height
                new_height = 100
            self.parent.geometry(f"{new_width}x{new_height}+{x1}+{y0}")
        elif self.resize_dir == 'bottomright':
            new_width = x1 - x0
            if new_width < 100:  # Minimum window width
                new_width = 100
            new_height = y1 - y0
            if new_height < 100:  # Minimum window height
                new_height = 100
            self.parent.geometry(f"{new_width}x{new_height}+{x0}+{y0}")

    def detect_resize_dir(self, e):
        x, y = e.x, e.y
        w, h = self.parent.winfo_width(), self.parent.winfo_height()

        if x > w - self.border_size and y > h - self.border_size:
            self.resize_dir = 'corner'
            self.parent.config(cursor="size_nw_se")
        elif x > w - self.border_size:
            self.resize_dir = 'right'
            self.parent.config(cursor="size_we")
        elif y > h - self.border_size:
            self.resize_dir = 'bottom'
            self.parent.config(cursor="size_ns")
        elif x < self.border_size and y < self.border_size:
            self.resize_dir = 'topleft'
            self.parent.config(cursor="size_nw_se")
        elif x < self.border_size:
            self.resize_dir = 'left'
            self.parent.config(cursor="size_we")
        elif y < self.border_size and x > w - self.border_size:
            self.resize_dir = 'topright'
            self.parent.config(cursor="size_ne_sw")
        elif y < self.border_size:
            self.resize_dir = 'top'
            self.parent.config(cursor="size_ns")
        elif x < self.border_size and y > h - self.border_size:
            self.resize_dir = 'bottomleft'
            self.parent.config(cursor="size_sw_ne")
        elif x > w - self.border_size and y > h - self.border_size:
            self.resize_dir = 'bottomright'
            self.parent.config(cursor="size_ne_sw")
        else:
            self.resize_dir = None
            self.parent.config(cursor="arrow")

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

class Sidebar(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="#151A22")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.chats = []
        self.chat_buttons = []

        self.load_chats()

        self.chat_frame = tk.Frame(self, bg="#151A22")
        self.chat_frame.grid(row=1, column=0)

        self.display_chats()
        self.autosave_chats()

    def new_chat(self):
        global conversation
        conversation = []
        chatbox.clear()
        entry.delete("1.0", "end")

    def load_chats(self):
        for file in os.listdir("."):
            if file.startswith("chat_") and file.endswith(".json"):
                with open(file, "r") as f:
                    chat = json.load(f)
                    self.chats.append((file, chat))

    def display_chats(self):
        for widget in self.chat_frame.winfo_children():
            widget.destroy()

        for i, (file, chat) in enumerate(self.chats):
            if len(chat) > 0:
                if "user" in chat[0]:
                    first_message = chat[0]["user"]
                else:
                    first_message = "Unknown"
            else:
                first_message = "Empty Chat"
            first_message = first_message[:50] + "..."
            button = tk.Button(self.chat_frame, text=first_message, command=lambda file=file: self.select_chat(file))
            button.grid(row=i, column=0)
        
    def select_chat(self, file):
        global conversation, current_chat
        current_chat = file
        chatbox.clear()
        try:
            with open(file, "r") as f:
                conversation = json.load(f)
                for msg in conversation:
                    if "user" in msg:
                        chatbox.add_message("User:\n" + msg["user"] + "\n\n", "user")
                    elif "assistant" in msg:
                        chatbox.add_message("Assistant:\n" + msg["assistant"] + "\n\n", "assistant")
        except json.JSONDecodeError:
            print("Error: Unable to load chat history from JSON file.")
        except KeyError:
            print("Error: Unexpected JSON file format.")

    def autosave_chats(self):
        global conversation, current_chat
        if current_chat:
            with open(current_chat, "w") as f:
                json.dump(conversation, f, indent=4)
        self.after(5000, self.autosave_chats)

class SettingsSidebar(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="#151A22")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.temperature = tk.StringVar(value="0.8")
        self.top_k = tk.StringVar(value="40")
        self.top_p = tk.StringVar(value="0.95")
        self.repetition_penalty = tk.StringVar(value="1.1")
        self.auto_stop = tk.StringVar(value="</s>")

        self.temperature_label = tk.Label(self, text="Temperature:", bg="#151A22", fg="#C7C5B8")
        self.temperature_label.grid(row=0, column=0)
        self.temperature_slider = tk.Scale(self, from_=0, to=1, resolution=0.1, orient="horizontal", variable=self.temperature)
        self.temperature_slider.grid(row=1, column=0)

        self.top_k_label = tk.Label(self, text="Top K:", bg="#151A22", fg="#C7C5B8")
        self.top_k_label.grid(row=2, column=0)
        self.top_k_slider = tk.Scale(self, from_=1, to=100, orient="horizontal", variable=self.top_k)
        self.top_k_slider.grid(row=3, column=0)

        self.top_p_label = tk.Label(self, text="Top P:", bg="#151A22", fg="#C7C5B8")
        self.top_p_label.grid(row=4, column=0)
        self.top_p_slider = tk.Scale(self, from_=0, to=1, resolution=0.01, orient="horizontal", variable=self.top_p)
        self.top_p_slider.grid(row=5, column=0)

        self.repetition_penalty_label = tk.Label(self, text="Repetition Penalty:", bg="#151A22", fg="#C7C5B8")
        self.repetition_penalty_label.grid(row=6, column=0)
        self.repetition_penalty_slider = tk.Scale(self, from_=0, to=2, resolution=0.1, orient="horizontal", variable=self.repetition_penalty)
        self.repetition_penalty_slider.grid(row=7, column=0)

        self.auto_stop_label = tk.Label(self, text="Auto-stop:", bg="#151A22", fg="#C7C5B8")
        self.auto_stop_label.grid(row=8, column=0)
        self.auto_stop_entry = tk.Entry(self, textvariable=self.auto_stop)
        self.auto_stop_entry.grid(row=9, column=0)

    def get_settings(self):
        return {
            "temperature": float(self.temperature.get()),
            "top_k": int(self.top_k.get()),
            "top_p": float(self.top_p.get()),
            "repetition_penalty": float(self.repetition_penalty.get()),
            "auto_stop": self.auto_stop.get()
        }

# Global flag to control the assistant's response streaming
stop_event = Event()

conversation = []
current_chat = None

def regenerate_message():
    stop_event.set()  # Stop the assistant
    send_button.config(text="Send", command=send_message)  # Update the send button
    root.update_idletasks()  # Update the GUI
    
    global conversation, current_chat
    if len(conversation) > 0:
        conversation.pop()
        chatbox.clear()
        for msg in conversation:
            if "user" in msg:
                chatbox.add_message(f"User:\n{msg['user']}\n\n", "user")
            elif "assistant" in msg:
                chatbox.add_message(f"Assistant:\n{msg['assistant']}\n\n", "assistant")

        url = "http://localhost:8080/v1/chat/completions"
        headers = {"Content-Type": "application/json"}

        messages = []
        for msg in conversation:
            if "user" in msg:
                messages.append({"role": "user", "content": msg["user"]})
            elif "assistant" in msg:
                messages.append({"role": "assistant", "content": msg["assistant"]})

        data = {
            "stream": True,
            "messages": messages,
            "max_new_tokens": 9000,
            **settings_sidebar.get_settings()
        }

        def process_stream():
            global conversation, current_chat
            assistant_msg = ""
            chatbox.add_message("Assistant:\n", "assistant")
            try:
                with requests.post(url, headers=headers, json=data, stream=True) as response:
                    for line in response.iter_lines(decode_unicode=True):
                        if stop_event.is_set():
                            response.close()
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
                                        if settings_sidebar.get_settings()["auto_stop"] in assistant_msg:
                                            stop_event.set()
                                            assistant_msg = assistant_msg.replace(settings_sidebar.get_settings()["auto_stop"], "")
                                        chatbox.add_message(content, "assistant")
                                        root.update_idletasks()  # Update the GUI
                            except json.JSONDecodeError:
                                print(f"Error decoding JSON: {line}")
            except Exception as e:
                chatbox.add_message(f"Error: {str(e)}\n", "assistant")

            chatbox.add_message("\n", "assistant")  # Add a newline after the assistant's message

            conversation.append({"assistant": assistant_msg})  # Add assistant's response to the conversation list

            if current_chat:
                with open(current_chat, "w") as f:
                    json.dump(conversation, f, indent=4)
            else:
                filename = f"chat_{re.sub('[^A-Za-z0-9]+', '_', assistant_msg[:50])}_{random.randint(1000, 9999)}.json"
                sidebar.chats.append((filename, conversation))
                sidebar.display_chats()
                with open(filename, "w") as f:
                    json.dump(conversation, f, indent=4)
                current_chat = filename

            update_button()

        stop_event.clear()
        send_button.config(text="Stop", command=stop_assistant)
        Thread(target=process_stream).start()

def send_message(event=None):
    global conversation, current_chat
    user_msg = entry.get("1.0", "end-1c").strip()
    if not user_msg:
        return

    entry.delete("1.0", "end")
    chatbox.add_message(f"User:\n{user_msg}\n\n", "user")

    conversation.append({"user": user_msg})  # Add user's input to the conversation list

    url = "http://localhost:8080/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    
    # Prepare the message history for the API call
    messages = []
    for msg in conversation:
        if "user" in msg:
            messages.append({"role": "user", "content": msg["user"]})
        elif "assistant" in msg:
            messages.append({"role": "assistant", "content": msg["assistant"]})

    messages.append({"role": "user", "content": user_msg})
    
    data = {
        "stream": True,
        "messages": messages,
        "max_new_tokens": 9000,
        **settings_sidebar.get_settings()
    }

    def process_stream():
        global conversation, current_chat
        assistant_msg = ""
        chatbox.add_message("Assistant:\n", "assistant")
        try:
            with requests.post(url, headers=headers, json=data, stream=True) as response:
                for line in response.iter_lines(decode_unicode=True):
                    if stop_event.is_set():
                        response.close()  # Close the response object
                        break  # Break the loop
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
                                    if settings_sidebar.get_settings()["auto_stop"] in assistant_msg:
                                        stop_event.set()
                                        assistant_msg = assistant_msg.replace(settings_sidebar.get_settings()["auto_stop"], "")
                                    chatbox.add_message(content, "assistant")
                                    root.update_idletasks()  # Update the GUI
                        except json.JSONDecodeError:
                            print(f"Error decoding JSON: {line}")
        except Exception as e:
            chatbox.add_message(f"Error: {str(e)}\n", "assistant")

        chatbox.add_message("\n", "assistant")  # Add a newline after the assistant's message

        conversation.append({"assistant": assistant_msg})  # Add assistant's response to the conversation list

        if current_chat:
            with open(current_chat, "w") as f:
                json.dump(conversation, f, indent=4)
        else:
            filename = f"chat_{re.sub('[^A-Za-z0-9]+', '_', assistant_msg[:50])}_{random.randint(1000, 9999)}.json"
            sidebar.chats.append((filename, conversation))
            sidebar.display_chats()
            with open(filename, "w") as f:
                json.dump(conversation, f, indent=4)
            current_chat = filename

        update_button()

    stop_event.clear()
    send_button.config(text="Stop", command=stop_assistant)
    Thread(target=process_stream).start()

def stop_assistant():
    stop_event.set()
    update_button()

def update_button():
    send_button.config(text="Send", command=send_message)

def toggle_sidebar():
    global conversation, current_chat
    if sidebar.grid_info():
        sidebar.grid_remove()
    else:
        sidebar.grid(row=1, column=0, sticky="ns")
        if current_chat:
            with open(current_chat, "r") as f:
                conversation.clear()
                conversation.extend(json.load(f))

def toggle_settings_sidebar():
    if settings_sidebar.grid_info():
        settings_sidebar.grid_remove()
    else:
        settings_sidebar.grid(row=1, column=2, sticky="ns")

root = tk.Tk()
root.title("Chat with Assistant")
root.configure(bg="#151A22")

root.geometry("1200x900")

root_frame = RootFrame(root, bg="#151A22", highlightthickness=0)
root_frame.pack(fill=tk.BOTH, expand=True)

root_frame.grid_rowconfigure(1, weight=1)
root_frame.grid_columnconfigure(0, weight=1)
root_frame.grid_columnconfigure(1, weight=5)

sidebar = Sidebar(root_frame)
sidebar.grid(row=1, column=0, sticky="ns")

new_chat_button = tk.Button(root_frame, text="New Chat", command=sidebar.new_chat, bg="#363F4A", fg="#C7C5B8")
new_chat_button.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

chatbox = ScrollableText(root_frame)
chatbox.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Configure tags for user and assistant messages
chatbox.text.tag_configure("user", background="#1A2027", foreground="#C7C5B8", lmargin1=10, lmargin2=10)
chatbox.text.tag_configure("assistant", background="#1A2027", foreground="#C7C5B8", lmargin1=10, lmargin2=10)

entry = tk.Text(root_frame, height=5, wrap="word", bg="#363F4A", fg="#C7C5B8")
entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
entry.bind("<Return>", lambda e: send_message() if not e.state & 0x1 else None)  # Send on Enter, newline on Shift+Enter

send_button = tk.Button(root_frame, text="Send", command=send_message, bg="#363F4A", fg="#C7C5B8")
send_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

regenerate_button = tk.Button(root_frame, text="Regenerate", command=regenerate_message, bg="#363F4A", fg="#C7C5B8")
regenerate_button.grid(row=3, column=2, padx=10, pady=10, sticky="ew")

settings_sidebar = SettingsSidebar(root_frame)

sidebar_toggle_button = tk.Button(root_frame, text="Toggle Sidebar", command=toggle_sidebar, bg="#363F4A", fg="#C7C5B8")
sidebar_toggle_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

settings_toggle_button = tk.Button(root_frame, text="Toggle Settings", command=toggle_settings_sidebar, bg="#363F4A", fg="#C7C5B8")
settings_toggle_button.grid(row=4, column=2, padx=10, pady=10, sticky="ew")

root.mainloop()