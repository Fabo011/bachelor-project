## Installation

Disclaimer: This is made and tested on Apple M1.

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Install Gpt4All on your machine: https://gpt4all.io/

**Start Server**
```
uvicorn server:app --reload
```

### LLM
local_llm = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")
This tells the gpt4all library to load a local language model, specifically: Meta-Llama-3-8B-Instruct.Q4_0.gguf

This .gguf file is the compressed weights of the actual LLM (Meta’s LLaMA 3–8B model). It's essentially the brain of the AI, and without it, the model can't function.
🔍 What's in the .gguf File?
- It's ~4–5 GB because it contains the neural network parameters trained by Meta.
- It's needed for inference (running the model locally) — this replaces calling an external API like OpenAI or Perplexity.
- Once downloaded, you can use it offline, and it's faster (no network latency).

---

### MCP
```
result = await zapier.call("gmail_send_email", {
    "to": "based011@protonmail.com",
    "subject": "Best places in Malaga",
    "body": email_body
})
```
