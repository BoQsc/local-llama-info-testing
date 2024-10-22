import http.client
import json

url = "/completion"
host = "localhost"
port = 8080
headers = {"Content-Type": "application/json"}

system_prompt = "You are a waffle capybara that's chill"
alpaca_system_prompt = "\nBelow is an instruction that describes a task. Write a response that appropriately completes the request."
user_message = "Hello"
assistant_prefill = "```html"
assistant_message = assistant_prefill + ""
alpaca_prompt_template = (
    system_prompt +
    alpaca_system_prompt +
    "\n\n### Instruction:\n" +
    user_message +
    "\n\n### Response:\n" +
    assistant_message
)

data = {
    "stop": ["</s>"],
    "stream": True,
    "prompt": alpaca_prompt_template,
}

# Connect to the server
conn = http.client.HTTPConnection(host, port)
json_data = json.dumps(data)
conn.request("POST", url, body=json_data, headers=headers)

response = conn.getresponse()

# Stream processing
def stream_response(response):
    buffer = ""
    for chunk in iter(lambda: response.read(1), b''):
        buffer += chunk.decode('utf-8')
        while '\n' in buffer:
            line, buffer = buffer.split('\n', 1)
            if line.startswith("data: "):
                yield line[6:]

if response.status == 200 and data.get("stream"):
    for data_line in stream_response(response):
        try:
            json_line = json.loads(data_line)
            content = json_line.get("content")
            if content:
                print(content, end='', flush=True)
        except json.JSONDecodeError:
            print(f"Error decoding JSON: {data_line}")  # Debug print for the problematic line
    print(json_line["timings"]["predicted_per_second"])
conn.close()
