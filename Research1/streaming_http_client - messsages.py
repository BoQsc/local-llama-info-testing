import http.client
import json

messages_history = [
 "\n\n### Instruction:\nSomeMessage",
 "\n\n### Response:\n"SomeMessage2,
]

def alpaca_agent(user_message = "Hello, who am I?", system_prompt = "You are a waffle capybara that's chill"):
    alpaca_system_prompt = "\nBelow is an instruction that describes a task. Write a response that appropriately completes the request."
    if system_prompt == "": alpaca_system_prompt = ""
    assistant_prefill = "" #"```html"

    alpaca_prompt_template = (
        system_prompt +
        alpaca_system_prompt +
        "\n\n### Instruction:\n" +
        user_message +
        "\n\n### Response:\n" +
        (assistant_message := assistant_prefill + "")
    )

    data = {

        "stop": ["</s>", "###"],
        "stream": True,
        "prompt": alpaca_prompt_template,   # . as prompt leads to utf error.
        
    }


    def api_request():
        conn = http.client.HTTPConnection("localhost", 8080)
        json_data = json.dumps(data)
        conn.request("POST", "/completion", body=json_data, headers={"Content-Type": "application/json"})

        response = conn.getresponse()

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
                    print(f"Error decoding JSON: {data_line}")  
            print(json_line["timings"]["predicted_per_second"])
        conn.close()
        return json_line
    return api_request()

#alpaca_agent(user_message="write 't'")
alpaca_agent("hello")