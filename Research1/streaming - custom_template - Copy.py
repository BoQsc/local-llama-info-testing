import requests
import json

url = "http://localhost:8080/completion"
headers = {"Content-Type": "application/json"}
data = {
    "penalty_prompt_tokens":["### Instruction"],
    "stop": ["</s>"],
    # diagnostic: "stopped_word"
    # Diagnostic: "stopping_word"
    "use_penalty_prompt_tokens":True,
    "penalize_nl":True,
    "presence_penalty":1.0,
    "frequency_penalty":1.0,
    "stream": True,
    "prompt": "### Instruction: Hello \n ### Response: ",

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
input()