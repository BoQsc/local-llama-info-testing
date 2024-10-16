# local-llama-info-testing


#### server with instruction: Response: prompt | Not deepseek related, no way to set custom prompt for llama-server for now. `-p` prompt only works for non-server cli.
`llamafile --server -m "ana-v1-m7.Q2_K.gguf" --chat-template deepseek`

https://github.com/ggerganov/llama.cpp/wiki/Templates-supported-by-llama_chat_apply_template  
https://github.com/ggerganov/llama.cpp/issues/5974  

```
import requests
import json

url = "http://localhost:8080/v1/chat/completions"
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

```


### Initial test

Note: llamafile seems to be censoring, maybe system prompt needs to be changed.

https://github.com/Mozilla-Ocho/llamafile/releases
```
llamafile-0.8.14 -m ana-v1-m7.Q2_K.gguf
```

```
curl --request POST --url http://localhost:8080/completion --header "Content-Type: application/json" --data "{""prompt"": ""Building a website can be done in 10 simple steps:"",""n_predict"": 128}"
```





```
import requests
import json

url = "http://localhost:8080/v1/chat/completions"
headers = {"Content-Type": "application/json"}
data = {
    "stream": True,
    "messages": [
        {"role": "system", "content": "You are a poetic assistant."},
        {"role": "user", "content": "Compose a poem that explains FORTRAN."}
    ]
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

```





### original way
Download https://github.com/ggerganov/llama.cpp/releases
`llama-b3923-bin-win-cuda-cu11.7.1-x64`

use `llama-server.exe --model "C:\Users\Windows10\AppData\Local\nomic.ai\GPT4All\TheBloke\Ana-v1-m7-GGUF\ana-v1-m7.Q2_K.gguf" --threads 3 --mlock --no-mmap --prio 2 --cpu-strict 1 --gpu-layers 25 --main-gpu 0`

Doesn't work too well, so GPU can be disabled.

`llama-server.exe --model "C:\Users\Windows10\AppData\Local\nomic.ai\GPT4All\TheBloke\Ana-v1-m7-GGUF\ana-v1-m7.Q2_K.gguf" --threads 3 --mlock --no-mmap --prio 2 --cpu-strict 1
`

3 threads, to mimic what I have on LM Studio. Probably not needed in the lastest llama CPP since it's bad performance no matter how many threads.
