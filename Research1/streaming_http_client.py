import http.client
import json

url = "/completion"
host = "localhost:8080"
headers = {"Content-Type": "application/json"}

system_prompt = "You are a waffle capybara that's chill"
alpaca_system_prompt = "\nBelow is an instruction that describes a task. Write a response that appropriately completes the request."
user_message = "Hello"
assistant_prefill = "```html"
assistant_message = assistant_prefill + ""
alpaca_prompt_template = system_prompt + alpaca_system_prompt + "\n\n### Instruction:\n"+ user_message +"\n\n### Response:\n" + assistant_message

print ("A"+assistant_message+"A")
data = {
    "stop": ["</s>"],
    "stream": True,
    "prompt": alpaca_prompt_template,
}

conn = http.client.HTTPConnection(host)
json_data = json.dumps(data)
conn.request("POST", url, body=json_data, headers=headers)

response = conn.getresponse()

for line in response:
    line = line.decode('utf-8').strip()
    if line.startswith("data: "):
        line = line[len("data: "):]
    try:
        json_line = json.loads(line)
        content = json_line.get("content")
        if content:
            print(content, end='', flush=True)
    except json.JSONDecodeError:
        print(f"Error decoding JSON: {line}")

if json_line.get("generation_settings"):
    print(json_line["timings"]["predicted_per_second"])
    print(json.dumps(json_line, indent=2))

conn.close()
# input()
