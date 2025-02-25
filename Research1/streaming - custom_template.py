import requests
import json

url = "http://localhost:8080/completion"
headers = {"Content-Type": "application/json"}
data = {
    "stream": True,
    "prompt": "### Instruction: Hello \n ### Response: ",

}

# Send the POST request with streaming enabled
with requests.post(url, headers=headers, stream=True, json=data) as response:
    #print(response.content)
    for line in response.iter_lines(decode_unicode=True):
        if line.strip():  # Ensure the line is not empty or just whitespace
            # Strip the prefix before JSON
            if line.startswith("data: "):
                line = line[len("data: "):]  # Remove the prefix

            try:
                json_line = json.loads(line)
                choices = json_line.get("content", [])


                if choices:  # Print only non-empty content
                    print(choices, end='', flush=True)
            except json.JSONDecodeError:
                print(f"Error decoding JSON: {line}")  # Print the problematic line
input()