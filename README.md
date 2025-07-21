# AI Workflow

## Installation

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

**Start Server**
```
uvicorn server:app --reload
```

---

### LLM
local_llm = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")
This tells the gpt4all library to load a local language model, specifically: Meta-Llama-3-8B-Instruct.Q4_0.gguf

This .gguf file is the compressed weights of the actual LLM (Meta’s LLaMA 3–8B model).
🔍 What's in the .gguf File?
- It's ~4–5 GB because it contains the neural network parameters trained by Meta.
- It's needed for inference (running the model locally) — this replaces calling an external API like OpenAI or Perplexity.
- Once downloaded, you can use it offline, and it's faster (no network latency).

---

### Prompt for the model
**Info:** The prompt can be sent via an API call using Thunder Client. Use the Thunder Client collection and the Thunder Client VSCode extension.

Given the following plant data: Soil moisture: 15%, Last watered: 4 days ago, Temperature: 30°C. Decide whether the plant needs water or not. If the plant needs water, include the phrase 'plant needs water' in your answer. Otherwise, explain why it does not need water.

---

### MCP
Based on the response from the LLM, the MCP server sends an email notifying that the plant needs watering. If the LLM indicates that watering is not needed, the MCP server will not send any email.

---

### Links
- Gpt4All: https://gpt4all.io/
- mcp-use: https://pypi.org/project/mcp-use/#quick-start
- fastmcp for Zapier: https://pypi.org/project/fastmcp/
- Docker MCP-Toolkit: https://hub.docker.com/search?q=mcp+toolkit

---

### Testing

##### API Response
<img width="1843" height="854" alt="ai-workfloe-response" src="https://github.com/user-attachments/assets/e48e2e11-c6d4-40c4-80d3-490c17a2d557" />



