# local-llama-info-testing
```
llamafile-0.8.14 -m ana-v1-m7.Q2_K.gguf
```

```
curl --request POST --url http://localhost:8080/completion --header "Content-Type: application/json" --data "{""prompt"": ""Building a website can be done in 10 simple steps:"",""n_predict"": 128}"
```


https://github.com/Mozilla-Ocho/llamafile/releases


### original way
Download https://github.com/ggerganov/llama.cpp/releases
`llama-b3923-bin-win-cuda-cu11.7.1-x64`

use `llama-server.exe --model "C:\Users\Windows10\AppData\Local\nomic.ai\GPT4All\TheBloke\Ana-v1-m7-GGUF\ana-v1-m7.Q2_K.gguf" --threads 3 --mlock --no-mmap --prio 2 --cpu-strict 1 --gpu-layers 25 --main-gpu 0`

Doesn't work too well, so GPU can be disabled.

`llama-server.exe --model "C:\Users\Windows10\AppData\Local\nomic.ai\GPT4All\TheBloke\Ana-v1-m7-GGUF\ana-v1-m7.Q2_K.gguf" --threads 3 --mlock --no-mmap --prio 2 --cpu-strict 1
`

3 threads, to mimic what I have on LM Studio. Probably not needed in the lastest llama CPP since it's bad performance no matter how many threads.
