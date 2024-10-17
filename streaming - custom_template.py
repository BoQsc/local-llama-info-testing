import requests
import json

url = "http://localhost:8080/completion"
headers = {"Content-Type": "application/json"}
data = {
    "stream": True,
    "prompt": "Instruction: Hello \nResponse: ",

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
                # Attempt to parse the line as JSON
                json_line = json.loads(line)
                # Extract and print the text from 'choices'
                #print(json_line["content"])
                choices = json_line.get("content", [])
                #print(choices)
                #print("new line")
                #input()

                if choices:  # Print only non-empty content
                    print(choices, end='', flush=True)
            except json.JSONDecodeError:
                print(f"Error decoding JSON: {line}")  # Print the problematic line
input()