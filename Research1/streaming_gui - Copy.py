import tkinter as tk
import requests
import json
from threading import Thread

# Function to send user message and process assistant's response
def send_message():
    user_msg = entry.get("1.0", tk.END).strip()  # Get user input
    if not user_msg:
        return  # Do nothing if user input is empty

    # Clear the input field
    entry.delete("1.0", tk.END)

    # Display user message in chatbox
    display_message("User: " + user_msg + "\n", "user")

    # Prepare the assistant request
    url = "http://localhost:8080/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "stream": True,
        "messages": [
            {"role": "system", "content": " "},
            {"role": "user", "content": user_msg}
        ],
        "max_new_tokens": 0,
        "top_k": 40,
        "top_p": 0.95,
        "temperature": 0.8,
        "repetition_penalty": 1.1
    }

    # Thread to handle assistant streaming response
    def process_stream():
        assistant_msg = ""  # Initialize the assistant message
        try:
            with requests.post(url, headers=headers, json=data, stream=True) as response:
                for line in response.iter_lines(decode_unicode=True):
                    if line.strip():
                        if line.startswith("data: "):
                            line = line[len("data: "):]  # Remove the prefix
                        try:
                            json_line = json.loads(line)
                            choices = json_line.get("choices", [])
                            for choice in choices:
                                delta = choice.get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    assistant_msg += content
                                    update_chatbox(content, "assistant", end_char="")
                        except json.JSONDecodeError:
                            print(f"Error decoding JSON: {line}")
        except Exception as e:
            update_chatbox(f"Error: {str(e)}\n", "assistant")

        # Save conversation to a JSON file
        conversation.append({"user": user_msg, "assistant": assistant_msg})
        with open("conversation.json", "w") as f:
            json.dump(conversation, f, indent=4)

    # Function to update chatbox in the main thread
    def update_chatbox(content, sender, end_char="\n"):
        display_message(content + end_char, sender)

    # Run the stream processing in a separate thread
    Thread(target=process_stream).start()

# Function to display a message in the chatbox
def display_message(message, sender):
    chatbox.config(state=tk.NORMAL)
    
    # Insert message with proper styling
    if sender == "user":
        tag = "user_bubble"
    else:
        tag = "assistant_bubble"
    
    chatbox.insert(tk.END, message, tag)
    chatbox.config(state=tk.DISABLED)
    chatbox.yview(tk.END)  # Auto scroll to the latest message

# Initialize the tkinter window
root = tk.Tk()
root.title("Chat with Assistant")

# Configure the grid to be responsive
root.grid_rowconfigure(0, weight=1)  # Chatbox row should expand
root.grid_rowconfigure(1, weight=0)  # Entry row is fixed
root.grid_rowconfigure(2, weight=0)  # Button row is fixed
root.grid_columnconfigure(0, weight=1)  # All content in one column should expand

# Create the chat display box
chatbox = tk.Text(root, state=tk.DISABLED, wrap=tk.WORD)
chatbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # Sticky allows the chatbox to expand

# Define the tag styles for the bubbles
chatbox.tag_configure("user_bubble", background="#d1e7dd", foreground="black", lmargin1=10, lmargin2=10, font=("Arial", 12))
chatbox.tag_configure("assistant_bubble", background="#f8d7da", foreground="black", lmargin1=10, lmargin2=10, font=("Arial", 12))

# Create the user input box
entry = tk.Text(root, height=5)
entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")  # Sticky allows horizontal resizing

# Create the send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")  # Sticky allows horizontal resizing

# Initialize conversation list to store chat history
conversation = []

# Start the tkinter main loop
root.mainloop()
