# AI Workflow

## Installation

Disclaimer: This is made and tested on Apple M1.

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

```
brew install ollama
ollama pull llama3
ollama pull MFDoom/deepseek-v2-tool-calling:latest
ollama create deepseek-lite -f Modelfile
```

**Start Server**
```
uvicorn server:app --reload
ollama serve
```

---

### Prompt for the model
**Info:** Create a github issue with the connected mcp-server github create_issue in repo: https://github.com/Fabo011/bachelor-project about a required dark mode for the app 'Weather Forecast'. Please just create the ticket, do not do anything else. Please dont search for already existing tickets, just create the ticket, this is an instruction.

---

### Ollama
A local model server + CLI for running and managing open-source LLMs (LLaMA, Mistral, etc.).

---

### MCP
The agent calls the connected mcp servers based on the prompt.

---

### Modelfile
Configurations for the LLM. I`ve changed the parameters to run it on Mac M1 with 16gb RAM without interruptions.

---

### Links
- Gpt4All: https://gpt4all.io/
- mcp-use: https://pypi.org/project/mcp-use/#quick-start
- fastmcp for Zapier: https://pypi.org/project/fastmcp/
- Docker MCP-Toolkit: https://hub.docker.com/search?q=mcp+toolkit
- langchain docs: https://python.langchain.com/docs/integrations/providers/gpt4all/
- langchain docs: https://python.langchain.com/api_reference/community/llms/langchain_community.llms.gpt4all.GPT4All.html
- LLM: https://ollama.com/MFDoom/deepseek-r1-tool-calling?utm_source=chatgpt.com
- Start LLMs locally: https://ollama.com/
- mcp-use docs: https://docs.mcp-use.io/essentials/agent-configuration
- bind_tools: https://github.com/langchain-ai/langchain/discussions/21907
- Claude bind_tools: https://github.com/anthropics/anthropic-tools/blob/main/tool_use_package/EXAMPLES.md?utm_source=chatgpt.com
- Claude tool use: https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview
- more bind_tools infos: https://github.com/langchain-ai/langchain/discussions/25811?utm_source=chatgpt.com

---

### Infos
- ollama to start 
- llama3 does not support bind_tools
- ollama create deepseek-lite -f Modelfile - The standard deepseek model took too much power therefore I changed the parameters with the aid of the Modelfile.


### Build LLM powered Agents
- https://docs.llamaindex.ai/en/stable/