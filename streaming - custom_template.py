import requests
import json

url = "http://localhost:8080/completion"
headers = {"Content-Type": "application/json"}
data = {
    "stream": True,
    "messages": [
        {"role": "system", "content": " "},
        {"role": "user", "content": "Some instructions \n"}
    ],
    "max_new_tokens": 0,
    "top_k": 40,
    "top_p": 0.95,
    "temperature": 0.8,
    "repetition_penalty": 1.1
}

# Send the POST request with streaming enabled
with requests.post(url, headers=headers, json=data, stream=True) as response:
    for line in response.iter_lines(decode_unicode=True):
        if line.strip():  # Ensure the line is not empty or just whitespace
            # Strip the prefix before JSON
            if line.startswith("data: "):
                line = line[len("data: "):]  # Remove the prefix

            try:
                # Attempt to parse the line as JSON
                json_line = json.loads(line)
                # Extract and print delta content from choices
                choices = json_line.get("choices", [])
                for choice in choices:
                    delta = choice.get("delta", {})
                    content = delta.get("content", "")
                    if content:  # Print only non-empty content
                        print(content, end='', flush=True)
            except json.JSONDecodeError:
                print(f"Error decoding JSON: {line}")  # Print the problematic line
