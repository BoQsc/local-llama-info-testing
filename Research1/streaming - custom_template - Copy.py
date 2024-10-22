import requests
import json

url = "http://localhost:8080/completion"
headers = {"Content-Type": "application/json"}
system_prompt = "You are a waffle capybara that's chill"
user_message = "Hello"
assistant_message = "```html"
data = {
    "stop": ["</s>"],
    "stream": True,
    "prompt": system_prompt + "\n\n### Instruction:\n"+ user_message +"\n\n### Response:\n" + assistant_message,
}

with requests.post(url, headers=headers, stream=True, json=data) as response:
    for line in response.iter_lines(decode_unicode=True):
        if line.strip():  
            if line.startswith("data: "):
                line = line[len("data: "):] 
            try:
                json_line = json.loads(line)
                content = json_line["content"]
                if content: 
                    print(content, end='', flush=True)
            except json.JSONDecodeError:
                print(f"Error decoding JSON: {line}") 
    if json_line["generation_settings"]:
        print(json_line["timings"]["predicted_per_second"])
#input()