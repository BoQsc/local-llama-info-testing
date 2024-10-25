import http.client
import json
global messages_history
messages_history = []
def alpaca_agent(user_message="Hello, who am I?", system_prompt=""):
    alpaca_system_prompt = "\nBelow is an instruction that describes a task. Write a response that appropriately completes the request."
    if system_prompt == "":
        alpaca_system_prompt = ""
    
    assistant_prefill = ""  # "```html"
    global messages_history
    if messages_history == []:
        messages_history += [
            "\n\n### Instruction:\nUser: boqsc is wow player.",
            "\n\n### Response:\nAssistant: understood.",
            "\n\n### Response:\nAssistant: My name is hamham.",
        ]
        messages_history= []

    #system_prompt = "The '### Instruction:' is Human. The '### Response:' is Assistant." + system_prompt

    alpaca_prompt_template = [
        system_prompt +
        "".join(messages_history) +
        #alpaca_system_prompt +
        "\n\n### Instruction:\nUser:" +
        user_message +
        "\n\n### Response:\nAssistant:" +
        (assistant_message := assistant_prefill + "")
    ]
    
    data = {
        "stop": ["</s>", "###"],
        "stream": True,
        "prompt": alpaca_prompt_template,  # . as prompt leads to utf error.
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
            answer = ""
            for data_line in stream_response(response):
                try:
                    json_line = json.loads(data_line)
                    content = json_line.get("content")
                    if content:
                        answer += content
                        print(content, end='', flush=True)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON: {data_line}")
            print(json_line["timings"]["predicted_per_second"])
        conn.close()
        global messages_history
        messages_history.append("\n\n### Instruction:\nUser: " + user_message)
        messages_history.append("\n\n### Response:\nAssistant: " + answer)
        return json_line
    
    return api_request()

# Example usage
while True:
    alpaca_agent(input("message:"))
    #alpaca_agent(input("message:"), system_prompt="Do not assume. Confirm only known facts without speculation. Provide only what is asked. Expand only if prompted. Be assertive only, completely factual, empirical, circumspect and precise with information given.")

input()
