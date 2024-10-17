import requests
import json

url = "http://localhost:8080/completion"
headers = {"Content-Type": "application/json"}
data = {
    "stream": True,
    "prompt": "User: Some instructions \nAssistant: ",

}

# Send the POST request with streaming enabled
with requests.post(url, headers=headers, stream=True, json=data) as response:
    print("starting")
    print(response.content)
    print("done")
    input()
    for line in response.iter_lines(decode_unicode=True):
        if line.strip():  # Ensure the line is not empty or just whitespace
            # Strip the prefix before JSON
            if line.startswith("data: "):
                line = line[len("data: "):]  # Remove the prefix

            try:
                # Attempt to parse the line as JSON
                json_line = json.loads(line)
                # Extract and print the text from 'choices'
                choices = json_line.get("choices", [])
                for choice in choices:
                    text = choice.get("text", "")
                    if text:  # Print only non-empty content
                        print(text, end='', flush=True)
            except json.JSONDecodeError:
                print(f"Error decoding JSON: {line}")  # Print the problematic line
